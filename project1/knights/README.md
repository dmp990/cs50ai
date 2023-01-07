# Knights

This program aims to solve a bunch of puzzles from Raymond Smullyan's Knights and Knaves class of puzzles.

## Rules

In a Knights and Knaves puzzle, the following information is given: Each character is either a knight or a knave. A knight will always tell the truth: if knight states a sentence, then that sentence is true. Conversely, a knave will always lie: if a knave states a sentence, then that sentence is false.

## Understanding

This folder contains two files: `logic.py` and `puzzle.py`. `logic.py` defines several classes for different types of logical connectives e.g. `Or(A, B)` represents A or B or both. It also defines the `model_check` function that checks whether or not our knowledge base entails a proposition. `logic.py` was provided with the distribution code.

In `puzzle.py`, we need to:
* Define what the rules of the game are
* Translate the sentences of each character into propositional logic

The program then lays out every possible model and checks to see where our knowledge base entails our symbol.

## Run Locally

`cd` into the directory and run:

`python3 puzzle.py`

Sample Output:

```shell
$ python puzzle.py 
Puzzle 0
    A is a Knave
Puzzle 1
    A is a Knave
    B is a Knight
Puzzle 2
    A is a Knave
    B is a Knight
Puzzle 3
    A is a Knight
    B is a Knave
    C is a Knight
```
