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
        #setting title
        root.title("TICKET")
        #setting window size
        width=998
        height=531
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)
        
        
        now = datetime.now()
        today = date.today()
        current_time = now.strftime("%H:%M:%S")

        GLineEdit_515=tk.Entry(root)
        GLineEdit_515["bg"] = "#ffffff"
        GLineEdit_515["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        GLineEdit_515["font"] = ft
        GLineEdit_515["fg"] = "#333333"
        GLineEdit_515["justify"] = "center"
        GLineEdit_515["text"] = "Entry"
        GLineEdit_515.delete(0, tk.END) 
        GLineEdit_515.place(x=540,y=150,width=456,height=49)

        GLineEdit_115=tk.Entry(root)
        GLineEdit_115["bg"] = "#ffffff"
        GLineEdit_115["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        GLineEdit_115["font"] = ft
        GLineEdit_115["fg"] = "#333333"
        GLineEdit_115["justify"] = "center"
        GLineEdit_115["text"] = "Entry"
        GLineEdit_115.delete(0, tk.END) 
        GLineEdit_115.place(x=0,y=240,width=449,height=49)

        GLineEdit_155=tk.Entry(root)
        GLineEdit_155["bg"] = "#ffffff"
        GLineEdit_155["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        GLineEdit_155["font"] = ft
        GLineEdit_155["fg"] = "#333333"
        GLineEdit_155["justify"] = "center"
        GLineEdit_155["text"] = 'date now'
        GLineEdit_155.delete(0, tk.END) 
        GLineEdit_155.place(x=0,y=150,width=447,height=49)

        GLineEdit_275=tk.Entry(root)
        GLineEdit_275["bg"] = "#ffffff"
        GLineEdit_275["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        GLineEdit_275["font"] = ft
        GLineEdit_275["fg"] = "#333333"
        GLineEdit_275["justify"] = "center"
        GLineEdit_275["text"] = "Entry"
        GLineEdit_275.delete(0, tk.END) 
        GLineEdit_275.place(x=540,y=240,width=456,height=49)

        GLineEdit_251=tk.Entry(root)
        GLineEdit_251["bg"] = "#ffffff"
        GLineEdit_251["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        GLineEdit_251["font"] = ft
        GLineEdit_251["fg"] = "#333333"
        GLineEdit_251["justify"] = "center"
        GLineEdit_251["text"] = "Entry"
        GLineEdit_251.delete(0, tk.END) 
        GLineEdit_251.place(x=60,y=330,width=859,height=82)

        GButton_675=tk.Button(root)
        GButton_675["bg"] = "#5fb878"
        ft = tkFont.Font(family='Times',size=10)
        GButton_675["font"] = ft
        GButton_675["fg"] = "#fbfbfb"
        GButton_675["justify"] = "center"
        GButton_675["text"] = "SUBMIT"
        GButton_675.place(x=850,y=460,width=125,height=49)
        GButton_675["command"] = self.GButton_675_command

        GButton_250=tk.Button(root)
        GButton_250["bg"] = "#ff0909"
        ft = tkFont.Font(family='Times',size=10)
        GButton_250["font"] = ft
        GButton_250["fg"] = "#ffffff"
        GButton_250["justify"] = "center"
        GButton_250["text"] = "CANCEL"
        GButton_250.place(x=700,y=460,width=124,height=50)
        GButton_250["command"] = self.GButton_250_command

        GLabel_466=tk.Label(root)
        GLabel_466["bg"] = "#fefefe"
        GLabel_466["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        GLabel_466["font"] = ft
        GLabel_466["fg"] = "#333333"
        GLabel_466["justify"] = "center"
        GLabel_466["text"] = extracted_fullname
        GLabel_466.place(x=0,y=40,width=516,height=60)

        GLabel_360=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        GLabel_360["font"] = ft
        GLabel_360["fg"] = "#333333"
        GLabel_360["justify"] = "center"
        GLabel_360["text"] = "REQUESTOR"
        GLabel_360.place(x=0,y=10,width=144,height=30)

        GLabel_447=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        GLabel_447["font"] = ft
        GLabel_447["fg"] = "#333333"
        GLabel_447["justify"] = "center"
        GLabel_447["text"] = "REMARKS"
        GLabel_447.place(x=440,y=300,width=101,height=30)

        GLabel_503=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        GLabel_503["font"] = ft
        GLabel_503["fg"] = "#333333"
        GLabel_503["justify"] = "center"
        GLabel_503["text"] = "DATE DOWN"
        GLabel_503.place(x=0,y=120,width=70,height=25)

        GLabel_990=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        GLabel_990["font"] = ft
        GLabel_990["fg"] = "#333333"
        GLabel_990["justify"] = "center"
        GLabel_990["text"] = "TIME DOWN"
        GLabel_990.place(x=920,y=120,width=70,height=25)

        GLabel_477=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        GLabel_477["font"] = ft
        GLabel_477["fg"] = "#333333"
        GLabel_477["justify"] = "center"
        GLabel_477["text"] = "MACHINE #"
        GLabel_477.place(x=0,y=210,width=70,height=25)

        GLabel_412=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        GLabel_412["font"] = ft
        GLabel_412["fg"] = "#333333"
        GLabel_412["justify"] = "center"
        GLabel_412["text"] = "DOWNTIME TYPE"
        GLabel_412.place(x=890,y=210,width=104,height=30)

    def GButton_675_command(self):
        print("command")


    def GButton_250_command(self):
        print("command")

if __name__ == "__main__":
    root = tk.Tk()
    app = RequestTicket(root)
    root.mainloop()
