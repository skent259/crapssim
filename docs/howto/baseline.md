# How to Regenerate Baseline

```bash
python tools/api_baseline_smoke.py
python tools/api_fingerprint.py
cat reports/baseline/fingerprint.txt
```

Expect:
- 3 JSON files + 1 fingerprint.txt
- engine_api.version = 0.2.0-api.p2
- 64-hex fingerprint hash.
