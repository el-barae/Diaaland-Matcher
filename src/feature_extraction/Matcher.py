import ast 
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


class Matcher:
    
    def __init__(self, labels, resume, job):
        self.labels = labels
        self.resume = resume
        self.job = job

    def modifying_type_resume(self, resume):
        for i in range(len(resume["degrees"])):
            resume["degrees"][i] = ast.literal_eval(resume["degrees"][i])
        for i in range(len(resume["skills"])):
            resume["skills"][i] = ast.literal_eval(resume["skills"][i])
        for i in range(len(resume["experiences"])):
            resume["experiences"][i] = ast.literal_eval(resume["experiences"][i])
        resume['job_title'][i] = ast.literal_eval(resume['job_title'])
        return resume
