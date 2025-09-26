# {{cookiecutter.project_name}}

{{cookiecutter.project_description}}

## Installation

```bash
pip install -e .
```

## Usage

### Training
```bash
python train.py
```

### Evaluation
```bash
python eval.py
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
pip install -e ".[dev]"
```

Run tests:
```bash
pytest
```

Run pre-commit hooks:
```bash
pre-commit run --all-files
```

## Author

{{cookiecutter.project_author_name}} ({{cookiecutter.project_author_email}})

## License

{{cookiecutter.license}}