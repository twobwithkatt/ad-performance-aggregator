import subprocess
import sys
from pathlib import Path

def test_cli_execution_success(sample_csv_file: Path, tmp_path: Path):
    """TC-CLI-01: CLI executes and writes output CSV files."""
    output_dir = tmp_path / "cli_results"
    cmd = [
        sys.executable,
        "aggregator.py",
        "--input",
        str(sample_csv_file),
        "--output",
        str(output_dir),
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    assert res.returncode == 0
    assert "Successfully generated" in res.stdout
    assert (output_dir / "top10_ctr.csv").exists()
    assert (output_dir / "top10_cpa.csv").exists()

def test_cli_missing_input(tmp_path: Path):
    """TC-CLI-02: CLI reports error and returns non-zero code on missing file."""
    output_dir = tmp_path / "cli_results"
    cmd = [
        sys.executable,
        "aggregator.py",
        "--input",
        "missing_file_xyz.csv",
        "--output",
        str(output_dir),
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    assert res.returncode != 0
    assert "Error" in res.stderr or "Error" in res.stdout
