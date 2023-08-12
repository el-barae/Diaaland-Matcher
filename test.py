from sentence_transformers import SentenceTransformer, util
model = SentenceTransformer('all-MiniLM-L6-v2')

# Two lists of sentences
sentences1 = ["Au moins 10 ans d'expérience en tant que Data Scientist,",
             "une expérience avérée en développement d'algorithmes de prédiction pour des solutions SaaS" ]

sentences2 = ["Au moins 2 ans à 3 ans d'experience comme étant ingénieur d'apprentissage automatique",
              "Au moins 2 ans à 3 ans d'experience comme étant ingénieur developpement",
              'The new movie is so great']

#Compute embedding for both lists
embeddings1 = model.encode(sentences1, convert_to_tensor=True)
embeddings2 = model.encode(sentences2, convert_to_tensor=True)

#Compute cosine-similarities
cosine_scores = util.cos_sim(embeddings1, embeddings2)

for i, element in enumerate(cosine_scores):
    print(sentences1[i])
    for j, ele in enumerate(cosine_scores):
        print(sentences2[j])
        print(cosine_scores[i][j])
