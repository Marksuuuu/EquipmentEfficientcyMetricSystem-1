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
import logging
import datetime



class MO_Details:
    def __init__(self,root,extracted_fullname,extracted_employee_no,extracted_photo_url,extracted_username,data):
        #setting title
        root.title("MO")
        #setting window size
        width=1264
        height=675
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)
        
        self.root = root
        self.extracted_employee_no = extracted_employee_no
        self.extracted_photo_url = extracted_photo_url
        self.extracted_username = extracted_username
        self.root.title("MO DETAILS")
        self.test_data = data
        
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
        
        
        script_directory = os.path.dirname(os.path.abspath(__file__))
        self.log_folder = os.path.join(script_directory, "data")
        if not os.path.exists(self.log_folder):
            os.makedirs(self.log_folder)
        self.csv_file_path = os.path.join(self.log_folder, 'time.csv')


        self.image = ImageTk.PhotoImage(pil_image)

        GLabel_932=tk.Label(root)
        GLabel_932["bg"] = "#ffffff"
        ft = tkFont.Font(family='Times',size=18)
        GLabel_932["font"] = ft
        GLabel_932["fg"] = "#333333"
        GLabel_932["justify"] = "center"
        GLabel_932["text"] = f"Device : {data[2]}"
        GLabel_932.place(x=20,y=180,width=526,height=97)

        GLabel_771=tk.Label(root)
        GLabel_771["bg"] = "#ffffff"
        ft = tkFont.Font(family='Times',size=18)
        GLabel_771["font"] = ft
        GLabel_771["fg"] = "#333333"
        GLabel_771["justify"] = "center"
        GLabel_771["text"] = f"Package : {data[4]}"
        GLabel_771.place(x=20,y=300,width=526,height=97)

        GLabel_146=tk.Label(root)
        GLabel_146["bg"] = "#ffffff"
        ft = tkFont.Font(family='Times',size=18)
        GLabel_146["font"] = ft
        GLabel_146["fg"] = "#333333"
        GLabel_146["justify"] = "center"
        GLabel_146["text"] = f"Customer : {data[1]}"
        GLabel_146.place(x=20,y=420,width=526,height=97)

        GLabel_915=tk.Label(root)
        GLabel_915["bg"] = "#ffffff"
        ft = tkFont.Font(family='Times',size=18)
        GLabel_915["font"] = ft
        GLabel_915["fg"] = "#333333"
        GLabel_915["justify"] = "center"
        GLabel_915["text"] = f"Running Qty : {data[5]}"
        GLabel_915.place(x=20,y=540,width=526,height=97)

        GLabel_514=tk.Label(root)
        ft = tkFont.Font(family='Times',size=24)
        GLabel_514["font"] = ft
        GLabel_514["fg"] = "#333333"
        GLabel_514["justify"] = "center"
        GLabel_514["text"] = extracted_fullname
        GLabel_514.place(x=820,y=20,width=424,height=87)

        GLabel_978=tk.Label(root, image=self.image)
        ft = tkFont.Font(family='Times',size=10)
        GLabel_978["font"] = ft
        GLabel_978["fg"] = "#333333"
        GLabel_978["justify"] = "center"
        GLabel_978["text"] = "img"
        GLabel_978.place(x=680,y=20,width=120,height=87)

        self.start_btn=tk.Button(root)
        self.start_btn["bg"] = "#5fb878"
        ft = tkFont.Font(family='Times',size=23)
        self.start_btn["font"] = ft
        self.start_btn["fg"] = "#ffffff"
        self.start_btn["justify"] = "center"
        self.start_btn["text"] = "START"
        self.start_btn.place(x=1000,y=540,width=245,height=97)
        self.start_btn["command"] = self.start_command

        self.stop_btn=tk.Button(root)
        self.stop_btn["bg"] = "#cc0000"
        ft = tkFont.Font(family='Times',size=23)
        self.stop_btn["font"] = ft
        self.stop_btn["fg"] = "#f9f9f9"
        self.stop_btn["justify"] = "center"
        self.stop_btn["text"] = "STOP"
        self.stop_btn.place(x=1000,y=430,width=245,height=97)
        self.stop_btn["command"] = self.stop_command

        GLabel_65=tk.Label(root)
        GLabel_65["bg"] = "#ffffff"
        GLabel_65["borderwidth"] = "2px"
        ft = tkFont.Font(family='Times',size=58)
        GLabel_65["font"] = ft
        GLabel_65["fg"] = "#333333"
        GLabel_65["justify"] = "center"
        GLabel_65["text"] =  data[6]
        GLabel_65.place(x=20,y=20,width=526,height=87)

        GLabel_566=tk.Label(root)
        ft = tkFont.Font(family='Times',size=11)
        GLabel_566["font"] = ft
        GLabel_566["fg"] = "#333333"
        GLabel_566["justify"] = "center"
        GLabel_566["text"] = "PERSON ASSIGNED"
        GLabel_566.place(x=820,y=80,width=424,height=30)

    def log_event(self, msg):
        current_time = datetime.datetime.now()
        date = current_time.strftime('%Y-%m-%d')
        time = current_time.strftime('%H:%M:%S')

        with open(self.csv_file_path, mode='a', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([msg, date, time ])

    def start_command(self):
        print("START button clicked")
        self.log_event('START')
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

            with open("data/main.json", "r") as json_file:
                data = json.load(json_file)
                extracted_data = []

                for item in data["data"]:
                    customer = item["customer"]
                    device = item["device"]
                    main_opt = item["main_opt"]
                    package = item["package"]
                    running_qty = item["running_qty"]
                    wip_entity_name = item["wip_entity_name"]

                    extracted_data.append((customer, device, main_opt, package, running_qty, wip_entity_name))
                    
                    extracted_running_qty = int(running_qty)

                if total_finished >= extracted_running_qty:
                    self.start_btn["state"] = "normal"
                    self.log_event('START')
                else:
                    showinfo('Notice', f'Total Finished inputted by {self.extracted_employee_no}')
                    self.log_event('STOP')

                # Load existing log data
                try:
                    with open("data/mo_logs.json", "r") as logs_file:
                        logs_data = json.load(logs_file)
                        if not isinstance(logs_data, dict):  # Check if logs_data is a dictionary
                            logs_data = {}  # Initialize as dictionary if not
                except FileNotFoundError:
                    logs_data = {}  # Initialize as dictionary if file doesn't exist

                # Calculate new total_finished and append to logs_data
                new_total_finished = total_finished + logs_data.get("total_finished", 0)
                # logs_data["total_finished"] = new_total_finished

                new_log_entry = {
                    "wip_entity_name": wip_entity_name,
                    "running_qty": extracted_running_qty,
                    "total_finished": new_total_finished
                }

                # Append new_log_entry to logs_data
                logs_data.append(new_log_entry)

                # Write logs_data to mo_logs.json
                with open("data/mo_logs.json", "w") as logs_file:
                    json.dump(logs_data, logs_file)


            # self.root.destroy()

    def on_close(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            os.system("python operator_dashboard.py")

# class MO_Details:
#     def __init__(
#         self,
#         root,
#         extracted_fullname,
#         extracted_employee_no,
#         extracted_photo_url,
#         extracted_username,
#         data,
#     ):
#         self.root = root
#         self.extracted_employee_no = extracted_employee_no
#         self.extracted_photo_url = extracted_photo_url
#         self.extracted_username = extracted_username
#         self.root.title("MO DETAILS")
#         self.test_data = data

#         root.protocol('WM_DELETE_WINDOW', self.on_close)

#         # setting window size
#         width = 985
#         height = 482
#         screenwidth = self.root.winfo_screenwidth()
#         screenheight = self.root.winfo_screenheight()
#         alignstr = "%dx%d+%d+%d" % (
#             width,
#             height,
#             (screenwidth - width) / 2,
#             (screenheight - height) / 2,
#         )
#         self.root.geometry(alignstr)
#         self.root.resizable(width=False, height=False)

#         if self.extracted_photo_url == False or self.extracted_photo_url is None:
#             image_url = "https://www.freeiconspng.com/uploads/no-image-icon-15.png"
#         else:
#             image_url = f"http://hris.teamglac.com/{self.extracted_photo_url}"  # Replace with your image URL

#         response = requests.get(image_url)
#         pil_image = Image.open(BytesIO(response.content))
#         desired_width = 83
#         desired_height = 60
#         pil_image = pil_image.resize((desired_width, desired_height), Image.ANTIALIAS)
        
        
#         script_directory = os.path.dirname(os.path.abspath(__file__))
#         self.log_folder = os.path.join(script_directory, "data")
#         if not os.path.exists(self.log_folder):
#             os.makedirs(self.log_folder)
#         self.csv_file_path = os.path.join(self.log_folder, 'time.csv')


#         self.image = ImageTk.PhotoImage(pil_image)

#         self.start_btn = tk.Button(self.root)
#         self.start_btn["bg"] = "#f0f0f0"
#         ft = tkFont.Font(family="Times", size=12)
#         self.start_btn["font"] = ft
#         self.start_btn["fg"] = "#000000"
#         self.start_btn["justify"] = "center"
#         self.start_btn["text"] = "START"
#         self.start_btn.place(x=820, y=390, width=155, height=77)
#         self.start_btn["command"] = self.start_command

#         self.stop_btn = tk.Button(self.root)
#         self.stop_btn["bg"] = "#f0f0f0"
#         ft = tkFont.Font(family="Times", size=12)
#         self.stop_btn["font"] = ft
#         self.stop_btn["fg"] = "#000000"
#         self.stop_btn["justify"] = "center"
#         self.stop_btn["text"] = "STOP"
#         self.stop_btn.place(x=620, y=390, width=155, height=77)
#         self.stop_btn["command"] = self.stop_command
#         self.stop_btn["state"] = "disabled"

#         employee_photo = tk.Label(root, image=self.image)
#         employee_photo["bg"] = "#999999"
#         employee_photo["font"] = ft
#         employee_photo["fg"] = "#333333"
#         employee_photo["justify"] = "center"
#         employee_photo["text"] = "label"
#         employee_photo.place(x=600, y=10, width=82, height=50)

#         lbl_employee_name = tk.Label(self.root)
#         lbl_employee_name["bg"] = "#fefefe"
#         ft = tkFont.Font(family="Times", size=12)
#         lbl_employee_name["font"] = ft
#         lbl_employee_name["fg"] = "#333333"
#         lbl_employee_name["justify"] = "center"
#         lbl_employee_name["text"] = extracted_fullname
#         lbl_employee_name.place(x=700, y=10, width=273, height=50)

#         lbl_mo = tk.Label(self.root)
#         lbl_mo["bg"] = "#ffffff"
#         ft = tkFont.Font(family="Times", size=12)
#         lbl_mo["font"] = ft
#         lbl_mo["fg"] = "#333333"
#         lbl_mo["justify"] = "center"
#         lbl_mo["text"] = f"Main Operation: {data[1]}"
#         lbl_mo.place(x=20, y=110, width=487, height=65)

#         lbl_customer = tk.Label(self.root)
#         lbl_customer["bg"] = "#fbfbfb"
#         ft = tkFont.Font(family="Times", size=12)
#         lbl_customer["font"] = ft
#         lbl_customer["fg"] = "#333333"
#         lbl_customer["justify"] = "center"
#         lbl_customer["text"] = f"Sub-Operation: {data[2]}"
#         lbl_customer.place(x=20, y=210, width=487, height=65)

#         lbl_device = tk.Label(self.root)
#         lbl_device["bg"] = "#ffffff"
#         ft = tkFont.Font(family="Times", size=12)
#         lbl_device["font"] = ft
#         lbl_device["fg"] = "#333333"
#         lbl_device["justify"] = "center"
#         lbl_device["text"] = f"WIP Entity Name: {data[3]}"
#         lbl_device.place(x=20, y=310, width=487, height=65)
        

#     def log_event(self, msg):
#         current_time = datetime.datetime.now()
#         date = current_time.strftime('%Y-%m-%d')
#         time = current_time.strftime('%H:%M:%S')

#         with open(self.csv_file_path, mode='a', newline='') as csv_file:
#             csv_writer = csv.writer(csv_file)
#             csv_writer.writerow([msg, date, time ])

#     def start_command(self):
#         print("START button clicked")
#         self.log_event('START')
#         self.start_btn["state"] = "disabled"  # Disable the START button
#         self.stop_btn["state"] = "normal"  # Enable the STOP button

#     def stop_command(self):
#         print(self.test_data)
#         print("STOP button clicked")
#         # self.start_btn["state"] = "normal"    # Enable the START button
#         self.stop_btn["state"] = "disabled"  # Disable the STOP button
#         hris_password = simpledialog.askstring(
#             "Password",
#             "Enter Password", show='*'
#         )

#         if hris_password is not None and hris_password.strip() != "":
#             input_password = str(hris_password)

#             url = f"http://hris.teamglac.com/api/users/login?u={self.extracted_username}&p={input_password}"
#             response = requests.get(url).json()
#             if response['result'] == False:
#                 print("FAILED")
#                 self.stop_btn["state"] = "normal"    # Enable the START button
#                 showerror(
#                 title="Login Failed",
#                 message=f"Password is incorrect. Please try again.",
#             )
#             else:
#                 # self.start_btn["state"] = "normal"    # Enable the START button
#                 print("Success")
#                 self.show_input_dialog()
#         else:
#             showwarning("Error", "Invalid input. Buttons not changed.")



#     def show_input_dialog(self):
#         total_finished = simpledialog.askstring(
#             "Enter Total Number of finished",
#             "Please enter the total number of finish items",
#         )

#         if total_finished is not None and total_finished.strip() != "":
#             total_finished = int(total_finished)
            
#             # dataPass = int(dataPass)

#             dataPass = 100
#             # Ensure dataPass is an integer
#             dataPass = int(dataPass)

#             if total_finished >= dataPass:
#                 print('True')
#                 self.start_btn["state"] = "normal"    # Enable the START button
#             else:
#                 print('False')

#             showinfo('Notice', f'Total Finished.. inputted by {self.extracted_employee_no}')
#             self.log_event('STOP')
#             self.root.destroy()

#     def on_close(self):
#         if messagebox.askokcancel("Quit", "Do you want to quit?"):
#             os.system("python operator_dashboard.py")
            

if __name__ == "__main__":
    root = tk.Tk()
    app = MO_Details(root)
    root.mainloop()
