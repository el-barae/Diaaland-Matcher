from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
import pandas as pd
from resource import DEGREES_IMPORTANCE


class JobInfoExtraction:

    def __init__(self, custom_model_path, custom_tokenizer_path, job):
        self.jobs = jobs[['description']]
        self.custom_model = BertForTokenClassification.from_pretrained(custom_model_path)
        self.custom_tokenizer = AutoTokenizer.from_pretrained(custom_tokenizer_path)
        self.degrees_importance = DEGREES_IMPORTANCE

    def predict_named_entities(self, text):
        # Run the model in order to perform ner on the job description
        # Input : text
        # Output : list of identified labels.
        nlp = pipeline('ner', model = self.model, tokenizer = self.tokenizer, aggregation_strategy="simple")

        predicted_entities = nlp(text)

        return predicted_entities

    def extract_named_entities(self, predicted_labels):
        # To be implemented later.
        pass

    def match_experience_by_custom_ner(self, job):
        predicted_labels = self.predict_named_entities(job)
        named_entities = self.extract_named_entities(predicted_labels)

        acceptable_experiences = []
        for entity_text, entity_type in named_entities:
            if entity_type == "EXPERIENCE":
                normalized_experience = entity_text.replace("-", " ")
                if normalized_experience not in acceptable_experiences:
                    acceptable_experiences.append(normalized_experience)
        return acceptable_experiences

    def match_skills_by_custom_ner(self, job):
        predicted_labels = self.predict_named_entities(job)
        named_entities = self.extract_named_entities(predicted_labels)

        job_skills = []
        for entity_text, entity_type in named_entities:
            if entity_type == "SKILL":
                normalized_skill = entity_text.replace("-", " ")
                if normalized_skill not in job_skills:
                    job_skills.append(normalized_skill)
        return job_skills

    def match_jobtitle_by_custom_ner(self, job):
        predicted_labels = self.predict_named_entities(job)
        named_entities = self.extract_named_entities(predicted_labels)

        job_title = []
        for entity_text, entity_type in named_entities:
            if entity_type == "JOB_TITLE":
                normalized_job_title = entity_text.replace("-", " ")
                if normalized_job_title not in job_title:
                    job_title.append(normalized_job_title)
        return job_title

    def match_degrees_by_custom_ner(self, job):
        predicted_labels = self.predict_named_entities(job)
        named_entities = self.extract_named_entities(predicted_labels)

        degree_levels = []
        for entity_text, entity_type in named_entities:
            if entity_type == "DEGREE":
                degree_level = entity_text.split("|")[1]
                if degree_level not in degree_levels:
                    degree_levels.append(degree_level)
        return degree_levels

    def get_minimum_degree(self, degrees):
        d = {degree: self.degrees_importance[degree] for degree in degrees}
        return min(d, key=d.get)

    def extract_entities(self, row):
        row_num = jobs[jobs['id'] == row['id']]
        # recognize and extract entities
        self.jobs['Skills'] = ""
        self.jobs['Acceptable experiences'] = ""
        self.jobs['Degree'] = ""
        self.jobs['Job title'] = ""
        job = row['description'].replace('. ', ' ')
        degrees = self.match_degrees_by_custom_ner(job)
        if len(degrees) != 0:
            self.jobs.at[row_num, 'Degree'] = self.get_minimum_degree(degrees)
        else:
            self.jobs.at[row_num, 'Degree'] = ""
        self.jobs.at[row_num, 'Job title'] = self.match_job_title_by_custom_ner(job)
        self.jobs.at[row_num, 'Skills'] = self.match_skills_by_custom_ner(job)
        return self.jobs

# Example usage
custom_model_path = "path_to_model"
custom_tokenizer_path = "path_to_tokenizer"
jobs_data = pd.read_csv("path_to_jobs_data.csv")

job_info_extractor = JobInfoExtraction(custom_model_path, custom_tokenizer_path, jobs_data)
extracted_info = job_info_extractor.extract_entities()
print(extracted_info)
