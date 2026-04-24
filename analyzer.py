import os
from pathlib import Path
from typing import Optional
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class SolidityAnalyzer:
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the Solidity analyzer with Gemini API."""
        key = api_key or os.getenv("GEMINI_API_KEY")
        if not key:
            raise ValueError(
                "GEMINI_API_KEY not provided. Set it as an environment variable or pass it directly."
            )
        
        genai.configure(api_key=key)
        self.model = genai.GenerativeModel("gemini-2.5-flash")
    
    def read_contract(self, file_path: str) -> str:
        """Read a Solidity contract from file."""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Contract file not found: {file_path}")
        if not path.suffix == ".sol":
            raise ValueError(f"Expected .sol file, got: {path.suffix}")
        
        return path.read_text()
    
    def analyze(self, contract_code: str) -> dict:
        """Analyze a Solidity contract using Gemini API."""
        
        prompt = f"""You are a Solidity smart contract security and optimization expert. Analyze the following Solidity contract and provide a detailed assessment.

Return your analysis as a structured JSON response with these exact keys:
- "contract_name": (string) Name of the main contract
- "gas_optimizations": (list) Array of gas optimization opportunities with 'issue' and 'suggestion' keys
- "security_concerns": (list) Array of security issues with 'severity' (CRITICAL/HIGH/MEDIUM/LOW), 'issue', and 'recommendation' keys
- "code_quality": (list) Array of code quality improvements with 'issue' and 'suggestion' keys
- "summary": (string) Brief overall assessment (2-3 sentences)

SOLIDITY CONTRACT:
```solidity
{contract_code}
```

Provide ONLY valid JSON, no additional text."""

        try:
            response = self.model.generate_content(prompt)
            return self._parse_response(response.text)
        except Exception as e:
            raise RuntimeError(f"Gemini API error: {str(e)}")
    
    def _parse_response(self, response_text: str) -> dict:
        """Parse the Gemini response into structured JSON."""
        import json
        
        # Try to extract JSON from response
        try:
            # If the response is wrapped in markdown code blocks, extract it
            if "```json" in response_text:
                json_str = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                json_str = response_text.split("```")[1].split("```")[0].strip()
            else:
                json_str = response_text.strip()
            
            return json.loads(json_str)
        except (json.JSONDecodeError, IndexError) as e:
            raise RuntimeError(f"Failed to parse Gemini response as JSON: {str(e)}\nResponse: {response_text}")
    
    def format_report(self, analysis: dict) -> str:
        """Format analysis results into a readable report."""
        report = []
        report.append("=" * 70)
        report.append(f"SOLIDITY CONTRACT ANALYSIS: {analysis.get('contract_name', 'Unknown')}")
        report.append("=" * 70)
        report.append("")
        
        # Summary
        report.append("SUMMARY")
        report.append("-" * 70)
        report.append(analysis.get("summary", "No summary available"))
        report.append("")
        
        # Security Concerns
        report.append("SECURITY CONCERNS")
        report.append("-" * 70)
        security = analysis.get("security_concerns", [])
        if security:
            for item in security:
                severity = item.get("severity", "UNKNOWN")
                issue = item.get("issue", "Unknown issue")
                recommendation = item.get("recommendation", "No recommendation")
                report.append(f"[{severity}] {issue}")
                report.append(f"  → {recommendation}")
                report.append("")
        else:
            report.append("No security concerns identified.")
            report.append("")
        
        # Gas Optimizations
        report.append("GAS OPTIMIZATION OPPORTUNITIES")
        report.append("-" * 70)
        gas = analysis.get("gas_optimizations", [])
        if gas:
            for item in gas:
                issue = item.get("issue", "Unknown issue")
                suggestion = item.get("suggestion", "No suggestion")
                report.append(f"• {issue}")
                report.append(f"  → {suggestion}")
                report.append("")
        else:
            report.append("No gas optimization opportunities identified.")
            report.append("")
        
        # Code Quality
        report.append("CODE QUALITY IMPROVEMENTS")
        report.append("-" * 70)
        quality = analysis.get("code_quality", [])
        if quality:
            for item in quality:
                issue = item.get("issue", "Unknown issue")
                suggestion = item.get("suggestion", "No suggestion")
                report.append(f"• {issue}")
                report.append(f"  → {suggestion}")
                report.append("")
        else:
            report.append("No code quality issues identified.")
            report.append("")
        
        report.append("=" * 70)
        return "\n".join(report)
