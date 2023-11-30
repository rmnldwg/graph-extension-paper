"""
Compute the difference between the winning and the loosing graph model's evidence and
write it to a file.
"""
import json

import paths


if __name__ == "__main__":
    with open(paths.data / "wg_metrics.json", encoding="utf-8") as f:
        winning = json.load(f)

    with open(paths.data / "lg_metrics.json", encoding="utf-8") as f:
        loose = json.load(f)

    diff = winning["evidence"] - loose["evidence"]

    with open(paths.output / "evidence_diff.txt", "w", encoding="utf-8") as f:
        f.write(f"{diff:.2f}")
