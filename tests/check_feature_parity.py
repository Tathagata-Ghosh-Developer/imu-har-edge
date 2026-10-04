"""Compare on-device feature extraction with the training pipeline.

The decision tree was trained on features computed by NumPy code in
notebooks/model_development.ipynb, but on the board the features are
computed by the pure-Python functions in firmware/model_deployment.py.
Any difference between the two shifts the tree's thresholds.

This script runs both on every 20-sample window (step 10) of
data/sample/*.csv and reports:
  * which of the 126 features disagree, and by how much
  * how often the on-device tree gives a different class when fed the
    firmware features instead of the training features

Run from the repo root:  python tests/check_feature_parity.py
Exit status is 1 if any feature differs by more than the tolerance.
"""
import ast
import csv
import glob
import json
import math
import os
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WINDOW, STEP = 20, 10
CHANNELS = ["ax", "ay", "az", "gx", "gy", "gz"]
STATS = ["mean", "std", "min", "max", "range", "var", "skew", "kurt", "energy",
         "entropy", "rms", "zcr", "mad", "median", "iqr", "autocorr", "wl",
         "dom_freq", "spec_ent", "std_jerk"]
NAMES = [f"{c}_{s}" for c in CHANNELS for s in STATS] + [f"{c}_raw" for c in CHANNELS]
LABELS = {"sitting": 0, "standing": 1, "walking": 2, "brisk_walking": 3, "jogging": 4,
          "cycling": 5, "stair_up": 6, "stair_down": 7, "sit_stand_sit": 8,
          "phone_interaction": 9, "eating_with_spoon": 10, "pick_and_place": 11}
RTOL, ATOL = 1e-6, 1e-9


def training_features():
    """Exec the notebook cell that defines extract_features_window."""
    nb = json.load(open(os.path.join(ROOT, "notebooks", "model_development.ipynb"),
                        encoding="utf-8"))
    for cell in nb["cells"]:
        src = "".join(cell["source"])
        if cell["cell_type"] == "code" and "def extract_features_window" in src:
            ns = {"np": np}
            exec(compile(src, "model_development.ipynb", "exec"), ns)
            return ns["extract_features_window"]
    raise SystemExit("feature cell not found in model_development.ipynb")


def firmware_functions():
    """Load only the function definitions from the MicroPython firmware."""
    path = os.path.join(ROOT, "firmware", "model_deployment.py")
    tree = ast.parse(open(path, encoding="utf-8").read())
    defs = ast.Module(body=[n for n in tree.body if isinstance(n, ast.FunctionDef)],
                      type_ignores=[])
    ns = {"math": math}
    exec(compile(defs, path, "exec"), ns)
    return ns["extract_features_window_manual"], ns["predict_activity_features"]


def windows():
    for path in sorted(glob.glob(os.path.join(ROOT, "data", "sample", "*.csv"))):
        with open(path, newline="") as fh:
            rows = list(csv.DictReader(fh))
        label = LABELS[os.path.splitext(os.path.basename(path))[0]]
        data = np.array([[float(r[c]) for c in CHANNELS] for r in rows])
        for start in range(0, len(data) - WINDOW + 1, STEP):
            yield label, data[start:start + WINDOW]


def main():
    train_fx = training_features()
    dev_fx, predict = firmware_functions()

    n = 0
    worst = np.zeros(len(NAMES))
    bad_counts = np.zeros(len(NAMES), dtype=int)
    same_pred = correct_train = correct_dev = 0
    for label, win in windows():
        f_train = np.asarray(train_fx(win), dtype=float)
        f_dev = np.asarray(dev_fx(win.tolist()), dtype=float)
        diff = np.abs(f_train - f_dev)
        diff[np.isnan(f_train) & np.isnan(f_dev)] = 0.0
        diff[np.isnan(diff)] = np.inf
        bad = diff > ATOL + RTOL * np.abs(f_train)
        bad_counts += bad
        worst = np.maximum(worst, np.where(np.isfinite(diff), diff, np.inf))
        p_train = predict(list(f_train))
        p_dev = predict(list(f_dev))
        same_pred += p_train == p_dev
        correct_train += p_train == label
        correct_dev += p_dev == label
        n += 1

    print(f"windows compared: {n}")
    mismatched = [(NAMES[i], bad_counts[i], worst[i]) for i in range(len(NAMES)) if bad_counts[i]]
    if mismatched:
        print(f"features that differ (> {RTOL:g} relative): {len(mismatched)} of {len(NAMES)}")
        for name, count, w in mismatched:
            print(f"  {name:14s} differs in {count:5d}/{n} windows, max |diff| = {w:.4g}")
    else:
        print(f"all {len(NAMES)} features match within rtol={RTOL:g}")
    print(f"tree prediction identical for training vs firmware features: "
          f"{same_pred}/{n} ({100 * same_pred / n:.2f}%)")
    print(f"label agreement on the sample windows: training features "
          f"{100 * correct_train / n:.2f}%, firmware features {100 * correct_dev / n:.2f}%")
    print("(sample windows come from the training capture, so this is not a test accuracy)")
    sys.exit(1 if mismatched else 0)


if __name__ == "__main__":
    main()
