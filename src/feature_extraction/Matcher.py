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

    def job(self, job):
        for i in range(len(jon["degrees"])):
            job["degrees"][i] = ast.literal_eval(job["degrees"][i])
        for i in range(len(resume["skills"])):
            job["skills"][i] = ast.literal_eval(job["skills"][i])
        for i in range(len(resume["experiences"])):
            job["experiences"][i] = ast.literal_eval(job["experiences"][i])
        job['job_title'][i] = ast.literal_eval(job['job_title'])
        return job

    @staticmethod
    def assign_degree_match(match_scores):
        match_score = 0
        if len(match_scores) != 0:
            if max(match_scores) >= 2:
                match_score = 0.5
            elif (max(match_scores) >= 0) and (max(match_scores) < 2):
                match_score = 1
        return match_score

    
    def degree_matching(self, resumes, job, job_index):
        job_degree = job['Degree'][job_index]
        resumes['degree job' + str(job_index) + 'matching'] = 0
        for i, row in resumes.iterrows():
            match_scores = []
            for j in resumes['DEGREE'][i]:
                score = self.labels['DEGREE'][j] - self.labels['DEGREE'][job_degree]
                match_scores.append(score)

    
