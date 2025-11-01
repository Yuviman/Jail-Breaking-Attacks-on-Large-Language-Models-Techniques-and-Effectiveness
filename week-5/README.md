# Week-5

### Sanitizer (code/sanitizer.py)
Cleans input text, removes HTML, normalizes casing, and de-obfuscates leetspeak (e.g. 1gn0r3 → ignore).

### Rewriter (code/rewriter.py)
Rewrites or neutralizes unsafe instructions into factual, harmless prompts.

### Verifier (code/verifier.py)
Uses regex rules to detect procedural, harmful, or policy-bypass content.

### ML Detector (code/train_detector.py)
A TF-IDF + Logistic Regression model trained to classify prompts as safe or unsafe.

### Evaluation Notebook (code/eval_pipeline.ipynb)
Integrates all modules to evaluate and visualize performance on test data and adversarial variants.

- Prepare dataset → python scripts/prepare_ml_dataset.py

- Train detector → python code/train_detector.py

- Evaluate pipeline → run code/eval_pipeline.ipynb

- Generate adversarial variants → test obfuscation resistance

### Appended slips and retrain to continuously harden the model.

## Key Outputs
File	                      Description
data/dataset.csv	          Labeled combined dataset
models/tfidf.joblib	        Saved TF-IDF vectorizer
models/clf.joblib	          Trained classifier
data/test_eval_results.csv	Pipeline evaluation results


100 % detection accuracy on test and adversarial variants.

Combined sanitizer + rewriter + verifier + ML pipeline fully operational.
