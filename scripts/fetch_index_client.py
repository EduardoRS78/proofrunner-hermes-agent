"""Fetch the official client at an immutable revision and verify its bytes."""
import hashlib
from pathlib import Path
from urllib.request import urlopen

SHA = "87901f8b182a8a7c65ee3dd7267f8f835ee2a545"
HASH = "c3bf54ed37aec22704b8003a7ff6385a1fd3ef49207ce55613ddc41df36a1b01"
URL = f"https://raw.githubusercontent.com/plow-pbc/agent-index-client/{SHA}/standalone/agent_index_client.py"

def main():
    target = Path(__file__).resolve().parents[1] / "vendor" / "agent_index_client.py"
    if target.is_file() and hashlib.sha256(target.read_bytes()).hexdigest() == HASH:
        print("Official Agent Index client already verified")
        return
    with urlopen(URL, timeout=60) as response:
        data = response.read()
    if hashlib.sha256(data).hexdigest() != HASH:
        raise RuntimeError("Official client checksum mismatch; refusing installation")
    target.parent.mkdir(exist_ok=True)
    target.write_bytes(data)
    print("Official Agent Index client installed and verified")

if __name__ == "__main__":
    main()
