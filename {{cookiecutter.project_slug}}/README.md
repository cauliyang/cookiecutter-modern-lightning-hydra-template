# {{cookiecutter.project_name}}

{{cookiecutter.project_description}}

## Installation

```bash
uv sync
```

## Usage

### Training
```bash
uv run train.py
```

### Evaluation
```bash
uv run eval.py
```

## Project Structure

```
├── configs/                   # Configuration files
├── data/                     # Data directory
├── logs/                     # Training logs
├── notebooks/                # Jupyter notebooks
├── scripts/                  # Utility scripts
├── tests/                    # Test files
├── {{cookiecutter.package_name}}/           # Main package
├── train.py                  # Training script
├── eval.py                   # Evaluation script
├── Makefile                  # Make commands
└── pyproject.toml           # Project dependencies
```

## Development

Install development dependencies:
```bash
uv sync --dev
```

Run tests:
```bash
uv run pytest
```

Run pre-commit hooks:
```bash
pre-commit run --all-files
```

## Author

{{cookiecutter.project_author_name}} ({{cookiecutter.project_author_email}})

## License

{{cookiecutter.license}}