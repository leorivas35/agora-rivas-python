# agora-rivas-python

This repository contains a starter project skeleton for a Python application built around Clean Architecture principles.

## Architecture overview

The project is split into these layers:

- `domain`: business entities, value objects, domain rules, and repository contracts
- `application`: use cases and application-level orchestration
- `infrastructure`: concrete repository and external service implementations
- `interfaces`: API routes and adapters
- `bootstrap`: dependency wiring

## Project structure

```text
src/
  agora_rivas/
    domain/
    application/
    infrastructure/
    interfaces/
    bootstrap/
    main.py

tests/
  unit/
```

## Quick start

```bash
python -m venv .venv
. .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e .[dev]
pytest
```

## Run the app

```bash
python -m agora_rivas.main
```
