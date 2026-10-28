import json

import pytest

from open_tally import chainlog


def make_log(tmp_path, count=3):
    path = tmp_path / "log.jsonl"
    for i in range(count):
        chainlog.append(path, {"unit": f"PU-{i:03d}", "votes": 100 + i})
    return path


def test_append_builds_a_chain(tmp_path):
    path = tmp_path / "log.jsonl"
    first = chainlog.append(path, {"unit": "PU-001", "votes": 120})
    second = chainlog.append(path, {"unit": "PU-002", "votes": 98})

    assert first["index"] == 0
    assert first["prev_hash"] == chainlog.GENESIS_HASH
    assert second["index"] == 1
    assert second["prev_hash"] == first["hash"]
    assert first["hash"] != second["hash"]


def test_hash_ignores_key_order():
    a = chainlog.compute_hash(0, {"a": 1, "b": 2}, chainlog.GENESIS_HASH)
    b = chainlog.compute_hash(0, {"b": 2, "a": 1}, chainlog.GENESIS_HASH)
    assert a == b
    assert len(a) == 64


def test_untouched_log_verifies(tmp_path):
    path = make_log(tmp_path)
    assert chainlog.verify(path) == []


def test_edited_record_is_detected(tmp_path):
    path = make_log(tmp_path)
    lines = path.read_text().splitlines()
    entry = json.loads(lines[1])
    entry["record"]["votes"] = 999
    lines[1] = json.dumps(entry)
    path.write_text("\n".join(lines) + "\n")

    assert chainlog.verify(path) != []


def test_deleted_record_is_detected(tmp_path):
    path = make_log(tmp_path)
    lines = path.read_text().splitlines()
    del lines[1]
    path.write_text("\n".join(lines) + "\n")

    assert chainlog.verify(path) != []


@pytest.mark.stretch
def test_truncated_tail_needs_a_known_head(tmp_path):
    path = make_log(tmp_path)
    head = chainlog.head_hash(path)

    lines = path.read_text().splitlines()
    path.write_text("\n".join(lines[:-1]) + "\n")

    # The shorter chain is internally consistent, so plain verify cannot see it.
    assert chainlog.verify(path) == []
    # Someone holding the earlier head hash can.
    assert chainlog.verify(path, expected_head=head) != []
