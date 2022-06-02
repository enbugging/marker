from collections import deque
from reading_frame import ReadingFrame
    
class PositionRank(ReadingFrame):
    def __init__(self, \
                maximum_number_of_words = 150, \
                token_window_size = 7, \
                alpha = 0.15):
        super().__init__(maximum_number_of_words)
        self.token_window_size  = token_window_size
        self.alpha              = alpha
        self.weight             = [[0] * maximum_number_of_words] * maximum_number_of_words
    
    def update_weights(self, label, left_lim, right_lim, change):
        if right_lim <= self.maximum_number_of_words:
            for i in range(left_lim, right_lim):
                temporary_label = self.word_first_label(self.labels_to_words[i])
                self.weight[label][temporary_label] += change
                self.weight[temporary_label][label] += change
        else:
            right_lim -= self.maximum_number_of_words
            for i in range(left_lim, self.maximum_number_of_words):
                temporary_label = self.word_first_label(self.labels_to_words[i])
                self.weight[label][temporary_label] += change
                self.weight[temporary_label][label] += change
            for i in range(0, right_lim):
                temporary_label = self.word_first_label(self.labels_to_words[i])
                self.weight[label][temporary_label] += change
                self.weight[temporary_label][label] += change

    def append(self, word):
        previous_id = self.current_position
        word_to_pop = self.labels_to_words[previous_id]
        old_label_word_to_pop = self.word_first_label(word_to_pop)
        if self.isFull():
            """
            If the reading frame is complete, we would need 
            to pop the leftmost word from the frame.
            """
            # Pop the old word
            if self.number_of_words_scanned >= 2 * self.maximum_number_of_words:
                self.update_weights(old_label_word_to_pop, \
                                    previous_id - self.token_window_size + 1, \
                                    previous_id, 
                                    -1)
                self.update_weights(old_label_word_to_pop, \
                                    previous_id + 1, \
                                    previous_id + self.token_window_size, \
                                    -1)
            else:
                self.update_weights(old_label_word_to_pop, \
                                    max(previous_id - self.token_window_size + 1, 0), \
                                    previous_id, 
                                    -1)
            

        old_label_word_to_push = self.word_first_label(word)
        super().append(word)
        new_label_word_to_push = self.word_first_label(word)

        if self.isFull():
            # If the old word still occurs, we need to transfer adjacency list to the new label
            new_label_word_to_pop = self.word_first_label(word_to_pop)
            if new_label_word_to_pop is not None:
                for i in range(0, self.maximum_number_of_words):
                    self.weight[new_label_word_to_pop][i] = self.weight[old_label_word_to_pop][i]
                    self.weight[i][new_label_word_to_pop] = self.weight[i][old_label_word_to_pop]
        
        # If the new word has already occurred, we need to transfer adjacency list to the new label, if any
        if old_label_word_to_push != new_label_word_to_push and \
            old_label_word_to_push is not None:
            for i in range(0, self.maximum_number_of_words):
                self.weight[new_label_word_to_push][i] = self.weight[old_label_word_to_push][i]
                self.weight[i][new_label_word_to_push] = self.weight[i][old_label_word_to_push]


        # Push the new word
        
        if self.isFull():
            self.update_weights(new_label_word_to_push, \
                            previous_id - self.token_window_size + 1, \
                            previous_id, 
                            1)
            self.update_weights(new_label_word_to_push, \
                                previous_id + 1, \
                                previous_id + self.token_window_size, \
                                1)
        else:
            self.update_weights(new_label_word_to_push, \
                            max(previous_id - self.token_window_size + 1, 0), \
                            previous_id, 
                            1)

    def extract_boldness(self):
        id_to_word = [(self.word_first_label(w), w) for w in self.words_to_labels.keys()]
        number_of_distinct_words = len(id_to_word)
        word_to_id = {}
        for i in range(number_of_distinct_words):
            word_to_id[id_to_word[i][0]] = i
        
        number_of_words = min(self.maximum_number_of_words, self.number_of_words_scanned)
        total_weights = [0] * number_of_distinct_words
        for i in range(number_of_distinct_words):
            for j in range(number_of_distinct_words):
                total_weights[i] += self.weight[id_to_word[i][0]][id_to_word[j][0]]
        
        prob = [0] * number_of_distinct_words
        for i in range(number_of_words):
            prob[word_to_id[self.word_first_label(self.labels_to_words[i])]] += 1.0 / (number_of_words - i)
        
        sum_prob = sum(prob)
        for i in range(number_of_distinct_words):
            prob[i] /= sum_prob
        
        scores = [1.0/number_of_distinct_words] * number_of_distinct_words
        for _ in range(10):
            new_scores = [0] * number_of_distinct_words
            for i in range(number_of_distinct_words):
                sigma = 0
                for j in range(number_of_distinct_words):
                    sigma += scores[j] * self.weight[id_to_word[i][0]][id_to_word[j][0]]/total_weights[j]
                new_scores[i] = self.alpha * prob[i] + (1 - self.alpha) * sigma
            for i in range(number_of_distinct_words):
                scores[i] = new_scores[i]

        boldness_score = [] * number_of_words
        for i in range(0, number_of_words):
            boldness_score[i] = \
                scores[ \
                    word_to_id[ \
                        self.word_first_label( \
                            self.labels_to_words[i] \
                            ) \
                        ] \
                    ]
        if self.isFull():
            boldness_score = list(
                deque(boldness_score)
                .rotate(self.maximum_number_of_words - self.current_position)
            )
        return boldness_score