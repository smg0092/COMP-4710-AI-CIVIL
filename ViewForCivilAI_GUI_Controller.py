import ViewForCivilAI_GUI_support as gui_support
import ViewForCivilAI_GUI as gui_layout
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import matlab.engine
import os
import threading

current_folder_files = []
current_index = 0
file_list_frame = None
_w = None  # Global GUI instance
run_button = None

# Scrollable frame for file list
class ScrollableFileList(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.canvas = tk.Canvas(self, borderwidth=0)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
def on_left_click():
    global current_index
    if current_folder_files:
        current_index = max(0, current_index - 1)
        show_image(current_folder_files[current_index])

def on_right_click():
    global current_index
    if current_folder_files:
        current_index = min(len(current_folder_files) - 1, current_index + 1)
        show_image(current_folder_files[current_index])

def show_image(image_path):
    frame = _w.get_pictures_from_folder_frame()
    for widget in frame.winfo_children():
        widget.destroy()

    def display_resized_image(event=None):
        try:
            img = Image.open(image_path)

            # Get frame dimensions (after it's laid out)
            width = frame.winfo_width()
            height = frame.winfo_height()

            if width > 1 and height > 1:  # Avoid weird 1x1 default size
                resized = img.resize((width, height), Image.LANCZOS)
                photo = ImageTk.PhotoImage(resized)

                label.config(image=photo)
                label.image = photo
            # Damage analysis on original (not resized)
            original_img = Image.open(image_path).convert("RGB")
            pixels = list(original_img.getdata())
            red = (250, 50, 83)
            blue = (51, 221, 255)
            red_count = sum(1 for px in pixels if px == red)
            blue_count = sum(1 for px in pixels if px == blue)
            total = red_count + blue_count
            percent = (red_count / total * 100) if total > 0 else 0
            _w.get_actual_percentage_label().config(text=f"{percent:.2f}%")

        except Exception as e:
            print(f"Failed to display image {image_path}: {e}")

    # Placeholder label for image
    label = tk.Label(frame)
    label.pack(fill="both", expand=True)

    # Initial resize (delayed in case frame size isn't available yet)
    frame.after(10, display_resized_image)

    # Bind to resize event
    frame.bind("<Configure>", display_resized_image)

    # Add image name below
    filename = tk.Label(frame, text=os.path.basename(image_path))
    filename.pack()

def on_folder_label_click(event):
    global current_folder_files, current_index, file_list_frame, run_button

    folder = filedialog.askdirectory()
    if not folder:
        return

    current_folder_files = [
        os.path.join(folder, f)
        for f in os.listdir(folder)
        if f.lower().endswith(('.png', '.jpg', '.jpeg'))
    ]
    current_folder_files.sort()
    current_index = 0

    folder_frame = _w.get_folder_frame()

    # Destroy old frame if it exists
    if file_list_frame:
        file_list_frame.destroy()

    # Create a new scrollable canvas area inside FolderFrame
    container = tk.Frame(folder_frame)
    container.place(relx=0.02, rely=0.05, relwidth=0.95, relheight=0.9)  # under Label8

    canvas = tk.Canvas(container)
    scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
    scroll_frame = tk.Frame(canvas)

    scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    file_list_frame = container  # Save reference

    for file_path in current_folder_files:
        btn = tk.Button(scroll_frame, text=os.path.basename(file_path), anchor="w",
                        command=lambda p=file_path: show_image(p))
        btn.pack(fill="x", padx=4, pady=2)

    if current_folder_files:
        show_image(current_folder_files[0])


    # Add Run Prediction button next to HISTORY label
    if not run_button:
        run_button = tk.Button(_w.get_top(), text="Choose Output Folder and Run Prediction", command=lambda: run_prediction(folder))
        run_button.place(relx=0.85, rely=0.035, width=250, height=25)

def run_prediction(input_folder):
    output_folder = filedialog.askdirectory(title="Select Output Folder")
    if not output_folder:
        return

    # 🧠 Step 1: Create popup
    popup = tk.Toplevel(_w.get_top())
    popup.title("Please wait")
    popup.geometry("300x100")
    popup.transient(_w.get_top())  # Tie to main window
    popup.grab_set()  # Make it modal

    label = tk.Label(popup, text="Running prediction...\nPlease wait.", font=("Segoe UI", 12))
    label.pack(expand=True, padx=10, pady=20)

    def task():
        try:
            eng = matlab.engine.start_matlab()

            script_dir = os.path.dirname(os.path.abspath(__file__))
            matlab_code_path = os.path.abspath(os.path.join(script_dir, '..', 'matlab_code'))
            print(f"Adding MATLAB path: {matlab_code_path}")
            eng.addpath(matlab_code_path, nargout=0)

            input_path = os.path.join(input_folder, "*.jpg").replace("\\", "/")
            output_path = output_folder.replace("\\", "/")

            eng.RC_predictionFunction(input_path, output_path, nargout=0)

            # ✅ Step 2: Close popup & update display
            _w.get_top().after(0, popup.destroy)
            _w.get_top().after(0, lambda: update_display_from_folder(output_folder))
            _w.get_top().after(0, lambda: messagebox.showinfo("Success", "RC Prediction Completed."))
        except Exception as e:
            _w.get_top().after(0, popup.destroy)
            _w.get_top().after(0, lambda: messagebox.showerror("Error", f"An error occurred:\n{e}"))

    threading.Thread(target=task).start()

def update_display_from_folder(folder):
    global current_folder_files, current_index, file_list_frame
    current_folder_files = [os.path.join(folder, f) for f in os.listdir(folder)
                            if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    current_folder_files.sort()
    current_index = 0

    folder_frame = _w.get_folder_frame()
    for widget in folder_frame.winfo_children():
        if widget != _w.get_label8():
            widget.destroy()

    file_list_frame = ScrollableFileList(folder_frame)
    file_list_frame.pack(fill="both", expand=True, padx=5, pady=(25, 5))

    for file_path in current_folder_files:
        btn = tk.Button(file_list_frame.scrollable_frame, text=os.path.basename(file_path), anchor="w",
                        command=lambda p=file_path: show_image(p))
        btn.pack(fill="x", padx=5, pady=2)

    if current_folder_files:
        show_image(current_folder_files[0])

def main():
    global _w
    gui_support.root = gui_support.tk.Tk()
    gui_support.root.title("Civil AI Dummy Controller")
    gui_support._top1 = gui_support.root

    _w = gui_layout.Toplevel1(gui_support.root)

    _w.get_move_picture_left_button().config(
        text="◀",  # or use "<" if you prefer
        font=("Segoe UI", 14, "bold"),
        command=on_left_click
    )

    _w.get_move_picture_right_button().config(
        text="▶",  # or use ">"
        font=("Segoe UI", 14, "bold"),
        command=on_right_click
    )

    _w.get_label8().bind("<Button-1>", on_folder_label_click)

    gui_support.root.mainloop()

if __name__ == "__main__":
    main()
