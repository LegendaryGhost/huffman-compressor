class Node:
    def __init__(self, letter, freq, left=None, right=None):
        """
        Initializes a new tree node.
        :param letter: A character (or None for internal nodes)
        :param freq: The frequency count (number)
        :param left: Left child (another Node or None)
        :param right: Right child (another Node or None)
        """
        self.letter = letter
        self.freq = freq
        self.left = left
        self.right = right

    def __repr__(self):
        return f"Node(letter={self.letter}, freq={self.freq})"

    def print_tree(self, indent=0):
        """
        Recursively prints the tree with indentation.
        Internal nodes are shown with '*' as the letter.
        """
        prefix = "  " * indent
        node_label = f"{self.letter}:{self.freq}" if self.letter is not None else f"*:{self.freq}"
        print(prefix + node_label)
        if self.left:
            self.left.print_tree(indent + 1)
        if self.right:
            self.right.print_tree(indent + 1)
