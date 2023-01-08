import itertools
import random


class Minesweeper:
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines

    def __str__(self):
        str = ""
        for i in range(self.height):
            str += "--" * self.width + "-\n"
            for j in range(self.width):
                if self.board[i][j]:
                    str += "|X"
                else:
                    str += f"|{self.nearby_mines((i, j))}"
            str += "|\n"
        str += "--" * self.width + "-\n"
        return str


class Sentence:
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if len(self.cells) == self.count:
            return self.cells.copy()

        return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells.copy()

        return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.count -= 1
            self.cells.remove(cell)

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI:
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # Cell is represented by a tuple (i, j) and a number k

        # Mark the cell as one of the moves made
        self.moves_made.add(cell)

        # Mark the cell as safe
        self.mark_safe(cell)

        # Add a new sentence to knowledge
        self.add_new_sentence(cell, count)

        # If, based on any of the sentences in self.knowledge, new cells can be marked as safe or as mines, then the function should do so.
        self.mark_if_possible()

        # If, based on any of the sentences in self.knowledge, new sentences can be inferred (using the subset method described in the Background), then those sentences should be added to the knowledge base as well.
        inferred = self.infer_more_sentences()
        while inferred:
            for sentence in inferred:
                self.knowledge.append(sentence)
            self.mark_if_possible()
            # See if further inferences can be made using the subset method
            inferred = self.infer_more_sentences()

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """

        for safe in self.safes:
            if safe not in self.moves_made and safe not in self.mines:
                return safe
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        available_cells = []
        for i in range(self.height):
            for j in range(self.width):
                if (i, j) not in self.mines and (i, j) not in self.moves_made:
                    available_cells.append((i, j))

        return random.choice(available_cells) if len(available_cells) else None

    def add_new_sentence(self, cell, count):
        cellsToBeAdded = set()
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue
                # Ensure (i, j) is within bounds
                if 0 <= i < self.height and 0 <= j < self.width:
                    if (
                        (i, j) not in self.safes
                        or (i, j) not in self.mines
                        or (i, j) not in self.moves_made
                    ):
                        cellsToBeAdded.add((i, j))

        sentenceToAdd = Sentence(cellsToBeAdded, count)
        if sentenceToAdd not in self.knowledge:
            self.knowledge.append(sentenceToAdd)

    def infer_more_sentences(self):
        inferred = []
        if len(self.knowledge) > 1:
            for i in range(len(self.knowledge) - 1):
                if self.knowledge[i].cells == self.knowledge[i + 1].cells:
                    # No need to check futher
                    continue
                if self.knowledge[i].cells.issubset(self.knowledge[i + 1].cells):
                    cellsToAdd = self.knowledge[i + 1].cells.difference(
                        self.knowledge[i].cells
                    )
                    countToAdd = self.knowledge[i + 1].count - self.knowledge[i].count
                    if Sentence(cellsToAdd, countToAdd) not in self.knowledge:
                        inferred.append(Sentence(cellsToAdd, countToAdd))
                if self.knowledge[i + 1].cells.issubset(self.knowledge[i].cells):
                    cellsToAdd = self.knowledge[i].cells.difference(
                        self.knowledge[i + 1].cells
                    )
                    countToAdd = self.knowledge[i].count - self.knowledge[i + 1].count
                    if Sentence(cellsToAdd, countToAdd) not in self.knowledge:
                        inferred.append(Sentence(cellsToAdd, countToAdd))

        return inferred

    def mark_if_possible(self):
        for sentence in self.knowledge:
            for mine in sentence.known_mines():
                self.mark_mine(mine)
            for safe in sentence.known_safes():
                self.mark_safe(safe)
        for mine in self.mines:
            self.mark_mine(mine)
        for safe in self.safes:
            self.mark_safe(safe)

    def print_internals(self, knowledge=True, moves=False, mines=False, safes=False):
        if knowledge:
            print("Knowledge: ", end="")
            for elem in self.knowledge:
                print(elem)
            print()
        if moves:
            print(f"Moves Made: {self.moves_made}")
        if mines:
            print(f"Mines: {self.mines}")
        if safes:
            print(f"Safes: {self.safes}")

    def add_knowledge_testing_purpose(self, setIn, count):
        self.knowledge.append(Sentence(setIn, count))
