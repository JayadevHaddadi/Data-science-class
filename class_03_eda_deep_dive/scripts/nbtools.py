"""Tiny helpers shared by the Class 03 notebook generators.

* Cell DSL:  md / code / note / predict, each tagged with an audience
              ("all", "instr" or "student")
* build():   turn a cell list into an .ipynb dict for one audience
* render():  execute the code cells and store outputs (plots, tables, prints)
             inside the notebook so the instructor can preview it without running it
* setup_cell(): the Colab-friendly setup cell, with the dataset embedded in the notebook
             (the repo may be private, so notebooks must work without any download)
"""
import ast
import base64
import gzip
import io
import json
import os
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "datasets")
NB_DIR = os.path.join(HERE, "..", "notebooks")


# ---------------------------------------------------------------- cell DSL
def md(text, aud="all"):
    return {"type": "md", "text": text.strip("\n"), "aud": aud}


def code(text, aud="all"):
    return {"type": "code", "text": text.strip("\n"), "aud": aud}


def note(text):
    """Instructor-only talking points (rendered as a coloured quote block)."""
    body = "\n".join("> " + line if line.strip() else ">" for line in text.strip("\n").splitlines())
    return {"type": "md", "text": body, "aud": "instr"}


def predict(prompt, instr_hint=""):
    """A 'predict before you run' box. Students answer in chat."""
    text = f"### 🔮 PREDICT (answer in chat *before* running the next cell)\n\n{prompt}"
    cells = [md(text)]
    if instr_hint:
        cells.append(note(instr_hint))
    return cells


def flatten(items):
    out = []
    for it in items:
        out.extend(it if isinstance(it, list) else [it])
    return out


def build(cells, audience):
    """audience: 'instr' or 'student'"""
    nb_cells = []
    for c in flatten(cells):
        if c["aud"] not in ("all", audience):
            continue
        src = c["text"].splitlines(keepends=True)
        if c["type"] == "md":
            nb_cells.append({"cell_type": "markdown", "metadata": {}, "source": src})
        else:
            nb_cells.append({"cell_type": "code", "execution_count": None, "metadata": {},
                             "outputs": [], "source": src})
    return {
        "cells": nb_cells,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python"},
            "colab": {"provenance": []},
        },
        "nbformat": 4,
        "nbformat_minor": 4,
    }


def save(nb, filename):
    path = os.path.join(NB_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)
    return path


# ---------------------------------------------------------------- setup cell
def _embed(name):
    with open(os.path.join(DATA, f"campus_survey_{name}.csv"), "rb") as f:
        return base64.b64encode(gzip.compress(f.read(), 9)).decode()


def setup_cell(datasets=("clean",)):
    blobs = ",\n    ".join(f'"{n}": "{_embed(n)}"' for n in datasets)
    return code(f'''#@title ▶️ Setup — run this cell first (double-click to see the code) {{ display-mode: "form" }}
import base64, gzip, io, warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

warnings.filterwarnings("ignore")
sns.set_theme(style="whitegrid", context="notebook")
plt.rcParams["figure.dpi"] = 110
pd.set_option("display.max_columns", 30)

# The survey data is stored inside this notebook, so nothing needs to be downloaded.
_DATA = {{
    {blobs}
}}

def load(name="clean"):
    """load('raw') -> messy survey file | load('clean') -> cleaned survey file"""
    return pd.read_csv(io.BytesIO(gzip.decompress(base64.b64decode(_DATA[name]))))

print("✅ Setup complete. Available datasets:", list(_DATA))''')


# ---------------------------------------------------------------- renderer
class _Collector:
    def __init__(self):
        self.outputs, self.text = [], []

    # stdout-like
    def write(self, s):
        self.text.append(s)
        return len(s)

    def flush(self):
        pass

    def _flush_text(self):
        if self.text:
            joined = "".join(self.text)
            self.outputs.append({"name": "stdout", "output_type": "stream",
                                 "text": joined.splitlines(keepends=True)})
            self.text = []

    def rich(self, obj, execute=False):
        self._flush_text()
        data = {"text/plain": repr(obj).splitlines(keepends=True)}
        if hasattr(obj, "_repr_html_"):
            html = obj._repr_html_()
            if html:
                data["text/html"] = html.splitlines(keepends=True)
        if execute:
            self.outputs.append({"output_type": "execute_result", "execution_count": 1,
                                 "metadata": {}, "data": data})
        else:
            self.outputs.append({"output_type": "display_data", "metadata": {}, "data": data})

    def figures(self, *a, **k):
        self._flush_text()
        for n in plt.get_fignums():
            fig = plt.figure(n)
            buf = io.BytesIO()
            fig.savefig(buf, format="png", bbox_inches="tight")
            self.outputs.append({"output_type": "display_data", "metadata": {},
                                 "data": {"image/png": base64.b64encode(buf.getvalue()).decode(),
                                          "text/plain": ["<Figure>"]}})
            plt.close(fig)


def render(nb):
    """Execute every code cell in order (shared namespace) and attach outputs."""
    ns = {"__name__": "__main__"}
    plt.show = lambda *a, **k: None  # replaced per cell below
    problems = []
    for i, cell in enumerate(nb["cells"]):
        if cell["cell_type"] != "code":
            continue
        col = _Collector()
        ns["display"] = lambda obj, c=col: c.rich(obj)
        plt.show = lambda *a, c=col, **k: c.figures()
        src = "".join(cell["source"])
        old = sys.stdout
        sys.stdout = col
        try:
            tree = ast.parse(src)
            last = None
            if tree.body and isinstance(tree.body[-1], ast.Expr):
                last = ast.Expression(tree.body.pop().value)
            exec(compile(tree, f"<cell {i}>", "exec"), ns)
            if last is not None:
                val = eval(compile(last, f"<cell {i}>", "eval"), ns)
                if val is not None:
                    col.rich(val, execute=True)
        except Exception as e:  # noqa: BLE001
            col._flush_text()
            col.outputs.append({"output_type": "error", "ename": type(e).__name__, "evalue": str(e),
                                "traceback": [f"{type(e).__name__}: {e}"]})
            problems.append((i, f"{type(e).__name__}: {e}"))
        finally:
            sys.stdout = old
        col.figures()
        col._flush_text()
        cell["outputs"] = col.outputs
        cell["execution_count"] = i + 1
    return problems
