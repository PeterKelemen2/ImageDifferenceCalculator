import tkinter as tk


def append_text(new_text):
    global manual_scroll
    # Append new text to the label
    text.set(text.get() + new_text)

    # Update the canvas scroll region
    frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

    # If manual_scroll is True, don't adjust the scrollbar position
    if not manual_scroll:
        # Set the scrollbar to the bottom
        canvas.yview_moveto(1.0)


def on_mousewheel(event):
    global manual_scroll
    # Set manual_scroll to True when the user manually scrolls
    manual_scroll = True
    # Perform the default scrolling behavior
    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


def append_text_with_delay(i):
    if i <= 200:
        append_text(f"Text nr. {i}\n")
        root.after(200, append_text_with_delay, i + 1)
        print(canvas.yview()[1])
        if float(canvas.yview()[1]) >= 0.95:
            print("Moving to bottom")
            canvas.yview_moveto(1.0)
        else:
            print("Hold")


root = tk.Tk()
root.geometry("300x200")

# Create a Canvas widget with a vertical scrollbar
canvas = tk.Canvas(root, bg="white")
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview, width=15)
scrollbar.pack(side="right", fill="y")
canvas.config(yscrollcommand=scrollbar.set)
canvas.pack(side="left", fill="both", expand=True)

# Create a frame inside the canvas to contain the label
frame = tk.Frame(canvas, bg="white")
canvas.create_window((0, 0), window=frame, anchor="nw")

# Create a label with a text variable
text = tk.StringVar()
label = tk.Label(frame, textvariable=text, bg="white", wraplength=250)
label.pack()

# Bind mouse wheel scrolling to the canvas
canvas.bind_all("<MouseWheel>", on_mousewheel)

# Bind the configure event to the canvas

# Set manual_scroll to False initially
manual_scroll = False

append_text_with_delay(1)
frame.update_idletasks()

root.mainloop()
