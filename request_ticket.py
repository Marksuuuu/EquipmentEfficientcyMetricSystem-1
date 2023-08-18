import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import requests
from io import BytesIO
import tkinter as tk
import tkinter.font as tkFont
import os
import csv
from tkinter import Toplevel
from datetime import datetime
from datetime import date


class RequestTicket:
    def __init__(self, root, extracted_fullname):
        self.root = root
        # setting title
        root.title("TICKET")
        # setting window size
        width = 998
        height = 531
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = "%dx%d+%d+%d" % (
            width,
            height,
            (screenwidth - width) / 2,
            (screenheight - height) / 2,
        )
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        now = datetime.now()
        today = date.today()
        current_time = now.strftime("%H:%M:%S")
        
        # ////////////////////////////////////////
        # REQUESTOR  
        lbl_Requestor = tk.Label(root)
        ft = tkFont.Font(family="Times", size=13)
        lbl_Requestor["font"] = ft
        lbl_Requestor["fg"] = "#333333"
        lbl_Requestor["justify"] = "center"
        lbl_Requestor["text"] = "REQUESTOR"
        lbl_Requestor.place(x=0, y=10, width=144, height=50)

        lbl_FullName = tk.Label(root)
        lbl_FullName["bg"] = "#fefefe"
        lbl_FullName["borderwidth"] = "1px"
        ft = tkFont.Font(family="Times", size=13)
        lbl_FullName["font"] = ft
        lbl_FullName["fg"] = "#333333"
        lbl_FullName["justify"] = "center"
        lbl_FullName["text"] = extracted_fullname
        lbl_FullName.place(x=0, y=40, width=516, height=50)

        # ////////////////////////////////////////
        # DATE NOW  
        
        lbl_DateNow = tk.Label(root)
        ft = tkFont.Font(family="Times", size=13)
        lbl_DateNow["font"] = ft
        lbl_DateNow["fg"] = "#333333"
        lbl_DateNow["justify"] = "center"
        lbl_DateNow["text"] = "DATETIME NOW"
        lbl_DateNow.place(x=20, y=120, width=100, height=50)

        # le_DateNow = tk.Entry(root)
        # le_DateNow["bg"] = "#ffffff"
        # le_DateNow["borderwidth"] = "1px"
        # ft = tkFont.Font(family="Times", size=13)
        # le_DateNow["font"] = ft
        # le_DateNow["fg"] = "#333333"
        # le_DateNow["justify"] = "center"
        # le_DateNow["text"] = "date now"
        # le_DateNow.delete(0, tk.END)
        # le_DateNow.place(x=0, y=150, width=447, height=50)


        # ////////////////////////////////////////
        # TIME DOWN 

        lbl_TimeDown = tk.Label(root)
        ft = tkFont.Font(family="Times", size=13)
        lbl_TimeDown["font"] = ft
        lbl_TimeDown["fg"] = "#333333"
        lbl_TimeDown["justify"] = "center"
        lbl_TimeDown["text"] = "TIME DOWN"
        lbl_TimeDown.place(x=900, y=120, width=300, height=50)

        # le_TimeDown = tk.Entry(root)
        # le_TimeDown["bg"] = "#ffffff"
        # le_TimeDown["borderwidth"] = "1px"
        # ft = tkFont.Font(family="Times", size=13)
        # le_TimeDown["font"] = ft
        # le_TimeDown["fg"] = "#333333"
        # le_TimeDown["justify"] = "center"
        # le_TimeDown["text"] = "Entry"
        # le_TimeDown.delete(0, tk.END)
        # le_TimeDown.place(x=540, y=150, width=456, height=50)


        # ////////////////////////////////////////
        # MACHINE NO. 

        lbl_MachineNo = tk.Label(root)
        ft = tkFont.Font(family="Times", size=13)
        lbl_MachineNo["font"] = ft
        lbl_MachineNo["fg"] = "#333333"
        lbl_MachineNo["justify"] = "center"
        lbl_MachineNo["text"] = "MACHINE #"
        lbl_MachineNo.place(x=20, y=210, width=100, height=50)

        # le_MachineNo = tk.Entry(root)
        # le_MachineNo["bg"] = "#ffffff"
        # le_MachineNo["borderwidth"] = "1px"
        # ft = tkFont.Font(family="Times", size=13)
        # le_MachineNo["font"] = ft
        # le_MachineNo["fg"] = "#333333"
        # le_MachineNo["justify"] = "center"
        # le_MachineNo["text"] = "Entry"
        # le_MachineNo.delete(0, tk.END)
        # le_MachineNo.place(x=0, y=240, width=449, height=50)

        # ////////////////////////////////////////
        # DOWNTIME TYPE  

        # le_DownTimeType = tk.Entry(root)
        # le_DownTimeType["bg"] = "#ffffff"
        # le_DownTimeType["borderwidth"] = "1px"
        # ft = tkFont.Font(family="Times", size=13)
        # le_DownTimeType["font"] = ft
        # le_DownTimeType["fg"] = "#333333"
        # le_DownTimeType["justify"] = "center"
        # le_DownTimeType["text"] = "Entry"
        # le_DownTimeType.delete(0, tk.END)
        # le_DownTimeType.place(x=540, y=240, width=456, height=50)


        lbl_DowntimeType=tk.Label(root)
        ft = tkFont.Font(family='Times',size=13)
        lbl_DowntimeType["font"] = ft
        lbl_DowntimeType["fg"] = "#333333"
        lbl_DowntimeType["justify"] = "center"
        lbl_DowntimeType["text"] = "DOWNTIME TYPE"
        lbl_DowntimeType.place(x=540,y=200,width=250,height=50)

        dropdown_var = tk.StringVar()
        # Create a dropdown widget
        dropdown = ttk.Combobox(root, textvariable=dropdown_var, state="readonly")
        dropdown["values"] = ("SETUP", "RECTIFICATION", "CONVERSION")
        dropdown.bind("<<ComboboxSelected>>", self.on_select)  # Bind a function to the selection event
        dropdown.place(x=540, y=240, width=250, height=30)

        # dropdown.pack(padx=20, pady=20)

        # ////////////////////////////////////////
        # REMARKS

        le_Remarks = tk.Entry(root)
        le_Remarks["bg"] = "#ffffff"
        le_Remarks["borderwidth"] = "1px"
        ft = tkFont.Font(family="Times", size=13)
        le_Remarks["font"] = ft
        le_Remarks["fg"] = "#333333"
        le_Remarks["justify"] = "center"
        le_Remarks["text"] = "Entry"
        le_Remarks.delete(0, tk.END)
        le_Remarks.place(x=60, y=330, width=859, height=82)


        lbl_Remarks = tk.Label(root)
        ft = tkFont.Font(family="Times", size=13)
        lbl_Remarks["font"] = ft
        lbl_Remarks["fg"] = "#333333"
        lbl_Remarks["justify"] = "center"
        lbl_Remarks["text"] = "REMARKS"
        lbl_Remarks.place(x=440, y=300, width=101, height=30)

        # ////////////////////////////////////////
        # BUTTONS

        btn_Submit = tk.Button(root)
        btn_Submit["bg"] = "#5fb878"
        ft = tkFont.Font(family="Times", size=13)
        btn_Submit["font"] = ft
        btn_Submit["fg"] = "#fbfbfb"
        btn_Submit["justify"] = "center"
        btn_Submit["text"] = "SUBMIT"
        btn_Submit.place(x=850, y=460, width=125, height=49)
        btn_Submit["command"] = self.submit

        btn_Cancel = tk.Button(root)
        btn_Cancel["bg"] = "#ff0909"
        ft = tkFont.Font(family="Times", size=13)
        btn_Cancel["font"] = ft
        btn_Cancel["fg"] = "#ffffff"
        btn_Cancel["justify"] = "center"
        btn_Cancel["text"] = "CANCEL"
        btn_Cancel.place(x=700, y=460, width=124, height=50)
        btn_Cancel["command"] = self.close_window

        # ////////////////////////////////////////
        # FUNCTIONS

    def on_select(event):
        selected_downtime_type = dropdown_var.get()
        print("Selected:", selected_downtime_type)

    def submit(self):
        print("command")

    def close_window(self):
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = RequestTicket(root)
    root.mainloop()
