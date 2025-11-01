import argparse
from pathlib import Path
import pandas as pd
import random
import csv


def read_lines(path):
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    with path.open("r", encoding="utf-8") as f:
        lines = [ln.rstrip() for ln in f.readlines()]
   
    cleaned = []
    for ln in lines:
        if ln is None:
            continue
        ln2 = ln.strip()
        if ln2 == "":
            continue
        cleaned.append(ln2)
    return cleaned


def prepare_dataset(jail_path, benign_path, outdir, seed=42, split=True, train_frac=0.8, dev_frac=0.1, test_frac=0.1):
    random.seed(seed)

    jb = read_lines(jail_path)
    benign = read_lines(benign_path)

    print(f"Read {len(jb)} jailbreak prompts and {len(benign)} benign prompts.")

    rows = []
    for t in jb:
        rows.append({"text": t, "label": 1})
    for t in benign:
        rows.append({"text": t, "label": 0})

    
    seen = set()
    unique_rows = []
    for r in rows:
        txt = r["text"]
        if txt in seen:
            continue
        seen.add(txt)
        unique_rows.append(r)

    print(f"After deduplication: {len(unique_rows)} total examples.")

  
    random.shuffle(unique_rows)

 
    df = pd.DataFrame(unique_rows)

    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)

   
    combined_csv = outdir / "prompt_classifier_train.csv"
    df.to_csv(combined_csv, index=False, quoting=csv.QUOTE_ALL, encoding="utf-8")
    print(f"Wrote combined CSV: {combined_csv} (rows={len(df)})")

   
    if split:
        n = len(df)
        n_train = int(n * train_frac)
        n_dev = int(n * dev_frac)

        n_test = n - n_train - n_dev

        train_df = df.iloc[:n_train].reset_index(drop=True)
        dev_df = df.iloc[n_train : n_train + n_dev].reset_index(drop=True)
        test_df = df.iloc[n_train + n_dev :].reset_index(drop=True)

        train_csv = outdir / "prompt_classifier_train_split_train.csv"
        dev_csv = outdir / "prompt_classifier_train_split_dev.csv"
        test_csv = outdir / "prompt_classifier_train_split_test.csv"

        train_df.to_csv(train_csv, index=False, quoting=csv.QUOTE_ALL, encoding="utf-8")
        dev_df.to_csv(dev_csv, index=False, quoting=csv.QUOTE_ALL, encoding="utf-8")
        test_df.to_csv(test_csv, index=False, quoting=csv.QUOTE_ALL, encoding="utf-8")

        print(f"Wrote train/dev/test splits: {len(train_df)}/{len(dev_df)}/{len(test_df)}")
        print(f"Files: {train_csv}, {dev_csv}, {test_csv}")

    return combined_csv


def main():
    parser = argparse.ArgumentParser(description="Prepare labeled prompt dataset CSV.")
    parser.add_argument("--jailbreaks", required=True, help="Path to jailbreaks_raw.txt")
    parser.add_argument("--benign", required=True, help="Path to benign_raw.txt")
    parser.add_argument("--outdir", default=".", help="Output directory")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for shuffling")
    parser.add_argument("--no-split", dest="split", action="store_false", help="Do not create train/dev/test splits")
    parser.add_argument("--train-frac", type=float, default=0.8, help="Train fraction")
    parser.add_argument("--dev-frac", type=float, default=0.1, help="Dev fraction")
    parser.add_argument("--test-frac", type=float, default=0.1, help="Test fraction (ignored, computed)")

    args = parser.parse_args()


    if args.train_frac <= 0 or args.train_frac >= 1:
        raise ValueError("train-frac must be between 0 and 1")
    if args.dev_frac < 0 or args.dev_frac >= 1:
        raise ValueError("dev-frac must be between 0 and 1")

    prepare_dataset(
        jail_path=args.jailbreaks,
        benign_path=args.benign,
        outdir=args.outdir,
        seed=args.seed,
        split=args.split,
        train_frac=args.train_frac,
        dev_frac=args.dev_frac,
        test_frac=args.test_frac,
    )


if __name__ == "__main__":
    main()

