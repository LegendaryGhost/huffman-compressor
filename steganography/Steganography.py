import struct
import wave

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
    def binary_to_text(binary_str: str) -> str:
        """
        Converts a binary string (assumed to be in 8-bit chunks) back into text.
        """
        return ''.join(chr(int(binary_str[i:i + 8], 2)) for i in range(0, len(binary_str), 8))

    @staticmethod
    def hide_message_in_image(png_image_file_path: str, secret_message: str,
                              output_image_path: str, pixel_numbers_file_path: str):
        """
        Hide a text message inside a PNG image by modifying the LSB of each pixel.
        The image is converted to grayscale ('L' mode) and each character is encoded
        as 8-bit binary.  A pixel index file is saved alongside the image.

        Steps:
         - Convert the secret message into an 8-bit binary string.
         - Open the image in L mode (grayscale).
         - For each selected pixel (the first pixels up to the length of the binary message):
             - Get its grayscale channel value.
             - Replace the LSB of that value with the corresponding secret bit.
         - Save the new image in the original mode.
         - Save the list of pixel indices used in a file.
        """
        # Convert the secret message to binary
        binary_text = Steganography.text_to_binary(secret_message)
        binary_length = len(binary_text)

        # Open the image in grayscale mode
        img = Image.open(png_image_file_path).convert('L')
        pixels = list(img.getdata())
        if binary_length > len(pixels):
            raise ValueError("Secret message is too long to hide in this image.")

        # Select the first binary_length pixel indices
        pixel_numbers = list(range(binary_length))

        # Modify the LSB of the grayscale channel for each selected pixel
        new_pixels = list(pixels)
        for idx, bit in zip(pixel_numbers, binary_text):
            pixel = pixels[idx]  # Get the pixel
            # Set the LSB of the red channel to the secret bit
            new_pixel = (pixel & ~1) | int(bit)
            # Reconstruct the pixel with the modified red channel and original other channels
            new_pixels[idx] = new_pixel

        # Create a new image with the same mode and save it
        new_img = Image.new(img.mode, img.size)
        new_img.putdata(new_pixels)
        new_img.save(output_image_path)

        # Save the pixel indices
        with open(pixel_numbers_file_path, "w") as f:
            f.write(','.join(str(n) for n in pixel_numbers))

    @staticmethod
    def extract_message_from_image(png_image_file_path: str, pixel_numbers_file_path: str) -> str:
        """
        Extracts a hidden message from a PNG image by reading the least
        significant bit (LSB) of the specified pixel grayscale channel values.

        Steps:
         - Read the list of pixel indices from the pixel numbers file.
         - Open the image in L mode (grayscale).
         - For each pixel index in the list:
             - Get the pixel's grayscale channel value.
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
        if img.mode != 'L':
            raise ValueError("Image must be in 'L' mode (grayscale).")
        pixels = list(img.getdata())

        # Extract the LSB from the grayscale channel of each specified pixel
        binary_message = ""
        for idx in pixel_numbers:
            pixel = pixels[idx]  # Get the pixel value
            bit = pixel & 1  # Extract the LSB
            binary_message += str(bit)

        return Steganography.binary_to_text(binary_message)

    @staticmethod
    def hide_message_in_audio(wav_audio_file_path: str, secret_message: str,
                              output_audio_file_path: str, sample_numbers_file_path: str):
        """
        Hides the secret message in a WAV audio file by modifying the least
        significant bit (LSB) of the audio samples.

        Steps:
         - Convert the secret message into its 8-bit binary representation.
         - Open the WAV file and read its frames as audio samples.
         - For each sample (up to the length of the binary message), modify the LSB.
           For signed sample values (common for 16-bit audio), convert to the corresponding
           unsigned representation for bit manipulation and then convert back.
         - Write the modified samples into a new WAV file with the same parameters.
         - Save the list of sample indices used in a file.

        Note: This function assumes a mono PCM WAV file with either 8-bit or 16-bit samples.
        """
        # Convert secret message to binary
        binary_text = Steganography.text_to_binary(secret_message)
        binary_length = len(binary_text)

        # Open the WAV file
        with wave.open(wav_audio_file_path, 'rb') as wav_in:
            params = wav_in.getparams()
            nchannels, sampwidth, framerate, nframes, comptype, compname = params
            # Read all audio frames
            frames = wav_in.readframes(nframes)

        # For simplicity, assume mono (nchannels == 1)
        if nchannels != 1:
            raise ValueError("Audio file must be mono for this steganography method.")

        # Determine the format for unpacking based on sample width
        if sampwidth == 1:
            fmt = f"{nframes}B"  # 8-bit unsigned
            max_val = 0xFF
        elif sampwidth == 2:
            fmt = f"<{nframes}h"  # 16-bit signed, little-endian
            max_val = (1 << (sampwidth * 8)) - 1
        else:
            raise ValueError("Only 8-bit and 16-bit audio are supported.")

        # Unpack frames to a tuple of samples
        samples = list(struct.unpack(fmt, frames))

        if binary_length > len(samples):
            raise ValueError("Secret message is too long to hide in this audio file.")

        # Use the first binary_length sample indices
        sample_numbers = list(range(binary_length))

        # Modify the LSB of each selected sample
        new_samples = samples.copy()
        for idx, bit in zip(sample_numbers, binary_text):
            sample = samples[idx]
            # For 16-bit samples, handle potential negatives by converting to unsigned
            if sampwidth == 2:
                # Convert to unsigned representation
                if sample < 0:
                    sample_unsigned = sample + (1 << (sampwidth * 8))
                else:
                    sample_unsigned = sample
                # Modify the LSB
                new_sample_unsigned = (sample_unsigned & ~1) | int(bit)
                # Convert back to signed if necessary
                if new_sample_unsigned >= (1 << (sampwidth * 8 - 1)):
                    new_sample = new_sample_unsigned - (1 << (sampwidth * 8))
                else:
                    new_sample = new_sample_unsigned
            else:
                # For 8-bit samples (unsigned), simply modify the LSB.
                new_sample = (sample & ~1) | int(bit)
            new_samples[idx] = new_sample

        # Pack the modified samples back to bytes
        new_frames = struct.pack(fmt, *new_samples)

        # Write the new frames to the output audio file with the same parameters
        with wave.open(output_audio_file_path, 'wb') as wav_out:
            wav_out.setparams(params)
            wav_out.writeframes(new_frames)

        # Save the sample indices that were modified
        with open(sample_numbers_file_path, "w") as f:
            f.write(','.join(str(n) for n in sample_numbers))

    @staticmethod
    def extract_message_from_audio(wav_audio_file_path: str, sample_numbers_file_path: str) -> str:
        """
        Extracts a hidden message from a WAV audio file by reading the least
        significant bit (LSB) from the samples specified in the sample numbers file.

        Steps:
         - Read the list of sample indices from the given file.
         - Open the WAV file and read its audio samples.
         - For each specified sample, extract the LSB and reassemble the binary message.
         - Convert the binary message back into the text.

        Note: This function assumes the audio is mono and has either 8-bit or 16-bit samples.
        """
        # Read the sample indices
        with open(sample_numbers_file_path, "r") as f:
            content = f.read().strip()
        if not content:
            raise ValueError("No sample indices found in the provided file.")
        sample_numbers = [int(num) for num in content.split(',')]

        # Open the WAV file
        with wave.open(wav_audio_file_path, 'rb') as wav_in:
            params = wav_in.getparams()
            nchannels, sampwidth, framerate, nframes, comptype, compname = params
            frames = wav_in.readframes(nframes)

        if nchannels != 1:
            raise ValueError("Audio file must be mono for this steganography method.")

        # Determine the unpacking format
        if sampwidth == 1:
            fmt = f"{nframes}B"  # 8-bit unsigned
        elif sampwidth == 2:
            fmt = f"<{nframes}h"  # 16-bit signed
        else:
            raise ValueError("Only 8-bit and 16-bit audio are supported.")

        samples = list(struct.unpack(fmt, frames))

        # Extract the LSB from each specified sample to reconstruct the binary message
        binary_message = ""
        for idx in sample_numbers:
            sample = samples[idx]
            if sampwidth == 2:
                # For signed 16-bit, convert to unsigned representation if necessary
                if sample < 0:
                    sample_unsigned = sample + (1 << (sampwidth * 8))
                else:
                    sample_unsigned = sample
                bit = sample_unsigned & 1
            else:
                bit = sample & 1
            binary_message += str(bit)

        return Steganography.binary_to_text(binary_message)
