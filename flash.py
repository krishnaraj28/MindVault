import tkinter as tk
from tkinter import messagebox,simpledialog,scrolledtext,ttk
import random
import json
import os
from PIL import Image, ImageTk  # Import Pillow for image handling

FLASHCARD_FILE = "flashcard.json"

# Flashcards dictionary
flashcards = {}

# Color mapping for each flashcard topic
flashcard_colors = {}


def load_flashcards():
    """Load flashcards from a file."""
    global flashcards, flashcard_colors, flashcard_keys
    if os.path.exists(FLASHCARD_FILE):
        try:
            with open(FLASHCARD_FILE, "r") as file:
                data = json.load(file)
                flashcards = data.get("flashcards", {})
                flashcard_colors = data.get("flashcard_colors", {})
                flashcard_keys = list(flashcards.keys())
                if not flashcards:  # If the flashcards are empty, load defaults
                    load_default_flashcards()
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Error loading flashcards from file.")
    else:
        load_default_flashcards()

def load_default_flashcards():
    """Load predefined Python flashcards if the file is empty or missing."""
    global flashcards, flashcard_colors, flashcard_keys
    # Predefined Python flashcards
    default_flashcards = {
        "Python": "A high-level programming language used for general-purpose programming.",
        "Variable": "A symbolic name for data stored in memory.",
        "Function": "A block of code that only runs when it is called.",
        "List": "A collection of items in a particular order, denoted by square brackets.",
        "Loop": "A programming construct that repeats a block of code multiple times.",
        "Dictionary": "A collection of key-value pairs, denoted by curly braces.",
        "Class": "A blueprint for creating objects, providing initial values for state, and implementations of behavior."
    }
    
    flashcards = default_flashcards
    flashcard_colors = {topic: generate_random_color() for topic in default_flashcards}
    flashcard_keys = list(flashcards.keys())
    save_flashcards()  # Save the default flashcards to the file

def save_flashcards():
    """Save flashcards to a file."""
    data = {
        "flashcards": flashcards,
        "flashcard_colors": flashcard_colors
    }
    with open(FLASHCARD_FILE, "w") as file:
        json.dump(data, file)

flashcard_keys = list(flashcards.keys())
current_flashcard_index = 0
showing_definition = False  # Toggle between topic and definition

def open_flashcard_window():
    """Open the flashcard window."""
    home_window.destroy()  # Close the home window
    global window, topic_label, definition_label, flashcard_frame, flip_button
    window = tk.Tk()
    window.title("Flashcard App")
    window.state("zoomed")  # Resized window for larger flashcards


    
    # Frame for buttons
    button_frame = tk.Frame(window)
    button_frame.pack(pady=10)

    add_button = tk.Button(button_frame, text="Add", command=add_flashcard, font=("Helvetica", 14), bg="#4CAF50", fg="white")
    button_style = {"relief": "groove","borderwidth":6}
    add_button.configure(**button_style)
    add_button.pack(side="left", padx=4)

    delete_button = tk.Button(button_frame, text="Delete", command=delete_flashcard, font=("Helvetica", 14), bg="#f44336", fg="white")
    button_style = {"relief": "groove","borderwidth":6}
    delete_button.configure(**button_style)
    delete_button.pack(side="left", padx=4)

    edit_button = tk.Button(button_frame, text="Edit", command=edit_flashcard, font=("Helvetica", 14), bg="#FF9800", fg="white")
    button_style = {"relief": "groove","borderwidth":6}
    edit_button.configure(**button_style)
    edit_button.pack(side="left", padx=4)

    review_button = tk.Button(button_frame, text="Review", command=review_flashcards, font=("Helvetica", 14), bg="#2196F3", fg="white")
    button_style = {"relief": "groove","borderwidth":6}
    review_button.configure(**button_style)
    review_button.pack(side="left", padx=4)

    # Flashcard frame (Resized)
    flashcard_frame = tk.Frame(window,
     width=500, height=400, bg="white", relief="raised", borderwidth=20, bd=2
    )
    flashcard_frame.pack_propagate(False)  # Prevent resizing
    flashcard_frame.pack(expand=True, pady=30)  # Adjusted padding

    
    topic_label = tk.Label(flashcard_frame, text="", font=("Arial", 18, "bold"), bg="white", fg="black", wraplength=480)
    topic_label.place(relx=0.5, rely=0.4, anchor="center")

    definition_label = tk.Label(flashcard_frame, text="", font=("Arial", 14), bg="white", fg="black", wraplength=480, justify="center")
    definition_label.place(relx=0.5, rely=0.6, anchor="center")


    flip_button = tk.Button(window, text="Flip", command=flip_flashcard, font=("Helvetica", 14), bg="#673AB7", fg="white")
    button_style = {"relief": "groove","borderwidth":6}
    flip_button.configure(**button_style)
    flip_button.pack(pady=10)

    navigation_frame = tk.Frame(window)
    navigation_frame.pack(pady=10)

    prev_button = tk.Button(navigation_frame, text="Previous", command=show_previous_flashcard, font=("Helvetica", 14), bg="#FF9800", fg="white")
    button_style = {"relief": "groove","borderwidth":6}
    prev_button.configure(**button_style)
    prev_button.pack(side="left", padx=4)

    next_button = tk.Button(navigation_frame, text="Next", command=show_next_flashcard, font=("Helvetica", 14), bg="#4CAF50", fg="white")
    button_style = {"relief": "groove","borderwidth":6}
    next_button.configure(**button_style)
    next_button.pack(side="left", padx=4)

    update_flashcard()
    window.mainloop()



