import string
import sys
import random

#@Author Arthur Strizheus
# Opening file containing 1,000 English words, reading it into a list.
wordFile = open("hManWords.txt")
content = wordFile.read()
wordList = content.splitlines()


def getGuessedWord(secretWord, lettersGuessed):
    '''
    secretWord: string, the word the user is guessing
    lettersGuessed: list, what letters have been guessed so far
    returns: string, comprised of letters and underscores that represents
    what letters in secretWord have been guessed so far.
    :param secretWord:                   # String of secret word to be guessed
    :param lettersGuessed:               # List of letters guessed so far by player
    :return:                             # Returns Word with guessed letters and '_' were no letters were guessed
    '''
    guessed = ''
    result = ''
    count = 0
    for x in secretWord:
        for y in lettersGuessed:
            if x == y:
                guessed += y
                break
    for x in secretWord:
        if guessed != '':
            y = guessed[count]
            if x == y:
                result += x
                if count < len(guessed)-1:
                    count += 1
            elif x != y:
                result += '_ '
        else:
            result += '_ '
    return result


def isWordGuessed(secretWord, lettersGuessed):
    '''
    secretWord: string, the word the user is guessing
    lettersGuessed: list, what letters have been guessed so far
    returns: boolean, True if all the letters of secretWord are in lettersGuessed;
    False otherwise
    :param secretWord:                    # String of secret word to be guessed
    :param lettersGuessed:                # List of letters guessed by the player
    :return: T ot F                       # T if full secret is is guessed F is not
    '''
    found = False
    guessed = ''
    for x in secretWord:
        for y in lettersGuessed:
            if x == y:
                guessed += y
                break
    if secretWord == guessed:
        print(guessed)
        print(secretWord)
        found = True
    return found


def getAvailableLetters2(lettersGuessed, avaliableLetters):
    '''
    lettersGuessed: list, what letters have been guessed so far
    returns: string, comprised of letters that represents what letters have not
    yet been guessed.
    :param lettersGuessed:                 # List of Letters guessed by the player
    :param avaliableLetters:               # String of Letters available for the player to guess
    :return:                               # Updates String of available letters removing the recent guessed letter
    '''
    result = ''
    temp = []
    for i in avaliableLetters:
        temp += i
    for x in temp:
        for z in lettersGuessed:
            if z == x:
                temp.remove(z)
    for y in temp:
        result += y
    return result.strip()


def isLetterInWord(secretWord, lettersGuessed):
    '''
    Checks if Letters is in Word
    :param secretWord:                     # String of the secret word to be guessed
    :param lettersGuessed:                 # Letters guessed by the player
    :return: T or F                        # T if letter guessed is in secret word F is not
    '''
    foundLetter = False
    temp = lettersGuessed[len(lettersGuessed) - 1]
    for x in secretWord:
        if x == temp:
            foundLetter = True
    return foundLetter


def isLetterGuessed(lettersGuessed, availableLetters):
    '''
    Checks if letter has been guessed before
    :param lettersGuessed:                  # List of Letters guessed by player
    :param availableLetters:                # List of letters not yet guessed by player
    :return: T or F                         # T if letter has been guessed before and F is not
    '''
    result = False
    count = len(lettersGuessed)-1
    temp = lettersGuessed[count]
    for y in availableLetters:
        if temp == y:
            result = True
            break
        else:
            result = False
    return result


def hManRunning():
    '''
    This is the main running code, contains all the outputs and calls to all other methods.
    Player is able to exit game by typing ` in command line.
    :var: letters:                          # All letters in Alphabet
    :var: lettersGuessed:                   # Letters guessed by player
    :var: preGuess:                         # Place holder for players input
    :var: mistakesMade:                     # Mistakes made by the player
    :var: allowedMistakes:                  # Mistakes allowed before players looses game
    :var: finish:                           # Boolean T or F, checks if game is over
    :var: restart:                          # Boolean T or F, checks if game has restarted
    :var: availableLetters:                 # String of not yet guessed letters by the player
    :return: Void
    '''

    print("Welcome to the game Hangman!")
    restart = False
    for x in wordList:                       # Loop over all words or until game is exited(1000 Words)
        if restart:
            print("-----------")
            print("-----------")
            print("-----------")
            restart = False
        secretWord = random.choice(wordList)  # Resets the secret word to random word in .txt file
        print("-----------")
        print("I am thinking of a word that is", len(secretWord), "letters long")
        print("-----------")
        mistakesMade = 0
        allowedMistakes = len(secretWord)*2
        letters = string.ascii_lowercase
        availableLetters = letters
        lettersGuessed = []
        lettersGuessed.clear()
        finish = False
        while mistakesMade < allowedMistakes | finish:
            # Checks if both conditions are met to keep the game loop going,
            # [CONDITION] Mistakes made by player is less than allowed mistakes(2* the word length)
            # {CONDITION] Boolean finish is F, if T current game end, next round starts
            print("You have", allowedMistakes - mistakesMade, "guesses left")
            availableLetters = getAvailableLetters2(lettersGuessed, availableLetters)
            print('Available letters:', availableLetters)
            preGuess = input("Please guess a letter: ").lower()
            while len(preGuess) > 1:
                print("-----------")
                print("Please enter one letter at a time: ")
                preGuess = input("Please enter a letter: ").lower()
                if preGuess == "hack":
                    print("YOU CHEATER HERE YOU GO!! (=", secretWord, "=)")
            lettersGuessed += preGuess
            mostRecent = len(lettersGuessed)-1
            if lettersGuessed[mostRecent] == "`":  # Function that allows the player to exit early
                wordFile.close()
                sys.exit()
            elif not isLetterGuessed(lettersGuessed, availableLetters):
                # Checks of letter has been guessed before by the player, prompts the player if T
                print("Opps! You've already guessed that letter:", getGuessedWord(secretWord, lettersGuessed))
                print("-----------")
            elif isLetterInWord(secretWord, lettersGuessed):
                # Checks of letter guessed is in secret word, prompts player 'Good guess' if T
                if isWordGuessed(secretWord, lettersGuessed):
                    # Checks of full secret word is guessed, if T game over
                    print("Good guess:", getGuessedWord(secretWord, lettersGuessed))
                    print("-----------")
                    print("Congratulations, you won!")
                    restart = True
                    finish = True
                    break
                print("Good geuss: ", getGuessedWord(secretWord, lettersGuessed))
                print("-----------")
            elif not isLetterInWord(secretWord, lettersGuessed):
                # checks is letter guessed is in secret word, if F prompts the player and +1 to mistakes
                print("Opps! That letter is not in my word:", getGuessedWord(secretWord, lettersGuessed))
                mistakesMade += 1
                if mistakesMade >= allowedMistakes:
                    # Checks if mistakes made by player is greater than allowed mistakes, game over if T
                    print("-----------")
                    print("Sorry, you ran out of guesses. The word was:", secretWord)
                    restart = True
                    finish = True
                    break
                print("-----------")
    wordFile.close()  # Close input file

# Calling the main running method.
hManRunning()
