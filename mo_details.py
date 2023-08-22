import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import requests
from io import BytesIO
import tkinter.font as tkFont
import os
import csv
import json
from tkinter import Toplevel
from tkinter import messagebox
from tkinter import simpledialog
from tkinter.messagebox import showinfo, showwarning, showerror



class MO_Details:
    def __init__(
        self,
        root,
        extracted_fullname,
        extracted_employee_no,
        extracted_photo_url,
        extracted_username,
        data,
    ):
        self.root = root
        self.extracted_employee_no = extracted_employee_no
        self.extracted_photo_url = extracted_photo_url
        self.extracted_username = extracted_username
        self.root.title("MO DETAILS")
        self.test_data = data

        root.protocol('WM_DELETE_WINDOW', self.on_close)

        # setting window size
        width = 985
        height = 482
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        alignstr = "%dx%d+%d+%d" % (
            width,
            height,
            (screenwidth - width) / 2,
            (screenheight - height) / 2,
        )
        self.root.geometry(alignstr)
        self.root.resizable(width=False, height=False)

        if self.extracted_photo_url == False or self.extracted_photo_url is None:
            image_url = "https://www.freeiconspng.com/uploads/no-image-icon-15.png"
        else:
            image_url = f"http://hris.teamglac.com/{self.extracted_photo_url}"  # Replace with your image URL

        response = requests.get(image_url)
        pil_image = Image.open(BytesIO(response.content))
        desired_width = 83
        desired_height = 60
        pil_image = pil_image.resize((desired_width, desired_height), Image.ANTIALIAS)

        self.image = ImageTk.PhotoImage(pil_image)

        self.start_btn = tk.Button(self.root)
        self.start_btn["bg"] = "#f0f0f0"
        ft = tkFont.Font(family="Times", size=12)
        self.start_btn["font"] = ft
        self.start_btn["fg"] = "#000000"
        self.start_btn["justify"] = "center"
        self.start_btn["text"] = "START"
        self.start_btn.place(x=820, y=390, width=155, height=77)
        self.start_btn["command"] = self.start_command

        self.stop_btn = tk.Button(self.root)
        self.stop_btn["bg"] = "#f0f0f0"
        ft = tkFont.Font(family="Times", size=12)
        self.stop_btn["font"] = ft
        self.stop_btn["fg"] = "#000000"
        self.stop_btn["justify"] = "center"
        self.stop_btn["text"] = "STOP"
        self.stop_btn.place(x=620, y=390, width=155, height=77)
        self.stop_btn["command"] = self.stop_command
        self.stop_btn["state"] = "disabled"

        employee_photo = tk.Label(root, image=self.image)
        employee_photo["bg"] = "#999999"
        employee_photo["font"] = ft
        employee_photo["fg"] = "#333333"
        employee_photo["justify"] = "center"
        employee_photo["text"] = "label"
        employee_photo.place(x=600, y=10, width=82, height=50)

        lbl_employee_name = tk.Label(self.root)
        lbl_employee_name["bg"] = "#fefefe"
        ft = tkFont.Font(family="Times", size=12)
        lbl_employee_name["font"] = ft
        lbl_employee_name["fg"] = "#333333"
        lbl_employee_name["justify"] = "center"
        lbl_employee_name["text"] = extracted_fullname
        lbl_employee_name.place(x=700, y=10, width=273, height=50)

        lbl_mo = tk.Label(self.root)
        lbl_mo["bg"] = "#ffffff"
        ft = tkFont.Font(family="Times", size=12)
        lbl_mo["font"] = ft
        lbl_mo["fg"] = "#333333"
        lbl_mo["justify"] = "center"
        lbl_mo["text"] = f"Main Operation: {data[1]}"
        lbl_mo.place(x=20, y=110, width=487, height=65)

        lbl_customer = tk.Label(self.root)
        lbl_customer["bg"] = "#fbfbfb"
        ft = tkFont.Font(family="Times", size=12)
        lbl_customer["font"] = ft
        lbl_customer["fg"] = "#333333"
        lbl_customer["justify"] = "center"
        lbl_customer["text"] = f"Sub-Operation: {data[2]}"
        lbl_customer.place(x=20, y=210, width=487, height=65)

        lbl_device = tk.Label(self.root)
        lbl_device["bg"] = "#ffffff"
        ft = tkFont.Font(family="Times", size=12)
        lbl_device["font"] = ft
        lbl_device["fg"] = "#333333"
        lbl_device["justify"] = "center"
        lbl_device["text"] = f"WIP Entity Name: {data[3]}"
        lbl_device.place(x=20, y=310, width=487, height=65)

    def start_command(self):
        print("START button clicked")
        self.start_btn["state"] = "disabled"  # Disable the START button
        self.stop_btn["state"] = "normal"  # Enable the STOP button

    def stop_command(self):
        print(self.test_data)
        print("STOP button clicked")
        # self.start_btn["state"] = "normal"    # Enable the START button
        self.stop_btn["state"] = "disabled"  # Disable the STOP button

        hris_password = simpledialog.askstring(
            "Password",
            "Enter Password", show='*'
        )

        if hris_password is not None and hris_password.strip() != "":
            input_password = str(hris_password)

            url = f"http://hris.teamglac.com/api/users/login?u={self.extracted_username}&p={input_password}"
            response = requests.get(url).json()
            if response['result'] == False:
                print("FAILED")
                self.stop_btn["state"] = "normal"    # Enable the START button
                showerror(
                title="Login Failed",
                message=f"Password is incorrect. Please try again.",
            )
            else:
                # self.start_btn["state"] = "normal"    # Enable the START button
                print("Success")
                self.show_input_dialog()
        else:
            showwarning("Error", "Invalid input. Buttons not changed.")



    def show_input_dialog(self):
        total_finished = simpledialog.askstring(
            "Enter Total Number of finished",
            "Please enter the total number of finish items",
        )

        if total_finished is not None and total_finished.strip() != "":
            total_finished = int(total_finished)
            
            # dataPass = int(dataPass)

            dataPass = 100
            # Ensure dataPass is an integer
            dataPass = int(dataPass)

            if total_finished >= dataPass:
                print('True')
                self.start_btn["state"] = "normal"    # Enable the START button
            else:
                print('False')

            showinfo('Notice', f'Total Finished.. inputted by {self.extracted_employee_no}')
            self.root.destroy()

    def on_close(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            os.system("python operator_dashboard.py")
            

if __name__ == "__main__":
    root = tk.Tk()
    app = MO_Details(root)
    root.mainloop()
