import pytest
from pathlib import Path
from src.aggregator import AdPerformanceAggregator

def test_full_pipeline_export(sample_csv_file: Path, tmp_path: Path):
    """TC-AGG-01: End-to-end processing and CSV file export."""
    output_dir = tmp_path / "results"
    aggregator = AdPerformanceAggregator(engine_type="polars")
    
    result = aggregator.run(
        input_path=str(sample_csv_file),
        output_dir=str(output_dir),
        top_n=10,
    )

    ctr_file = output_dir / "top10_ctr.csv"
    cpa_file = output_dir / "top10_cpa.csv"

    assert ctr_file.exists()
    assert cpa_file.exists()

    ctr_lines = ctr_file.read_text().strip().splitlines()
    assert ctr_lines[0] == "campaign_id,total_impressions,total_clicks,total_spend,total_conversions,CTR,CPA"
    # Header + 4 campaigns in sample
    assert len(ctr_lines) == 5

    cpa_lines = cpa_file.read_text().strip().splitlines()
    assert cpa_lines[0] == "campaign_id,total_impressions,total_clicks,total_spend,total_conversions,CTR,CPA"
    # Header + 3 campaigns with conv > 0
    assert len(cpa_lines) == 4