def update_flashcard():
    """Update the flashcard content in the current window."""
    global showing_definition
    if not flashcard_keys:
        topic_label.config(text="No Flashcards", bg="#FFFFFF", fg="black")
        definition_label.config(text="", bg="#FFFFFF", fg="black")
        return

    topic = flashcard_keys[current_flashcard_index]
    if showing_definition:
        content = flashcards[topic]
    else:
        content = topic

    color = flashcard_colors.get(topic, "#FFFFFF")
    flashcard_frame.config(bg=color)
    topic_label.config(text=content, bg=color, fg="black")
    definition_label.config(bg=color, fg="black")

def show_next_flashcard():
    """Show the next flashcard."""
    global current_flashcard_index
    if current_flashcard_index < len(flashcard_keys) - 1:
        current_flashcard_index += 1
        update_flashcard()

def show_previous_flashcard():
    """Show the previous flashcard."""
    global current_flashcard_index
    if current_flashcard_index > 0:
        current_flashcard_index -= 1
        update_flashcard()

def flip_flashcard():
    """Flip the flashcard to show topic/definition."""
    global showing_definition
    showing_definition = not showing_definition
    update_flashcard()

def generate_random_color():
    """Generate a random color in hex format."""
    return "#{:02x}{:02x}{:02x}".format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def add_flashcard():
    """Add a new flashcard with a random color."""
    topic = simpledialog.askstring("Add Flashcard", "Enter the topic:")
    if not topic:
        messagebox.showerror("Error", "You didn't enter a topic. Please try again.")
        return
    definition = simpledialog.askstring("Add Flashcard", f"Enter the definition for {topic}:")
    if not definition:
        messagebox.showerror("Error", f"You didn't enter definition for '{topic}'. Please try again.")
        return
    if definition:
        color = generate_random_color()
        flashcards[topic] = definition
        flashcard_keys.append(topic)
        flashcard_colors[topic] = color
        save_flashcards()
        messagebox.showinfo("Flashcard Added", f"Flashcard for '{topic}' added successfully.")

def delete_flashcard():
    """Delete a selected flashcard."""
    global current_flashcard_index
    if not flashcard_keys:
        messagebox.showerror("Error", "No flashcards to delete.")
        return
    topic = flashcard_keys[current_flashcard_index]
    if messagebox.askyesno("Delete Flashcard", f"Are you sure you want to delete '{topic}'?"):
        del flashcards[topic]
        flashcard_colors.pop(topic, None)
        flashcard_keys.remove(topic)
        if current_flashcard_index >= len(flashcard_keys):
            current_flashcard_index -= 1
        save_flashcards()
        update_flashcard()

def edit_flashcard():
    """Edit an existing flashcard."""
    if not flashcard_keys:
        messagebox.showerror("Error", "No flashcards to edit.")
        return
    topic = flashcard_keys[current_flashcard_index]
    new_definition = simpledialog.askstring("Edit Flashcard", f"Enter the new definition for '{topic}':")
    if new_definition:
        flashcards[topic] = new_definition
        save_flashcards()
        messagebox.showinfo("Flashcard Edited", f"Flashcard for '{topic}' updated successfully.")
        update_flashcard()
