---
title: Overview
hide:
- feedback
---

# gale-shapley

A Python implementation of the celebrated Gale-Shapley (a.k.a. the Deferred Acceptance) Algorithm.

Time complexity is O(n^2), space complexity is O(n).

## Installation

```bash
pip install gale-shapley-algorithm
```

With CLI support:

```bash
pip install "gale-shapley-algorithm[cli]"
```

With GUI:

```bash
pip install "gale-shapley-algorithm[gui]"
```

## Quick Start

### As a Library

```python
import gale_shapley_algorithm as gsa

result = gsa.create_matching(
    proposer_preferences={
        "alice": ["bob", "charlie"],
        "dave": ["charlie", "bob"],
    },
    responder_preferences={
        "bob": ["alice", "dave"],
        "charlie": ["dave", "alice"],
    },
)
print(result.matches)  # {'alice': 'bob', 'dave': 'charlie'}
```

### As a CLI

```bash
# Run with default settings
uvx --from "gale-shapley-algorithm[cli]" python -m gale_shapley_algorithm

# See all options
uvx --from "gale-shapley-algorithm[cli]" python -m gale_shapley_algorithm --help
```

### With Docker

```bash
# Build the image
docker build -t gale-shapley .

# Run with a config file
docker run --rm -it \
  -v $(pwd)/config/example_config_custom_input.yaml:/app/config/config.yaml \
  -v $(pwd)/logs:/app/logs \
  gale-shapley

# Run the GUI
docker run --rm -p 8000:8000 gale-shapley \
  uv run uvicorn gale_shapley_algorithm._api.app:app --host 0.0.0.0 --port 8000
```

## Development

This project is managed with [uv](https://github.com/astral-sh/uv) and uses [taskipy](https://github.com/taskipy/taskipy) for task running.

```bash
git clone https://github.com/oedokumaci/gale-shapley-algorithm
cd gale-shapley
uvx --from taskipy task setup   # Install dependencies
uvx --from taskipy task run     # Run the application
uvx --from taskipy task fix     # Auto-format + lint fix
uvx --from taskipy task ci      # Run all CI checks
uvx --from taskipy task test    # Run tests
uvx --from taskipy task docs    # Serve docs locally
```
