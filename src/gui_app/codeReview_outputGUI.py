import tkinter as tk

# Create a new instance of Tkinter
root = tk.Tk()

# Set the title of the window
root.title("Code Review")

def tkinterDisplay(codellama_output):
   # Create a new instance of Tkinter's Text widget to display the code review results
    text = tk.Text(root, height=20, width=80)
    text.pack()

    # Set the text of the Text widget to the output of CodelLLama
    text.insert("end", codellama_output)

# Start the GUI event loop
root.mainloop()

