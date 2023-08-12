# This file contains the code responsible for training the model


# The model does not know all the words in existance, so the word which are not known are splitted into sub-words:
from DataMaker import NERDataMaker
from data_format import format_data
import os
os.environ['TRANSFORMERS_NO_ADVISORY_WARNINGS'] = 'true'

data = format_data('../../../Annotated0.json')

data_maker = NERDataMaker(data)

from transformers import AutoTokenizer, DataCollatorForTokenClassification, AutoModelForTokenClassification, TrainingArguments, Trainer
tokenizer = AutoTokenizer.from_pretrained("")
data_collator = DataCollatorForTokenClassification(tokenizer=tokenizer)
model = AutoModelForTokenClassification.from_pretrained("", num_labels=len(data_maker.unique_entities), id2label=data_maker.id2label, label2id=data_maker.label2id, ignore_mismatched_sizes=True)

training_args = TrainingArguments(
    output_dir="./results",
    evaluation_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    num_train_epochs=40,
    weight_decay=0.01,
    optim="adamw_torch" 
)

train_ds = data_maker.as_hf_dataset(tokenizer=tokenizer)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_ds,
    eval_dataset=train_ds, # eval on training set! ONLY for DEMO!!
    tokenizer=tokenizer,
    data_collator=data_collator,
)

trainer.train()

