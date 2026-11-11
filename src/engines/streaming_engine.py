import os
from pathlib import Path
from typing import Tuple, List, Dict
from src.engines.base import BaseAggregatorEngine
from src.models import CampaignMetrics


class StreamingAggregatorEngine(BaseAggregatorEngine):
    """Pure Python streaming aggregation engine with O(1) memory complexity.
    Requires zero external dependencies and processes arbitrary file sizes line by line.
    """

    def process(
        self, input_path: str, top_n: int = 10
    ) -> Tuple[List[CampaignMetrics], List[CampaignMetrics]]:
        path = Path(input_path)
        if not path.exists():
            raise FileNotFoundError(f"Input file not found: {input_path}")

        # Dict structure: campaign_id -> [impressions, clicks, spend, conversions]
        stats: Dict[str, List] = {}

        with open(path, "r", encoding="utf-8", errors="replace") as f:
            # Read and inspect header
            header_line = f.readline()
            if not header_line:
                return [], []

            for line in f:
                line = line.strip()
                if not line:
                    continue

                parts = line.split(",")
                if len(parts) != 6:
                    continue  # Malformed row

                cid = parts[0].strip()
                if not cid or cid == "campaign_id":
                    continue

                try:
                    imp = int(parts[2].strip())
                    clk = int(parts[3].strip())
                    spend = float(parts[4].strip())
                    conv = int(parts[5].strip())
                except (ValueError, IndexError):
                    continue  # Skip row with non-numeric / malformed columns

                if cid in stats:
                    entry = stats[cid]
                    entry[0] += imp
                    entry[1] += clk
                    entry[2] += spend
                    entry[3] += conv
                else:
                    stats[cid] = [imp, clk, spend, conv]

        if not stats:
            return [], []

        all_metrics: List[CampaignMetrics] = [
            CampaignMetrics(
                campaign_id=cid,
                total_impressions=val[0],
                total_clicks=val[1],
                total_spend=round(val[2], 4),
                total_conversions=val[3],
            )
            for cid, val in stats.items()
        ]

        # Top CTR: sorted by CTR descending, tie-breaker by impressions descending
        top_ctr = sorted(
            all_metrics,
            key=lambda m: (m.ctr, m.total_impressions),
            reverse=True,
        )[:top_n]

        # Top CPA: exclude campaigns with 0 conversions, sorted by CPA ascending
        cpa_candidates = [m for m in all_metrics if m.total_conversions > 0 and m.cpa is not None]
        top_cpa = sorted(
            cpa_candidates,
            key=lambda m: (m.cpa, -m.total_conversions),
        )[:top_n]

        return top_ctr, top_cpa
