import pytest
from pathlib import Path
from src.engines.polars_engine import PolarsAggregatorEngine
from src.engines.streaming_engine import StreamingAggregatorEngine

@pytest.mark.parametrize("engine_cls", [PolarsAggregatorEngine, StreamingAggregatorEngine])
def test_engine_basic_aggregation(engine_cls, sample_csv_file: Path):
    """TC-ENG-01: Engine aggregates metrics correctly from CSV."""
    engine = engine_cls()
    top_ctr, top_cpa = engine.process(str(sample_csv_file), top_n=10)

    # In sample_csv_data:
    # CMP001: imp = 12000 + 14000 = 26000, clicks = 300 + 340 = 640, spend = 45.50 + 48.20 = 93.70, conv = 12 + 15 = 27
    # CTR = 640 / 26000 = 0.024615... CPA = 93.70 / 27 = 3.47037...
    # CMP002: imp = 8000 + 8500 = 16500, clicks = 120 + 150 = 270, spend = 28.00 + 31.00 = 59.00, conv = 4 + 5 = 9
    # CTR = 270 / 16500 = 0.016363... CPA = 59.00 / 9 = 6.5555...
    # CMP003: imp = 5000, clicks = 60, spend = 15.00, conv = 3
    # CTR = 60 / 5000 = 0.012, CPA = 15.00 / 3 = 5.00
    # CMP004: imp = 1000, clicks = 100, spend = 20.00, conv = 0
    # CTR = 100 / 1000 = 0.10, CPA = None (0 conv)

    # Top CTR should have CMP004 at index 0 (CTR = 0.10)
    assert top_ctr[0].campaign_id == "CMP004"
    assert top_ctr[0].formatted_ctr == "0.1000"
    assert top_ctr[0].cpa is None
    assert top_ctr[0].formatted_cpa == "null"

    assert top_ctr[1].campaign_id == "CMP001"
    assert top_ctr[1].formatted_ctr == "0.0246"

    # Top CPA should exclude CMP004 (conv = 0)
    # Remaining campaigns by lowest CPA: CMP001 (3.47), CMP003 (5.00), CMP002 (6.56)
    assert len(top_cpa) == 3
    assert [m.campaign_id for m in top_cpa] == ["CMP001", "CMP003", "CMP002"]
    assert top_cpa[0].formatted_cpa == "3.47"

def test_engine_parity(sample_csv_file: Path):
    """TC-ENG-02: Parity between Polars and Pure Python Streaming engine."""
    polars_engine = PolarsAggregatorEngine()
    streaming_engine = StreamingAggregatorEngine()

    p_ctr, p_cpa = polars_engine.process(str(sample_csv_file), top_n=10)
    s_ctr, s_cpa = streaming_engine.process(str(sample_csv_file), top_n=10)

    assert len(p_ctr) == len(s_ctr)
    assert len(p_cpa) == len(s_cpa)

    for p_item, s_item in zip(p_ctr, s_ctr):
        assert p_item.campaign_id == s_item.campaign_id
        assert p_item.total_impressions == s_item.total_impressions
        assert p_item.total_clicks == s_item.total_clicks
        assert p_item.total_spend == pytest.approx(s_item.total_spend, abs=1e-2)
        assert p_item.total_conversions == s_item.total_conversions
        assert p_item.formatted_ctr == s_item.formatted_ctr
        assert p_item.formatted_cpa == s_item.formatted_cpa

    for p_item, s_item in zip(p_cpa, s_cpa):
        assert p_item.campaign_id == s_item.campaign_id
        assert p_item.formatted_cpa == s_item.formatted_cpa
