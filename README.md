# open-tally

An open-source learning project: tools that make election results **tamper-evident and publicly checkable**, even where there is no network.

Target: be useful before Nigeria's next general election after 2027 (around 2031), by learning one skill at a time and building something real with each.

## Principles

1. **Paper stays the source of truth.** This software verifies and audits; it never replaces ballots or signed result sheets.
2. **Open source from day one.** Nobody should have to trust code they cannot read.
3. **Fake data only** until an independent security review says otherwise. Never run unreviewed code on real votes.
4. **Detectable, not impossible.** We aim to make cheating visible and costly, not to promise it cannot happen.

## Roadmap

| Phase | Build | Status |
|---|---|---|
| 1 | Hash-chained log that detects tampering | **you are here** |
| 2 | Merkle tree with inclusion proofs | |
| 3 | Signed result records (Ed25519) | |
| 4 | Compact record format for QR/SMS, and offline merge | |
| 5 | Risk-limiting audit simulator (fake data) | |
| 6 | Small API and phone client | |
| 7 | Security review of our own code | |
| 8 | Low-stakes real pilot (e.g. a student union vote) | |

## Setup

Phase 1 uses only the Python standard library plus `pytest`.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install pytest
pytest
```

Right now the tests fail. That is intended: your job is to make them pass.

## How to work

1. Read `docs/phase-1-exercise.md`.
2. Implement the functions in `src/open_tally/chainlog.py` one at a time, running `pytest` after each.
3. Break the log by hand and watch `verify()` catch it.
4. Fill in `THREAT_MODEL.md` in your own words.
5. Write an entry in `LEARNING_LOG.md`, then commit.
