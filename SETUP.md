# Project environment: Vaccination Coverage & Disease Incidence

The project uses an ETL workflow: historical CDC vaccination coverage data and disease surveillance reports are extracted and cleaned, merged by state and year (with disease labels for incidence), and loaded into a combined dataset for the analysis engine.

## Software used

- **Python:** 3.12
- **Spyder IDE:** 5.5.1
- **R:** 4.5.1
- **RStudio:** used to work with the R ingestion scripts (exact RStudio version not recorded)

## Install Python dependencies

From the project directory, preferably in a fresh environment:

```bash
python -m pip install -r requirements.txt
```

If you already use **Anaconda / Conda** to manage Spyder, prefer installing Spyder 5.5.1 with Conda rather than replacing your existing Spyder installation with pip:

```bash
conda install spyder=5.5.1
```

Then install the project libraries in the appropriate environment. Avoid installing a different Spyder version into an existing Conda base environment via pip.

## Install R and RStudio separately

Install R and the RStudio desktop IDE. Then, from R or the RStudio console, run:

```r
source("requirements_R.R")
```

This installs `tidyverse` (including `dplyr`, `tidyr`, `ggplot2`, and `readr`) and `Hmisc` if needed.

## Notes

- The correct Python package name for reading RData/RDS exports is **`pyreadr`**, not `pdfreadr`.
- `scipy.stats` is a submodule of **`scipy`**, so only `scipy` belongs in requirements.txt.
- **`pypdf`** handles PDF files. It is different from `pyreadr`.
- Standard Python libraries (`pathlib`, `subprocess`, `re`, `csv`, etc.) do not need entries in `requirements.txt`.
- `streamlit` and `plotly` are commented out as optional because the final dashboard stack may differ.
- Only Spyder's version is pinned in `requirements.txt`; package versions should be pinned later using the actual environment if exact reproducibility is required (e.g., `python -m pip freeze`).
