import json

# This file formats the data in json file in the output format of the model.


def format_data(file):

    with open(file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    annotated = []

    for job_desc in data['annotations']:
        text = job_desc[0]
        phrase_annot = {'text' : text}
        phrase_annot['entities'] = []
        for element in job_desc[1]['entities']:
            start = element[0]
            end = element[1]
            entity_group = element[2]
            if entity_group == "LOCATION":
                entity_group = "LOC"
            elif entity_group == "ORGANIZATION":
                entity_group = "ORG"
            phrase_annot['entities'].append({
                "entity_group" : entity_group,
                "word": text[start:end],
                "start": start,
                "end": end
            })
        annotated.append(phrase_annot)

    return annotated



def save_data(file, path):
    data = format_data(file)

    with open(path, "w", encoding='utf-8') as f:
        data = json.dumps(data, indent = 4)
        f.write(data)


