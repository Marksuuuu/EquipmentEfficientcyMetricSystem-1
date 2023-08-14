import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import requests
from io import BytesIO
import tkinter as tk
import tkinter.font as tkFont
import os
import csv
import json
from tkinter import Toplevel
from tkinter import messagebox





class CSVMonitor:
    def __init__(self, csv_file_path):
        self.csv_file_path = csv_file_path
        self.previous_content = self.read_csv_content()
        self.new_data_count = 0

    def read_csv_content(self):
        try:
            with open(self.csv_file_path, "r") as csv_file:
                return csv_file.read()
        except FileNotFoundError:
            return ""

    def check_for_new_data(self):
        current_content = self.read_csv_content()

        if self.previous_content != current_content:
            current_rows = current_content.strip().split('\n')
            previous_rows = self.previous_content.strip().split('\n')

            new_rows = len(current_rows) - len(previous_rows)
            if new_rows > 0:
                self.new_data_count += new_rows
                print(new_data_count)

            self.previous_content = current_content

        return self.new_data_count

class OperatorDashboard:
    def __init__(self, root, user_department, user_position, dataJson):
        data = dataJson['data']
        extracted_user_department = data[0]
        extracted_fullname = data[1]
        extracted_employee_no = data[2]
        extracted_employee_department = data[3]
        extracted_photo_url = data[4]
        extracted_possition = data[5]
        self.root = root
        
        #setting title
        root.title(f"OPERATOR DASHBOARD - {extracted_employee_no} -- POSSITION - {extracted_possition}")

        width=1705
        height=1000
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)
        
        if extracted_photo_url == False or extracted_photo_url is None:
            image_url = "https://www.freeiconspng.com/uploads/no-image-icon-15.png"
        else:
            image_url = f"http://hris.teamglac.com/{extracted_photo_url}"  # Replace with your image URL
        
        response = requests.get(image_url)
        pil_image = Image.open(BytesIO(response.content))
        desired_width = 83
        desired_height = 60
        pil_image = pil_image.resize((desired_width, desired_height), Image.ANTIALIAS)
        
        self.image = ImageTk.PhotoImage(pil_image)
        
        ft = tk.font.Font(family='Times', size=14)  # Use tk.font instead of tkFont

        employee_name = tk.Label(root)
        employee_name["bg"] = "#ffffff"
        employee_name["font"] = ft 
        employee_name["fg"] = "#333333"
        employee_name["justify"] = "center"
        employee_name["text"] = extracted_fullname
        employee_name.place(x=1420, y=0, width=281, height=60)

        employee_photo = tk.Label(root, image=self.image)
        employee_photo["bg"] = "#999999"
        employee_photo["font"] = ft 
        employee_photo["fg"] = "#333333"
        employee_photo["justify"] = "center"
        employee_photo["text"] = "label"
        employee_photo.place(x=1320, y=0, width=83, height=60)
        
        logout_btn = tk.Button(root)
        logout_btn["bg"] = "#999999"
        logout_btn["cursor"] = "tcross"
        ft = tkFont.Font(family='Times', size=10)
        logout_btn["font"] = ft
        logout_btn["fg"] = "#333333"
        logout_btn["justify"] = "center"
        logout_btn["text"] = "LOGOUT"
        logout_btn["command"] = self.logout  # Use the logout method directly
        logout_btn.place(x=1620, y=70, width=66, height=37)
        
        self.tree = ttk.Treeview(root, show="headings", columns=("MAIN OPERATION", "SUB-OPERATION", "WIP ENTITY NAME"))
        self.tree.heading("#0", text="Row")
        self.tree.heading("MAIN OPERATION", text="MAIN OPERATION")
        self.tree.heading("SUB-OPERATION", text="SUB-OPERATION")
        self.tree.heading("WIP ENTITY NAME", text="WIP ENTITY NAME")
        self.tree.pack(pady=120)

        # self.populate_table()
        self.read_json_file()
        
    def logout(self):
        response = messagebox.askyesno("Logout", "Are you sure you want to logout?")
        if response:
            self.root.destroy()  # Close the current root window
            self.root.quit()     #

    # /////////////////////////// POPULATE TABLE FROM JSON ///////////////////////////////
    
    def read_json_file(self):
        with open('data/main.json', 'r') as json_file:
            data = json.load(json_file)
            for item in data['data']:
                main_op = item['main_opt']
                sub_op = item['sub_opt']
                wip_entity = item['wip_entity_name']
                self.tree.insert("", "end", values=(main_op, sub_op, wip_entity))
                
        return data
        
    # def populate_table(self):
    #     script_directory = os.path.dirname(os.path.abspath(__file__))
    #     log_folder = os.path.join(script_directory, "data")
    #     csv_file_path = os.path.join(log_folder, 'setup-data.csv')
        
    #     with open(csv_file_path, "r") as csv_file:
    #         csv_reader = csv.reader(csv_file, delimiter="\t")
    #         for i, row in enumerate(csv_reader, start=1):
    #             self.tree.insert("", "end", text=str(i), values=row)
     
if __name__ == "__main__":
    root = tk.Tk()
    dashboard = OperatorDashboard(root, user_department, user_position, dataJson)
    logout_btn = tk.Button(root)
    logout_btn["bg"] = "#999999"
    logout_btn["cursor"] = "tcross"
    ft = tkFont.Font(family='Times', size=10)
    logout_btn["font"] = ft
    logout_btn["fg"] = "#333333"
    logout_btn["justify"] = "center"
    logout_btn["text"] = "LOGOUT"
    logout_btn["command"] = dashboard.logout  # Use the logout method directly
    logout_btn.place(x=1620, y=70, width=66, height=37)

    root.mainloop() 