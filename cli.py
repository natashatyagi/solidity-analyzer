#!/usr/bin/env python3
"""
Solidity Contract Analyzer CLI
Analyzes Solidity smart contracts for gas optimization, security, and code quality.
"""

import sys
import json
import argparse
from pathlib import Path
from analyzer import SolidityAnalyzer


def main():
    parser = argparse.ArgumentParser(
        description="Analyze Solidity smart contracts for gas optimization, security, and code quality.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cli.py contracts/MyContract.sol
  python cli.py contracts/MyContract.sol --output report.json
  python cli.py contracts/MyContract.sol --json
        """
    )
    
    parser.add_argument(
        "contract_file",
        help="Path to the Solidity contract file (.sol)"
    )
    parser.add_argument(
        "-o", "--output",
        help="Save report to file (txt or json)",
        default=None
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output raw JSON analysis"
    )
    
    args = parser.parse_args()
    
    try:
        # Initialize analyzer
        analyzer = SolidityAnalyzer()
        
        # Read contract
        print(f"Reading contract from {args.contract_file}...", file=sys.stderr)
        contract_code = analyzer.read_contract(args.contract_file)
        
        # Analyze
        print("Analyzing contract with Gemini API...", file=sys.stderr)
        analysis = analyzer.analyze(contract_code)
        
        # Output
        if args.json:
            output = json.dumps(analysis, indent=2)
        else:
            output = analyzer.format_report(analysis)
        
        print(output)
        
        # Save to file if requested
        if args.output:
            output_path = Path(args.output)
            output_path.write_text(output)
            print(f"\nReport saved to {args.output}", file=sys.stderr)
    
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nInterrupted by user", file=sys.stderr)
        sys.exit(130)


if __name__ == "__main__":
    main()
