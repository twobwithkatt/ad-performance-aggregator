#!/usr/bin/env python3
"""FV-SEC001 - Ad Performance Aggregator CLI Application.

Processes large advertising datasets (~1GB+) and computes aggregated performance metrics:
- Top 10 campaigns with highest CTR
- Top 10 campaigns with lowest CPA (excluding zero conversions)
"""

import argparse
import sys
from pathlib import Path

# Add project root to sys.path so 'src' can be imported cleanly
sys.path.insert(0, str(Path(__file__).resolve().parent))

from src.aggregator import AdPerformanceAggregator
from src.utils import Timer, get_peak_memory_mb


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Aggregate advertising performance metrics from a large CSV dataset.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--input",
        "-i",
        type=str,
        required=True,
        help="Path to the input CSV file (e.g. ad_data.csv)",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        default="results",
        help="Directory to save the aggregated result CSV files",
    )
    parser.add_argument(
        "--engine",
        "-e",
        choices=["polars", "streaming"],
        default="polars",
        help="Execution engine: 'polars' (high performance) or 'streaming' (O(1) memory, zero dependencies)",
    )
    parser.add_argument(
        "--top-n",
        "-n",
        type=int,
        default=10,
        help="Number of top campaigns to rank",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    input_file = Path(args.input)
    if not input_file.exists():
        print(f"Error: Input file does not exist: {args.input}", file=sys.stderr)
        return 1

    print("=" * 60)
    print("FV-SEC001: Ad Performance Aggregator")
    print(f"Input file:  {args.input}")
    print(f"Output dir:  {args.output}")
    print(f"Engine:      {args.engine}")
    print(f"Top N:       {args.top_n}")
    print("=" * 60)

    try:
        aggregator = AdPerformanceAggregator(engine_type=args.engine)

        with Timer() as timer:
            top_ctr, top_cpa = aggregator.run(
                input_path=args.input,
                output_dir=args.output,
                top_n=args.top_n,
            )

        peak_mem = get_peak_memory_mb()

        print("\nProcessing completed successfully!")
        print(f"Elapsed Time:    {timer.elapsed:.2f} seconds")
        print(f"Peak Memory:     {peak_mem:.2f} MB")
        print(f"Successfully generated result files:")
        print(f"  - Top CTR: {Path(args.output) / 'top10_ctr.csv'}")
        print(f"  - Top CPA: {Path(args.output) / 'top10_cpa.csv'}")
        print("=" * 60)
        return 0

    except Exception as exc:
        print(f"Error during execution: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
