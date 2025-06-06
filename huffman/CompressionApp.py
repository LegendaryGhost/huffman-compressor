import os
import tkinter.filedialog as fd

import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from huffman.Huffman import Huffman
from steganography.Steganography import Steganography
from evaluator.LanguageEvaluator import LanguageEvaluator


class CompressionApp(ttk.Window):
    def __init__(self, *args, **kwargs):
        # Initialize the window with a modern theme.
        super().__init__(themename="litera", *args, **kwargs)
        self.title("Huffman encoding / Steganography")
        self.geometry("1000x800")

        # Use a Notebook widget to create multiple tabs.
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill='both', expand=True)

        # Huffman compression UI
        self.build_compression_form()
        self.build_decompression_form()

        # Image steganography UI
        self.build_steganography_hide_form()
        self.build_steganography_extract_form()

        # Audio steganography UI
        self.build_audio_steganography_hide_form()
        self.build_audio_steganography_extract_form()

        # Langage examination UI
        self.build_language_evaluation_form()

    # --------------- Compression Tab ---------------
    def build_compression_form(self):
        self.compress_frame = ttk.Frame(self.notebook, padding=20)
        self.notebook.add(self.compress_frame, text="Compress")

        # Input file selection.
        ttk.Label(self.compress_frame, text="Select Text File:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.file_path_var = ttk.StringVar()
        self.file_entry = ttk.Entry(self.compress_frame, textvariable=self.file_path_var, width=40)
        self.file_entry.grid(row=0, column=1, padx=5, pady=5)
        self.browse_file_button = ttk.Button(
            self.compress_frame, text="Browse", bootstyle=PRIMARY, command=self.browse_text_file
        )
        self.browse_file_button.grid(row=0, column=2, padx=5, pady=5)

        # Output folder selection.
        ttk.Label(self.compress_frame, text="Output Folder:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.out_folder_var = ttk.StringVar()
        self.out_folder_entry = ttk.Entry(self.compress_frame, textvariable=self.out_folder_var, width=40)
        self.out_folder_entry.grid(row=1, column=1, padx=5, pady=5)
        self.browse_out_button = ttk.Button(
            self.compress_frame, text="Browse", bootstyle=PRIMARY, command=self.browse_output_folder
        )
        self.browse_out_button.grid(row=1, column=2, padx=5, pady=5)

        # Compress button.
        self.compress_button = ttk.Button(
            self.compress_frame, text="Compress", bootstyle=SUCCESS, command=self.compress_file
        )
        self.compress_button.grid(row=2, column=1, pady=10)

        # Status label.
        self.comp_status_label = ttk.Label(self.compress_frame, text="")
        self.comp_status_label.grid(row=3, column=0, columnspan=3, pady=5)

    def browse_text_file(self):
        filetypes = (("Text files", "*.txt"), ("All files", "*.*"))
        filename = fd.askopenfilename(title="Select a Text File", initialdir=os.getcwd(), filetypes=filetypes)
        if filename:
            self.file_path_var.set(filename)

    def browse_output_folder(self):
        folder = fd.askdirectory(title="Select Output Folder", initialdir=os.getcwd())
        if folder:
            self.out_folder_var.set(folder)

    def compress_file(self):
        filepath = self.file_path_var.get()
        out_folder = self.out_folder_var.get() or os.path.dirname(filepath)
        if not filepath:
            self.comp_status_label.config(text="Please select a text file!", bootstyle="danger")
            return
        try:
            # Construct output filenames based on the chosen folder.
            base = os.path.splitext(os.path.basename(filepath))[0]
            compressed_filepath = os.path.join(out_folder, base + ".huff")
            dictionary_filepath = os.path.join(out_folder, base + "_dict.json")

            Huffman.compress(filepath, compressed_filepath, dictionary_filepath)

            self.comp_status_label.config(
                text=f"File compressed:\n{compressed_filepath}\nDictionary saved at:\n{dictionary_filepath}",
                bootstyle="success"
            )
        except Exception as e:
            self.comp_status_label.config(text=f"Error: {str(e)}", bootstyle="danger")

    # --------------- Decompression Tab ---------------
    def build_decompression_form(self):
        self.decomp_frame = ttk.Frame(self.notebook, padding=20)
        self.notebook.add(self.decomp_frame, text="Decompress")

        # Compressed file input.
        ttk.Label(self.decomp_frame, text="Compressed File:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.comp_file_var = ttk.StringVar()
        self.comp_file_entry = ttk.Entry(self.decomp_frame, textvariable=self.comp_file_var, width=40)
        self.comp_file_entry.grid(row=0, column=1, padx=5, pady=5)
        self.browse_comp_button = ttk.Button(
            self.decomp_frame, text="Browse", bootstyle=PRIMARY, command=self.browse_compressed_file
        )
        self.browse_comp_button.grid(row=0, column=2, padx=5, pady=5)

        # Encoding dictionary file input.
        ttk.Label(self.decomp_frame, text="Encoding Dictionary File:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.dict_file_var = ttk.StringVar()
        self.dict_file_entry = ttk.Entry(self.decomp_frame, textvariable=self.dict_file_var, width=40)
        self.dict_file_entry.grid(row=1, column=1, padx=5, pady=5)
        self.browse_dict_button = ttk.Button(
            self.decomp_frame, text="Browse", bootstyle=PRIMARY, command=self.browse_dict_file
        )
        self.browse_dict_button.grid(row=1, column=2, padx=5, pady=5)

        # Output file selection.
        ttk.Label(self.decomp_frame, text="Output File:").grid(row=2, column=0, sticky='w', padx=5, pady=5)
        self.out_file_var = ttk.StringVar()
        self.out_file_entry = ttk.Entry(self.decomp_frame, textvariable=self.out_file_var, width=40)
        self.out_file_entry.grid(row=2, column=1, padx=5, pady=5)
        self.browse_out_file_button = ttk.Button(
            self.decomp_frame, text="Browse", bootstyle=PRIMARY, command=self.browse_output_file
        )
        self.browse_out_file_button.grid(row=2, column=2, padx=5, pady=5)

        # Decompress button.
        self.decomp_button = ttk.Button(
            self.decomp_frame, text="Decompress", bootstyle=SUCCESS, command=self.decompress_file
        )
        self.decomp_button.grid(row=3, column=1, pady=10)

        # Status label.
        self.decomp_status_label = ttk.Label(self.decomp_frame, text="")
        self.decomp_status_label.grid(row=4, column=0, columnspan=3, pady=5)

    def browse_compressed_file(self):
        filetypes = (("Huffman files", "*.huff"), ("All files", "*.*"))
        filename = fd.askopenfilename(title="Select Compressed File", initialdir=os.getcwd(), filetypes=filetypes)
        if filename:
            self.comp_file_var.set(filename)

    def browse_dict_file(self):
        filetypes = (("JSON files", "*.json"), ("All files", "*.*"))
        filename = fd.askopenfilename(title="Select Encoding Dictionary", initialdir=os.getcwd(), filetypes=filetypes)
        if filename:
            self.dict_file_var.set(filename)

    def browse_output_file(self):
        filename = fd.asksaveasfilename(title="Select Output File", initialdir=os.getcwd(), defaultextension=".txt",
                                        filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
        if filename:
            self.out_file_var.set(filename)

    def decompress_file(self):
        comp_filepath = self.comp_file_var.get()
        dict_filepath = self.dict_file_var.get()
        output_filepath = self.out_file_var.get()

        if not (comp_filepath and dict_filepath and output_filepath):
            self.decomp_status_label.config(text="Please select all three inputs!", bootstyle="danger")
            return

        try:
            Huffman.decode(comp_filepath, dict_filepath, output_filepath)
            self.decomp_status_label.config(
                text=f"File decompressed successfully and saved to:\n{output_filepath}",
                bootstyle="success"
            )
        except Exception as e:
            self.decomp_status_label.config(text=f"Error: {str(e)}", bootstyle="danger")

    # --------------- Steganography Hide Tab ---------------
    def build_steganography_hide_form(self):
        self.hide_frame = ttk.Frame(self.notebook, padding=20)
        self.notebook.add(self.hide_frame, text="Steganography - Hide")

        # PNG image file selection.
        ttk.Label(self.hide_frame, text="Select PNG Image File:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.stego_image_var = ttk.StringVar()
        self.stego_image_entry = ttk.Entry(self.hide_frame, textvariable=self.stego_image_var, width=40)
        self.stego_image_entry.grid(row=0, column=1, padx=5, pady=5)
        self.browse_stego_image_button = ttk.Button(
            self.hide_frame, text="Browse", bootstyle=PRIMARY, command=self.browse_stego_image
        )
        self.browse_stego_image_button.grid(row=0, column=2, padx=5, pady=5)

        # Text message input.
        ttk.Label(self.hide_frame, text="Text Message to Hide:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.stego_text_message = ttk.Entry(self.hide_frame, width=53)
        self.stego_text_message.grid(row=1, column=1, padx=5, pady=5, columnspan=2)

        # Output file for the new image.
        ttk.Label(self.hide_frame, text="Output Image File:").grid(row=2, column=0, sticky='w', padx=5, pady=5)
        self.out_stego_image_var = ttk.StringVar()
        self.out_stego_image_entry = ttk.Entry(self.hide_frame, textvariable=self.out_stego_image_var, width=40)
        self.out_stego_image_entry.grid(row=2, column=1, padx=5, pady=5)
        self.browse_out_stego_image_button = ttk.Button(
            self.hide_frame, text="Browse", bootstyle=PRIMARY, command=self.browse_out_stego_image
        )
        self.browse_out_stego_image_button.grid(row=2, column=2, padx=5, pady=5)

        # Output file for the pixel numbers.
        ttk.Label(self.hide_frame, text="Output Pixel Numbers File:").grid(row=3, column=0, sticky='w', padx=5, pady=5)
        self.out_pixels_var = ttk.StringVar()
        self.out_pixels_entry = ttk.Entry(self.hide_frame, textvariable=self.out_pixels_var, width=40)
        self.out_pixels_entry.grid(row=3, column=1, padx=5, pady=5)
        self.browse_out_pixels_button = ttk.Button(
            self.hide_frame, text="Browse", bootstyle=PRIMARY, command=self.browse_out_pixels
        )
        self.browse_out_pixels_button.grid(row=3, column=2, padx=5, pady=5)

        # Submit button.
        self.hide_submit_button = ttk.Button(
            self.hide_frame, text="Hide Message", bootstyle=SUCCESS, command=self.hide_message_in_image
        )
        self.hide_submit_button.grid(row=4, column=1, pady=10)

        # Status label.
        self.hide_status_label = ttk.Label(self.hide_frame, text="")
        self.hide_status_label.grid(row=5, column=0, columnspan=3, pady=5)

    def browse_stego_image(self):
        filetypes = (("PNG files", "*.png"), ("All files", "*.*"))
        filename = fd.askopenfilename(title="Select PNG Image File", initialdir=os.getcwd(), filetypes=filetypes)
        if filename:
            self.stego_image_var.set(filename)

    def browse_out_stego_image(self):
        filename = fd.asksaveasfilename(title="Output Image File", initialdir=os.getcwd(),
                                         defaultextension=".png", filetypes=(("PNG files", "*.png"), ("All files", "*.*")))
        if filename:
            self.out_stego_image_var.set(filename)

    def browse_out_pixels(self):
        filename = fd.asksaveasfilename(title="Output Pixel Numbers File", initialdir=os.getcwd(),
                                         defaultextension=".txt", filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
        if filename:
            self.out_pixels_var.set(filename)

    def hide_message_in_image(self):
        try:
            # Call the function to hide the message in the image
            Steganography.hide_message_in_image(
                png_image_file_path=self.stego_image_var.get(),
                secret_message=self.stego_text_message.get(),
                output_image_path=self.out_stego_image_var.get(),
                pixel_numbers_file_path=self.out_pixels_var.get()
            )
            self.hide_status_label.config(text="Message hidden successfully.", bootstyle="success")
        except Exception as e:
            self.hide_status_label.config(text=f"Error: {str(e)}", bootstyle="danger")

    # --------------- Steganography Extract Tab ---------------
    def build_steganography_extract_form(self):
        self.extract_frame = ttk.Frame(self.notebook, padding=20)
        self.notebook.add(self.extract_frame, text="Steganography - Extract")

        # PNG image file selection.
        ttk.Label(self.extract_frame, text="Select PNG Image File:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.extract_image_var = ttk.StringVar()
        self.extract_image_entry = ttk.Entry(self.extract_frame, textvariable=self.extract_image_var, width=40)
        self.extract_image_entry.grid(row=0, column=1, padx=5, pady=5)
        self.browse_extract_image_button = ttk.Button(
            self.extract_frame, text="Browse", bootstyle=PRIMARY, command=self.browse_extract_image
        )
        self.browse_extract_image_button.grid(row=0, column=2, padx=5, pady=5)

        # Pixel numbers file selection.
        ttk.Label(self.extract_frame, text="Pixel Numbers File:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.extract_pixels_var = ttk.StringVar()
        self.extract_pixels_entry = ttk.Entry(self.extract_frame, textvariable=self.extract_pixels_var, width=40)
        self.extract_pixels_entry.grid(row=1, column=1, padx=5, pady=5)
        self.browse_extract_pixels_button = ttk.Button(
            self.extract_frame, text="Browse", bootstyle=PRIMARY, command=self.browse_extract_pixels
        )
        self.browse_extract_pixels_button.grid(row=1, column=2, padx=5, pady=5)

        # Hidden message output.
        ttk.Label(self.extract_frame, text="Hidden Message:").grid(row=2, column=0, sticky='w', padx=5, pady=5)
        self.hidden_message_text = ttk.Entry(self.extract_frame, width=53)
        self.hidden_message_text.grid(row=2, column=1, padx=5, pady=5, columnspan=2)

        # Submit button.
        self.extract_submit_button = ttk.Button(
            self.extract_frame, text="Extract Message", bootstyle=SUCCESS, command=self.extract_message_from_image
        )
        self.extract_submit_button.grid(row=3, column=1, pady=10)

        # Status label.
        self.extract_status_label = ttk.Label(self.extract_frame, text="")
        self.extract_status_label.grid(row=4, column=0, columnspan=3, pady=5)

    def browse_extract_image(self):
        filetypes = (("PNG files", "*.png"), ("All files", "*.*"))
        filename = fd.askopenfilename(title="Select PNG Image File", initialdir=os.getcwd(), filetypes=filetypes)
        if filename:
            self.extract_image_var.set(filename)

    def browse_extract_pixels(self):
        filetypes = (("Text files", "*.txt"), ("All files", "*.*"))
        filename = fd.askopenfilename(title="Select Pixel Numbers File", initialdir=os.getcwd(), filetypes=filetypes)
        if filename:
            self.extract_pixels_var.set(filename)

    def extract_message_from_image(self):
        try:
            # Call the extract function with the image path and pixel indices file.
            hidden_message = Steganography.extract_message_from_image(
                png_image_file_path=self.extract_image_var.get(),
                pixel_numbers_file_path=self.extract_pixels_var.get()
            )
            # Display the hidden message in the entry widget.
            self.hidden_message_text.delete(0, 'end')
            self.hidden_message_text.insert(0, hidden_message)
            self.extract_status_label.config(text="Message extracted successfully.", bootstyle="success")
        except Exception as e:
            self.extract_status_label.config(text=f"Error: {str(e)}", bootstyle="danger")

    # --------------- Audio Steganography Hide Tab ---------------
    def build_audio_steganography_hide_form(self):
        self.audio_hide_frame = ttk.Frame(self.notebook, padding=20)
        self.notebook.add(self.audio_hide_frame, text="Steganography (audio) - Hide")

        # WAV audio file selection.
        ttk.Label(self.audio_hide_frame, text="Select WAV Image File:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.stego_audio_var = ttk.StringVar()
        self.stego_audio_entry = ttk.Entry(self.audio_hide_frame, textvariable=self.stego_audio_var, width=40)
        self.stego_audio_entry.grid(row=0, column=1, padx=5, pady=5)
        self.browse_stego_audio_button = ttk.Button(
            self.audio_hide_frame, text="Browse", bootstyle=PRIMARY, command=self.browse_stego_audio
        )
        self.browse_stego_audio_button.grid(row=0, column=2, padx=5, pady=5)

        # Text message input.
        ttk.Label(self.audio_hide_frame, text="Text Message to Hide:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.audio_stego_text_message = ttk.Entry(self.audio_hide_frame, width=53)
        self.audio_stego_text_message.grid(row=1, column=1, padx=5, pady=5, columnspan=2)

        # Output file for the new audio.
        ttk.Label(self.audio_hide_frame, text="Output Audio File:").grid(row=2, column=0, sticky='w', padx=5, pady=5)
        self.out_stego_audio_var = ttk.StringVar()
        self.out_stego_audio_entry = ttk.Entry(self.audio_hide_frame, textvariable=self.out_stego_audio_var, width=40)
        self.out_stego_audio_entry.grid(row=2, column=1, padx=5, pady=5)
        self.browse_out_stego_audio_button = ttk.Button(
            self.audio_hide_frame, text="Browse", bootstyle=PRIMARY, command=self.browse_out_stego_audio
        )
        self.browse_out_stego_audio_button.grid(row=2, column=2, padx=5, pady=5)

        # Output file for the pixel numbers.
        ttk.Label(self.audio_hide_frame, text="Output Sample Numbers File:").grid(row=3, column=0, sticky='w', padx=5, pady=5)
        self.audio_out_samples_var = ttk.StringVar()
        self.audio_out_samples_entry = ttk.Entry(self.audio_hide_frame, textvariable=self.audio_out_samples_var, width=40)
        self.audio_out_samples_entry.grid(row=3, column=1, padx=5, pady=5)
        self.audio_browse_out_pixels_button = ttk.Button(
            self.audio_hide_frame, text="Browse", bootstyle=PRIMARY, command=self.browse_out_samples
        )
        self.audio_browse_out_pixels_button.grid(row=3, column=2, padx=5, pady=5)

        # Submit button.
        self.audio_hide_submit_button = ttk.Button(
            self.audio_hide_frame, text="Hide Message", bootstyle=SUCCESS, command=self.hide_message_in_audio
        )
        self.audio_hide_submit_button.grid(row=4, column=1, pady=10)

        # Status label.
        self.audio_hide_status_label = ttk.Label(self.audio_hide_frame, text="")
        self.audio_hide_status_label.grid(row=5, column=0, columnspan=3, pady=5)

    def browse_stego_audio(self):
        filetypes = (("WAV files", "*.wav"), ("All files", "*.*"))
        filename = fd.askopenfilename(title="Select WAV Audio File", initialdir=os.getcwd(), filetypes=filetypes)
        if filename:
            self.stego_audio_var.set(filename)

    def browse_out_stego_audio(self):
        filename = fd.asksaveasfilename(title="Output Audio File", initialdir=os.getcwd(),
                                         defaultextension=".wav", filetypes=(("WAV files", "*.wav"), ("All files", "*.*")))
        if filename:
            self.out_stego_audio_var.set(filename)

    def browse_out_samples(self):
        filename = fd.asksaveasfilename(title="Output Sample Numbers File", initialdir=os.getcwd(),
                                         defaultextension=".txt", filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
        if filename:
            self.audio_out_samples_var.set(filename)

    def hide_message_in_audio(self):
        try:
            # Call the function to hide the message in the audio
            Steganography.hide_message_in_audio(
                wav_audio_file_path=self.stego_audio_var.get(),
                secret_message=self.audio_stego_text_message.get(),
                output_audio_file_path=self.out_stego_audio_var.get(),
                sample_numbers_file_path=self.audio_out_samples_var.get()
            )
            self.audio_hide_status_label.config(text="Message hidden successfully.", bootstyle="success")
        except Exception as e:
            self.audio_hide_status_label.config(text=f"Error: {str(e)}", bootstyle="danger")

    # --------------- Audio Steganography Extract Tab ---------------
    def build_audio_steganography_extract_form(self):
        self.audio_extract_frame = ttk.Frame(self.notebook, padding=20)
        self.notebook.add(self.audio_extract_frame, text="Steganography (audio) - Extract")

        # WAV audio file selection.
        ttk.Label(self.audio_extract_frame, text="Select WAV Audio File:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.extract_audio_var = ttk.StringVar()
        self.extract_audio_entry = ttk.Entry(self.audio_extract_frame, textvariable=self.extract_audio_var, width=40)
        self.extract_audio_entry.grid(row=0, column=1, padx=5, pady=5)
        self.browse_extract_audio_button = ttk.Button(
            self.audio_extract_frame, text="Browse", bootstyle=PRIMARY, command=self.browse_extract_audio
        )
        self.browse_extract_audio_button.grid(row=0, column=2, padx=5, pady=5)

        # Sample numbers file selection.
        ttk.Label(self.audio_extract_frame, text="Sample Numbers File:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.extract_samples_var = ttk.StringVar()
        self.extract_samples_entry = ttk.Entry(self.audio_extract_frame, textvariable=self.extract_samples_var, width=40)
        self.extract_samples_entry.grid(row=1, column=1, padx=5, pady=5)
        self.browse_extract_samples_button = ttk.Button(
            self.audio_extract_frame, text="Browse", bootstyle=PRIMARY, command=self.browse_extract_samples
        )
        self.browse_extract_samples_button.grid(row=1, column=2, padx=5, pady=5)

        # Hidden message output.
        ttk.Label(self.audio_extract_frame, text="Hidden Message:").grid(row=2, column=0, sticky='w', padx=5, pady=5)
        self.audio_hidden_message_text = ttk.Entry(self.audio_extract_frame, width=53)
        self.audio_hidden_message_text.grid(row=2, column=1, padx=5, pady=5, columnspan=2)

        # Submit button.
        self.audio_extract_submit_button = ttk.Button(
            self.audio_extract_frame, text="Extract Message", bootstyle=SUCCESS, command=self.extract_message_from_audio
        )
        self.audio_extract_submit_button.grid(row=3, column=1, pady=10)

        # Status label.
        self.audio_extract_status_label = ttk.Label(self.audio_extract_frame, text="")
        self.audio_extract_status_label.grid(row=4, column=0, columnspan=3, pady=5)

    def browse_extract_audio(self):
        filetypes = (("WAV files", "*.wav"), ("All files", "*.*"))
        filename = fd.askopenfilename(title="Select WAV Audio File", initialdir=os.getcwd(), filetypes=filetypes)
        if filename:
            self.extract_audio_var.set(filename)

    def browse_extract_samples(self):
        filetypes = (("Text files", "*.txt"), ("All files", "*.*"))
        filename = fd.askopenfilename(title="Select Sample Numbers File", initialdir=os.getcwd(), filetypes=filetypes)
        if filename:
            self.extract_samples_var.set(filename)

    def extract_message_from_audio(self):
        try:
            # Call the extract function with the audio path and samples indices file.
            hidden_message = Steganography.extract_message_from_audio(
                wav_audio_file_path=self.extract_audio_var.get(),
                sample_numbers_file_path=self.extract_samples_var.get()
            )
            # Display the hidden message in the entry widget.
            self.audio_hidden_message_text.delete(0, 'end')
            self.audio_hidden_message_text.insert(0, hidden_message)
            self.audio_extract_status_label.config(text="Message extracted successfully.", bootstyle="success")
        except Exception as e:
            self.audio_extract_status_label.config(text=f"Error: {str(e)}", bootstyle="danger")

    # --------------- Language Evaluation Tab ---------------
    def build_language_evaluation_form(self):
        self.language_frame = ttk.Frame(self.notebook, padding=20)
        self.notebook.add(self.language_frame, text="Language evaluation")

        # Language characters list file input
        ttk.Label(self.language_frame, text="Language Characters List File:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.language_file_var = ttk.StringVar()
        self.language_file_entry = ttk.Entry(self.language_frame, textvariable=self.language_file_var, width=40)
        self.language_file_entry.grid(row=1, column=1, padx=5, pady=5)
        self.browse_language_file = ttk.Button(
            self.language_frame, text="Browse", bootstyle=PRIMARY, command=self.browse_language_list_file
        )
        self.browse_language_file.grid(row=1, column=2, padx=5, pady=5)

        # Langugage evaluation button.
        self.evaluate_language_button = ttk.Button(
            self.language_frame, text="Evaluate", bootstyle=SUCCESS, command=self.evaluate_language_file
        )
        self.evaluate_language_button.grid(row=2, column=1, pady=10)

        # Status label.
        self.language_status_label = ttk.Label(self.language_frame, text="")
        self.language_status_label.grid(row=3, column=0, columnspan=3, pady=5)

    def browse_language_list_file(self):
        filetypes = (("JSON files", "*.json"), ("All files", "*.*"))
        filename = fd.askopenfilename(title="Select Language Characters List", initialdir=os.getcwd(), filetypes=filetypes)
        if filename:
            self.language_file_var.set(filename)

    def evaluate_language_file(self):
        language_file = self.language_file_var.get()
        if not language_file:
            self.comp_status_label.config(text="Please select a language characters list JSON file!", bootstyle="danger")
            return
        try:
            is_valid_code = LanguageEvaluator.evaluate_language(language_file)

            if is_valid_code:
                self.language_status_label.config(
                    text=f"The language is a valid code!",
                    bootstyle="success"
                )
            else:
                self.language_status_label.config(
                    text=f"The language is not a valid code!",
                    bootstyle="danger"
                )
        except Exception as e:
            self.language_status_label.config(text=f"Error: {str(e)}", bootstyle="danger")


if __name__ == "__main__":
    app = CompressionApp()
    app.mainloop()
