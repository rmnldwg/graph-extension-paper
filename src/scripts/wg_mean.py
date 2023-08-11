"""
Write all mean parameter samples to a file.
"""
from pathlib import Path

from emcee.backends import HDFBackend

import paths


INPUT = paths.data / "wg_samples.hdf5"
OUTPUT = paths.output
THIN = 10
NAMES = ["b1", "b2", "b3", "b4", "b5", "b7", "t21", "t23", "t25", "t34", "t35", "late_p"]


if __name__ == "__main__":
    # open samples
    backend = HDFBackend(paths.data / INPUT, read_only=True)
    samples = backend.get_chain(flat=True, thin=THIN)

    for i in range(samples.shape[1]):
        # compute mean
        mean = samples[:, i].mean()

        # write to file
        filename = f"wg_mean_{NAMES[i]}.txt"
        with open(OUTPUT / filename, "w", encoding="utf-8") as f:
            f.write(f"{mean:.2%}")
