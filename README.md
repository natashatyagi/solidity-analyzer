# Solidity Contract Analyzer

An AI-powered tool for analyzing Solidity smart contracts. Uses Google's Gemini API to identify gas optimization opportunities, security vulnerabilities, and code quality issues.

## Features

- **Gas Optimization Analysis**: Identifies opportunities to reduce transaction costs
- **Security Assessment**: Detects potential vulnerabilities and security concerns
- **Code Quality Review**: Suggests improvements for maintainability and readability
- **Structured Reports**: Outputs analysis in human-readable or JSON format

## Prerequisites

- Python 3.8+
- Google Gemini API key (free tier available at https://ai.google.dev/aistudio)

## Installation

1. Clone or download this project
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set up your Gemini API key (choose one method):

### Method A: Environment Variable
```bash
export GEMINI_API_KEY="your-api-key-here"
```

### Method B: .env File
Create a `.env` file in the project root:
```
GEMINI_API_KEY=your-api-key-here
```

## Usage

### Basic Analysis
```bash
python cli.py contracts/MyContract.sol
```

### Save to File
```bash
python cli.py contracts/MyContract.sol --output report.txt
```

### JSON Output
```bash
python cli.py contracts/MyContract.sol --json
```

### Save JSON Report
```bash
python cli.py contracts/MyContract.sol --json --output analysis.json
```

## Example Output

```
======================================================================
SOLIDITY CONTRACT ANALYSIS: SimpleToken
======================================================================

SUMMARY
------
The contract implements a basic token transfer mechanism but has missing
features from standard token interfaces and potential security concerns.

SECURITY CONCERNS
------
[HIGH] Missing ReentrancyGuard
  → Add ReentrancyGuard from OpenZeppelin to prevent reentrancy attacks
  
[MEDIUM] No overflow/underflow protection
  → Use SafeMath or upgrade to Solidity 0.8.0+ for automatic overflow checks

GAS OPTIMIZATION OPPORTUNITIES
------
• Redundant state reads
  → Cache balances[msg.sender] to reduce SLOAD operations

• Inefficient loop patterns
  → Consider using assembly for critical paths

CODE QUALITY IMPROVEMENTS
------
• Missing event emissions
  → Emit events for all state-changing operations for better off-chain tracking

• Incomplete ERC20 implementation
  → Implement full ERC20 standard for interoperability
```

## Project Structure

```
solidity-analyzer/
├── cli.py                    # Command-line interface
├── analyzer.py               # Core analysis logic
├── requirements.txt          # Python dependencies
├── contracts/                # Example Solidity contracts
│   ├── SimpleToken.sol
│   └── Staking.sol
└── README.md                 # This file
```

## How It Works

1. **Contract Reading**: Loads your Solidity file
2. **API Analysis**: Sends contract to Gemini API with specialized prompt
3. **Structured Parsing**: Extracts analysis into structured JSON
4. **Report Generation**: Formats results for readability

## API Rate Limits

The free tier of Gemini API provides:
- 5-15 requests per minute
- 250,000 tokens per minute
- 1,000 requests per day

Each contract analysis uses ~1-2 requests depending on contract size.

## Limitations

- Analysis is AI-assisted; always do manual review for production contracts
- Large contracts (>5000 lines) may hit token limits
- Gemini API free tier has rate limits
- Results should complement, not replace, professional audits

## Getting Your API Key

1. Visit https://ai.google.dev/aistudio
2. Click "Get API key"
3. Create a new key in a Google Cloud project
4. Copy and use with this tool

## Contributing

Feel free to fork, improve, and submit pull requests.

## License

MIT License

## Disclaimer

This tool provides AI-assisted analysis. Always:
- Conduct thorough manual code review
- Test extensively before mainnet deployment
- Consider professional security audits for critical contracts
- Verify all recommendations before implementation

---

**Built with**: Python, Gemini API, ❤️
