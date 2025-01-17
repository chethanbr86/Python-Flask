import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttkb

def convert():
    return output_string.set(entry_int.get()*1.61)

#window
# window = tk.Tk()
window = ttkb.Window(themename='journal') #darkly
window.title('Test')
window.geometry('800x300')

#title
title_label = ttkb.Label(master=window, text='Miles to KM', font='Ariel 20 bold')
title_label.pack()

#input
input_frame = ttkb.Frame(master=window)
entry_int = tk.IntVar()
entry = ttkb.Entry(master=input_frame, textvariable=entry_int)
button = ttkb.Button(master=input_frame, text='Convert', command=convert)
entry.pack(side='left', padx=20)
button.pack(side='left')
input_frame.pack(pady=20)

#output
output_string = tk.StringVar()
output_label = ttkb.Label(master=window, text='Output', font='Calibre 15', textvariable=output_string)
output_label.pack(pady=5)

#run
window.mainloop()