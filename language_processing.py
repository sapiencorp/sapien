import json
import asyncio
from pydantic import BaseModel
from typing import Dict, Any
from openai import OpenAI

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    solana_query: str
    explanation: str

def parse_rust_output(rust_output: str) -> Dict[str, Any]:
    start = rust_output.find('{')
    end = rust_output.rfind('}') + 1
    if start == -1 or end == 0:
        return {}
    return json.loads(rust_output[start:end])

async def translate_query(query: str, api_key: str) -> QueryResponse:
    client = OpenAI(api_key=api_key)
    prompt = f"Translate this natural language query into a Solana blockchain data query:\n\n{query}\n\n"
    prompt += "Provide both the query and an explanation of what data this query would fetch."

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a blockchain data translator for Solana."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150
    )

    content = response.choices[0].message.content
    parts = content.split('\n')
    solana_query = parts[0].split(':')[1].strip() if len(parts) > 0 else "unknown"
    explanation = parts[1].split(':')[1].strip() if len(parts) > 1 else "No explanation provided."
    
    return QueryResponse(solana_query=solana_query, explanation=explanation)

async def execute_solana_query(query: str, solana_endpoint: str) -> str:
    return f"Queried {query} on {solana_endpoint}. Result would be here."

async def main():
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)

    user_query = input("Enter your blockchain query in natural language: ")
    translated = await translate_query(user_query, config['api_key'])

    print(f"Translated query: {translated.solana_query}")
    print(f"Explanation: {translated.explanation}")

    result = await execute_solana_query(translated.solana_query, config['solana_endpoint'])
    print(f"Result: {result}")

if __name__ == "__main__":
    asyncio.run(main())
