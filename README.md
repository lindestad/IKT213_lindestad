# IKT213 Coursework

This repository contains assignments for IKT213. Pixi is used and recommended for dependency and environment management. You can alternatively use uv (virtualenv) or Anaconda/conda if you prefer.

## Assignments

- [Assignment 1](assignment_1/)

## Recommended: Pixi

Pixi manages both conda packages and PyPI packages from a single `pyproject.toml`.

```powershell
# from repo root
pixi install
pixi run python --version
```

Run an assignment:

```powershell
pixi run python assignment_1/main.py
```

## Alternative: uv (virtualenv)

```powershell
# from repo root
uv venv .venv
# Then activate the virtual environment (command printed by uv)
uv sync
python assignment_1/main.py
```

## Alternative: Anaconda/conda

```powershell
conda create -n ikt213 python=3.12 -y
conda activate ikt213
pip install opencv-python numpy
# pip install whatever else is needed. Use pixi for a consistent cross-platform setup.
python assignment_1/main.py
```
