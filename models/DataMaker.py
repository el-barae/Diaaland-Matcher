import re

# This file makes the data into a suitable format for the model to train.


def get_tokens_with_entities(raw_text: str, entities: list):
    raw_tokens = re.split(r"\s(?![^\[]*\])", raw_text)
    tokens_with_entities = []

    for raw_token in raw_tokens:
        token_entities = []
        for entity in entities:
            if entity["start"] <= raw_text.find(raw_token) < entity["end"]:
                token_entities.append(entity)

        if token_entities:
            main_entity = max(token_entities, key=lambda x: len(x["word"]))
            raw_entity_name, raw_entity_value = main_entity["entity_group"], main_entity["word"]

            for i, raw_entity_token in enumerate(re.split("\s", raw_entity_value)):
                entity_prefix = "B" if i == 0 else "I"
                entity_name = f"{entity_prefix}-{raw_entity_name}"
                tokens_with_entities.append((raw_entity_token, entity_name))
        else:
            tokens_with_entities.append((raw_token, "O"))

    return tokens_with_entities



class NERDataMaker:
    def __init__(self, data):
        self.unique_entities = []
        self.processed_texts = []

        temp_processed_texts = []
        for example in data:
            text = example["text"]
            entities = example["entities"]
            tokens_with_entities = get_tokens_with_entities(text, entities)
            for _, ent in tokens_with_entities:
                if ent not in self.unique_entities:
                    self.unique_entities.append(ent)
            temp_processed_texts.append(tokens_with_entities)

        self.unique_entities.sort(key=lambda ent: ent if ent != "O" else "")

        for tokens_with_entities in temp_processed_texts:
            self.processed_texts.append([(t, self.unique_entities.index(ent)) for t, ent in tokens_with_entities])


    @property
    def id2label(self):
        return dict(enumerate(self.unique_entities))

    @property
    def label2id(self):
        return {v:k for k, v in self.id2label.items()}

    def __len__(self):
        return len(self.processed_texts)

    def __getitem__(self, idx):
        def _process_tokens_for_one_text(id, tokens_with_encoded_entities):
            ner_tags = []
            tokens = []
            for t, ent in tokens_with_encoded_entities:
                ner_tags.append(ent)
                tokens.append(t)

            return {
                "id": id,
                "ner_tags": ner_tags,
                "tokens": tokens
            }

        tokens_with_encoded_entities = self.processed_texts[idx]
        if isinstance(idx, int):
            return _process_tokens_for_one_text(idx, tokens_with_encoded_entities)
        else:
            return [_process_tokens_for_one_text(i+idx.start, tee) for i, tee in enumerate(tokens_with_encoded_entities)]

    def as_hf_dataset(self, tokenizer):
        from datasets import Dataset, Features, Value, ClassLabel, Sequence
        def tokenize_and_align_labels(examples):
            tokenized_inputs = tokenizer(examples["tokens"], truncation=True, is_split_into_words=True)

            labels = []
            for i, label in enumerate(examples[f"ner_tags"]):
                word_ids = tokenized_inputs.word_ids(batch_index=i)  # Map tokens to their respective word.
                previous_word_idx = None
                label_ids = []
                for word_idx in word_ids:  # Set the special tokens to -100.
                    if word_idx is None:
                        label_ids.append(-100)
                    elif word_idx != previous_word_idx:  # Only label the first token of a given word.
                        label_ids.append(label[word_idx])
                    else:
                        label_ids.append(-100)
                    previous_word_idx = word_idx
                labels.append(label_ids)

            tokenized_inputs["labels"] = labels
            return tokenized_inputs

        ids, ner_tags, tokens = [], [], []
        for i, pt in enumerate(self.processed_texts):
            ids.append(i)
            pt_tokens,pt_tags = list(zip(*pt))
            ner_tags.append(pt_tags)
            tokens.append(pt_tokens)
        data = {
            "id": ids,
            "ner_tags": ner_tags,
            "tokens": tokens
        }
        features = Features({
            "tokens": Sequence(Value("string")),
            "ner_tags": Sequence(ClassLabel(names=self.unique_entities)),
            "id": Value("int32")
        })
        ds = Dataset.from_dict(data, features)
        tokenized_ds = ds.map(tokenize_and_align_labels, batched=True)
        return tokenized_ds
