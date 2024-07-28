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
After you enter that word to wordly, you will need to enter additional information:
* Enter correct positions (separated by comma) - Starting from 0, you will need to enter letter indexes that are in correct position (marked green).
* Enter incorrect positions (separated by comma) - Starting from 0, you will need to enter letter indexes that are in incorrect positions (marked yellow).
From it the application will display the second word to enter to wordly.
Repeat this process until you have been given the correct word.

Performance:
Current performance of this app is 2.9 average guesses.
Average guesses:  2.904103671706263
Guessed frequency:  {1: 145, 2: 700, 3: 903, 4: 412, 5: 116, 6: 32, 7: 7}
