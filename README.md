# zk-block-soundness

## Overview
**zk-block-soundness** is a lightweight CLI tool for verifying block integrity on EVM-compatible chains by generating a checksum based on block metadata.  
It can be used for monitoring block-level consistency and data reliability in **Aztec**, **Zama**, or general Web3 networks.

## Features
- Fetches detailed block info (number, timestamp, hash, transaction count)  
- Computes a keccak-based checksum for reproducible block integrity checks  
- JSON output for monitoring, CI/CD, or zk-proof validation pipelines  
- Compatible with any EVM RPC (Ethereum, Arbitrum, Optimism, Base, etc.)  
- Safe and read-only  

## Installation
1. Install Python 3.9+  
2. Install dependencies:
   pip install web3
3. Optionally set your RPC endpoint:
   export RPC_URL=https://mainnet.infura.io/v3/YOUR_KEY

## Usage
Analyze the latest block:
   python app.py

Analyze a specific block:
   python app.py --block 21000000

Emit JSON output for automation:
   python app.py --block 21000000 --json
   
## Example Output
🕒 Timestamp: 2025-11-08T12:22:35.415Z  
🔧 zk-block-soundness  
🔗 RPC: https://mainnet.infura.io/v3/YOUR_KEY  
🧭 Chain ID: 1  
🧱 Analyzing block: 21000000  
📦 Block #21000000  
⏰ Timestamp: 2023-10-24T09:35:20Z  
🔹 Block hash: 0x45a4b49f32a9911d56f884fd8d82c7d98bb9ff5c8826763b7ef88d5dca8a245e  
🔸 Integrity checksum: 0x71ff3f52922153b0d8abf71c53aa1a9e5cc7e13dd1e31d9c94179e14ee53d0a3  
📊 Transactions: 182  
⏱️ Completed in 0.41s  

## Notes
- This tool computes an additional keccak checksum for quick integrity validation.  
- The checksum is deterministic — it will always match for identical block data.  
- Useful for verifying RPC consistency or cross-node synchronization.  
- Works across all EVM-based chains and archive nodes.  
- Can be integrated into nightly monitoring pipelines to detect block divergence.  
- For Aztec/Zama use, block checksum validation ensures proof soundness and data reproducibility.  
- Exit codes:  
  `0` → success  
  `2` → failed to fetch block data.  
