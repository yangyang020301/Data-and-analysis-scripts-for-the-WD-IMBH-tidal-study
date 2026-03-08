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

3. Run the notebooks in the `notebooks/`  directory to generate the figures.

## Notes

- The scripts assume the directory structure of this repository. 
  Please make sure the file paths are consistent with the repository layout when running the code.

- Some scripts load `.npz` data files directly. 
  The internal structure and variable names of these files can be seen in the corresponding code where they are loaded.

- Some data files are too large. 
  Due to the size of the `FIG_6_trajectory_data_part` and `all_teukolsky_modes_p_20-40_part` files in the `data_npz` file, they were uploaded in separate volumes. 
  Please download and restore the files to `.npz` format. 
```
cat data_npz/FIG_6_trajectory_data_part/data_FIG_6_trajectory_part_* > data_FIG_6_trajectory.npz
cat data_npz/all_teukolsky_modes_p_20-40_part/all_teukolsky_modes_p_20-40_part_* > all_teukolsky_modes_p_20-40.npz
```  
  
- The interpolant functions in `rt_interpolant_function/` are loaded using `joblib`. 
  Ensure the paths in the scripts correctly point to these files.

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




