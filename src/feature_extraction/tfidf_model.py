from sklearn.feature_extraction.text import TfidfVectorizer # TF-IDF Vectorization
from sklearn.metrics.pairwise import cosine_similarity # Cosine similarity
import numpy as np
# This file contains the calculations for cosine similarity using TF-IDF (will be modified later with a better approach)


def tfidf_cosine_similarity(resumes, job_descriptions):
    
    vectorizer = TfidfVectorizer(ngram_range=(1, 2))
    
    all_documents = job_descriptions + resumes
    tfidf_matrix = vectorizer.fit_transform(all_documents)
    
    job_description_tfidf = tfidf_matrix[:len(job_descriptions)]
    resumes_tfidf = tfidf_matrix[len(job_descriptions):]
    
    cosine_scores = cosine_similarity(job_description_tfidf, resumes_tfidf)
    similarity_score = np.mean(cosine_scores)

    return similarity_score

print(tfidf_cosine_similarity("hello, my name is adam", 'Hi, my name is mjid'))