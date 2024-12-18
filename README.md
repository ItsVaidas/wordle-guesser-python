A simple wordly Python guesser

App has two dictionaries: wordly with 2315 words and random list with 5757 words.
All words contain 5 letters.

To launch the app you just need to enter ```python3 bot.py``` to a terminal while being in that directory.

After launching the app it will ask if you want it to be in a simulation mode "y" or user input mode "n".
The application then runs in selected mode.

Simulation mode:
Application will begin to test each word in la-words.txt file and try to guess that word. The frequencies will be displayed on screen. When the application finishes up, it will show the average amount of guesses it took to find the word and frequencies of each guess.

Input mode:
A word will be displayed in the terminal of which word to enter. The first word will always be "CRANE".
After you enter that word to wordly, you will need to write the result in the app. 
w - incorrect letter
g - correct letter in correct position
y - correct letter in incorrect position
example: ggwwy
From it the application will display the second word to enter to wordly.
Repeat this process until you have been given the correct word.

Performance:
Current performance of this app is 3.82 average guesses.
Average guesses:  3.8267818574514043
Guessed frequency:  {1: 1, 2: 132, 3: 786, 4: 901, 5: 375, 6: 86, 7: 31, 8: 3}
