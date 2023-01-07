from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    # A is either a knight or a knave - A xor B
    Or(AKnave, AKnight),
    Not(And(AKnight, AKnave)),
    # If A is a knight, then A is both a knight and a knave
    # But A cannot be both (per the first two clauses) so for the implication to be true
    # A must be a knave
    Implication(AKnight, And(AKnight, AKnave)),
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    # A character is either a knight or a knave - A xor B
    Or(AKnave, AKnight),
    Not(And(AKnight, AKnave)),
    Or(BKnave, BKnight),
    Not(And(BKnight, BKnave)),
    # A says we are both knave, B says nothing -> A must be a knave and B must be a knight
    # If A is a knave, then both A and B cannot be Knaves
    Implication(AKnave, BKnight),
    # If A is a knight, then both A and B are knaves, but A can't be both a knight and a knave at the same time so A must be a knave
    Implication(AKnight, And(AKnave, BKnave)),
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
# A must be a knave
# B must be a knight
knowledge2 = And(
    # A character is either a knight or a knave - A xor B
    Or(AKnave, AKnight),
    Not(And(AKnight, AKnave)),
    Or(BKnave, BKnight),
    Not(And(BKnight, BKnave)),
    # A says we are the same kind
    Biconditional(AKnight, Or(And(AKnight, BKnight), And(AKnave, BKnave))),
    # We are different kinds
    Biconditional(BKnight, Or(And(AKnave, BKnight), And(AKnight, BKnave))),
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
# A must be a knight
# C must be a knight
# B must be a knave
knowledge3 = And(
    # A character is either a knight or a knave - A xor B
    Or(AKnave, AKnight),
    Not(And(AKnight, AKnave)),
    Or(BKnave, BKnight),
    Not(And(BKnight, BKnave)),
    Or(CKnave, CKnight),
    Not(And(CKnight, CKnave)),
    # A says either "I am a knight." or "I am a knave.", but you don't know which.
    Biconditional(AKnight, And(Or(AKnave, AKnight),
                  Not(And(AKnight, AKnave)))),
    # C says A is a knight
    Implication(CKnight, AKnight),
    Implication(CKnave, AKnave),
    # B says 'C is a knave' AND 'A said I am a knave'
    Implication(BKnight, And(CKnave, AKnave)),
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3),
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
