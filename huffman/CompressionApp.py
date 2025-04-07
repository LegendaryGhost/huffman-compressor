import os
import tkinter.filedialog as fd

import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from huffman.Huffman import Huffman


class CompressionApp(ttk.Window):
    def __init__(self, *args, **kwargs):
        # Initialize the window with a modern theme (e.g., "litera")
        super().__init__(themename="litera", *args, **kwargs)
        self.title("Huffman compressor")
        self.geometry("500x200")

        # Create a frame to hold our form widgets with some padding
        self.form_frame = ttk.Frame(self, padding=20)
        self.form_frame.pack(fill='both', expand=True)

        # Label to prompt user for a file
        self.file_label = ttk.Label(self.form_frame, text="Select Text File:")
        self.file_label.grid(row=0, column=0, sticky='w', padx=5, pady=5)

        # Entry widget to display the selected file path; tied to a StringVar
        self.file_path_var = ttk.StringVar()
        self.file_entry = ttk.Entry(self.form_frame, textvariable=self.file_path_var, width=40)
        self.file_entry.grid(row=0, column=1, padx=5, pady=5)

        # Button to open a file dialog for file selection
        self.browse_button = ttk.Button(
            self.form_frame,
            text="Browse",
            bootstyle=PRIMARY,
            command=self.browse_file
        )
        self.browse_button.grid(row=0, column=2, padx=5, pady=5)

        # Button to trigger the file compression
        self.compress_button = ttk.Button(
            self.form_frame,
            text="Compress",
            bootstyle=SUCCESS,
            command=self.compress_file
        )
        self.compress_button.grid(row=1, column=1, pady=10)

        # Label to display status messages to the user
        self.status_label = ttk.Label(self.form_frame, text="")
        self.status_label.grid(row=2, column=0, columnspan=3, pady=5)

    def browse_file(self):
        # Open a file dialog limited to text files (*.txt) or all files.
        filetypes = (("Text files", "*.txt"), ("All files", "*.*"))
        filename = fd.askopenfilename(
            title="Open a file",
            initialdir=os.getcwd(),
            filetypes=filetypes
        )
        if filename:
            self.file_path_var.set(filename)

    def compress_file(self):
        # Get the file path from the entry field.
        filepath = self.file_path_var.get()
        if not filepath:
            self.status_label.config(text="Please select a file!", bootstyle="danger")
            return

        try:
            frequency_list = Huffman.count_characters(filepath)
            for letter, count in frequency_list:
                print(f"'{letter}': {count}")

            compressed_filepath = filepath + ".huff"

            # Inform the user of the successful compression.
            self.status_label.config(
                text=f"File compressed successfully:\n{compressed_filepath}",
                bootstyle="success"
            )
        except Exception as e:
            # If any error occurs, display the error message.
            self.status_label.config(text=f"Error: {str(e)}", bootstyle="danger")

if __name__ == "__main__":
    # Instantiate and run the application.
    app = CompressionApp()
    app.mainloop()
