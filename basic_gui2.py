import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import matlab.engine
import os
import glob

class RCApp:
    def __init__(self, root):
        self.root = root
        self.root.title("RC Prediction Runner")
        self.root.geometry("800x600")

        self.input_folder = ""
        self.output_folder = ""
        self.thumbnails = []  # Store image references

        # === Top container ===
        top_frame = tk.Frame(self.root)
        top_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        # === Left buttons ===
        side_frame = tk.Frame(top_frame)
        side_frame.pack(side=tk.LEFT)

        self.input_button = tk.Button(side_frame, text="Choose Input Folder", command=self.choose_input_folder)
        self.input_button.pack(pady=5)

        self.output_button = tk.Button(side_frame, text="Choose Output Folder", command=self.choose_output_folder)
        self.output_button.pack(pady=5)

        # === Right Run Button ===
        self.run_button = tk.Button(top_frame, text="Run Prediction", command=self.run_prediction, width=20, height=3)
        self.run_button.pack(side=tk.RIGHT, padx=20)

        # === Bottom: Output Viewer (images) ===
        bottom_frame = tk.LabelFrame(self.root, text="Output Folder Images")
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Scrollable Canvas for images
        self.canvas = tk.Canvas(bottom_frame)
        self.scrollbar = tk.Scrollbar(bottom_frame, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.image_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.image_frame, anchor="nw")
        self.image_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

    def choose_input_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.input_folder = folder
            print("Input folder set to:", self.input_folder)

    def choose_output_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.output_folder = folder
            print("Output folder set to:", self.output_folder)
            self.update_output_display()

    def update_output_display(self):
        # Clear previous thumbnails
        for widget in self.image_frame.winfo_children():
            widget.destroy()
        self.thumbnails.clear()

        if self.output_folder:
            jpg_files = sorted(glob.glob(os.path.join(self.output_folder, "*.png")))
            if jpg_files:
                for i, filepath in enumerate(jpg_files):
                    try:
                        img = Image.open(filepath)
                        img.thumbnail((100, 100))
                        photo = ImageTk.PhotoImage(img)
                        self.thumbnails.append(photo)  # Store reference

                        frame = tk.Frame(self.image_frame, padx=5, pady=5)
                        frame.grid(row=i // 5, column=i % 5)

                        label_img = tk.Label(frame, image=photo)
                        label_img.pack()

                        label_name = tk.Label(frame, text=os.path.basename(filepath), wraplength=100)
                        label_name.pack()
                    except Exception as e:
                        print(f"Error loading {filepath}: {e}")
            else:
                tk.Label(self.image_frame, text="No .png files found.").pack()

    def run_prediction(self):
        if not self.input_folder or not self.output_folder:
            messagebox.showerror("Error", "Please select both input and output folders.")
            return

        try:
            eng = matlab.engine.start_matlab()
            eng.addpath(rf"C:\Users\Sgadz\OneDrive\AUBURN UNIV\Senior (2024 Fall - 2025 Spring)\COMP-4710\Spring 2025")

            input_path = os.path.join(self.input_folder, "*.jpg")
            eng.RC_predictionFunction(input_path, self.output_folder, nargout=0)

            self.update_output_display()
            messagebox.showinfo("Success", "RC Prediction Completed.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{e}")

# Run GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = RCApp(root)
    root.mainloop()
