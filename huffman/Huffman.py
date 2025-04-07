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
            # Count only alphabetical characters, converting them to lower case
            for ch in text:
                if ch.isalpha():
                    ch = ch.lower()
                    counts[ch] = counts.get(ch, 0) + 1

        # Create a list of tuples and sort it by count (and letter as secondary sort)
        sorted_counts = sorted(counts.items(), key=lambda x: (x[1], x[0]))
        return sorted_counts