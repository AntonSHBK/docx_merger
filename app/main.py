import tkinter as tk
from gui import DocxMergerGUI


def main():
    root = tk.Tk()
    app = DocxMergerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
