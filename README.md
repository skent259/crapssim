# CrapsSim Evo


## Recent Updates (2025-08-12)
- **Legal Bet Validation**: All generated strategies now conform to table rules:
  - Whole-dollar bet amounts only
  - Correct minimum increments on 6 and 8
  - No impossible bet combinations
- **New CLI Flags for `run_evolution.py`**:
  - `--out <folder>`: Specify output directory name
  - `--report`: Print end-of-generation reports to stdout
- **Output Structure**:
  - Each run is saved in a timestamped subdirectory under `--out`
  - `summary.json` written at the end with aggregate stats
- **Bug Fixes**:
  - Resolved indentation errors in `run_evolution.py` and `crapssim_adapter.py`
  - Fixed missing `bet_amount` parameter in `BetHardWay` calls
  - Removed stale `BetCome` references
- **Test Improvements**:
  - Cleaned cache directories before running tests
  - Added minimal pytest run targeting adapter handler tests
