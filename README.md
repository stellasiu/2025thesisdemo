# Speaking Volumes: How Acoustic Features Reveal Speaker Height

This repository contains scripts and tools for preprocessing, feature extraction, and regression modeling of my master's thesis.
The project includes modules for working with pitch (F0), formants, MFCCs, and various regression methods.

---

## Repository Structure

<pre>
2025thesisdemo
├── regression/
│   ├── f0_sr.py
│   ├── formants_sr.py
│   ├── formants_mr.py
│   ├── formants_rf.py
│   ├── mfcc_sr.py
│   ├── mfcc_mr.py
│   ├── mfcc_rf.py
│
├── preprocessing/
│   ├── timitrename.py
│   ├── sr2s.py
│   ├── phn2txt.py
│   ├── txt2grid.py
│   ├── heightconversion.py
│
├── extraction/
│   ├── f0_all.praat
│   ├── formants_all.praat
│   ├── mfcc_phoneme.py
│
├── cleaning/
│   ├── praat_sm_clean.py
│
├── stat/
│   ├── stat_example.py
│
├── image/
│   ├── heatmap.png
│   ├── fiplot.png
│
└── README.md
</pre>

## Usage Instruction

1. Download the dataset (TIMIT)

```bash
wget https://data.deepai.org/timit.zip
unzip timit.zip -d 'path to timit data folder'
```

2. Preprocessing
  - Download all the Python scripts, adjust the root directory of TIMIT dataset accordingly.
  - Use sr2s.py to convert all start and end times in the .PHN files from sample indices to seconds.
  - Use phn2txt.py to convert .PHN to .txt.
  - Use txt2grid.py to create .TextGrid files for phoneme alignment.
  - Use timitrename.py to copy and rename all the required files (.WAV and .TextGrid) to a new directory. Filenames will contain details in this pattern: "train/test_dialect region_speaker ID_prompt name".
  - Since TIMIT dataset uses feet and inches as metric unit for length measurement, use heightconversion.py to get speaker ID and height information converted to cm. This will also prevent using unnessary metadata.

```bash
python3 'name of the python script you want to use'
```

3. Feature Extraction
  - F0 and formants are extracted using [Praat](https://www.fon.hum.uva.nl/praat/). Download the praat script files, choose Praat > Open Praat script, update the input and output path. Each .WAV file will generate a .csv file, modifying is recommended to eliminate manual files arrangement. Note: Praat cannot process more than 10,000 files at once, manual file batching is recommended.
  - MFCC are extrated using Python, mfcc_phoneme.py will extract 13 MFCCs for each phoneme, this can be modified to fit individual need.

4. Data Cleaning
  - praat_sm_clean.py is a sample Python script that requires manual editing to fit project usage. This script allows parsing file information which follows the naming pattern used in timitrename.py, merging extracted features (.csv files) according to train or test set, and with height data.

5. Regression
  - Regression directory contains all the regression models named after "feature set_regression model".
  - Each script will run the height prediction and generate a heatmap (and feature importance score plot for random forest regression).
  - Manual editing of root is required.

Example of heatmap:
![alt text]( "Heatmap of Formants of Simple linear regression")

Example of feature importance score plot:
![alt text]( "Formants feature importance score plot of Random forest regression")

6. Statistical Analysis
  - stat_example.py is provided as a sample script that use all performs Friedman test and generate a boxplot.
![alt text]( "Boxplot of Simple Linear Regression Comparison")

## License
This project is licensed under the MIT License.

## Citation
Citation details will be provided after the successful upload of the associated thesis.
