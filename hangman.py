import string

class NLetterWord: 
    def __init__(self, n_letters):
        self.n_letters = n_letters
        self.word_list = []
        self.letters = []
        self.letter_stats = {}
        for letter in string.ascii_lowercase:
            self.letters.append(letter)
            self.letter_stats[letter] = {
                "word_occurrences": 0,
                "occurrences": 0
            }
        self.init_word_list()
        self.update_letter_stats()


    def init_word_list(self):
        master_word_list = open('master_word_list')
        
        word = master_word_list.readline().rstrip('\n\r') #remove line endings
        word_length = len(word)
        
        while word_length > 0:

            if word_length == self.n_letters:
                self.word_list.append(word)

            word = master_word_list.readline().rstrip('\n\r')
            word_length = len(word) 
            
    def update_letter_stats(self):
        for word in self.word_list:
            has_occured_in_word = {}
            for letter in word:
                if (letter not in has_occured_in_word.keys()):
                    self.letter_stats[letter]['word_occurrences'] += 1
                    has_occured_in_word[letter] = True
                self.letter_stats[letter]['occurrences'] += 1
                
        self.letters.sort(key = lambda letter: self.letter_stats[letter]['word_occurrences'], reverse = True)
        
        for letter in self.letter_stats.keys():
            self.letter_stats[letter]['probability'] = self.letter_stats[letter]['word_occurrences'] / len(self.word_list)

    def handle_guess(self, letter, accepted):
        self.letters.remove(letter)
        del self.letter_stats[letter]

        if not accepted:
            self.remove_words_containing(letter)
        else:
            self.remove_words_not_containing(letter)
        
        self.update_letter_stats()

    
    def remove_words_containing(self, letter):
        for word in self.word_list:
            if letter in word:
                self.word_list.remove(word)

    
    def remove_words_not_containing(self, letter):
        for word in self.word_list:
            if letter not in word:
                self.word_list.remove(word)


    def print_word_list(self):
        for word in self.word_list:
            print(word)

    
    def print_letter_stats(self):
        for letter in self.letters:
            print(letter,': ', self.letter_stats[letter]['probability'])


if __name__ == '__main__':
    word_length = input("Word length: ")
    game = NLetterWord(int(word_length))
    
    print("Letter Statistics:\n\n")
    game.print_letter_stats()
    
