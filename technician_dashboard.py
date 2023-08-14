import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import requests
from io import BytesIO
import tkinter as tk
import tkinter.font as tkFont
import os
import csv
# from main import App



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

class TechnicianDashboard:
    def __init__(self, root, user_department, user_position, dataJson):
        self.checkUpdates()
        data = dataJson['data']
        extracted_user_department = data[0]
        extracted_fullname = data[1]
        extracted_employee_no = data[2]
        extracted_employee_department = data[3]
        extracted_photo_url = data[4]
        extracted_possition = data[5]
        
        #setting title
        root.title(f"TECHNICIAN DASHBOARD - {extracted_employee_no} -- POSSITION - {extracted_possition}")

        width = 1475
        height = 935
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
        employee_name["font"] = ft  # Assign the created font
        employee_name["fg"] = "#333333"
        employee_name["justify"] = "center"
        employee_name["text"] = extracted_fullname
        employee_name.place(x=1190, y=0, width=281, height=60)

        employee_photo = tk.Label(root, image=self.image)
        employee_photo["bg"] = "#999999"
        employee_photo["font"] = ft  # Assign the created font
        employee_photo["fg"] = "#333333"
        employee_photo["justify"] = "center"
        employee_photo["text"] = "label"
        employee_photo.place(x=1100, y=0, width=83, height=60)
        
        
        logout_btn=tk.Button(root)
        logout_btn["bg"] = "#999999"
        logout_btn["cursor"] = "tcross"
        ft = tkFont.Font(family='Times',size=10)
        logout_btn["font"] = ft
        logout_btn["fg"] = "#333333"
        logout_btn["justify"] = "center"
        logout_btn["text"] = "LOGOUT"
        logout_btn["command"] = self.logout
        logout_btn.place(x=1400,y=70,width=66,height=37)
        
        tickets=tk.Button(root)
        tickets["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        tickets["font"] = ft
        tickets["fg"] = "#000000"
        tickets["justify"] = "center"
        tickets["text"] = "TICKETS"
        tickets.place(x=250,y=0,width=210,height=42)
        # tickets["command"] = self.tickets_command
        
        matriNewlyAdded=tk.Button(root)
        matriNewlyAdded["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        matriNewlyAdded["font"] = ft
        matriNewlyAdded["fg"] = "#000000"
        matriNewlyAdded["justify"] = "center"
        matriNewlyAdded["text"] = "UPDATES"
        matriNewlyAdded.place(x=0,y=0,width=210,height=40)
        # matriNewlyAdded["command"] = self.matriNewlyAdded_command
        
        
        self.tree = ttk.Treeview(root)
        self.tree["columns"] = ("Matrix1", "Matrix2", "Matrix3", "Matrix4", "Matrix5", "Matrix6")
        self.tree.heading("#0", text="Row")
        self.tree.heading("Matrix1", text="Matrix 1")
        self.tree.heading("Matrix2", text="Matrix 2")
        self.tree.heading("Matrix3", text="Matrix 3")
        self.tree.heading("Matrix4", text="Matrix 4")
        self.tree.heading("Matrix5", text="Matrix 5")
        self.tree.heading("Matrix6", text="Matrix 6")
        self.tree.pack(pady=150)

        self.populate_table()
        
    def logout(self):
        # mainDashboard = Toplevel(root)
        # main_dashboard = App()  
        # root.withdraw()
        root.quit
        
    def populate_table(self):
        script_directory = os.path.dirname(os.path.abspath(__file__))
        log_folder = os.path.join(script_directory, "data")
        csv_file_path = os.path.join(log_folder, 'matrix.csv')
        
        with open(csv_file_path, "r") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=",")
            for i, row in enumerate(csv_reader, start=1):
                # Align data in each column accordingly
                values = [row[0], row[1], row[2], row[3], row[4], row[5]]
                self.tree.insert("", "end", text=str(i), values=values)

                
     
    def checkUpdates(self):
        script_directory = os.path.dirname(os.path.abspath(__file__))
        log_folder = os.path.join(script_directory, "data")
        log_file_path = os.path.join(log_folder, 'matrix.csv')
        monitor = CSVMonitor(log_file_path)

        def update_status():
            new_data_count = monitor.check_for_new_data()
            if new_data_count > 0:
                print(new_data_count)
                matriNewlyAdded = tk.Button(root)
                matriNewlyAdded["bg"] = "#f0f0f0"
                ft = tkFont.Font(family='Times', size=10)
                matriNewlyAdded["font"] = ft
                matriNewlyAdded["fg"] = "#000000"
                matriNewlyAdded["justify"] = "center"
                matriNewlyAdded["text"] = f"UPDATES {new_data_count}"
                matriNewlyAdded.place(x=0, y=0, width=210, height=40)
                # matriNewlyAdded["command"] = self.matriNewlyAdded_command
            
            root.after(5000, update_status)  # Check every 5 seconds  
            
    
     
        
        
if __name__ == "__main__":
    root = tk.Tk()
    dashboard = TechnicianDashboard(root, user_department, user_position, dataJson)
    root.mainloop()  # Start the Tkinter main loop