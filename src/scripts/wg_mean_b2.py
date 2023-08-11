"""
Write mean spread probability from the tumor to LNL II to a file.
"""
from pathlib import Path

from emcee.backends import HDFBackend

import paths


INPUT = paths.data / "wg_samples.hdf5"
OUTPUT = (paths.output / Path(__file__).name).with_suffix(".txt")
THIN = 10


if __name__ == "__main__":
    # open samples
    backend = HDFBackend(paths.data / INPUT, read_only=True)
    samples = backend.get_chain(flat=True, thin=THIN)

    # compute mean
    mean = samples[:, 1].mean()

    # write to file
    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write(f"{mean:.2%}")
