import tkinter as tk
import tkinter.font as tkFont
from tkinter import messagebox
from tkinter import ttk
from tkinter.messagebox import showinfo, showwarning, showerror
import requests
import json
import os
import csv
from tkinter import Toplevel
from operator_dashboard import OperatorDashboard
from technician_dashboard import TechnicianDashboard
import socketio
import uuid
import re



sio = socketio.Client(reconnection=True, reconnection_attempts=5, reconnection_delay=1, reconnection_delay_max=5)
client = str(uuid.uuid4())
filename = os.path.basename(__file__)
removeExtension = re.sub('.py', '', filename)

@sio.event
def connect():
    print('Connected to server')
    sio.emit('client_connected', {'machine_name': filename, 'client': client})
    sio.emit('client', {'machine_name': filename, 'client': client})

@sio.event
def disconnect():
    print('disconnected to server')
    
    
    



class UserPermissions:
    def __init__(self, config_path):
        self.config_path = config_path
        self.employee_departments = []
        self.employee_positions = []
        self.technician = []
        self.operator = []

    def load_permissions(self):
        try:
            with open(self.config_path) as json_file:
                data = json.load(json_file)
                self.employee_departments = data["allowed_users"]["employee_department"]
                self.employee_positions = data["allowed_users"]["employee_position"]
                self.operator = data["allowed_users"]["operator"]
                self.technician = data["allowed_users"]["technician"]
        except FileNotFoundError as e:
            print(e)
            self.employee_departments = []
            self.employee_positions = []
            self.technician = []
            self.operator = []

    def is_department_allowed(self, department):
        return department in self.employee_departments

    def is_position_allowed(self, position):
        return position in self.employee_positions

    def is_technician(self, position):
        return position in self.technician

    def is_operator(self, position):
        return position in self.operator

    
    
