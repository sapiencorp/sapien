import json
import subprocess
from pydantic import BaseModel
from typing import Dict, Any
from openai import OpenAI

class ContractAnalysisRequest(BaseModel):
    contract_data: str
    analysis_type: str

class ContractAnalysisResponse(BaseModel):
    explanation: str
    risks: List[str]
    benefits: List[str]

def parse_rust_output(rust_output: str) -> Dict[str, Any]:
    start = rust_output.find('{')
    end = rust_output.rfind('}') + 1
    if start == -1 or end == 0:
        return {}
    return json.loads(rust_output[start:end])

def analyze_contract_with_llm(contract_data: Dict[str, Any], analysis_type: str, api_key: str) -> ContractAnalysisResponse:
    client = OpenAI(api_key=api_key)
    prompt = f"Analyze the following Solana smart contract for {analysis_type}:\n\n{json.dumps(contract_data)}\n\n"
    prompt += "Provide an explanation, list potential risks, and benefits."

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a smart contract analyst for Solana."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000
    )

    analysis = response.choices[0].message.content
    return ContractAnalysisResponse(
        explanation=analysis,
        risks=[],
        benefits=[]
    )

def main():
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)

    rust_output = subprocess.run(['cargo', 'run', '--release', '--', config['contract_path']], capture_output=True, text=True).stdout
    parsed_contract = parse_rust_output(rust_output)

    analysis = analyze_contract_with_llm(parsed_contract, config['analysis_type'], config['api_key'])
    
    print("Contract Analysis:")
    print(f"Explanation: {analysis.explanation}")
    print(f"Risks: {analysis.risks}")
    print(f"Benefits: {analysis.benefits}")

if __name__ == "__main__":
    main()
