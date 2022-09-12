"""
Graphical user interface (GUI)
- Requires start and duration of interval of interest

Author: Anne Meester
Date: February 2022
"""
import tkinter as tk


def determine_segment(parameters):

    segment = tk.Tk()
    print('Specify length of segment and starting time of the segment')
    param = parameters

    def get_segment():
        param.append(segment_length_entry.get())
        param.append(segment_start_entry.get())
        segment.quit()
        segment.destroy()

    # Create GUI
    canvas = tk.Canvas(segment, height=200, width=200, bg="#003c7d")
    canvas.pack()
    frame = tk.Frame(segment, bg="white")
    frame.place(relwidth=0.96, relheight=0.96, relx=0.02, rely=0.02)
    segment.title('Specify the length of the segment and the starting time')

    # segment options
    segment_length_title = tk.Label(frame, text="Segment length in MINUTES:", fg="#009fbd")
    segment_length_title.pack()
    segment_length_entry = tk.Entry(frame, bd=5, bg="white")
    segment_length_entry.pack()
    segment_start_title = tk.Label(frame, text="Starting time of segment in SECONDS:", fg="#009fbd")
    segment_start_title.pack()
    segment_start_entry = tk.Entry(frame, bd=5, bg="white")
    segment_start_entry.pack()

    # Exit GUI and run code
    submit_button = tk.Button(frame, text="OK", padx=10, pady=5,
                        fg="white", bg="#007cc2", command=get_segment)
    submit_button.pack()

    # End tkinter module
    segment.mainloop()

    return param

