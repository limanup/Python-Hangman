
# Hangman Game
# -----------------------------------
import random
import string
import os

dir_path = os.path.dirname(os.path.realpath(__file__))

WORDLIST_FILENAME = dir_path + "/" + "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist



def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)


# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()



def is_word_guessed(secret_word : str, letters_guessed : list):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    secret_word = secret_word.lower()
    letters_guessed = list(map(lambda x: x.lower(), letters_guessed))
    return all([letter in letters_guessed for letter in secret_word ])


def get_guessed_word(secret_word:str, letters_guessed:list):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    secret_word = secret_word.lower()
    letters_guessed = list(map(lambda x: x.lower(), letters_guessed))
    word = str()
    for letter in secret_word:
      if letter in letters_guessed: word += letter
      else: word += '_ '
    return word


def get_available_letters(letters_guessed:list):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    letters_guessed = list(map(lambda x: x.lower(), letters_guessed))
    available_letters = string.ascii_lowercase
    letters_list = list(available_letters)
    for letter in letters_guessed:
      if letter in letters_list:
        letters_list.remove(letter)
    available_letters = ''.join(letters_list)
    return available_letters


def guess_fail_msg(warnings_remaining:int):
    if warnings_remaining > 0:
      msg =  'You have ' + str(warnings_remaining - 1) + ' warnings left:'
    else:
      msg = 'You have no warnings left so you lose one guess:'
    return msg


# -----------------------------------



def match_with_gaps(my_word:str, other_word:str):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''
    my_word = my_word.replace(' ', '')
    if len(my_word) != len(other_word): 
      return False
    else:
      return all([((my_word[i] == '_' and other_word[i] not in my_word) or 
      my_word[i] == other_word[i]) for i in range(len(other_word))])


def show_possible_matches(my_word:str):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    like_word_list = list()
    for word in wordlist:
      if match_with_gaps(my_word, word):
        like_word_list.append(word)
    if len(like_word_list) == 0:
      return 'No matches found'
    else:
      return ' '.join(like_word_list)



def hangman_with_hints(secret_word:str):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses
    
    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter
      
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
      
    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word. 
    
    '''
    
    secret_word = secret_word.lower()
    guesses_remaining = 6
    warnings_remaining = 3
    letters_guessed = list()

    print('Welcome to the game Hangman!\n' + 
      'I am thinking of a word that is', 
      len(secret_word), 'letters long.\n' +
      'You have', warnings_remaining, 'warnings left.')

    while guesses_remaining > 0:
      print('---------------\nYou have', guesses_remaining, 
      'guesses left.\nAvailable letters:', 
      get_available_letters(letters_guessed))
      guess = input('Please guess a letter: ')
      
      if guess == '*':
        print('Possible word matches are: \n' + 
        show_possible_matches(get_guessed_word(secret_word, letters_guessed)))
        continue

      elif not(len(guess) == 1 and guess.isalpha()):
        
        print('Oops! That is not a valid letter.',
        guess_fail_msg(warnings_remaining),
        get_guessed_word(secret_word, letters_guessed))
        
        if warnings_remaining > 0:
          warnings_remaining -= 1 
        else:
          guesses_remaining -= 1
        continue
      
      elif guess.lower() in letters_guessed:

        print("Oops! You've already guessed that letter.",
        guess_fail_msg(warnings_remaining),
        get_guessed_word(secret_word, letters_guessed))

        if warnings_remaining > 0:
          warnings_remaining -= 1
        else:
          guesses_remaining -= 1
        continue
      
      guess = guess.lower()
      letters_guessed.append(guess)

      if guess in secret_word:
        print('Good guess:', 
        get_guessed_word(secret_word, letters_guessed))
      else:
        if guess in 'aeiou': guesses_remaining -= 1
        guesses_remaining -= 1
        print('Oops! That letter is not in my word:',
        get_guessed_word(secret_word,letters_guessed))

      if is_word_guessed(secret_word, letters_guessed):
        print('---------------\nCongradulations, you won!\n' + 
          'Your total score for this game is:',
          guesses_remaining * len(set(secret_word)))
        break
      
    if guesses_remaining <= 0:
      print('---------------\nSorry, you ran out of guesses. ' + 
      'The word was ' + secret_word + '.')




if __name__ == "__main__":
    secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word)
