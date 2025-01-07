use solana_sdk::{
    client::nonblocking::rpc_client::RpcClient,
    pubkey::Pubkey,
    commitment_config::CommitmentConfig,
};
use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize, Debug)]
struct QueryResult {
    result: String,
}

async fn get_solana_data(client: &RpcClient, query: &str) -> Result<QueryResult, Box<dyn std::error::Error>> {
    let result = match query {
        "balance" => {
            let pubkey = Pubkey::new_unique(); // In real use, you'd use an actual user's pubkey
            let balance = client.get_balance_with_commitment(&pubkey, CommitmentConfig::confirmed()).await?;
            format!("Balance: {} SOL", balance/1e9) // SOL has 9 decimal places
        },
        "transaction_count" => {
            let count = client.get_transaction_count().await?;
            format!("Total transactions: {}", count)
        },
        _ => "Unsupported query".to_string(),
    };
    Ok(QueryResult { result })
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let client = RpcClient::new("https://api.devnet.solana.com");
    let result = get_solana_data(&client, "balance").await?;
    println!("{:?}", result);
    Ok(())
}
