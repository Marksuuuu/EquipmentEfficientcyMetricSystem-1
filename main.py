import csv
import json
import logging
import os
import re
import signal
import tkinter as tk
import tkinter.font as tkFont
import uuid
from datetime import datetime, timedelta
from tkinter import Toplevel
from tkinter import messagebox
from tkinter.messagebox import showerror
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk

import requests
import socketio
from ttkbootstrap.constants import *

from operator_dashboard import OperatorDashboard
from technician_dashboard import TechnicianDashboard

sio = socketio.Client(reconnection=True, reconnection_attempts=5,
                      reconnection_delay=1, reconnection_delay_max=5)
client = str(uuid.uuid4())
filename = os.path.basename(__file__)
removeExtension = re.sub('.py', '', filename)


@sio.event
def connect():
    print('Connected to server')
    sio.emit('client_connected', {'machine_name': filename, 'client': client})
    sio.emit('controller', {'machine_name': filename})
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
        # setting window size
        self.width = 1361
        self.height = 894
        self.screenwidth = root.winfo_screenwidth()
        self.screenheight = root.winfo_screenheight()
        self.alignstr = '%dx%d+%d+%d' % (self.width, self.height, (self.screenwidth -
                                                                   self.width) / 2,
                                         (self.screenheight - self.height) / 2)
        root.geometry(self.alignstr)
        root.resizable(width=False, height=False)

        root.protocol("WM_DELETE_WINDOW", self.handle_exit_signal)

        # Functions

        self.update_status()
        self.oee()
        self.init_logging()

        self.chart_image = None
        self.GLabel_544 = None
        self.create_ui()
        self.update_chart()
        # End

        ## END##
        dateNow = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.entry_employee_number = tk.Entry(root)
        self.entry_employee_number["bg"] = "#ffffff"
        self.ft = tkFont.Font(family='Times', size=48)
        self.entry_employee_number["font"] = self.ft
        self.entry_employee_number["fg"] = "#333333"
        self.entry_employee_number["justify"] = "center"
        self.entry_employee_number["text"] = "EMPLOYEE ID"
        self.entry_employee_number.bind(
            '<KeyRelease>', self.validate_employee_number)
        self.entry_employee_number.place(x=450, y=30, width=443, height=74)

        self.GMessage_33 = tk.Message(root)
        self.GMessage_33["bg"] = "#ffffff"
        self.ft = tkFont.Font(family='Times', size=14)
        self.GMessage_33["font"] = self.ft
        self.GMessage_33["fg"] = "#333333"
        self.GMessage_33["justify"] = "center"
        self.GMessage_33["text"] = "LOGS"
        self.GMessage_33.place(x=680, y=160, width=666, height=717)

        self.GLabel_111 = tk.Label(root)
        self.GLabel_111["bg"] = "#ffffff"
        self.ft = tkFont.Font(family='Times', size=10)
        self.GLabel_111["font"] = self.ft
        self.GLabel_111["fg"] = "#333333"
        self.GLabel_111["justify"] = "center"
        self.GLabel_111["text"] = "label"
        self.GLabel_111.place(x=360, y=160, width=301, height=338)

        self.init_logging()
        self.passLogDatatoServer()
        self.update_logs()

        self.log_activity(logging.INFO, f'Open Program')

    def handle_exit_signal(self):
        self.log_activity(logging.INFO, f'Terminated the program')
        root.destroy()
        # self.quit()

    def passLogDatatoServer(self):
        log_file = 'logs/activity_log.txt'
        try:
            with open(log_file, 'r') as file:
                logs_data = file.read()
            lines = logs_data.split('\n')
            last_5_logs = '\n'.join(lines[-6:])
            data = (last_5_logs, client, removeExtension)
            encoded_data = json.dumps({'data': data})
            sio.emit('passActivityData', encoded_data)
        except Exception as e:
            raise
        root.after(50000, self.update_logs)

    def update_logs(self):
        log_file = 'logs/activity_log.txt'
        try:
            with open(log_file, 'r') as file:
                log_content = file.read()
            lines = log_content.split('\n')
            last_5_logs = '\n'.join(lines[-6:])

            self.logs = tk.Message(root)
            self.logs["bg"] = "#ffffff"
            self.ft = tkFont.Font(family='Times', size=18)
            self.logs["font"] = self.ft
            self.logs["fg"] = "#333333"
            self.logs["justify"] = "left"
            self.logs["text"] = last_5_logs
            self.logs['width'] = 700
            self.logs.place(x=680, y=160, width=666, height=717)

        except FileNotFoundError:
            self.logs["text"] = "Log file not found."
        root.after(50000, self.update_logs)

    def init_logging(self):
        log_file = 'logs/activity_log.txt'
        logging.basicConfig(filename=log_file, level=logging.INFO,
                            format='[%(asctime)s] %(levelname)s: %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S', filemode='a')
        # print(f'Logging to {log_file}')-
    def log_activity(self, level, message):
        logging.log(level, message)

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
        machno = data['machno']
        remove_py = re.sub('.py', '', filename)
        fileNameWithIni = remove_py + '.json'
        folder_path = 'data'
        file_path = f'{folder_path}/{fileNameWithIni}'

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        with open(file_path, 'w') as file:
            data = {
                'machno': machno,
                'filename': remove_py,
                'data': toPassData
            }
            json.dump(data, file)
        sio.emit('my_response', {'response': 'my response'})

    @sio.event
    def getMatrixfromServer(data):
        print('Message received with', data)
        toPassData = data['dataToPass'][0]

        flattened_data = ', '.join(toPassData).replace("'", "")
        print(f"==>> toPassData: {flattened_data}")

        filename = 'matrix.csv'
        folder_path = 'data'
        file_path = os.path.join(folder_path, filename)

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        file_exists = os.path.exists(file_path)
        with open(file_path, 'a', newline='') as file:
            writer = csv.writer(file)

            if not file_exists:
                header_row = [f'data{i}' for i in range(
                    1, len(toPassData) + 1)]
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
                    username = data.get('username')

                    data = [
                        user_department,
                        fullname,
                        employee_no,
                        employee_department,
                        photo_url,
                        user_position,
                        username
                    ]
                    dataJson = {'data': data}

                    if user_department and user_position:
                        self.validate_permissions(
                            user_department, user_position, dataJson)
                    else:
                        print("Employee data doesn't contain department or position.")
                except KeyError:
                    print("Response data doesn't have expected keys.")
            else:
                print("Error accessing HRIS API:", response.status_code)
        except ValueError:
            tk.messagebox.showerror(
                "Invalid Input", "Please enter a valid integer employee number.")

    def validate_offline_employee(self, employee_number):
        log_file_path = os.path.join(
            self.get_script_directory(), "config", 'hris.json')

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
            # user_empNo = matching_employee.get('employee_id_no')

            self.validate_permissions(user_department, user_position)
        else:
            print("Employee not found.")

    def validate_permissions(self, user_department, user_position, dataJson):
        employee_number = self.entry_employee_number.get()

        permissions = self.load_permissions()
        if permissions.is_department_allowed(user_department) and permissions.is_position_allowed(user_position):
            if permissions.is_technician(user_position):
                self.show_tech_dashboard(
                    user_department, user_position, dataJson)
            elif permissions.is_operator(user_position):
                print(f"{user_position} is an operator.")
                self.show_operator_dashboard(
                    user_department, user_position, dataJson)
                self.log_activity(
                    logging.INFO, f'User login successful. ID NUM: {employee_number}')

            else:
                self.log_activity(
                    logging.INFO, f'User login unsuccessful. ID NUM: {employee_number}')

                showerror(title='Login Failed',
                          message=f"User's department or position is not allowed. Please check, Current Department / Possition  {user_department + ' ' + user_position}")

        else:
            self.log_activity(
                logging.INFO, f'User login unsuccessful. ID NUM: {employee_number}')
            showerror(title='Login Failed',
                      message=f"User's department or position is not allowed. Please check, Current Department / Possition  {user_department + ' ' + user_position}")

    def show_operator_dashboard(self, user_department, user_position, dataJson):
        OpeDashboard = Toplevel(root)
        ope_dashboard = OperatorDashboard(
            OpeDashboard, user_department, user_position, dataJson)
        root.withdraw()

    def show_tech_dashboard(self, user_department, user_position, dataJson):
        techDashboard = Toplevel(root)
        tech_dashboard = TechnicianDashboard(
            techDashboard, user_department, user_position, dataJson)
        root.withdraw()

    def load_permissions(self):
        log_file_path = os.path.join(
            self.get_script_directory(), "config", 'settings.json')
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

    def calculate_total_productive_time(self):
        script_directory = os.path.dirname(os.path.abspath(__file__))
        log_folder = os.path.join(script_directory, "data")
        log_file_path = os.path.join(log_folder, 'time.csv')

        data = []
        # Read data from CSV file
        with open(log_file_path, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                data.append(tuple(row))

        productive_hours = {}
        start_time = None

        for action, date_str, time_str in data:
            dt = datetime.strptime(
                date_str + " " + time_str, "%Y-%m-%d %H:%M:%S")

            if action == "START":
                start_time = dt
            elif action == "STOP" and start_time is not None:
                productive_time = dt - start_time
                day = dt.date()
                if day not in productive_hours:
                    productive_hours[day] = productive_time
                else:
                    productive_hours[day] += productive_time
                start_time = None

        total_productive_time = timedelta()

        for day, productive_time in productive_hours.items():
            total_productive_time += productive_time

        return total_productive_time

    def create_donut_chart(self):
        total = 100 - self.calculateOee()
        data = [self.calculateOee(), total]
        labels = ['Effectiveness', '']
        colors = ['#3498db', '#e74c3c']
        explode = (0.05, 0)

        figure = Figure(figsize=(5, 4), dpi=100)
        plot = figure.add_subplot(1, 1, 1)
        plot.pie(data, labels=labels, colors=colors, autopct='%1.1f%%',
                 startangle=90, pctdistance=0.85, explode=explode)

        centre_circle = plt.Circle((0, 0), 0.70, fc='white')
        plot.add_artist(centre_circle)
        
        center_text = 'OEE'
        plot.text(0, 0, center_text, va='center', ha='center', fontsize=12)

        plot.axis('equal')

        canvas = FigureCanvasTkAgg(figure, master=root)
        canvas_widget = canvas.get_tk_widget()

        canvas.draw()
        pil_image = Image.frombytes(
            'RGB', canvas.get_width_height(), canvas.tostring_rgb())
        img = ImageTk.PhotoImage(image=pil_image)
        root.after(50000, self.create_donut_chart)
        return img
    
    def update_chart(self):
        self.chart_image = self.create_donut_chart()
        if self.GLabel_544 is not None:
            self.GLabel_544.configure(image=self.chart_image)
        root.after(50000, self.update_chart)

    def create_ui(self):
        self.GLabel_544 = tk.Label(root, bg="#FFFFFF")
        self.GLabel_544["bg"] = "#FFFFFF"
        self.ft = tk.font.Font(family='Times', size=10)
        self.GLabel_544["font"] = self.ft
        self.GLabel_544["fg"] = "#333333"
        self.GLabel_544["justify"] = "center"
        self.GLabel_544["text"] = "label"
        self.GLabel_544.place(x=20, y=160, width=298, height=339)

    def calculateOee(self):
        availableHrs_str = self.getAvailableHours()
        availableHrs_parts = availableHrs_str.split(':')
        available_hours = int(availableHrs_parts[0])
        available_minutes = int(availableHrs_parts[1])
        available_seconds = int(availableHrs_parts[2])

        availableHrs = available_hours + \
            (available_minutes / 60) + (available_seconds / 3600)

        productiveHrs = self.calculate_total_productive_time().total_seconds() / \
            3600  # Convert timedelta to hours

        if availableHrs > 0:  # Make sure availableHrs is greater than 0 to avoid division by zero
            oee_percentage = (productiveHrs / availableHrs) * 100
            return round(oee_percentage, 5)
        else:
            return 0

    def format_time(self, seconds):
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        seconds = int(seconds % 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    def getAvailableHours(self):
        data = []
        with open('logs/logs.csv', 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                data.append(row)

        total_available_seconds = 0
        previous_event_time = None

        for event in data:
            event_type = event[0]
            event_date = event[1]
            event_time = event[2]

            event_datetime = datetime.strptime(
                event_date + " " + event_time, "%Y-%m-%d %H:%M:%S")

            if previous_event_time and event_type == "OFFLINE":
                time_difference = event_datetime - previous_event_time
                total_available_seconds += time_difference.total_seconds()

            previous_event_time = event_datetime

        if not any(event[0].startswith("OFFLINE") for event in data):
            current_datetime = datetime.now()
            if previous_event_time:
                time_difference = current_datetime - previous_event_time
            else:
                time_difference = current_datetime - \
                    datetime.strptime("2000-01-01 00:00:00",
                                      "%Y-%m-%d %H:%M:%S")
            total_available_seconds += time_difference.total_seconds()

        formatted_time = self.format_time(total_available_seconds)
        return formatted_time
    


    def update_status(self):
        script_directory = os.path.dirname(os.path.abspath(__file__))
        log_folder = os.path.join(script_directory, "logs")
        # Change extension to .csv
        log_file_path = os.path.join(log_folder, 'logs.csv')

        try:
            with open(log_file_path, 'r') as file:
                csv_reader = csv.reader(file)
                last_row = None
                for row in csv_reader:
                    last_row = row
                if last_row:
                    # Get the first value from the last row
                    last_value = last_row[0]
                    self.logs_message = tk.Message(root)
                    self.logs_message["bg"] = "#e0bdbd"
                    self.ft = tkFont.Font(family='Times', size=10)
                    self.logs_message["font"] = self.ft
                    self.logs_message["fg"] = "#333333"
                    self.logs_message["justify"] = "center"
                    self.logs_message['width'] = 200
                    self.logs_message["text"] = last_value
                    self.logs_message.place(x=20, y=20, width=284, height=51)
                else:
                    pass
        except FileNotFoundError as e:
            print(e)
        root.after(50000, self.update_status)

    def oee(self):
        script_directory = os.path.dirname(os.path.abspath(__file__))
        log_folder = os.path.join(script_directory, "logs")
        # Change extension to .csv
        log_file_path = os.path.join(log_folder, 'logs.csv')

        try:
            with open(log_file_path, 'r') as file:
                csv_reader = csv.reader(file)
                last_row = None
                for row in csv_reader:
                    last_row = row
                if last_row:
                    # Get the first value from the last row

                    label = f"""
                    1. PRODUCTIVE HOURS: {self.calculate_total_productive_time()} HOURS
                    2. AVAILABLE HOURS: {self.getAvailableHours()} HOURS
                    3. QUANTITY TO PROCESS: ' ' PCS
                    4. TOTAL PROCESS: ' ' PCS
                    5. TARGET TOTAL ' ' PCS
                    """
                    self.GMessage_465 = tk.Message(root)
                    self.GMessage_465["bg"] = "#ffffff"
                    self.ft = tkFont.Font(family='Times', size=15)
                    self.GMessage_465["font"] = self.ft
                    self.GMessage_465["fg"] = "#333333"
                    self.GMessage_465["justify"] = "center"
                    self.GMessage_465['width'] = 800
                    self.GMessage_465["justify"] = "left"
                    self.GMessage_465["text"] = label
                    self.GMessage_465.place(x=20, y=540, width=642, height=337)
                else:
                    pass
        except FileNotFoundError as e:
            print(e)
        root.after(50000, self.oee)

sio.connect('http://10.0.2.150:9090')

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    root = tk.Tk()
    app = App(root)
    root.mainloop()
