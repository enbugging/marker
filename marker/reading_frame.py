from collections import deque

class ReadingFrame:
    def __init__(self, maximum_number_of_words = 40):
        self.maximum_number_of_words    = maximum_number_of_words
        self.current_position                 = 0
        self.words_to_labels            = {}
        self.labels_to_words            = [None for _ in range(maximum_number_of_words)]
        self.number_of_words_scanned    = 0
    
    def isFull(self):
        return self.number_of_words_scanned > self.maximum_number_of_words
    
    def word_first_label(self, word):
        if word not in self.words_to_labels:
            return None
        else:
            return self.words_to_labels[word][0]

    def append(self, word):
        self.number_of_words_scanned += 1
        # If the frame is full, we need to delete the leftmost word from dictionary
        if self.isFull():
            previous_word = self.labels_to_words[self.current_position]
            self.words_to_labels[previous_word].popleft()
            if not self.words_to_labels[previous_word]:
                del self.words_to_labels[previous_word]

        # If the current word is not dictionary, we simply make a new entry
        if word not in self.words_to_labels:
            self.words_to_labels[word] = deque([])
        
        self.words_to_labels[word].append(self.current_position)
        self.labels_to_words[self.current_position] = word
        self.current_position += 1
        if self.current_position == self.maximum_number_of_words:
            self.current_position = 0