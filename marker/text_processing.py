from nltk.corpus import stopwords
from marker.position_rank import PositionRank
import string
import re

def model_boldness(len, boldness = 1.0):
    if len <= 2: return [boldness] * len
    len -= 1
    a = len//2
    b = (len + 1)//2
    result = [(max(i, len - i) - a)/b * boldness for i in range(len+1)]
    return result

def process(raw_text, \
            maximum_number_of_words = 150, \
            token_window_size = 7, \
            alpha = 0.15, 
            boldness_baseline = 0.05):
    importance_assigner = \
        PositionRank(maximum_number_of_words, \
            token_window_size, \
            alpha)
    # Preprocessing text
    preprocess_text = list(enumerate(raw_text.split(' ')))
    # Removing punctuation
    for i in range(len(preprocess_text)):
        w = preprocess_text[i][1]
        w = w.translate(str.maketrans('','',string.punctuation))
        preprocess_text[i] = (preprocess_text[i][0], w.lower())
    # Removing non-word and fillers
    stop_words = set(stopwords.words('english'))
    clean_text = [(i, w) for (i, w) in preprocess_text if w not in stop_words and re.search('[a-zA-Z0-9]', w)]

    boldness_total_scores = [0] * len(preprocess_text)
    for (position, word) in enumerate(clean_text):
        importance_assigner.append(word)
        boldness_scores = importance_assigner.extract_boldness()
        offset = max(0, position - maximum_number_of_words + 1)
        for i in range(len(boldness_scores)):
            boldness_total_scores[clean_text[i + offset][0]] += boldness_scores[i] * len(boldness_scores)
    
    # Normalization
    for i in range(len(boldness_total_scores)):
        boldness_total_scores[i] /= min(maximum_number_of_words, min(i + 1, len(boldness_total_scores) - i))
    normalization = max(boldness_total_scores)
    for i in range(len(boldness_total_scores)):
        boldness_total_scores[i] = \
            boldness_total_scores[i] / normalization *  (1 - boldness_baseline) + \
            boldness_baseline
    # Calculate boldness for each character
    final_boldness = [0] * len(raw_text)
    cnt = 0
    for (i, w) in preprocess_text:
        final_boldness[cnt:cnt + len(w)] = model_boldness(len(w), boldness_total_scores[i])
        cnt += len(w) + 1
    for i in range(len(raw_text)):
        if not (0 <= final_boldness[i] and final_boldness[i] <= 1):
            print("Final score error:", i, final_boldness[i])
            assert(False)
    return final_boldness