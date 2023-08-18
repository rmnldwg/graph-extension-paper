"""
Write the expected risk of LNL II and its standard deviation to a file.
"""
import h5py

import paths


INPUT = paths.data / "wg_risks.hdf5"
OUTPUT = paths.output / "wg_II_risks.tex"


if __name__ == "__main__":
    # open risks
    with h5py.File(INPUT, "r") as f:
        risks = f["early/II/N0"][:]

    # compute mean and standard deviation
    mean = 100 * risks.mean()
    stddev = 100 * risks.std()

    # write to file
    with open(OUTPUT, "w") as f:
        f.write(f"{mean:.2f} \% $\pm$ {stddev:.2f} \%")
