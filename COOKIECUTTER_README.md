# Modern Lightning Hydra Cookiecutter Template

This is a cookiecutter template for creating PyTorch Lightning projects with Hydra configuration management.

## Quick Start

### Install Cookiecutter

```bash
pip install cookiecutter
```

### Generate New Project

```bash
cookiecutter https://github.com/{{ cookiecutter.github_username }}/modern-lightning-hydra-template
```

Or if you have cloned this repository locally:

```bash
cookiecutter path/to/modern-lightning-hydra-template
```

### What You Get

After running cookiecutter, you'll be prompted to fill in the following information:

- **project_name**: The name of your project (e.g., "My Lightning Project")
- **project_slug**: Python package name (auto-generated from project_name)
- **package_name**: The name of your Python package (same as project_slug)
- **project_author_name**: Your name
- **project_author_email**: Your email address
- **project_description**: A brief description of your project
- **project_version**: Initial version (default: "0.1.0")
- **python_version**: Python version requirement (default: "3.10")
- **license**: License type (MIT, Apache-2.0, BSD-3-Clause, GPL-3.0, None)
- **github_username**: Your GitHub username
- **github_repo_name**: Repository name (auto-generated)

## Features

The generated project includes:

✅ **PyTorch Lightning** - For structured ML training  
✅ **Hydra** - For configuration management  
✅ **Modern Python tooling** - uv, ruff, pre-commit hooks  
✅ **Experiment tracking** - Support for W&B, TensorBoard, MLflow, etc.  
✅ **Testing** - pytest setup with example tests  
✅ **CI/CD** - GitHub Actions workflows  
✅ **Documentation** - README with examples and best practices  

## Project Structure

```
{{ cookiecutter.project_name }}
├── configs/                  # Hydra configuration files
├── {{ cookiecutter.package_name }}/           # Your Python package
│   ├── data/                # Data modules
│   ├── models/              # Model definitions
│   └── utils/               # Utility functions  
├── tests/                   # Test files
├── scripts/                 # Utility scripts
├── notebooks/               # Jupyter notebooks
├── .github/workflows/       # CI/CD workflows
├── pyproject.toml          # Project metadata and dependencies
├── environment.yaml        # Conda environment
└── README.md              # Project documentation
```

## After Generation

1. **Initialize git repository:**
   ```bash
   cd {{ cookiecutter.project_name }}
   git init
   git add .
   git commit -m "Initial commit"
   ```

2. **Set up environment:**
   ```bash
   # Using uv (recommended)
   pip install uv
   uv sync
   
   # Or using conda
   conda env create -f environment.yaml
   conda activate {{ cookiecutter.package_name }}
   ```

3. **Install pre-commit hooks:**
   ```bash
   pre-commit install
   ```

4. **Run a test training:**
   ```bash
   uv run train.py trainer=cpu  # For CPU training
   uv run train.py trainer=gpu  # For GPU training (if available)
   ```

## Next Steps

- Customize the model architecture in `{{ cookiecutter.package_name }}/models/`
- Update data loading in `{{ cookiecutter.package_name }}/data/`  
- Configure experiments in `configs/experiment/`
- Add your own datasets and preprocessing logic
- Set up experiment tracking (W&B, TensorBoard, etc.)

Happy coding! 🚀