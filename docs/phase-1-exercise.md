# Phase 1: a hash-chained log

## The idea

Store records one per line. Each entry holds a hash of its own contents **and** the hash of the entry before it. Change or remove any earlier entry and every later hash stops matching, so tampering shows up.

Each line in the file is a JSON object:

```json
{"index": 0, "record": {"unit": "PU-001", "votes": 120}, "prev_hash": "000...0", "hash": "ab12..."}
```

- `index` counts from 0.
- `prev_hash` of the first entry is `GENESIS_HASH` (64 zeros).
- `hash` is SHA-256 over `index`, `record` and `prev_hash`.

## Your tasks

Work in `src/open_tally/chainlog.py`. Run `pytest` after each step.

1. **`compute_hash`**: build a string from `index`, `record` and `prev_hash`, then hash it with `hashlib.sha256`.
   - Hint: use `json.dumps(..., sort_keys=True, separators=(",", ":"))` so the same data always gives the same text. Ask yourself why key order would otherwise break verification.
2. **`append`**: read the last entry (if any), build the new entry, write it as one line.
   - Hint: opening the file in append mode (`"a"`) adds to the end.
3. **`verify`**: walk the file and check, for each entry, that the index is right, `prev_hash` matches the previous entry's hash, and the stored `hash` equals a fresh `compute_hash`. Return a list of problem descriptions; an empty list means valid.
4. **Break it by hand.** Create a log, edit one number in the file with a text editor, and run `verify`. Then delete a middle line.

## Stretch goal

Deleting the **last** entry leaves a perfectly valid shorter chain, so `verify(path)` alone cannot see it. Implement `head_hash(path)` and the `expected_head` argument of `verify`. Think about who should hold a copy of the latest hash, and why one holder is not enough. That question leads straight to Phase 2 and to public mirrors.

## Questions to answer in your learning log

- Why does an attacker who edits entry 3 also have to rewrite entries 4, 5 and so on?
- If one person controls the whole file, can they rewrite the whole chain? What stops them?
- What would you add so that rewriting becomes detectable by someone else?
