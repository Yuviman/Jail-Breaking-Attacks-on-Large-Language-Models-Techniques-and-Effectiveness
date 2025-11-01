import pandas as pd
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
import joblib

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
MODEL_DIR = ROOT / "models"
MODEL_DIR.mkdir(exist_ok=True)

def load_csv(name):
    return pd.read_csv(DATA / name)

def train():
    # If explicit splits exist, use them; otherwise use dataset.csv and make a split
    if (DATA / "train.csv").exists() and (DATA / "valid.csv").exists():
        train = load_csv("train.csv")
        valid = load_csv("valid.csv")
    else:
        df = pd.read_csv(DATA / "dataset.csv")
        # simple deterministic split
        n = len(df)
        n_train = int(n * 0.7)
        n_valid = int(n * 0.15)
        train = df.iloc[:n_train].reset_index(drop=True)
        valid = df.iloc[n_train:n_train+n_valid].reset_index(drop=True)

    X_train = train["text"].astype(str).tolist()
    y_train = train["label"].map({"safe":0, "unsafe":1}).tolist()
    X_valid = valid["text"].astype(str).tolist()
    y_valid = valid["label"].map({"safe":0, "unsafe":1}).tolist()

    vect = TfidfVectorizer(ngram_range=(1,2), max_features=20000)
    Xtr = vect.fit_transform(X_train)
    Xv = vect.transform(X_valid)

    clf = LogisticRegression(max_iter=1000, class_weight='balanced')
    clf.fit(Xtr, y_train)

    # Eval
    preds = clf.predict(Xv)
    print("Validation classification report:")
    print(classification_report(y_valid, preds, target_names=["safe","unsafe"]))
    print("Confusion matrix:")
    print(confusion_matrix(y_valid, preds))

    # Save model + vectorizer
    joblib.dump(vect, MODEL_DIR / "tfidf.joblib")
    joblib.dump(clf, MODEL_DIR / "clf.joblib")
    print("Saved models to", MODEL_DIR)

if __name__ == "__main__":
    train()
