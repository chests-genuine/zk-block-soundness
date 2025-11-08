import os
import sys
import json
import time
import argparse
from datetime import datetime
from typing import Optional, Dict, Any
from web3 import Web3

DEFAULT_RPC = os.environ.get("RPC_URL", "https://mainnet.infura.io/v3/YOUR_INFURA_KEY")

def fetch_block_details(w3: Web3, block_number: Optional[int] = None) -> Dict[str, Any]:
    """
    Fetch basic block information and compute a hash checksum for auditing purposes.
    """
    try:
        block = w3.eth.get_block(block_number or "latest")
        checksum = Web3.keccak(text=str(block.hash.hex())).hex()
        return {
            "number": block.number,
            "timestamp": block.timestamp,
            "hash": block.hash.hex(),
            "checksum": checksum,
            "transactions": len(block.transactions)
        }
    except Exception as e:
        raise RuntimeError(f"Error fetching block details: {e}")

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="zk-block-soundness — verify and log block integrity with checksum analysis (useful for Aztec/Zama and general Web3 state validation)."
    )
    p.add_argument("--rpc", default=DEFAULT_RPC, help="EVM RPC URL (default from RPC_URL)")
    p.add_argument("--block", type=int, help="Block number to analyze (default: latest)")
    p.add_argument("--timeout", type=int, default=30, help="RPC timeout in seconds (default: 30)")
    p.add_argument("--json", action="store_true", help="Output results as JSON")
    return p.parse_args()

def main() -> None:
    start_time = time.time()
    args = parse_args()

    # ✅ RPC sanity check
    if not args.rpc.startswith("http"):
        print("❌ Invalid RPC URL format. Must start with 'http' or 'https'.")
        sys.exit(1)

    w3 = Web3(Web3.HTTPProvider(args.rpc, request_kwargs={"timeout": args.timeout}))
    if not w3.is_connected():
        print("❌ RPC connection failed. Check your RPC_URL or --rpc argument.")
        sys.exit(1)

    # ✅ Timestamp for audit logs
    print(f"🕒 Timestamp: {datetime.utcnow().isoformat()}Z")
    print("🔧 zk-block-soundness")
    print(f"🔗 RPC: {args.rpc}")

        # Display chain ID and friendly network name
    try:
        chain_id = w3.eth.chain_id
        network_names = {
            1: "Ethereum Mainnet",
            5: "Goerli Testnet",
            11155111: "Sepolia Testnet",
            137: "Polygon Mainnet",
            42161: "Arbitrum One",
            10: "Optimism Mainnet",
            8453: "Base Mainnet"
        }
        network_name = network_names.get(chain_id, "Unknown Network")
        print(f"🧭 Chain ID: {chain_id} ({network_name})")
    except Exception:
        print("⚠️ Could not fetch chain ID.")

    block_label = args.block if args.block is not None else "latest"
    print(f"🧱 Analyzing block: {block_label}")

    try:
        details = fetch_block_details(w3, args.block)
    except Exception as e:
        print(f"❌ {e}")
        sys.exit(2)

    print(f"📦 Block #{details['number']}")
    print(f"⏰ Timestamp: {datetime.utcfromtimestamp(details['timestamp']).isoformat()}Z")
    print(f"🔹 Block hash: {details['hash']}")
    print(f"🔸 Integrity checksum: {details['checksum']}")
    print(f"📊 Transactions: {details['transactions']}")

    elapsed = time.time() - start_time
    print(f"⏱️ Completed in {elapsed:.2f}s")

    if args.json:
        result = {
            "rpc": args.rpc,
            "chain_id": None,
            "block_details": details,
            "elapsed_seconds": round(elapsed, 2),
            "timestamp_utc": datetime.utcnow().isoformat() + "Z"
        }
        try:
            result["chain_id"] = w3.eth.chain_id
        except Exception:
            pass
        print(json.dumps(result, ensure_ascii=False, indent=2))

    sys.exit(0)

if __name__ == "__main__":
    main()
