import csv
from pathlib import Path
from typing import Tuple, List, Optional
import logging

from src.models import CampaignMetrics, CSV_HEADER
from src.engines.base import BaseAggregatorEngine
from src.engines.polars_engine import PolarsAggregatorEngine
from src.engines.streaming_engine import StreamingAggregatorEngine
from src.utils import Timer, get_peak_memory_mb

logger = logging.getLogger("AdPerformanceAggregator")

class AdPerformanceAggregator:
    """Coordinates data aggregation and result generation."""

    def __init__(self, engine_type: str = "polars"):
        self.engine_type = engine_type.lower()
        self.engine: BaseAggregatorEngine = self._resolve_engine(self.engine_type)

    def _resolve_engine(self, engine_type: str) -> BaseAggregatorEngine:
        if engine_type == "polars":
            try:
                return PolarsAggregatorEngine()
            except ImportError:
                logger.warning("Polars not installed, falling back to pure Python streaming engine.")
                return StreamingAggregatorEngine()
        elif engine_type in ("streaming", "python"):
            return StreamingAggregatorEngine()
        else:
            raise ValueError(f"Unsupported engine type: '{engine_type}'. Choose 'polars' or 'streaming'.")

    def run(
        self,
        input_path: str,
        output_dir: str,
        top_n: int = 10,
    ) -> Tuple[List[CampaignMetrics], List[CampaignMetrics]]:
        """Executes full aggregation pipeline and writes output CSV files."""
        out_path = Path(output_dir)
        out_path.mkdir(parents=True, exist_ok=True)

        top_ctr, top_cpa = self.engine.process(input_path, top_n=top_n)

        # Export top10_ctr.csv
        ctr_file = out_path / "top10_ctr.csv"
        self._write_csv(ctr_file, top_ctr)

        # Export top10_cpa.csv
        cpa_file = out_path / "top10_cpa.csv"
        self._write_csv(cpa_file, top_cpa)

        return top_ctr, top_cpa

    @staticmethod
    def _write_csv(file_path: Path, rows: List[CampaignMetrics]) -> None:
        with open(file_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(CSV_HEADER)
            for item in rows:
                writer.writerow(item.to_csv_row())
