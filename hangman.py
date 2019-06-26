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
import re

class NLetterWord:
    """
    Author: Nicklas Carpenter

    Date Created: June 5, 2019

    Date Last Modified: June 15, 2019
    """
    def __init__(self, n_letters):
        '''An NLetterWord'''
        self.n_letters = n_letters
        self.word_list = set()
        self.letters = []
        self.letter_stats = {}
        self.frame = n_letters * '_'

        for letter in string.ascii_lowercase:
            self.letters.append(letter)
            self.letter_stats[letter] = {
                "word_occurrences": 0,
                "occurrences": 0
            }
            
        self.init_word_list()
        self.update_letter_stats()


    def init_word_list(self):
        '''Initializes the list of potential words by reading from the master list and filtering by length.

        Date Created: June 5, 2019

        Date Last Modified: June 15, 2019
        '''
        master_word_list = open('master_word_list')
        
        word = master_word_list.readline().rstrip(' \n\r') # remove line endings
        word_length = len(word)
        
        while word_length > 0:

            if word_length == self.n_letters:
                self.word_list.add(word)

            word = master_word_list.readline().rstrip('\n\r')
            word_length = len(word) 

            
    def update_letter_stats(self):
        '''Updates the letter statistics by parsing throught the current word list.
        
        Date Created: June 5, 2019

        Date Last Modified: June 15, 2019
        '''

        # Reset the count for each letter before we recount.

        for letter in self.letters:
            self.letter_stats[letter]['occurrences'] = 0
            self.letter_stats[letter]['word_occurrences'] = 0

        # Count how many words each letter appears in as well as how many total times the letter appears in the list.
        for word in self.word_list:
            has_occured_in_word = set()
            for letter in word:
                if letter not in has_occured_in_word:
                    self.letter_stats[letter]['word_occurrences'] += 1
                    has_occured_in_word.add(letter)
                self.letter_stats[letter]['occurrences'] += 1

        # Sort letter list in order of occurences (descending).  
        self.letters.sort(key = lambda letter: self.letter_stats[letter]['word_occurrences'], reverse = True)
        
        # Calculate the probability a letter is in a given word.
        for letter in self.letters:
            self.letter_stats[letter]['probability'] = self.letter_stats[letter]['word_occurrences'] / len(self.word_list)


    def handle_guess(self, letter, accepted):
        '''Updates the possible letters, wordlist, and letter stats based on a given guess.
        
        Date Created: June 5, 2019

        Date Last Modified: June 15, 2019
        '''
        
        # Remove the letter even if it is correct. If it is an incorrect guess we know that the probability of it
        # occuring is 0. If it is a correct guess, we know the probability of it occuring is 1. Either way, we don't
        # care about the letter's statistics.
        self.letters.remove(letter)

        # Sort letter list in order of occurences (descending).
        self.letters.sort(key = lambda letter: self.letter_stats[letter]['word_occurrences'], reverse = True)
        
        if accepted:
            self.remove_words_if_not_contains(letter)
        else:
            self.remove_words_if_contains(letter)

        self.update_letter_stats()


    def accept(self, letter, positions):
        ''''''
        pass


    def filter_by_frame(self, letter, positions):
        ''''''

        regex = list('.' * self.n_letters)
        for i in range(len(regex)):
            regex[i] = letter
        regex = ''.join(regex)
        regex = re.compile(regex)

        updated_word_list = set()

        for word in self.word_list:
            if regex.fullmatch(word):
                updated_word_list.add(word)
        
        self.word_list = updated_word_list

    def remove_words_if_contains(self, letter):
        '''Removes words from the word list if they contain the given letter.

        Params:
            letter - The letter searched for

        Date Created: June 6, 2019

        Date Last Modified: June 23, 2019
        '''

        updated_word_list = set()

        for word in self.word_list:
            if letter not in word:
                updated_word_list.add(word)
        
        self.word_list = updated_word_list

        
    def remove_words_if_not_contains(self, letter):
        '''Removes words if they do not contain the given letter.

        Params:
            letter - The letter searched for

        Date Created: June 6, 2019

        Date Last Modified: June 23, 2019
        '''
        
        updated_word_list = set()

        for word in self.word_list:
            if letter in word:
                updated_word_list.add(word)
        
        self.word_list = updated_word_list
        

    def print_word_list(self):
        '''Prints the current word list (potential solutions). Used for CLI.

        Date Created: June 4, 2019

        Date Last Modified: June 15, 2019
        '''
        for word in self.word_list:
            print(word,'\n')

    
    def print_letter_stats(self):
        '''Prints probability of a given letter appearing in the solution. Used for CLI.

        Date Created: June 4, 2019
        Date Last Modified: June 15, 2019
        '''
        for letter in self.letters:
            print(letter,': ', self.letter_stats[letter]['probability'])
    

    def solutions_count(self):
        '''Returns the number of solutions in the word list.

        Date Created: June 19, 2019

        Date Last Modified: June 19, 2019
        '''

        return len(self.word_list)


# Used for testing and CLI purposes
if __name__ == '__main__':
    print('\nWelcome to Hangman Helper.')
    word_length = input("Word length: ")
    word = NLetterWord(int(word_length))
    
    # Main loop
    while True:
        command_str = input('>')
        args = command_str.split(sep = ' ')
        
        if args[0] == 'accept':
            if len(args) > 2:
                # print(len(args))
                # print(args)
                print('Usage: accept [LETTER]')
                continue
            word.handle_guess(args[1], True)
            
        elif args[0] == 'reject':
            if len(args) > 2:
                print('\nUsage: reject [LETTER]\n')
                continue
            word.handle_guess(args[1], False)

        elif args[0] == 'stats':
            if len(args) > 1:
                print('\nUsage: stats\n')
                continue
            print('\nLetter Stats:\n')
            word.print_letter_stats()
            print('\n')
        
        elif args[0] == 'words':
            if len(args) > 1:
                print('\nUsage: words\n')
                continue
            print('\nPossible solutions:\n')
            word.print_word_list()
            print('\n')
        
        elif args[0] == 'count':
            if len(args) > 1:
                print('\nUsage: count\n')
                continue
            print('\n',word.solutions_count(), 'possible solutions\n')

        elif args[0] == 'q':
            exit()

        else:
            print('\nUsage:\n\taccept [LETTER]\n\treject [LETTER]\n\tstats\n\twords\n\tcount')