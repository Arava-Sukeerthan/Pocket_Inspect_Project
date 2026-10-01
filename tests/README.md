# Test Suite (`tests/`)

Automated test suite using `pytest` for verifying functionality across `src/` modules.

## Organization
- `test_acquisition.py`: Tests for frame ingestion and camera interfaces.
- `test_quality.py`: Tests for blur and exposure assessment functions.
- `test_inference.py`: Tests for runtime abstraction contracts.
- `test_adaptation.py`: Tests for policy evaluation engines.
- `test_monitoring.py`: Tests for system metrics parsing.

## Execution
```bash
pytest tests/
```
