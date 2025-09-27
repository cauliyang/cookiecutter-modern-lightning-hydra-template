
{{ cookiecutter.project_description }}

## Installation

#### Pip

```bash
# clone project
git clone https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.github_repo_name }}
cd {{ cookiecutter.github_repo_name }}

# install pytorch according to instructions
# https://pytorch.org/get-started/

# install requirements
pip install uv
uv sync
```

## How to run

Train model with default configuration

```bash
# train on CPU
uv run train.py trainer=cpu

# train on GPU
uv run train.py trainer=gpu
```

Train model with chosen experiment configuration from [configs/experiment/](configs/experiment/)

```bash
uv run train.py experiment=experiment_name.yaml
```

You can override any parameter from command line like this

```bash
uv run train.py trainer.max_epochs=20 data.batch_size=64
```
