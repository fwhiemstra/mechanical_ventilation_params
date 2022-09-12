"""
Graphical user interface (GUI)
- input .txt file from the Hamilton C6 Mechanical Ventilator can be chosen
- existing output .xlsx file can be chosen or new file can be created
- Gives errors and doesnt run the script when mandatory entries are missing

Author: Sanne van Deelen
Date: February 2021

Modified by Bart Keulen
Date: October 2021

Modified by Anne Meester
Date: February 2022
"""
import tkinter as tk
from tkinter import filedialog, messagebox

from constants import OUTPUT_FILE


def graphical_user_interface_input_file():
    """ Returns:
    - PARAMS: parameters from the entries en selections of the GUI
    - input_filename: name of the chosen input file
    - output_filename: name of the chosen output file (when existing file option is chosen)
    """
    # Start tkinter module
    root = tk.Tk()

    # Get input and output file names from selection buttons
    input_filename = []

    def input_():
        filename = filedialog.askopenfilename(title="Select file",
                                              filetypes=(("executables", "*.txt"),
                                                         ("all files", "*.*")))
        input_filename.append(filename)
        if filename == '' or filename == []:  # if entry canceled or left empty
            tk.messagebox.showerror(
                title="Input Error", message="Input file is missing. Please try again.")
            input_filename.clear()  # clear the list
            filename.remove(0)  # remove answer from tkinter
        else:
            print(filename)
            for name in input_filename:
                label = tk.Label(frame, text=name, bg="#009fbd")
                label.pack()

    # Create background of GUI
    canvas = tk.Canvas(root, height=500, width=300, bg="#003c7d")
    canvas.pack()
    frame = tk.Frame(root, bg="white")
    frame.place(relwidth=0.96, relheight=0.96, relx=0.02, rely=0.02)

    # title of GUI
    title = tk.Label(frame, text="Power Calculator", font=('Calibri', 18, 'bold'),
                         fg='#003c7d')
    title.pack()

    # explanation of GUI
    explanation_var = tk.StringVar()
    explanation = tk.Message(frame, textvariable=explanation_var, width=600, bg="white")
    explanation_var.set("All settings with a '*' are mandatory to fill in")
    explanation.pack()

    # input file selection
    inputfile_title = tk.Label(frame, text="Select input file * :", fg="#009fbd")
    inputfile_title.pack()
    inputfile = tk.Button(frame, text="Select input file", padx=10, pady=5, fg="white",
                        bg="#003c7d", command=input_)
    inputfile.pack()

    def submitFunction():
        print('Submit button is clicked.')
        root.quit()
        root.destroy()

    # Exit GUI and run code
    runcode = tk.Button(frame, text="Submit", padx=10, pady=5,
                        fg="white", bg="#007cc2", command=submitFunction)
    runcode.pack()

    # End tkinter module
    root.mainloop()

    return input_filename
