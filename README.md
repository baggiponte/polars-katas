<h1 align="center">🐻‍❄️ Polars Katas</h1>

<div align="center">
    <i>
        In data's embrace,<br>
        Polars' dance, a swift, fine art,<br>
        Mastery's soft grace.
    </i>
</div>

---

![polar-youngling](./public/polars-katas.png)

## 🍱 Preparations for this Journey

### ☁️ With cloud editors

Jump straight in the katas by clicking on any of the following links:

**name** | **open in**
:-----: | :-------:
[Polars Katas](./notebooks/polars-katas.ipynb) | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/baggiponte/polars-katas/blob/main/notebooks/polars-katas.ipynb) [![Kaggle](https://kaggle.com/static/images/open-in-kaggle.svg)](https://kaggle.com/kernels/welcome?src=https://github.com/baggiponte/polars-katas/blob/main/notebooks/polars-katas.ipynb) [![SageMaker](https://raw.githubusercontent.com/roboflow-ai/notebooks/main/assets/badges/sage-maker.svg)](https://studiolab.sagemaker.aws/import/github/baggiponte/polars-katas/blob/main/notebooks/polars-katas.ipynb)

### ⛳ Locally

1. Install the project dependencies.

```bash
# with pip
python -m venv -- .venv
source ./.venv/bin/activate
python -m pip install -- "."

# to run data fetching scripts
python -m pip install -- ".[data]"

# to install jupyterlab
python -m pip install -- ".[ide]"
```

> [!TIP]
You can also install the libraries with any modern Python package management tool, such as [`pdm`](https://pdm-project.org/latest/#recommended-installation-method), [`rye`](https://rye-up.com/), [`hatch`](https://hatch.pypa.io/latest/install/) or any other PEP-517 PEP-518 compliant package manger (basically, not `poetry`).

2. Launch an IDE, a REPL or a Jupyter notebook to run the katas. For example:

```python
python -m jupyter lab
```

The notebooks are under the `notebooks` directory.

> [!IMPORTANT]
If you would need a thorough introduction to Polars' internals, you should have a look [here](https://baggiponte.github.io/pbg-polars/1)
