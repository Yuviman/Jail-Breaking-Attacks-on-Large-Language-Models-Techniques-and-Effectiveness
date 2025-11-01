from datasets import Dataset
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TrainingArguments, Trainer

# preparing datasets
train_ds = Dataset.from_pandas(train_df)  
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")
def preprocess(batch):
    return tokenizer(batch["text"], truncation=True, padding="max_length")
train_ds = train_ds.map(preprocess, batched=True)
model = AutoModelForSequenceClassification.from_pretrained("distilbert-base-uncased", num_labels=2)

args = TrainingArguments("detector-checkpoint", per_device_train_batch_size=8, num_train_epochs=2, logging_steps=10)
trainer = Trainer(model, args, train_dataset=train_ds)
trainer.train()
trainer.save_model("prompt_detector")

