import tksheet
import tkinter as tk

root = tk.Tk()
sheet = tksheet.Sheet(root)
print("--- TKSHEET METHODS ---")
for method in dir(sheet):
    if not method.startswith("_"):
        print(method)
root.destroy()
