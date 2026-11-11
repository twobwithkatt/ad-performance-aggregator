from dataclasses import dataclass
from typing import Optional, List

@dataclass
class CampaignMetrics:
    """Represents aggregated advertising performance metrics for a single campaign."""
    campaign_id: str
    total_impressions: int
    total_clicks: int
    total_spend: float
    total_conversions: int

    @property
    def ctr(self) -> float:
        """Click-Through Rate (CTR) = total_clicks / total_impressions."""
        if self.total_impressions <= 0:
            return 0.0
        return self.total_clicks / self.total_impressions

    @property
    def cpa(self) -> Optional[float]:
        """Cost Per Acquisition (CPA) = total_spend / total_conversions.
        Returns None if total_conversions is zero.
        """
        if self.total_conversions <= 0:
            return None
        return self.total_spend / self.total_conversions

    @property
    def formatted_ctr(self) -> str:
        """Formatted CTR string with 4 decimal places (e.g. '0.0500')."""
        return f"{self.ctr:.4f}"

    @property
    def formatted_cpa(self) -> str:
        """Formatted CPA string with 2 decimal places (e.g. '20.00') or 'null'."""
        if self.cpa is None:
            return "null"
        return f"{self.cpa:.2f}"

    @property
    def formatted_spend(self) -> str:
        """Formatted total spend string with 2 decimal places (e.g. '12500.50')."""
        return f"{self.total_spend:.2f}"

    def to_csv_row(self) -> List[str]:
        """Serializes the metrics to a list of strings matching expected CSV output schema."""
        return [
            self.campaign_id,
            str(self.total_impressions),
            str(self.total_clicks),
            self.formatted_spend,
            str(self.total_conversions),
            self.formatted_ctr,
            self.formatted_cpa,
        ]

CSV_HEADER = [
    "campaign_id",
    "total_impressions",
    "total_clicks",
    "total_spend",
    "total_conversions",
    "CTR",
    "CPA",
]
