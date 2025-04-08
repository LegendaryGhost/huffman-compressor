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
        bit (LSB) of each of the selected pixels in the image.

        Steps:
        - Convert the secret message into a binary string.
        - Open the image (in grayscale mode) using Pillow.
        - Create a list of pixel indices that will be used for storing the message (first pixels).
        - Loop over these pixels and replace the LSB of each pixel with a bit from the binary message.
        - Output the new image with the hidden secret message.
        - Save the pixel numbers used in a file.

        Args:
            png_image_file_path (str): Path to the input PNG image file.
            secret_message (str): The message to hide.
            output_image_path (str): Path to save the modified output image.
            pixel_numbers_file_path (str): Path to save the list of pixel numbers used.
        """
        # Convert secret message to binary
        binary_text = Steganography.text_to_binary(secret_message)
        binary_length = len(binary_text)

        # Open the image and convert to grayscale
        img = Image.open(png_image_file_path)
        img = img.convert("L")

        # Get image pixels in a list
        pixels = list(img.getdata())
        if binary_length > len(pixels):
            raise ValueError("Secret message is too long to hide in this image.")

        # For now, select the first binary_length pixels
        pixel_numbers = list(range(binary_length))

        # Modify the LSB of each pixel using the corresponding bit from binary_text
        for idx, bit in zip(pixel_numbers, binary_text):
            old_pixel = pixels[idx]
            # Replace the least significant bit with the bit from the message
            new_pixel = (old_pixel & ~1) | int(bit)
            pixels[idx] = new_pixel

        # Create a new image with modified pixel data and save it
        new_img = Image.new("L", img.size)
        new_img.putdata(pixels)
        new_img.save(output_image_path)

        # Save the list of used pixel indices into a file
        with open(pixel_numbers_file_path, "w") as f:
            f.write(','.join(str(n) for n in pixel_numbers))