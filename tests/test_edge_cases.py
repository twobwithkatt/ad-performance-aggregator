import pytest
from pathlib import Path
from src.engines.polars_engine import PolarsAggregatorEngine
from src.engines.streaming_engine import StreamingAggregatorEngine

@pytest.mark.parametrize("engine_cls", [PolarsAggregatorEngine, StreamingAggregatorEngine])
def test_empty_csv(engine_cls, empty_csv_file: Path):
    """TC-EDGE-01: Processing empty CSV file produces empty lists."""
    engine = engine_cls()
    top_ctr, top_cpa = engine.process(str(empty_csv_file), top_n=10)
    assert top_ctr == []
    assert top_cpa == []

@pytest.mark.parametrize("engine_cls", [PolarsAggregatorEngine, StreamingAggregatorEngine])
def test_malformed_rows(engine_cls, malformed_csv_file: Path):
    """TC-EDGE-02: Gracefully ignore corrupt rows and parse valid ones."""
    engine = engine_cls()
    top_ctr, top_cpa = engine.process(str(malformed_csv_file), top_n=10)
    assert len(top_ctr) == 1
    assert top_ctr[0].campaign_id == "CMP001"
    assert top_ctr[0].total_impressions == 3000
    assert top_ctr[0].total_clicks == 150
    assert top_ctr[0].total_spend == pytest.approx(30.0, abs=1e-2)
    assert top_ctr[0].total_conversions == 15

@pytest.mark.parametrize("engine_cls", [PolarsAggregatorEngine, StreamingAggregatorEngine])
def test_nonexistent_file(engine_cls):
    """TC-EDGE-03: Raise FileNotFoundError on non-existent input path."""
    engine = engine_cls()
    with pytest.raises(FileNotFoundError):
        engine.process("non_existent_file_path_12345.csv", top_n=10)

@pytest.mark.parametrize("engine_cls", [PolarsAggregatorEngine, StreamingAggregatorEngine])
def test_all_zero_conversions(engine_cls, tmp_path: Path):
    """TC-EDGE-04: When all campaigns have zero conversions, top CPA must be empty."""
    csv_file = tmp_path / "zero_conv.csv"
    csv_file.write_text(
        "campaign_id,date,impressions,clicks,spend,conversions\n"
        "CMP001,2025-01-01,1000,50,10.00,0\n"
        "CMP002,2025-01-01,2000,40,20.00,0\n"
    )
    engine = engine_cls()
    top_ctr, top_cpa = engine.process(str(csv_file), top_n=10)
    assert len(top_ctr) == 2
    assert top_ctr[0].campaign_id == "CMP001"
    assert top_ctr[0].formatted_cpa == "null"
    assert top_cpa == []
