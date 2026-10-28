"""Phase 1: a hash-chained, append-only log stored as JSON lines."""
import hashlib
import json
from pathlib import Path

GENESIS_HASH = "0" * 64


def compute_hash(index: int, record: dict, prev_hash: str) -> str:
    data = {"index": index, "record": record, "prev_hash": prev_hash}
    text = json.dumps(data, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(text.encode()).hexdigest()


def append(path: Path, record: dict) -> dict:
    path = Path(path)
    index = 0
    prev_hash = GENESIS_HASH

    if path.exists() and path.read_text().strip():
        last_line = path.read_text().splitlines()[-1]
        last = json.loads(last_line)
        index = last["index"] + 1
        prev_hash = last["hash"]

    entry = {
        "index": index,
        "record": record,
        "prev_hash": prev_hash,
        "hash": compute_hash(index, record, prev_hash),
    }
    with open(path, "a") as f:
        f.write(json.dumps(entry) + "\n")
    return entry


def verify(path: Path, expected_head: str | None = None) -> list[str]:
    problems = []
    previous = GENESIS_HASH

    for i, line in enumerate(Path(path).read_text().splitlines()):
        entry = json.loads(line)

        if entry["index"] != i:
            problems.append(f"entry {i}: wrong index {entry['index']}")
        if entry["prev_hash"] != previous:
            problems.append(f"entry {i}: broken link to the previous entry")
        fresh = compute_hash(entry["index"], entry["record"], entry["prev_hash"])
        if entry["hash"] != fresh:
            problems.append(f"entry {i}: contents were changed")

        previous = entry["hash"]

    if expected_head is not None and previous != expected_head:
        problems.append("final hash does not match the expected head")

    return problems


def head_hash(path: Path) -> str:
    lines = Path(path).read_text().splitlines()
    if not lines:
        return GENESIS_HASH
    return json.loads(lines[-1])["hash"]
