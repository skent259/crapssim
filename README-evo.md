# crapssim-evo Enhancements

This fork adds:
- `evo_engine/` package with TableCQ, VarianceScore, EF, and Danger Zone logic.
- Minimal integration hook (to be expanded later).

## Quick Sanity Check
```bash
pip install -r requirements.txt
python examples/run_ef_check.py
```


## Running tests

```bash
pip install -r requirements.txt
pip install pytest pyyaml
python -m pytest -q
```
