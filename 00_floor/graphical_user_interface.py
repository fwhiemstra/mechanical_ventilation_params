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


def graphical_user_interface():
    """ Returns:
    - PARAMS: parameters from the entries en selections of the GUI
    - input_filename: name of the chosen input file
    - output_filename: name of the chosen output file (when existing file option is chosen)
    """
    # Start tkinter module
    root = tk.Tk()

    # Get input and output file names from selection buttons
    input_filename = []
    output_filename = []

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

    def output_():
        filename = filedialog.askopenfilename(title="Select file",
                                              filetypes=(("executables", "*.xlsx"),
                                                         ("all files", "*.*")))
        output_filename.append(filename)
        if filename == '' or filename == []:  # if entry canceled or left empty
            tk.messagebox.showerror(
                title="Input Error", message="Output file is missing. Please try again.")
            output_filename.clear()  # clear the list
            filename.remove(0)  # remove answer from tkinter
        else:
            print(filename)
            for name in output_filename:
                label = tk.Label(frame, text=name, bg="#009fbd")
                label.pack()

        # Get parameters from entries and selections and create a list
    params = []

    def get_variables():
        # Give error and do not run the script when mandatory entries are missing
        if patient_number_entry.get() == '':
            tk.messagebox.showerror(
                title="Input Error", message="Patient number is missing. Please try again.")
        else:
            params.append(patient_number_entry.get())
            if outputfile_var.get() != OUTPUT_FILE.EXISTING_FILE and \
                outputfile_var.get() != OUTPUT_FILE.NEW_FILE:
                tk.messagebox.showerror(
                    title="Input Error", message="Output file is missing. Please try again.")
                params.clear()  # clear list if entry is missing
            elif outputfile_var.get() == OUTPUT_FILE.EXISTING_FILE:
                if output_filename == []:
                    tk.messagebox.showerror(
                        title="Input Error", message="Existing output file is not chosen. Please try again.")
                    output_filename.clear()
                    params.clear()  # clear list if entry is missing
                else:
                    params.append(outputfile_var.get())
                    params.append(new_outputfile_entry.get())
                    root.destroy()
            elif outputfile_var.get() == OUTPUT_FILE.NEW_FILE:
                if new_outputfile_entry.get() == '':
                    tk.messagebox.showerror(
                        title="Input Error", message="New output file name is missing. Please try again.")
                    output_filename.clear()
                    params.clear()  # clear list if entry is missing
                else:
                    params.append(outputfile_var.get())
                    params.append(new_outputfile_entry.get())
                    root.destroy()

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

    # patient number entry box
    patient_number = tk.Label(frame, text="Patient number * :", fg="#009fbd")
    patient_number.pack()
    patient_number_entry = tk.Entry(frame, bd=5)
    patient_number_entry.pack()

    # input file selection
    inputfile_title = tk.Label(frame, text="Select input file * :", fg="#009fbd")
    inputfile_title.pack()
    inputfile = tk.Button(frame, text="Select input file", padx=10, pady=5, fg="white",
                        bg="#003c7d", command=input_)
    inputfile.pack()

    # output file selection
    outputfile_title = tk.Label(frame, text="Select output file * :", fg="#009fbd")
    outputfile_title.pack()
    outputfile_var = tk.IntVar()
    existing_outputfile = tk.Radiobutton(frame, text="Select existing output file:",
                                        variable=outputfile_var, value=OUTPUT_FILE.EXISTING_FILE, bg="white")
    existing_outputfile.pack()
    outputfile = tk.Button(frame, text="Select output file", padx=10, pady=5, fg="white",
                         bg="#003c7d", command=output_)
    outputfile.pack()
    new_outputfile = tk.Radiobutton(frame, text="Create new output file, with name:",
                                    variable=outputfile_var, value=OUTPUT_FILE.NEW_FILE, bg="white")
    new_outputfile.pack()
    new_outputfile_entry = tk.Entry(frame, bd=5, bg="white")
    new_outputfile_entry.pack()

    # Exit GUI and run code
    runcode = tk.Button(frame, text="Run power calculator", padx=10, pady=5,
                        fg="white", bg="#007cc2", command=get_variables)
    runcode.pack()

    # End tkinter module
    root.mainloop()
    return params, input_filename, output_filename
