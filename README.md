# Data and analysis scripts for the WD-IMBH tidal study
# Paper Data and Reproduction Scripts

This repository contains the data and code used to reproduce figures from Yang et al. (2026) arXiv:2602.22688. 
The goal is to allow others to inspect, verify, and reproduce the results.

## Repository Structure

```
notebooks/                  # Jupyter notebooks used for figure generation
data_npz/                   # Data files used to reproduce the figures
rt_interpolant_function/    # Interpolant functions for tidal disruption radius
function_py/                # Python functions and analysis scripts
Figure/                     # Figures from the paper (9 figures)

README.md                   # Project description
LICENSE                     # MIT License
.gitignore                  # Files ignored by git
```


## Environment and Dependencies

The scripts were tested with Python 3.13. 
They are expected to work with most recent Python 3 versions.

Main dependencies include:

```
numpy

scipy

matplotlib

joblib 

kerrgeopy

lisatools
```

The scripts also use several modules from the Python standard library.

## Reproducing the Figures

The figures in the paper can be reproduced using the notebooks in the notebooks/ directory.

Typical workflow:

1. Clone the repository

```
git clone https://github.com/yangyang020301/Data-and-analysis-scripts-for-the-WD-IMBH-tidal-study.git
cd your-repository
```

2. Install the required dependencies

```
pip install numpy scipy matplotlib joblib
pip install kerrgeopy lisatools
```

3. Run the notebooks in the notebooks/  directory to generate the figures.

## Citation

If you use the data or code from this repository, please cite the associated paper:

BibTeX:

```bibtex
@misc{yang2026relativistictidaldissipationgravitationalwave,
      title={Relativistic Tidal Dissipation and the Gravitational-wave Signal of a White Dwarf Orbiting an Intermediate-Mass Black Hole}, 
      author={Yang Yang and Leif Lui and Alejandro Torres-Orjuela and Xian Chen},
      year={2026},
      eprint={2602.22688},
      archivePrefix={arXiv},
      primaryClass={astro-ph.HE},
      url={https://arxiv.org/abs/2602.22688}, 
}
```

## License

This project is released under the MIT License.




