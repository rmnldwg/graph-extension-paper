"""
Compute the difference between the winning and the base graph model's evidence and
write it to a file.
"""
import json

import paths


if __name__ == "__main__":
    with open(paths.data / "wg_metrics.json") as f:
        winning = json.load(f)

    with open(paths.data / "bg_metrics.json") as f:
        base = json.load(f)

    diff = winning["evidence"] - base["evidence"]

    with open(paths.output / "evidence_diff.txt", "w") as f:
        f.write(f"{diff:.2f}")