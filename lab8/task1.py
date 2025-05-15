import tkinter as tk
from tkinter import font


def create_window_with_label():
    root = tk.Tk()
    root.title("Ivanov, Ivan")

    root.geometry("120x70")

    frame = tk.Frame(root, bg="red", bd=8, relief="solid")
    frame.pack(fill="both", expand=True)

    label_font = font.Font(family="Impact", size=25)
    label = tk.Label(frame, text="Informatika", fg="green", bg="red", font=label_font)
    label.pack(expand=True)

    root.mainloop()


create_window_with_label()


def create_window_without_label():
    root = tk.Tk()

    root.geometry("400x300")

    frame = tk.Frame(root, bg="blue", bd=8, relief="solid")
    frame.pack(fill="both", expand=True)

    root.mainloop()


create_window_without_label()


def create_window_with_relief(relief_type):
    root = tk.Tk()
    root.title(f"Relief: {relief_type}")

    root.geometry("200x150")

    frame = tk.Frame(root, bg="red", bd=8, relief=relief_type)
    frame.pack(fill="both", expand=True)

    root.mainloop()


relief_types = ["flat", "raised", "sunken", "groove", "ridge", "solid"]
for r in relief_types:
    create_window_with_relief(r)