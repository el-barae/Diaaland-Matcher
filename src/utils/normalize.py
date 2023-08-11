
degree_mapping = {
    "BAC+2": ["DEUG", "DEUST", "DUT", "TECHNICIEN", "BTS", "DTS", "DT"],
    "BAC+3": ["LICENSE", "LF", "LP", "Bachelor", "LST"],
    "BAC+5": ["Master", "Diplome d’Ingenieur", "Ingenieur", "MS", "MR", "MST", "IE"],
    "BAC+8": ["DOCTORAT", "DOCTEUR", "Phd"]
}

value_mapping = {
    "BAC+2": 0,
    "BAC+3": 1,
    "BAC+5": 2,
    "BAC+8": 3
}
def score_degree(degree):
    for level, diplome_list in degree_mapping.items():
        for diplome in diplome_list:
            degree = degree.replace(diplome, level)
    
    score = value_mapping[degree]
    return score


def score_experience(experiences):
    """
        input:
        experiences = [
            {
                'years_of_experience' = ?,
                'domain_of_experience' = ?
            }
        ]
    """
    
