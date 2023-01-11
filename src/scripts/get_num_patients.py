"""
Extract the number of patients used for training.
"""
import pandas as pd

import paths


INPUT = paths.data / "patients.csv"
OUTPUT = paths.output / "num_patients.txt"


if __name__ == "__main__":
    patients = pd.read_csv(INPUT, header=[0,1])
    num_patients = len(patients)

    with open(OUTPUT, mode="w", encoding="utf-8") as txt_file:
        txt_file.write(str(num_patients))
