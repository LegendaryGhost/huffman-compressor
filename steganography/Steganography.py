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
        Hides the secret message in the PNG image by modifying the least
        significant bit (LSB) of each red channel byte.

        New steps:
         - Convert the secret message into an 8-bit binary string.
         - Open the image in RGB mode.
         - For each pixel (here, the first pixels up to the length of the binary message):
             - Get its red channel value (a number 0–255).
             - Replace the least significant bit (LSB) of that value with the corresponding secret bit.
         - Save the new RGB image.
         - Save the list of pixel indices used in a file.
        """

        # Convert the secret message to binary.
        binary_text = Steganography.text_to_binary(secret_message)
        binary_length = len(binary_text)

        # Open the image in its original mode (e.g., RGB)
        img = Image.open(png_image_file_path)
        print(f"Image mode: {img.mode}")
        if img.mode != "RGB":
            raise ValueError("Image must be in RGB mode for this implementation.")
        pixels = list(img.getdata())
        if binary_length > len(pixels):
            raise ValueError("Secret message is too long to hide in this image.")

        # Select the first binary_length pixel indices
        pixel_numbers = list(range(binary_length))

        # Modify the LSB of the red channel for each selected pixel
        new_pixels = list(pixels)
        for idx, bit in zip(pixel_numbers, binary_text):
            r, g, b = pixels[idx]
            # Set the LSB of the red channel to the secret bit
            new_r = (r & ~1) | int(bit)
            new_pixels[idx] = (new_r, g, b)

        # Create a new image with the same mode and save it
        new_img = Image.new(img.mode, img.size)
        new_img.putdata(new_pixels)
        new_img.save(output_image_path)

        # Save the pixel indices
        with open(pixel_numbers_file_path, "w") as f:
            f.write(','.join(str(n) for n in pixel_numbers))

    @staticmethod
    def binary_to_text(binary_str: str) -> str:
        """
        Converts a binary string (assumed to be in 8-bit chunks) back into text.
        """
        return ''.join(chr(int(binary_str[i:i + 8], 2)) for i in range(0, len(binary_str), 8))

    @staticmethod
    def extract_message_from_image(png_image_file_path: str, pixel_numbers_file_path: str) -> str:
        """
        Extracts a hidden message from an RGB PNG image by reading the least
        significant bit (LSB) of the specified pixel values.

        Steps:
         - Read the list of pixel indices from the pixel numbers file.
         - Open the image in RGB mode.
         - For each pixel index in the list:
             - Get the pixel's red channel value (0–255).
             - Extract the LSB.
         - Reconstruct the binary message and convert it back to text.
        """

        # Read the pixel indices
        with open(pixel_numbers_file_path, "r") as f:
            content = f.read().strip()
        if not content:
            raise ValueError("No pixel indices found in the provided file.")
        pixel_numbers = [int(num) for num in content.split(',')]

        # Open the image in its original mode
        img = Image.open(png_image_file_path)
        if img.mode != "RGB":
            raise ValueError("Image must be in RGB mode for this implementation.")
        pixels = list(img.getdata())

        # Extract the LSB from the red channel of each specified pixel
        binary_message = ""
        for idx in pixel_numbers:
            r, g, b = pixels[idx]
            bit = r & 1
            binary_message += str(bit)

        return Steganography.binary_to_text(binary_message)
