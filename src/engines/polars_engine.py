from pathlib import Path
from typing import Tuple, List
import polars as pl

from src.engines.base import BaseAggregatorEngine
from src.models import CampaignMetrics


class PolarsAggregatorEngine(BaseAggregatorEngine):
    """High-performance out-of-core aggregation engine using Polars LazyFrames."""

    def process(
        self, input_path: str, top_n: int = 10
    ) -> Tuple[List[CampaignMetrics], List[CampaignMetrics]]:
        path = Path(input_path)
        if not path.exists():
            raise FileNotFoundError(f"Input file not found: {input_path}")

        schema = {
            "campaign_id": pl.String,
            "impressions": pl.Int64,
            "clicks": pl.Int64,
            "spend": pl.Float64,
            "conversions": pl.Int64,
        }

        # Scan lazily with robust handling for malformed / ragged lines
        lazy_df = pl.scan_csv(
            str(path),
            schema_overrides=schema,
            ignore_errors=True,
            truncate_ragged_lines=True,
        )

        # Filter out corrupt/null rows and header duplicates
        valid_df = lazy_df.filter(
            pl.col("campaign_id").is_not_null()
            & (pl.col("campaign_id") != "campaign_id")
            & pl.col("impressions").is_not_null()
            & pl.col("clicks").is_not_null()
            & pl.col("spend").is_not_null()
            & pl.col("conversions").is_not_null()
        )

        # Aggregate metrics grouped by campaign_id
        agg_df = (
            valid_df.group_by("campaign_id")
            .agg(
                [
                    pl.col("impressions").sum().alias("total_impressions"),
                    pl.col("clicks").sum().alias("total_clicks"),
                    pl.col("spend").sum().alias("total_spend"),
                    pl.col("conversions").sum().alias("total_conversions"),
                ]
            )
            .with_columns(
                [
                    pl.when(pl.col("total_impressions") > 0)
                    .then(pl.col("total_clicks") / pl.col("total_impressions"))
                    .otherwise(0.0)
                    .alias("CTR"),
                    pl.when(pl.col("total_conversions") > 0)
                    .then(pl.col("total_spend") / pl.col("total_conversions"))
                    .otherwise(None)
                    .alias("CPA"),
                ]
            )
        )

        # Collect the aggregated dataset into memory
        df = agg_df.collect()

        if len(df) == 0:
            return [], []

        # Sort top N by CTR descending (tie-breaker by total_impressions desc)
        ctr_df = df.sort(["CTR", "total_impressions"], descending=[True, True]).head(top_n)

        # Sort top N by CPA ascending (excluding campaigns with conversions = 0)
        cpa_df = (
            df.filter(pl.col("total_conversions") > 0)
            .sort(["CPA", "total_conversions"], descending=[False, True])
            .head(top_n)
        )

        top_ctr_metrics = [
            CampaignMetrics(
                campaign_id=row["campaign_id"],
                total_impressions=int(row["total_impressions"]),
                total_clicks=int(row["total_clicks"]),
                total_spend=float(row["total_spend"]),
                total_conversions=int(row["total_conversions"]),
            )
            for row in ctr_df.iter_rows(named=True)
        ]

        top_cpa_metrics = [
            CampaignMetrics(
                campaign_id=row["campaign_id"],
                total_impressions=int(row["total_impressions"]),
                total_clicks=int(row["total_clicks"]),
                total_spend=float(row["total_spend"]),
                total_conversions=int(row["total_conversions"]),
            )
            for row in cpa_df.iter_rows(named=True)
        ]

        return top_ctr_metrics, top_cpa_metrics
