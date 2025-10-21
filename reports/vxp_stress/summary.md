# CrapsSim-Vanilla Expansion — Stress Test Summary

- Timestamp: 2025-10-21 13:23:01 +0000
- Python: 3.11.12
- Platform: Linux-6.12.13-x86_64-with-glibc2.39
- Git: work @ 5d538f0ad932652c4f36771afb92969b61d6b7dd (dirty)

## Smoke (default test run)

- Tests: 3854  | Failures: 0  | Errors: 0  | Skipped: 1  | Time: 14.80s

## Stress (@stress marker)

- Tests: 1  | Failures: 0  | Errors: 0  | Skipped: 0  | Time: 3.15s

### Slowest Stress Cases (top 15)

- 2.082s  tests.stress.test_vxp_torture::test_vxp_heavy_stress  —  passed

### Artifacts

- **junit_smoke**: `reports/vxp_stress/junit_smoke.xml`
- **junit_stress**: `reports/vxp_stress/junit_stress.xml`
- **log_smoke**: `reports/vxp_stress/smoke.log`
- **log_stress**: `reports/vxp_stress/stress.log`
- **summary_md**: `reports/vxp_stress/summary.md`