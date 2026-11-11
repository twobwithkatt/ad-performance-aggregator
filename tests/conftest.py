import pytest
from pathlib import Path
import tempfile

@pytest.fixture
def sample_csv_data() -> str:
    """Standard CSV sample matching README specifications."""
    return (
        "campaign_id,date,impressions,clicks,spend,conversions\n"
        "CMP001,2025-01-01,12000,300,45.50,12\n"
        "CMP002,2025-01-01,8000,120,28.00,4\n"
        "CMP001,2025-01-02,14000,340,48.20,15\n"
        "CMP003,2025-01-01,5000,60,15.00,3\n"
        "CMP002,2025-01-02,8500,150,31.00,5\n"
        "CMP004,2025-01-01,1000,100,20.00,0\n"  # zero conversions, high CTR = 0.10
    )

@pytest.fixture
def sample_csv_file(sample_csv_data, tmp_path: Path) -> Path:
    csv_file = tmp_path / "sample_ad_data.csv"
    csv_file.write_text(sample_csv_data)
    return csv_file

@pytest.fixture
def malformed_csv_file(tmp_path: Path) -> Path:
    data = (
        "campaign_id,date,impressions,clicks,spend,conversions\n"
        "CMP001,2025-01-01,1000,50,10.00,5\n"
        "CORRUPT_ROW_MISSING_COLS,2025-01-01,100\n"
        "CMP002,2025-01-01,abc,xyz,invalid,foo\n"
        "CMP001,2025-01-02,2000,100,20.00,10\n"
    )
    csv_file = tmp_path / "malformed_ad_data.csv"
    csv_file.write_text(data)
    return csv_file

@pytest.fixture
def empty_csv_file(tmp_path: Path) -> Path:
    data = "campaign_id,date,impressions,clicks,spend,conversions\n"
    csv_file = tmp_path / "empty_ad_data.csv"
    csv_file.write_text(data)
    return csv_file
