# Mastermind
Mastermind game in python using tkinter library (menu, scores)

## MENU
### Play
Lauch the app with ```python3 game.py```
On the main window, enter your pseudo and click ```Lancer une partie``` to start the game.


### Scores
Click on ```Scores``` to see the number of games already dones and the TOP10 users' results.

### Rules
If you're french, you will also see and understand the rules of the game on the games main page.


## GAME
While you're playing, you can press space key to reset your progression and start a new game.
Use Left/Right keyboard arrow to navigate between value positions.
Use Top/Bottom keyboard arrow to change the color of a circle.
Use enter key to validate and go to next row
When you validate a row, some colors appears on circles on the right.
  - if circle is orange, you set a rigth color in a wrong position
  - if circle is green , you set a right color in a right position
  - if circle is white, nothing you set is correct, try another combination
  
When you find the right combination, a popup will appears 8 seconds with your score and then it disappears and you come back to menu window
If you loose the game, a defeat popup appears on your screen for 8 seconds and you come back to menu window

## Scores
The score is calculated like this : 
  - you have 10 try to find the right combination
  - you start with 10 points and for each validated combination, your score is discredited of 1 point
  
So, if you find the combination at the 3rd try, you will win with 7 points and if you win at the 1Oth try, you will have only one point.
If you loose, you will have no points, but your score is saved.
