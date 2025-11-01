#!/usr/bin/env python3
"""
Prepare a small labelled dataset for the safety/detector model.

Inputs:
 - flagged_prompts.log  (produced by your verifier wrapper) -> label "unsafe"
 - seed_safe.txt        (you create, one safe prompt per line) -> label "safe"
 - optional extra_safe/ directory (text files with one prompt per line)

Outputs:
 - data/dataset.csv     (columns: text,label)
 - data/train.csv, data/valid.csv, data/test.csv
"""
import csv
import os
import random
from pathlib import Path

random.seed(42)

ROOT = Path(__file__).resolve().parents[1]  # repo root (week-5)
LOG = ROOT / "flagged_prompts.log"
SEED_SAFE = ROOT / "seed_safe.txt"
EXTRA_SAFE_DIR = ROOT / "extra_safe"
OUT_DIR = ROOT / "data"
OUT_DIR.mkdir(parents=True, exist_ok=True)

def read_flagged():
    items = []
    if not LOG.exists():
        print("Warning: flagged_prompts.log not found:", LOG)
        return items
    with LOG.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # expected "reason<TAB>text"
            parts = line.split("\t", 1)
            if len(parts) == 2:
                _, text = parts
            else:
                text = parts[0]
            items.append(text)
    return items

def read_safe():
    items = []
    if SEED_SAFE.exists():
        with SEED_SAFE.open("r", encoding="utf-8") as f:
            for line in f:
                t = line.strip()
                if t:
                    items.append(t)
    # extra_safe directory optional
    if EXTRA_SAFE_DIR.exists():
        for p in EXTRA_SAFE_DIR.glob("*.txt"):
            with p.open("r", encoding="utf-8") as f:
                for line in f:
                    t = line.strip()
                    if t:
                        items.append(t)
    return items

def dedupe_preserve_order(seq):
    seen = set()
    out = []
    for s in seq:
        if s not in seen:
            seen.add(s)
            out.append(s)
    return out

def write_csv(rows, path):
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["text", "label"])
        for text, label in rows:
            writer.writerow([text, label])

def main():
    unsafe = read_flagged()
    safe = read_safe()
    print(f"Found {len(unsafe)} flagged (unsafe) and {len(safe)} seed safe examples.")
    # If not enough safe examples, warn user
    if len(safe) < 20:
        print("Warning: few safe examples. Add more to seed_safe.txt or extra_safe/*.txt for balanced dataset.")
    # Label them
    rows = []
    rows.extend([(t, "unsafe") for t in unsafe])
    rows.extend([(t, "safe") for t in safe])
    rows = dedupe_preserve_order(rows)
    random.shuffle(rows)

    # Write full dataset
    out_all = OUT_DIR / "dataset.csv"
    write_csv(rows, out_all)
    print("Wrote", out_all, "with", len(rows), "rows")

    # Splits: 70/15/15
    n = len(rows)
    if n < 10:
        print("Too few examples to split; need more data.")
        return
    n_train = int(n * 0.7)
    n_valid = int(n * 0.15)
    train = rows[:n_train]
    valid = rows[n_train:n_train+n_valid]
    test = rows[n_train+n_valid:]
    write_csv(train, OUT_DIR / "train.csv")
    write_csv(valid, OUT_DIR / "valid.csv")
    write_csv(test, OUT_DIR / "test.csv")
    print("Wrote train/valid/test splits:", len(train), len(valid), len(test))

if __name__ == "__main__":
    main()
