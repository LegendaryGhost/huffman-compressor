class Steganography:
    @staticmethod
    def text_to_binary(text: str) -> str:
        """
        Converts a given text into its binary representation.

        Each character in the text is converted to an 8-bit binary string.

        Args:
            text (str): The input string to convert.

        Returns:
            str: A string containing the binary representation of the text.
        """
        return ''.join(format(ord(char), '08b') for char in text)