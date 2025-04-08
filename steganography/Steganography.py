from PIL import Image


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

    @staticmethod
    def hide_message_in_image(png_image_file_path: str, secret_message: str,
                              output_image_path: str, pixel_numbers_file_path: str):
        """
        Hides the secret message in the PNG image by modifying the least significant
        bit (LSB) of the grayscale value (luminance) for each of the selected pixels.
        The output image keeps its original colors, only adjusted slightly to reflect
        the modified grayscale values.

        Steps:
        - Convert the secret message into a binary string.
        - Open the image in RGB mode.
        - For each pixel selected (here, the first pixels up to the length of the binary message):
            - Compute its grayscale value using the luminance formula (0.299R + 0.587G + 0.114B).
            - Modify the LSB of the grayscale value to store the corresponding bit.
            - Calculate the difference (delta) between the new and old grayscale value.
            - Adjust the original pixel channels by the delta (with clamping to keep values in 0–255).
        - Save the new image.
        - Save the list of pixel indices used in a file.

        Args:
            png_image_file_path (str): Path to the input PNG image file.
            secret_message (str): The message to hide.
            output_image_path (str): Path to save the modified output image.
            pixel_numbers_file_path (str): Path to save the list of pixel numbers used.
        """
        # Convert the secret message to binary.
        binary_text = Steganography.text_to_binary(secret_message)
        binary_length = len(binary_text)

        # Open the image in RGB mode.
        img = Image.open(png_image_file_path).convert("RGB")
        pixels = list(img.getdata())
        if binary_length > len(pixels):
            raise ValueError("Secret message is too long to hide in this image.")

        # For now, select the first binary_length pixels.
        pixel_numbers = list(range(binary_length))

        # Duplicate the pixel list for modifications.
        new_pixels = list(pixels)
        for idx, bit in zip(pixel_numbers, binary_text):
            r, g, b = pixels[idx]
            # Compute the grayscale (luminance) of the pixel.
            old_lum = int(0.299 * r + 0.587 * g + 0.114 * b)
            # Replace the LSB of the grayscale value with the secret bit.
            new_lum = (old_lum & ~1) | int(bit)
            # Calculate the small difference: the change is only -1, 0, or +1.
            delta = new_lum - old_lum

            # Adjust each channel by the delta, ensuring values remain within [0, 255].
            new_r = max(0, min(255, r + delta))
            new_g = max(0, min(255, g + delta))
            new_b = max(0, min(255, b + delta))

            new_pixels[idx] = (new_r, new_g, new_b)

        # Create a new RGB image with the modified pixels and save it.
        new_img = Image.new("RGB", img.size)
        new_img.putdata(new_pixels)
        new_img.save(output_image_path)

        # Save the list of used pixel indices into the specified file.
        with open(pixel_numbers_file_path, "w") as f:
            f.write(','.join(str(n) for n in pixel_numbers))

    @staticmethod
    def binary_to_text(binary_str: str) -> str:
        """
        Converts a binary string (assumed to be in 8-bit chunks) back into text.

        Args:
            binary_str (str): The binary string to convert.

        Returns:
            str: The decoded text.
        """
        # Split the binary string into 8-bit chunks and convert each to a character.
        text = ''.join(chr(int(binary_str[i:i + 8], 2)) for i in range(0, len(binary_str), 8))
        return text

    @staticmethod
    def extract_message_from_image(png_image_file_path: str, pixel_numbers_file_path: str) -> str:
        """
        Extracts a hidden message from a PNG image by reading the LSB of the grayscale
        value of the specified pixels.

        Steps:
        - Read the list of pixel indices from the pixel numbers file.
        - Open the image (in RGB mode).
        - For each pixel index in the list:
            - Compute its grayscale value using the luminance formula (0.299R + 0.587G + 0.114B).
            - Extract the least significant bit.
        - Reconstruct the binary string from the collected bits.
        - Convert the binary string back into text using `binary_to_text`.

        Args:
            png_image_file_path (str): Path to the image with the hidden message.
            pixel_numbers_file_path (str): Path to the file containing the pixel indices.

        Returns:
            str: The hidden message extracted from the image.
        """
        # Read the comma-separated pixel indices from the file.
        with open(pixel_numbers_file_path, "r") as f:
            content = f.read().strip()
        if not content:
            raise ValueError("No pixel indices found in the provided file.")
        pixel_numbers = [int(num) for num in content.split(',')]

        # Open the image in RGB mode.
        img = Image.open(png_image_file_path).convert("RGB")
        pixels = list(img.getdata())

        binary_message = ""
        for idx in pixel_numbers:
            r, g, b = pixels[idx]
            # Compute the grayscale (luminance) of the pixel.
            lum = int(0.299 * r + 0.587 * g + 0.114 * b)
            # Extract the least significant bit.
            bit = lum & 1
            binary_message += str(bit)

        # Convert the binary message back to text.
        return Steganography.binary_to_text(binary_message)