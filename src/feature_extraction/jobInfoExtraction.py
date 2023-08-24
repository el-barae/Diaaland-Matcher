from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
import pandas as pd
from spacy.lang.fr import French
from spacy.lang.en import English
from langdetect import detect


class JobInfoExtraction:

    def __init__(self, custom_model_path, custom_tokenizer_path, jobs, DEGREES_IMPORTANCE, skills_patterns_path):
        self.jobs = jobs
        self.model = BertForTokenClassification.from_pretrained(custom_model_path)
        self.tokenizer = AutoTokenizer.from_pretrained(custom_tokenizer_path)
        self.degrees_importance = DEGREES_IMPORTANCE
        self.skills_patterns_path = skills_patterns_path

    @staticmethod
    def predict_named_entities(self, text):
        nlp = pipeline('ner', model=self.model, tokenizer=self.tokenizer, aggregation_strategy="simple")
        return nlp(text)

    @staticmethod
    def extract_named_entities(self, predicted_labels):
        entities = [(element['word'], element['entity_group']) for element in predicted_labels]
        return entities
        
    @staticmethod
    def match_experience_by_custom_ner(self, job):
        predicted_labels = self.predict_named_entities(job)
        named_entities = self.extract_named_entities(predicted_labels)

        acceptable_experiences = {entity_text for entity_text, entity_type in named_entities if entity_type == "EXP"}

        return list(acceptable_experiences)


    # def match_skills_by_custom_ner(self, job):
    #     predicted_labels = self.predict_named_entities(job)
    #     named_entities = self.extract_named_entities(predicted_labels)

    #     job_skills = []
    #     for entity_text, entity_type in named_entities:
    #         if entity_type == "SKILL":
    #             normalized_skill = entity_text.replace("-", " ")
    #             if normalized_skill not in job_skills:
    #                 job_skills.append(normalized_skill)
    #     return job_skills

    @staticmethod
    def match_skills_by_spacy(self, job):
        language = detect(job)
        nlp = French() if language.lower() == 'fr' else English()

        ruler = nlp.add_pipe('entity_ruler')
        ruler.from_disk(self.skills_patterns_path)

        doc = nlp(job)
        job_skills = list(set([ent.label_.split('|')[1].replace('-', ' ') for ent in doc.ents if ent.label_.startswith('SKILL')]))
        return job_skills

    @staticmethod
    def match_jobtitle_by_custom_ner(self, job):
        predicted_labels = self.predict_named_entities(job)
        named_entities = self.extract_named_entities(predicted_labels)

        job_titles = {entity_text.replace("-", " ").replace('(', '').replace(')', '') 
                    for entity_text, entity_type in named_entities if entity_type == "JOB"}

        return list(job_titles)

    @staticmethod
    def match_degrees_by_custom_ner(self, job):
        predicted_labels = self.predict_named_entities(job)
        named_entities = self.extract_named_entities(predicted_labels)

        degree_levels = {normalize_degree(entity_text) for entity_text, entity_type in named_entities if entity_type == "EDU"}

        return list(degree_levels)

    @staticmethod
    def get_minimum_degree(self, degrees):
        d = {degree: self.degrees_importance[degree] for degree in degrees}
        return min(d, key=d.get)

    def extract_entities(self, job_id):
        # Access the row using the 'id' column
        job = self.jobs[self.jobs['id'] == job_id]['description'].values[0]

        # Recognize and extract entities
        degrees = self.match_degrees_by_custom_ner(job)
        self.jobs.at[self.jobs['id'] == job_id, 'degrees'] = self.get_minimum_degree(degrees) if degrees else ""
        self.jobs.at[self.jobs['id'] == job_id, 'job_title'] = self.match_jobtitle_by_custom_ner(job)
        self.jobs.at[self.jobs['id'] == job_id, 'skills'] = self.match_skills_by_spacy(job)
        self.jobs.at[self.jobs['id'] == job_id, 'experiences'] = self.match_experience_by_custom_ner(job)

        return self.jobs


# Example usage
# custom_model_path = "path_to_model"
# custom_tokenizer_path = "path_to_tokenizer"
# jobs_data = pd.read_csv("path_to_jobs_data.csv")

# job_info_extractor = JobInfoExtraction(custom_model_path, custom_tokenizer_path, jobs_data, DEGREES_IMPORTANCE, skills_patterns)
# extracted_info = job_info_extractor.extract_entities()
# print(extracted_info)
