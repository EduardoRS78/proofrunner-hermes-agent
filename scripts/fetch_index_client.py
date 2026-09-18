"""Fetch the official client at an immutable revision and verify its bytes."""
import hashlib
from pathlib import Path
from urllib.request import urlopen

SHA = "3f116994930cb3d1c23a485851953dd6c1eef039"
HASH = "b23e7db974b1bd00b50557b44d759df170fc6ef17b471c9cfc0cd975843b535c"
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