class App:
    def __init__(self, root):
        root.title("LOG IN DASHBOARD")
        #setting window size
        self.width=1361
        self.height=894
        self.screenwidth = root.winfo_screenwidth()
        self.screenheight = root.winfo_screenheight()
        self.alignstr = '%dx%d+%d+%d' % (self.width, self.height, (self.screenwidth - self.width) / 2, (self.screenheight - self.height) / 2)
        root.geometry(self.alignstr)
        root.resizable(width=False, height=False)
        
        ##FUNCTIONS##
                
        ##END##

        self.entry_employee_number=tk.Entry(root)
        self.entry_employee_number["bg"] = "#ffffff"
        self.ft = tkFont.Font(family='Times',size=48)
        self.entry_employee_number["font"] = self.ft
        self.entry_employee_number["fg"] = "#333333"
        self.entry_employee_number["justify"] = "center"
        self.entry_employee_number["text"] = "EMPLOYEE ID"
        self.entry_employee_number.bind('<KeyRelease>', self.validate_employee_number)
        self.entry_employee_number.place(x=450,y=30,width=443,height=74)

        self.GMessage_33=tk.Message(root)
        self.GMessage_33["bg"] = "#ffffff"
        self.ft = tkFont.Font(family='Times',size=14)
        self.GMessage_33["font"] = self.ft
        self.GMessage_33["fg"] = "#333333"
        self.GMessage_33["justify"] = "center"
        self.GMessage_33["text"] = "LOGS"
        self.GMessage_33.place(x=680,y=160,width=666,height=717)


        self.GLabel_544=tk.Label(root)
        self.GLabel_544["bg"] = "#ffffff"
        self.ft = tkFont.Font(family='Times',size=10)
        self.GLabel_544["font"] = self.ft
        self.GLabel_544["fg"] = "#333333"
        self.GLabel_544["justify"] = "center"
        self.GLabel_544["text"] = "label"
        self.GLabel_544.place(x=20,y=160,width=298,height=339)

        self.GLabel_111=tk.Label(root)
        self.GLabel_111["bg"] = "#ffffff"
        self.ft = tkFont.Font(family='Times',size=10)
        self.GLabel_111["font"] = self.ft
        self.GLabel_111["fg"] = "#333333"
        self.GLabel_111["justify"] = "center"
        self.GLabel_111["text"] = "label"
        self.GLabel_111.place(x=360,y=160,width=301,height=338)
        
        ##Functions
        
        self.update_status()
        self.oee()
        
        ##End 
    
    def check_internet_connection_requests(self):
        try:
            response = requests.get("http://www.google.com", timeout=5)
            return response.status_code == 200
        except requests.ConnectionError:
            return False
    
    def validate_employee_number(self, event):
        employee_number = self.entry_employee_number.get()
        if len(employee_number) == 5:
            if self.check_internet_connection_requests():
                self.validate_online_employee(employee_number)
            else:
                self.validate_offline_employee(employee_number)
        elif len(employee_number) == 4:
            if self.check_internet_connection_requests():
                self.validate_online_employee(employee_number)
            else:
                self.validate_offline_employee(employee_number)
                

    @sio.event
    def my_message(data):
        print('Message received with', data)
        toPassData = data['dataToPass']
        remove_py = re.sub('.py', '', filename)
        fileNameWithIni = remove_py + '.json'
        folder_path = 'data'
        file_path = f'{folder_path}/{fileNameWithIni}'

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        with open(file_path, 'w') as file:
            data = {
                'filename': remove_py,
                'data': toPassData
            }
            json.dump(data, file)
        sio.emit('my_response', {'response': 'my response'})
        
    @sio.event
    def getMatrixfromServer(data):
        print('Message received with', data)
        toPassData = data['dataToPass']
        print(f"==>> toPassData: {toPassData}")

        filename = 'matrix.csv'
        folder_path = 'data'
        file_path = f'{folder_path}/{filename}'

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        file_exists = os.path.exists(file_path)
        with open(file_path, 'a', newline='') as file:
            writer = csv.writer(file)

            if not file_exists:
                header_row = [f'data{i}' for i in range(1, len(toPassData)+1)]
                writer.writerow(header_row)

            writer.writerow(toPassData)

        sio.emit('my_response', {'response': 'my response'})

        
    
    def validate_online_employee(self, employee_number):
        try:
            employee_number = int(employee_number)
            hris_url = f'http://hris.teamglac.com/api/users/emp-num?empno={employee_number}'
            response = requests.get(hris_url)
            
            if response.status_code == 200:
                try:
                    data = json.loads(response.text)['result']
                    user_department = data.get('employee_department')
                    fullname = data.get('fullname')
                    user_position = data.get('employee_position')
                    employee_no = data.get('employee_no')
                    employee_department = data.get('employee_department')
                    photo_url = data.get('photo_url')
                    
                    
                    data = [
                        user_department,
                        fullname,
                        employee_no,
                        employee_department,
                        photo_url,
                        user_position
                    ]
                    dataJson = {'data':data}

                    if user_department and user_position:
                        self.validate_permissions(user_department, user_position, dataJson)
                    else:
                        print("Employee data doesn't contain department or position.")
                except KeyError:
                    print("Response data doesn't have expected keys.")
            else:
                print("Error accessing HRIS API:", response.status_code)
        except ValueError:
            tk.messagebox.showerror("Invalid Input", "Please enter a valid integer employee number.")
    
    def validate_offline_employee(self, employee_number):
        log_file_path = os.path.join(self.get_script_directory(), "config", 'hris.json')
        
        with open(log_file_path, "r") as json_file:
            data = json.load(json_file)['result']

        matching_employee = None
        for employee in data:
            if employee.get('employee_id_no') == employee_number:
                matching_employee = employee
                break

        if matching_employee:
            user_department = matching_employee.get('employee_department')
            user_position = matching_employee.get('employee_position')
            
            self.validate_permissions(user_department, user_position)
        else:
            print("Employee not found.")
    
    def validate_permissions(self, user_department, user_position, dataJson):
        print(user_position)
        permissions = self.load_permissions()
        if permissions.is_department_allowed(user_department) and permissions.is_position_allowed(user_position):
            if permissions.is_technician(user_position):
                self.show_tech_dashboard(user_department, user_position, dataJson)
            elif permissions.is_operator(user_position):
                print(f"{user_position} is an operator.")
                self.show_operator_dashboard(user_department, user_position, dataJson)
            else:
                showerror(title='Login Failed', message=f"User's department or position is not allowed. Please check, Current Department / Possition  {user_department + ' ' + user_position}")

        else:
            showerror(title='Login Failed', message=f"User's department or position is not allowed. Please check, Current Department / Possition  {user_department + ' ' + user_position}")
            
    def show_operator_dashboard(self, user_department, user_position, dataJson):
        OpeDashboard= Toplevel(root)
        ope_dashboard = OperatorDashboard(OpeDashboard, user_department, user_position, dataJson)  
        root.withdraw()
        
    def show_tech_dashboard(self, user_department, user_position, dataJson):
        techDashboard = Toplevel(root)
        tech_dashboard = TechnicianDashboard(techDashboard, user_department, user_position, dataJson)  
        root.withdraw()
    
    def load_permissions(self):
        log_file_path = os.path.join(self.get_script_directory(), "config", 'settings.json')
        permissions = UserPermissions(log_file_path)
        permissions.load_permissions()
        return permissions
    
    def get_script_directory(self):
        return os.path.dirname(os.path.abspath(__file__))
            
    def checking_allowed_user(self):
        script_directory = os.path.dirname(os.path.abspath(__file__))
        log_folder = os.path.join(script_directory, "config")
        log_file_path = os.path.join(log_folder, 'settings.json')
        try:
            with open(log_file_path, 'r') as file:
                log_content = file.read()
                result = log_content['allowed_users']
        except FileNotFoundError as e:
            print(e)
        
    def update_status(self):
        script_directory = os.path.dirname(os.path.abspath(__file__))
        log_folder = os.path.join(script_directory, "logs")
        log_file_path = os.path.join(log_folder, 'logs.csv')  # Change extension to .csv
        
        try:
            with open(log_file_path, 'r') as file:
                csv_reader = csv.reader(file)
                last_row = None
                for row in csv_reader:
                    last_row = row
                if last_row:
                    last_value = last_row[0]  # Get the first value from the last row
                    self.logs = tk.Message(root)
                    self.logs["bg"] = "#e0bdbd"
                    self.ft = tkFont.Font(family='Times', size=10)
                    self.logs["font"] = self.ft
                    self.logs["fg"] = "#333333"
                    self.logs["justify"] = "center"
                    self.logs['width'] = 200
                    self.logs["text"] = last_value
                    self.logs.place(x=20, y=20, width=284, height=51)
                else:
                    pass
        except FileNotFoundError as e:
            print(e)
        root.after(5000, self.update_status)  
        
    
    def oee(self):
        script_directory = os.path.dirname(os.path.abspath(__file__))
        log_folder = os.path.join(script_directory, "logs")
        log_file_path = os.path.join(log_folder, 'logs.csv')  # Change extension to .csv
        
        
        try:
            with open(log_file_path, 'r') as file:
                csv_reader = csv.reader(file)
                last_row = None
                for row in csv_reader:
                    last_row = row
                if last_row:
                    last_value = last_row[2]  # Get the first value from the last row
                    
                    label = f"""
                    1. PRODUCTIVE HOURS: ' ' HOURS
                    2. AVAILABLE HOURS: {last_value} HOURS
                    3. QUANTITY TO PROCESS: ' ' PCS
                    4. TOTAL PROCESS: ' ' PCS
                    5. TARGET TOTAL ' ' PCS
                    """
                    self.GMessage_465=tk.Message(root)
                    self.GMessage_465["bg"] = "#ffffff"
                    self.ft = tkFont.Font(family='Times',size=15)
                    self.GMessage_465["font"] = self.ft
                    self.GMessage_465["fg"] = "#333333"
                    self.GMessage_465["justify"] = "center"
                    self.GMessage_465['width'] = 800
                    self.GMessage_465["justify"] = "left"
                    self.GMessage_465["text"] = label
                    self.GMessage_465.place(x=20,y=540,width=642,height=337)
                else:
                    pass
        except FileNotFoundError as e:
            print(e)
        root.after(5000, self.oee)  
        
sio.connect('http://10.0.2.150:9090')

        
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
