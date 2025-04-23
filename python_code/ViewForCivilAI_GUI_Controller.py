import ViewForCivilAI_GUI_support as gui_support
import ViewForCivilAI_GUI as gui_layout
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import os

file_list_frame = None  # Sub-frame for scrollable list
current_folder_files = []
current_index = 0
_w = None

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

    try:
        img = Image.open(image_path)
        img.thumbnail((400, 400))
        photo = ImageTk.PhotoImage(img)

        label = tk.Label(frame, image=photo)
        label.image = photo  # Prevent garbage collection
        label.pack()

        filename_label = tk.Label(frame, text=os.path.basename(image_path))
        filename_label.pack()
    except Exception as e:
        print(f"Failed to display image {image_path}: {e}")

def on_folder_label_click(event):
    global current_folder_files, current_index, file_list_frame

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


def main():
    global _w
    gui_support.root = gui_support.tk.Tk()
    gui_support.root.title("Civil AI Dummy Controller")
    gui_support._top1 = gui_support.root

    _w = gui_layout.Toplevel1(gui_support.root)

    _w.get_move_picture_left_button().config(command=on_left_click)
    _w.get_move_picture_right_button().config(command=on_right_click)
    _w.get_label8().bind("<Button-1>", on_folder_label_click)

    gui_support.root.mainloop()

if __name__ == "__main__":
    main()
