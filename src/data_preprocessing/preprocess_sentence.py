import string
import re
import unicodedata
import nltk


def preprocess_sentence(sentence, stopwords):
    """
    Preprocesses the data by performing the following steps:
        - To lowercase
        - Remove ponctuation, urls and accent characters
        - Tokenize words and remove stop words.
    
    Parameters:
    sentence (string): input data
    stopwords (list of words): input data
    
    Returns:
    string: preprocessed sentence. 
    """

    # Precompile regular expressions
    url_pattern = re.compile(r'\b(?:https?://|www\.)\S+\b')
    punctuations = re.compile(r'[{}]'.format(re.escape('''!"#$’%&'()•*,-./:;<=>?@[\]^_`{|}~''')))

    # Removing URLs:
    sentence = re.sub(url_pattern, '', sentence)
    
    # Removing accent characters
    sentence = ''.join(c for c in unicodedata.normalize('NFD', sentence) if unicodedata.category(c) != 'Mn')
    
    # Removing punctuations
    sentence = re.sub(punctuations, ' ', sentence)

    # Tokenize words and remove stopwords in one step using list comprehension:
    words_w_stopwords = [w for w in nltk.tokenize.word_tokenize(sentence) if w.lower() not in stopwords]


    preprocessed_sentence = ' '.join(words_w_stopwords)
    return preprocessed_sentence
