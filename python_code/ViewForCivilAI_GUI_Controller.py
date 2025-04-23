import ViewForCivilAI_GUI_support as gui_support
import ViewForCivilAI_GUI as gui_layout

def on_left_click():
    print("Left button clicked!")
    _w.get_label9().configure(text="Left Clicked")

def on_right_click():
    print("Right button clicked!")
    _w.get_label9().configure(text="Right Clicked")

def on_folder_label_click(event):
    print("Folder label clicked!")
    _w.get_label8().configure(text="Clicked + Add Folder")

def main():
    global _w  # GUI wrapper instance
    gui_support.root = gui_support.tk.Tk()
    gui_support.root.title("Civil AI Dummy Controller")
    gui_support._top1 = gui_support.root

    _w = gui_layout.Toplevel1(gui_support.root)

    # Example bindings
    _w.get_move_picture_left_button().config(command=on_left_click)
    _w.get_move_picture_right_button().config(command=on_right_click)

    # Bind label click
    _w.get_label8().bind("<Button-1>", on_folder_label_click)

    gui_support.root.mainloop()

if __name__ == "__main__":
    main()
