import os
import tkinter.filedialog as fd

import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from huffman.Huffman import Huffman


class CompressionApp(ttk.Window):
    def __init__(self, *args, **kwargs):
        # Initialize the window with a modern theme.
        super().__init__(themename="litera", *args, **kwargs)
        self.title("Huffman Compressor / Decompressor")
        self.geometry("600x300")

        # Use a Notebook widget to create two tabs.
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill='both', expand=True)

        # Build the Compression form.
        self.build_compression_form()

        # Build the Decompression form.
        self.build_decompression_form()

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
        # Use asksaveasfilename to get a file path for the decompressed file.
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


if __name__ == "__main__":
    app = CompressionApp()
    app.mainloop()
