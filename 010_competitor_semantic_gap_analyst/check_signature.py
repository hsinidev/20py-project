import tksheet
import tkinter as tk
import inspect

root = tk.Tk()
sheet = tksheet.Sheet(root)
print("--- insert_column Signature ---")
print(inspect.signature(sheet.insert_column))
print("--- insert_row Signature ---")
print(inspect.signature(sheet.insert_row))
root.destroy()