def review_flashcards():
    """Review all flashcards with uniformly sized boxes arranged horizontally."""
    review_window = tk.Toplevel(window)
    review_window.title("Review Flashcards")
    review_window.geometry("1920x1080")  # Set to Full HD resolution

    # Create a Canvas for scrolling
    canvas = tk.Canvas(review_window)
    canvas.pack(side="left", fill="both", expand=True)

    # Add a vertical scrollbar linked to the canvas
    scrollbar = tk.Scrollbar(review_window, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    canvas.config(yscrollcommand=scrollbar.set)

    # Create a frame inside the canvas for the flashcards
    review_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=review_frame, anchor="nw")

    # Flashcard configuration
    flashcard_size = 150  # Fixed size for both width and height of the flashcards
    padding = 7  # Padding between flashcards
    max_per_row = 9  # Maximum number of flashcards per row

    row = 0  # Row counter to track which row we're placing flashcards in
    col = 0  # Column counter to track where each flashcard goes in the row

    for topic, definition in flashcards.items():
        # Create a frame for each flashcard
        flashcard = tk.Frame(
            review_frame,
            bg=flashcard_colors.get(topic, "#FFFFFF"),
            width=flashcard_size,
            height=flashcard_size,
            padx=padding,
            pady=padding,
            relief="solid",
            bd=1,
        )
        
        # Using grid to position flashcards in a consistent layout
        flashcard.grid(row=row, column=col, padx=padding, pady=padding, sticky="nsew")  # Use grid layout

        flashcard.grid_propagate(False)  # Prevent resizing of the frame to fit its content

        # Add topic and definition labels to the flashcard
        tk.Label(flashcard, text=topic, font=("Arial", 10, "bold"), bg=flashcard_colors.get(topic, "#FFFFFF")).pack()
        tk.Label(flashcard, text=definition, wraplength=150, justify="left", bg=flashcard_colors.get(topic, "#FFFFFF")).pack()

        # Update column and row counters
        col += 1  # Move to the next column
        if col >= max_per_row:  # If the row is filled, move to the next row
            col = 0
            row += 1

    # Make sure that the canvas scrolls properly
    review_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

    # Update the grid weights to make the flashcards resize proportionally
    for i in range(max_per_row):
        review_frame.grid_columnconfigure(i, weight=1, minsize=flashcard_size)
    for i in range(row + 1):
        review_frame.grid_rowconfigure(i, weight=1, minsize=flashcard_size)
                                       
# Home window setup
home_window = tk.Tk()
home_window.title("Flashcard App")
screen_width=home_window.winfo_screenwidth()
screen_height=home_window.winfo_screenheight()
home_window.geometry(f"{screen_width}x{screen_height}+0+0")
home_window.resizable(True,True)


background_image_path = r"C:\python\flashcard.jpg"  # Correct way to specify the file path
if os.path.exists(background_image_path):  # Use the correct variable name here
    background_image = Image.open(background_image_path)  # Open the image using PIL
    background_image = background_image.resize((1600, 800))  # Resize to fit the window
    bg_photo = ImageTk.PhotoImage(background_image)  # Create a PhotoImage object for Tkinter

     # Create a label to display the background image
    bg_label = tk.Label(home_window, image=bg_photo)
    bg_label.place(relwidth=1, relheight=1)  # Cover the entire window
    bg_label.image = bg_photo  # Keep a reference to the image
else:
    messagebox.showerror("Error", f"Background image not found at {background_image_path}")
        

home_window.configure(bg="#f0f0f0") 

    # Create a custom style for the labels
style = ttk.Style()
style.configure("Title.TLabel", font=("Comic Sans MS", 24, "italic"), foreground="#333333") 
style.configure("Subtitle.TLabel", font=("Roboto", 18, "bold"), foreground="#666666") 

    # Create the title label
title_label = ttk.Label(home_window, text="MindVault", style="Title.TLabel")
title_label.pack(pady=(350,20))  

    # Create the subtitle label
subtitle_label = ttk.Label(home_window, text="Python-Based Flashcard System", style="Subtitle.TLabel")
subtitle_label.pack()


start_button = tk.Button(home_window, text="Start Flashcards", command=open_flashcard_window, font=("Roboto",14,"bold"),bg="#2196F3",fg="white")
button_style = {"relief": "sunken","borderwidth":6}
start_button.configure(**button_style)
start_button.pack(pady=20)

load_flashcards()
home_window.mainloop()