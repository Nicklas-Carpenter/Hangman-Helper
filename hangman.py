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
        self.solutions = set()
        self.potential_letters = []
        self.accepted_letters = set()
        self.reject_letters = set()
        self.letter_stats = {}
        self.frame = n_letters * '_'

        
            
        self.initialize()
        self.update_letter_stats()


    def initialize(self):
        '''Initializes the list of potential words by reading from the master list and filtering by length.

        Date Created: June 28, 2019

        Date Last Modified: June 28, 2019
        '''

        for letter in string.ascii_lowercase:
            self.potential_letters.append(letter)
            self.letter_stats[letter] = {
                "word_occurrences": 0,
                "occurrences": 0
            }
        
        master_word_list = open('master_word_list')
        
        word = master_word_list.readline().rstrip(' \n\r') # remove line endings
        word_length = len(word)
        
        while word_length > 0:

            if word_length == self.n_letters:
                self.solutions.add(word)

            word = master_word_list.readline().rstrip('\n\r')
            word_length = len(word) 

            
    def update_letter_stats(self):
        '''Updates the letter statistics by parsing throught the current word list.
        
        Date Created: June 5, 2019

        Date Last Modified: June 15, 2019
        '''

        # Reset the count for each letter before we recount.

        for letter in self.potential_letters:
            self.letter_stats[letter]['occurrences'] = 0
            self.letter_stats[letter]['word_occurrences'] = 0

        # Count how many words each letter appears in as well as how many total times the letter appears in the list.
        for word in self.solutions:
            has_occured_in_word = set()
            for letter in word:
                if letter not in has_occured_in_word:
                    self.letter_stats[letter]['word_occurrences'] += 1
                    has_occured_in_word.add(letter)
                self.letter_stats[letter]['occurrences'] += 1

        # Sort letter list in order of occurences (descending).  
        self.potential_letters.sort(key = lambda letter: self.letter_stats[letter]['word_occurrences'], reverse = True)
        
        # Calculate the probability a letter is in a given word.
        for letter in self.potential_letters:
            if self.letter_stats[letter]['occurrences'] == 0:
                self.reject_letters.add(letter)
                self.potential_letters.remove(letter)
            self.letter_stats[letter]['probability'] = self.letter_stats[letter]['word_occurrences'] / len(self.solutions)


    def accept(self, letter, positions):
        '''Handles a correct letter guess.

        Created: June 26, 2019
        Last Updated: June 28, 2019
        '''

        self.potential_letters.remove(letter)
        self.accepted_letters.add(letter)
        self.update_frame(letter, positions)
        self.filter_by_frame()
        self.update_letter_stats()
    
    def reject(self, letter):
        '''Handles and incorrect letter guess
        
        Created: June 28, 2019
        Last Updated: June 28, 2019
        '''

        self.potential_letters.remove(letter)
        self.reject_letters.add(letter)
        self.filter_by_contains(letter)
        self.update_letter_stats()


    def update_frame(self, letter, positions):
        '''Updates the frame by puttint the given letter in the specified positions. 
        
            To remove or reposition letters, the frame must be updated and therefore reconstructed.

            Created: June 28, 2019

            Last Updated: June 28, 2019
        '''
        
        for position in positions:
            index = int(position) -1 # Convert position (which starts at 1) to index (which starts at 0).
            self.frame = self.frame[0 : int(index )] + letter + self.frame[int(index) + 1: len(self.frame)]


    def set_state(self, frame, rejected):
        self.initialize()

        self.frame = frame

        for letter in frame.replace('_',''):
            if letter not in self.accepted_letters:
                self.accepted_letters.add(letter)
                self.potential_letters.remove(letter)
        
        for letter in rejected:
            self.reject_letters.add(letter)
            self.potential_letters.remove(letter)

        self.filter_by_frame()

        self.update_letter_stats()

    
    def filter_by_frame(self):
        '''Filters out words that do not match the letters and positions in the frame

        Created: June 26, 2019

        Last Updated: June 28, 2019
        '''

        regex = re.compile(self.frame.replace('_','.'))

        updated_solutions = set()

        for word in self.solutions:
            if regex.fullmatch(word):
                updated_solutions.add(word)
                print("Added: ", word)
        
        self.solutions = updated_solutions


    def filter_by_contains(self, letter):
        '''Removes words from the word list if they contain the given letter.

        Params:
            letter - The letter searched for

        Date Created: June 6, 2019

        Date Last Modified: June 23, 2019
        '''

        updated_word_list = set()

        for word in self.solutions:
            if letter not in word:
                updated_word_list.add(word)
        
        self.solutions = updated_word_list
        

    def print_word_list(self):
        '''Prints the current word list (potential solutions). Used for CLI.

        Date Created: June 4, 2019

        Date Last Modified: June 15, 2019
        '''
        for word in self.solutions:
            print(word,'\n')

    
    def print_letter_stats(self):
        '''Prints probability of a given letter appearing in the solution. Used for CLI.

        Date Created: June 4, 2019
        Date Last Modified: June 15, 2019
        '''
        for letter in self.potential_letters:
            print(letter,': ', self.letter_stats[letter]['probability'])
    

    def solutions_count(self):
        '''Returns the number of solutions in the word list.

        Date Created: June 19, 2019

        Date Last Modified: June 19, 2019
        '''

        return len(self.solutions)


# Used for testing and CLI purposes
if __name__ == '__main__':
    print('\nWelcome to Hangman Helper.')
    word_length = input("Word length: ")
    word = NLetterWord(int(word_length))
    
    # Main loop
    while True:
        command_str = input('>').lower()
        args = command_str.split(sep = ' ')
        
        if args[0] == 'accept':
            if len(args) < 3:
                # print(len(args))
                # print(args)
                print('Usage: accept [LETTER] [POSITION]...')
                continue
            word.accept(args[1], args[2 : len(args)])
            
        elif args[0] == 'reject':
            if len(args) > 2:
                print('\nUsage: reject [LETTER]\n')
                continue
            word.reject(args[1])

        elif args[0] == 'set':
            if len(args) > 2:
                print('\nUsage: set [FRAME]\n')

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

        elif args[0] == 'status':
            if len(args) > 1:
                print('\nUsage: status\n')
                continue
            print('\nCurrent: ', word.frame,'\n')

        elif args[0] == 'quit':
            exit()

        else:
            print('\nUsage:\n\taccept [LETTER]\n\treject [LETTER]\n\tstats\n\twords\n\tcount\n\tstatus')