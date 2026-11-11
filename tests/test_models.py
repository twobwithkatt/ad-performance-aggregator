import pytest
from src.models import CampaignMetrics

def test_metrics_calculation_standard():
    """TC-MOD-01: Calculate CTR and CPA with standard values."""
    m = CampaignMetrics(
        campaign_id="CMP001",
        total_impressions=10000,
        total_clicks=500,
        total_spend=250.0,
        total_conversions=25,
    )
    assert m.ctr == pytest.approx(0.05, abs=1e-6)
    assert m.cpa == pytest.approx(10.0, abs=1e-6)
    assert m.formatted_ctr == "0.0500"
    assert m.formatted_cpa == "10.00"
    assert m.formatted_spend == "250.00"

def test_metrics_zero_conversions():
    """TC-MOD-02: Zero conversions should yield None / null CPA."""
    m = CampaignMetrics(
        campaign_id="CMP002",
        total_impressions=5000,
        total_clicks=200,
        total_spend=100.0,
        total_conversions=0,
    )
    assert m.ctr == pytest.approx(0.04, abs=1e-6)
    assert m.cpa is None
    assert m.formatted_cpa == "null"

def test_metrics_zero_impressions():
    """TC-MOD-03: Zero impressions should yield 0.0 CTR without error."""
    m = CampaignMetrics(
        campaign_id="CMP003",
        total_impressions=0,
        total_clicks=0,
        total_spend=50.0,
        total_conversions=5,
    )
    assert m.ctr == 0.0
    assert m.formatted_ctr == "0.0000"
    assert m.cpa == pytest.approx(10.0, abs=1e-6)

def test_to_csv_row():
    """Verify standard CSV serialization matching the README table format."""
    m = CampaignMetrics(
        campaign_id="CMP042",
        total_impressions=125000,
        total_clicks=6250,
        total_spend=12500.5,
        total_conversions=625,
    )
    assert m.to_csv_row() == [
        "CMP042",
        "125000",
        "6250",
        "12500.50",
        "625",
        "0.0500",
        "20.00",
    ]
