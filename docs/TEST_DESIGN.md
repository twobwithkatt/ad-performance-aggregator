# Test Design & Test Specifications — FV-SEC001

Concise test specifications and validation matrix for the **Ad Performance Aggregator**.

---

## 1. Test Strategy & Scope
- **Methodology**: Test-Driven Development (TDD).
- **Testing Levels**:
  - **Unit Testing**: Calculation accuracy for CTR and CPA, decimal rounding precision, serialization.
  - **Engine Parity**: Bit-for-bit consistency between `PolarsAggregatorEngine` and `StreamingAggregatorEngine`.
  - **Edge Cases & Resilience**: Empty CSV handling, malformed/ragged rows tolerance, zero-division avoidance (`impressions = 0`), zero-conversion handling.
  - **CLI & Integration**: End-to-end command-line invocation, argument parsing, directory auto-creation, exit codes.

---

## 2. Test Cases Matrix

| Test ID | Module / File | Test Objective | Input Condition | Expected Result |
|---|---|---|---|---|
| **TC-01** | `test_models.py` | Standard metric calculations | `imp=10k, clk=500, spend=250, conv=25` | `CTR = 0.0500`, `CPA = 10.00` |
| **TC-02** | `test_models.py` | Zero conversions handling | `conv = 0, spend = 100` | `cpa is None`, formats as `"null"` |
| **TC-03** | `test_models.py` | Zero impressions handling | `imp = 0, clk = 0` | `CTR = 0.0000`, no `ZeroDivisionError` |
| **TC-04** | `test_models.py` | CSV row serialization | Campaign CMP042 sample | Matches specification table layout |
| **TC-05** | `test_engines.py` | Basic aggregation (Polars & Streaming) | 4-campaign sample dataset | Correct metric totals and ranking |
| **TC-06** | `test_engines.py` | Cross-engine parity check | Standard sample dataset | 100% identical outputs between engines |
| **TC-07** | `test_edge_cases.py` | Empty CSV dataset | Header-only file | Returns empty lists, exit code 0 |
| **TC-08** | `test_edge_cases.py` | Malformed/corrupted rows tolerance | Missing columns, string in numeric fields | Skips bad lines gracefully, aggregates valid rows |
| **TC-09** | `test_edge_cases.py` | Missing input file | Non-existent path | Raises `FileNotFoundError` |
| **TC-10** | `test_edge_cases.py` | All campaigns zero conversions | All rows `conv = 0` | Top CTR retains `"null"` CPA, Top CPA list is empty |
| **TC-11** | `test_aggregator.py` | End-to-end CSV export | Sample file, temporary output directory | Generates `top10_ctr.csv` & `top10_cpa.csv` |
| **TC-12** | `test_cli.py` | CLI execution with arguments | `--input`, `--output` flags | Exit code 0, files written |
| **TC-13** | `test_cli.py` | CLI error handling | Invalid/missing file path | Non-zero exit code, error logged to stderr |
| **TC-14** | `test_utils.py` | Execution timer & peak memory | `Timer` context & `get_peak_memory_mb` | Returns positive float numbers (> 0) |

---

## 3. Execution & Verification Report
```bash
# Run all tests with code coverage analysis
pytest -v --cov=src tests/
```
- **Test Result**: **22/22 passed (100%)**.
- **Code Coverage**: **95%**.
