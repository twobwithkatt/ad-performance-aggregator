from abc import ABC, abstractmethod
from typing import Tuple, List
from src.models import CampaignMetrics

class BaseAggregatorEngine(ABC):
    """Abstract base class for aggregation engines."""

    @abstractmethod
    def process(
        self, input_path: str, top_n: int = 10
    ) -> Tuple[List[CampaignMetrics], List[CampaignMetrics]]:
        """Process the input CSV file and return (top_n_ctr, top_n_cpa) metrics.

        Args:
            input_path: Path to the input CSV file.
            top_n: Number of top campaigns to return (default: 10).

        Returns:
            Tuple containing:
                - List of top N campaigns with highest CTR
                - List of top N campaigns with lowest CPA (excluding campaigns with 0 conversions)
        """
        pass
