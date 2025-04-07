import json

from huffman.Node import Node


class Huffman:
    @staticmethod
    def count_characters(file_path):
        """
        Reads the text file at file_path and counts the frequency of each letter (ignoring case).
        Returns a list of (letter, count) tuples sorted in ascending order by count.
        """
        counts = {}
        # Open the file and read its contents
        with open(file_path, 'r') as f:
            text = f.read()
            for ch in text:
                counts[ch] = counts.get(ch, 0) + 1

        # Create a list of tuples and sort it by count (and letter as secondary sort)
        return sorted(counts.items(), key=lambda x: (x[1], x[0]))

    @staticmethod
    def make_tree(sorted_counts):
        """
        Builds a Huffman tree from a sorted list of (letter, frequency) tuples.

        Steps:
          1. Convert each tuple into a Node.
          2. While more than one node exists:
              - Remove the two nodes with the smallest frequency.
              - Create a new node with no letter, frequency equal to the sum of the two,
                the first node as the left child, and the second as the right child.
              - Insert the new node back into the list keeping it sorted.
          3. Return the remaining node as the root of the tree.

        :param sorted_counts: List of tuples like [('a', 2), ('b', 3), ...]
        :return: The root Node of the Huffman tree.
        """
        # Step 1: Create a list of Nodes from the (letter, frequency) tuples.
        nodes = [Node(letter, freq) for letter, freq in sorted_counts]

        # Step 2: Build the tree.
        while len(nodes) > 1:
            # Pop the two nodes with the smallest frequency.
            left = nodes.pop(0)
            right = nodes.pop(0)
            # Create a new internal node with the combined frequency.
            new_node = Node(letter=None, freq=left.freq + right.freq, left=left, right=right)
            # Insert the new node and keep the list sorted.
            nodes.append(new_node)
            nodes.sort(key=lambda node: node.freq)

        # Step 3: The last remaining node is the root of the Huffman tree.
        return nodes[0]

    @staticmethod
    def traverse(code_dict, node, code_str = ""):
        # If the node is a leaf (has a letter), store its code.
        if node.letter is not None:
            code_dict[node.letter] = code_str
        else:
            # Traverse the left child, appending "0" to the code.
            if node.left:
                Huffman.traverse(code_dict, node.left, code_str + "0")
            # Traverse the right child, appending "1" to the code.
            if node.right:
                Huffman.traverse(code_dict, node.right, code_str + "1")

    @staticmethod
    def tree_to_dict(root):
        """
        Traverse the Huffman tree to create a dictionary mapping each letter to its binary encoding.
        For each left branch, add '0' to the encoding; for each right branch, add '1'.

        :param root: The root Node of the Huffman tree.
        :return: A dictionary mapping letters to their binary Huffman codes.
        """
        code_dict = {}

        Huffman.traverse(code_dict, root)
        return code_dict

    @staticmethod
    def compress(file_path, compressed_filename, dictionary_filename):
        """
        Compresses the given text file using Huffman encoding and outputs two files:
          - A binary file containing the encoded text.
          - A JSON file containing the encoding dictionary.

        Instead of padding the encoded bit string to a multiple of 8, this function writes a header byte
        indicating the number of valid bits in the final data byte.

        :param file_path: Path to the original text file.
        :param compressed_filename: Path for the output compressed binary file.
        :param dictionary_filename: Path for the output encoding dictionary (JSON file).
        """
        # 1. Count frequencies and build a sorted list.
        sorted_counts = Huffman.count_characters(file_path)

        # 2. Build the Huffman tree.
        root = Huffman.make_tree(sorted_counts)

        # 3. Get the encoding dictionary.
        code_dict = Huffman.tree_to_dict(root)

        # 4. Read the original file and build the encoded bit string.
        encoded_str = ""
        with open(file_path, 'r') as f:
            text = f.read()
            for ch in text:
                if ch in code_dict:
                    encoded_str += code_dict[ch]
                # You may choose to handle characters not present in code_dict here.

        # 5. Pack the bit string into bytes WITHOUT extra padding.
        # Determine how many full bytes we have and the number of valid bits in the last byte.
        full_bytes = len(encoded_str) // 8
        remainder = len(encoded_str) % 8  # number of valid bits in the last byte
        # If remainder is 0 but there is data, treat it as a full byte.
        if len(encoded_str) > 0 and remainder == 0:
            remainder = 8

        b_array = bytearray()
        # Process full bytes
        for i in range(0, full_bytes * 8, 8):
            byte = encoded_str[i:i + 8]
            b_array.append(int(byte, 2))
        # Process the final partial byte, if any.
        if remainder < 8:
            last_bits = encoded_str[full_bytes * 8:]
            # Convert the remaining bits to an integer (they are not padded)
            last_byte = int(last_bits, 2)
            b_array.append(last_byte)

        # 6. Write the binary file.
        # First byte: number of valid bits in the final data byte.
        with open(compressed_filename, "wb") as bf:
            bf.write(bytes([remainder]))
            bf.write(b_array)

        # 7. Save the encoding dictionary as a JSON file.
        with open(dictionary_filename, "w") as df:
            json.dump(code_dict, df, indent=4)
