from sqlalchemy import false
from marker.position_rank import PositionRank
import string
import re
import math

def model_boldness(len, boldness = 1.0):
    if len <= 2: return [boldness] * len
    len -= 1
    a = len//2
    result = [max(i, len - i)/len * boldness for i in range(len+1)]
    return result

def highlight(raw_text, \
            maximum_number_of_words = 40, \
            token_window_size = 7, \
            alpha = 0.15, 
            boldness_baseline = 0.2,
            removeStopWords = false):
    importance_assigner = \
        PositionRank(maximum_number_of_words, \
            token_window_size, \
            alpha)
    # Preprocessing text
    preprocess_text = list(enumerate(raw_text.split(' ')))
    words_lenghts = [len(w) for (_, w) in preprocess_text]
    # Removing punctuation
    for i in range(len(preprocess_text)):
        w = preprocess_text[i][1]
        w = w.translate(str.maketrans('','',string.punctuation))
        preprocess_text[i] = (preprocess_text[i][0], w.lower())
    # Removing non-word and fillers
    if removeStopWords:
        # TODO: include other languages. The issue is to reliably predict language and to use the corresponding stop words
        from nltk.corpus import stopwords
        stop_words = set(stopwords.words('english'))
        clean_text = [(i, w) for (i, w) in preprocess_text if re.search('[a-zA-Z0-9]', w) and w not in stop_words]
    else:
        clean_text = [(i, w) for (i, w) in preprocess_text if re.search('[a-zA-Z0-9]', w)]# and w not in stop_words]

    boldness_total_scores = [0] * len(preprocess_text)
    for (position, word) in enumerate(clean_text):
        importance_assigner.append(word)
        boldness_scores = importance_assigner.extract_boldness()
        offset = max(0, position - maximum_number_of_words + 1)
        for i in range(len(boldness_scores)):
            boldness_total_scores[clean_text[i + offset][0]] += boldness_scores[i] * len(boldness_scores)
    
    # Normalization
    for i in range(len(boldness_total_scores)):
        number_of_scanned_frames = \
            len(boldness_total_scores) - i \
            if i >= len(boldness_total_scores) - maximum_number_of_words \
            else maximum_number_of_words
        boldness_total_scores[i] /= number_of_scanned_frames
    #for i in range(len(boldness_total_scores)):
    #    boldness_total_scores[i] = math.log2(boldness_total_scores[i] + 1)
    normalization = max(boldness_total_scores)
    for i in range(len(boldness_total_scores)):
        boldness_total_scores[i] = boldness_total_scores[i] / normalization * (1 - boldness_baseline) + boldness_baseline
    # Calculate boldness for each character
    final_boldness = [0] * len(raw_text)
    cnt = 0
    for i in range(len(words_lenghts)):
        length = words_lenghts[i]
        final_boldness[cnt:cnt + length] = model_boldness(length, boldness_total_scores[i])
        cnt += length + 1
    return final_boldness