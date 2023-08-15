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
from request_ticket import RequestTicket






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
        self.root = root
        data = dataJson['data']
        self.extracted_user_department = data[0]
        self.extracted_fullname = data[1]
        self.extracted_employee_no = data[2]
        self.extracted_employee_department = data[3]
        self.extracted_photo_url = data[4]
        self.extracted_possition = data[5]
        
        #setting title
        root.title(f"OPERATOR DASHBOARD - {self.extracted_employee_no} -- POSSITION - {self.extracted_possition}")

        width=1705
        height=1000
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)
        
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
        
        ft = tk.font.Font(family='Times', size=14)  # Use tk.font instead of tkFont
        
     
  
        GButton_458=tk.Button(root)
        GButton_458["bg"] = "#cc0000"
        GButton_458["font"] = ft
        GButton_458["fg"] = "#ffffff"
        GButton_458["justify"] = "center"
        GButton_458["text"] = "REQUEST TICKET"
        GButton_458.place(x=10,y=0,width=172,height=44)
        GButton_458["command"] = self.tickets_command
        

        employee_name = tk.Label(root)
        employee_name["bg"] = "#ffffff"
        employee_name["font"] = ft 
        employee_name["fg"] = "#333333"
        employee_name["justify"] = "center"
        employee_name["text"] = self.extracted_fullname
        employee_name.place(x=1420, y=0, width=281, height=60)

        employee_photo = tk.Label(root, image=self.image)
        employee_photo["bg"] = "#999999"
        employee_photo["font"] = ft 
        employee_photo["fg"] = "#333333"
        employee_photo["justify"] = "center"
        employee_photo["text"] = "label"
        employee_photo.place(x=1320, y=0, width=83, height=60)
        
        
        logout_btn=tk.Button(root)
        logout_btn["bg"] = "#999999"
        logout_btn["cursor"] = "tcross"
        ft = tkFont.Font(family='Times',size=10)
        logout_btn["font"] = ft
        logout_btn["fg"] = "#333333"
        logout_btn["justify"] = "center"
        logout_btn["text"] = "LOGOUT"
        logout_btn["command"] = self.logout
        logout_btn.place(x=1620,y=70,width=66,height=37)
        
        
        self.tree = ttk.Treeview(root)
        self.tree["columns"] = ("MO NO.", "OPERATION", "SUB-OPERATION", "OPERATOR", "MACHINE", "USAGE CARD", "UPH")
        self.tree.heading("#0", text="Row")
        self.tree.heading("MO NO.", text="MO NO.")
        self.tree.heading("OPERATION", text="OPERATION")
        self.tree.heading("SUB-OPERATION", text="SUB-OPERATION")
        self.tree.heading("OPERATOR", text="OPERATOR")
        self.tree.heading("MACHINE", text="MACHINE")
        self.tree.heading("USAGE CARD", text="USAGE CARD")
        self.tree.heading("UPH", text="UPH")
        self.tree.pack(pady=120)

        self.populate_table()
        
    def logout(self):
        from main import App
        
        mainDashboard = Toplevel(root)
        main_dashboard = App()  
        root.withdraw()
    
    def tickets_command(self):
        # self.root.withdraw()
        self.ticket_dashboard = Toplevel(self.root)
        show_ticket_dashboard = RequestTicket(self.ticket_dashboard, self.extracted_fullname)
        
    def populate_table(self):
        script_directory = os.path.dirname(os.path.abspath(__file__))
        log_folder = os.path.join(script_directory, "data")
        csv_file_path = os.path.join(log_folder, 'setup-data.csv')
        
        with open(csv_file_path, "r") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter="\t")
            for i, row in enumerate(csv_reader, start=1):
                self.tree.insert("", "end", text=str(i), values=row)
     
            
    
     
        
        
if __name__ == "__main__":
    root = tk.Tk()
    dashboard = OperatorDashboard(root, user_department, user_position, dataJson)
    logout_btn["command"] = lambda: dashboard.logout(root)
    root.mainloop()  # Start the Tkinter main loop