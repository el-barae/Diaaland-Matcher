import nltk
from langdetect import detect


def clean_text(sentence, preprocess):
    """
    Cleanes the data by performing the following steps:
        - Detects the language of the sentence
        - Loads stopwords for the given language
        - Calls the preprocessing function.
    
    Parameters:
    sentence (string): input data
    preprocess (function): input data
    
    Returns:
    string: cleaned sentence.
    """

    # Detect language
    language = detect(sentence)
    
    # Configure language stopwords.
    if language.lower() == "fr":
        stopwords = set(nltk.corpus.stopwords.words('french'))
    else:
        stopwords = set(nltk.corpus.stopwords.words('english'))

    return preprocess(sentence, stopwords)
