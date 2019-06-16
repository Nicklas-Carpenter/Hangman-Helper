'''
A solver for Hangman puzzles
Copyright (C) 2019  Nicklas Carpenter

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

import string

class NLetterWord:
    """
    Author: Nicklas Carpenter
    Date Created: June 5, 2019
    Date Last Modified: June 15, 2019
    """
    def __init__(self, n_letters):
        """An NLetterWord
        """
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
        """Initializes the list of potential words by reading from the master list and filtering by length

        Date Created: June 5, 2019

        Date Last Modified: June 15, 2019
        """
        master_word_list = open('master_word_list')
        
        word = master_word_list.readline().rstrip('\n\r') #remove line endings
        word_length = len(word)
        
        while word_length > 0:

            if word_length == self.n_letters:
                self.word_list.append(word)

            word = master_word_list.readline().rstrip('\n\r')
            word_length = len(word) 
            
    def update_letter_stats(self):
        """Updates the letter statistics by parsing throught the current word list
        
        Date Created: June 5, 2019

        Date Last Modified: June 15, 2019
        """

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
        """Calls for to the NLetterWord based on the guess and whether it was correct or not

        Params:
            letter - The letter guesed
            accepted - Whether the letter guessed was correct or not
            
        Date Created: June 6, 2019

        Date Last Modified: June 15, 2019
        """
        self.letters.remove(letter)
        del self.letter_stats[letter]

        if not accepted:
            self.remove_words_containing(letter)
        else:
            self.remove_words_not_containing(letter)
        
        self.update_letter_stats()

    
    def remove_words_containing(self, letter):
        """Removes words from the word list that contain the specified letter

        Params:
            letter - The letter searched for

        Date Created: June 6, 2019
        Date Last Modified: June 15, 2019
        """
        for word in self.word_list:
            if letter in word:
                self.word_list.remove(word)

    
    def remove_words_not_containing(self, letter):
        """Removes words from the word list that do not contain the specified letter

        Params:
            letter - The letter searched for

        Date Created: June 6, 2019
        Date Last Modified: June 15, 2019
        """
        for word in self.word_list:
            if letter not in word:
                self.word_list.remove(word)


    def print_word_list(self):
        """Prints the current word list (potential solutions). Used for CLI.

        Date Created: June 4, 2019
        Date Last Modified: June 15, 2019
        """
        for word in self.word_list:
            print(word)

    
    def print_letter_stats(self):
        """Prints probability of a given letter appearing in the solution. Used for CLI.

        Date Created: June 4, 2019
        Date Last Modified: June 15, 2019
        """
        for letter in self.letters:
            print(letter,': ', self.letter_stats[letter]['probability'])

# Used for testing and CLI purposes
if __name__ == '__main__':
    word_length = input("Word length: ")
    word = NLetterWord(int(word_length))
    
    print("Letter Statistics:\n\n")
    word.print_letter_stats()
    
