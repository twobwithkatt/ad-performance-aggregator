import pytest
from pathlib import Path
from src.utils import Timer, get_peak_memory_mb
from src.aggregator import AdPerformanceAggregator

def test_timer_context():
    with Timer() as timer:
        total = sum(range(10000))
    assert timer.elapsed > 0

def test_get_peak_memory():
    mem = get_peak_memory_mb()
    assert mem > 0

def test_aggregator_unsupported_engine():
    with pytest.raises(ValueError, match="Unsupported engine type"):
        AdPerformanceAggregator(engine_type="invalid_engine")

def test_aggregator_streaming_engine_selection(sample_csv_file: Path, tmp_path: Path):
    agg = AdPerformanceAggregator(engine_type="streaming")
    output_dir = tmp_path / "stream_out"
    top_ctr, top_cpa = agg.run(str(sample_csv_file), str(output_dir))
    assert len(top_ctr) > 0
    assert (output_dir / "top10_ctr.csv").exists()
