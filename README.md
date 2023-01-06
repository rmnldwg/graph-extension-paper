<p align="center">
<a href="https://github.com/showyourwork/showyourwork">
<img width = "250" src="./src/static/showyourwork.png" alt="showyourwork"/>
</a>
<br>
<br>
<a href="https://github.com/rmnldwg/graph-extension/actions/workflows/build.yml">
<img src="https://github.com/rmnldwg/graph-extension/actions/workflows/build.yml/badge.svg?branch=main" alt="Article status"/>
</a>
<a href="https://github.com/rmnldwg/graph-extension/raw/main-pdf/arxiv.tar.gz">
<img src="https://img.shields.io/badge/article-tarball-blue.svg?style=flat" alt="Article tarball"/>
</a>
<a href="https://github.com/rmnldwg/graph-extension/raw/main-pdf/ms.pdf">
<img src="https://img.shields.io/badge/article-pdf-blue.svg?style=flat" alt="Read the article"/>
</a>
</p>

# Modelling Lymphatic Metastatic Progression in HNSCC: Extending the Graph

**Authors:** 
_Roman Ludwig_[^1], _Jean-Marc Hoffmann_[^1], _Bertrand Pouymayou_[^1], _Panagiotis Balermpas_[^1], _Lauence Bauwens_[^2], _Vincent Grégoire_[^2], _Roland Giger_[^3], _Jan Unkelbach_[^1],

[^1]: University Hospital Zurich, Switzerland
[^2]: Centre Léon Bérard, France
[^3]: Inselspital Bern, Switzerland


This is an open-access _and_ open-source publication that is made fully reproducible with the help of [DVC] and _[showyourwork!]_.

## How to reproduce

There are two levels of how this article can be reproduced:

1. **Shallow:** Every figure and table that contains quantitative findings can be recreated by following the instructions by the _[showyourwork!]_ people. This does not include the results on which the generation of the figures depends. A bit further down I will give a brief manual on how to achieve this "shallow" reproduction and essentially recompile the article from the source code in this repository.
2. **Deep:** The individual experiments that are shown in the article were run and live in a separate GitHub repository called [`rmnldwg/lynference`]. Head over to this repository to learn about how this can be reproduced. This will also involve learning about the tool [DVC].

### Shallow

1. Start by cloning the repository and `cd` into it:

   ```
   $ git clone https://github.com/rmnldwg/graph-extension
   $ cd graph-extension
   ```

2. Install _[showyourwork!]_ (ideally in a separate, virtual environment like [conda] or [venv]) using [pip]:
   
   ```
   $ pip install showyourwork
   ```

3. Tell _[showyourwork!]_ to prepare everything and create the article PDF:
   
   ```
   $ showyourwork build
   ```

## Repository structure

Due to this mix of shallow reproducibility using _[showyourwork!]_ and the deep reproducibility using [DVC], this article repo might not be entirely intuitive to understand. Let me walk you through its layout:

The rendered article PDF lives at the root of this repo and is called `ms.pdf`. Also at the root are the YAML files `showyourwork.yml` and `environment.yml` which define some settings and should not be touched.

Everything else that is not automatically created and managed lives in the `src` directory. Inside of it are another three subdirectories. The `tex` folder contains everything that is necessary to render the article PDF, including the main manuscript file `ms.tex` and the folders where generated results live, namely `figures` and `output`.

The `static` folder is simple: It contains figures that are not dynamically created (like schematics or images).

In `scripts` you can find Python, YAML and [DVC] files. The Python scripts correspond to figures and tables and are dynamically run before compiling the article PDF. However, they often _depend_ on data, which is found in the `data` folder next to the `scripts`. On initial inspection, you will find this folder to be empty. This is because the data is dynamically computed using commands from the [lyscripts] package based on configurations in the YAML files (those back in the `scripts` folder).

One last thing though: The [lyscripts] commands that dynamically compute data that the Python scripts depend on, themselves _depend_ on data from the [`rmnldwg/lynference`] repo. And the [DVC] tool figures out where to get that source data from when reading the `.dvc` files in the `scripts` folder.

### Example

To create figure 4 in the article (the one with the core prevalences), the script `bg_core_prevs.py` will be executed (the name stands for "base graph core prevalences"). It depends **TODO**


[DVC]: https://dvc.org
[showyourwork!]: https://github.com/showyourwork/showyourwork
[`rmnldwg/lynference`]: https://github.com/rmnldwg/lynference
[conda]: https://docs.conda.io/en/latest/
[venv]: https://docs.python.org/3.10/library/venv.html
[pip]: https://pip.pypa.io/en/stable/
[lyscripts]: https://rmnldwg.github.io/lyscripts
