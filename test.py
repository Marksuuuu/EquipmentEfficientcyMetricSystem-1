# import tkinter as tk
# from tkinter import ttk
# import requests

# class MyApp:
#     def __init__(self, root):
#         self.root = root
#         self.root.geometry("800x600")

#         self.dropdown_var = tk.StringVar()

#         self.fetch_downtime_types()
        
#         dropdown = ttk.Combobox(root, textvariable=self.dropdown_var, state="readonly")
#         dropdown["values"] = [item["DOWNTIME_TYPE"] for item in self.downtime_data]
#         dropdown.bind("<<ComboboxSelected>>", self.on_select)
#         dropdown.place(x=540, y=240, width=250, height=30)

#     def fetch_downtime_types(self):
#         cmms_url = 'http://cmms.teamglac.com/main_downtime_type.php'
#         response = requests.get(cmms_url)
#         data = response.json()
#         self.downtime_data = data["result"]

#     def on_select(self, event):
#         selected_text = self.dropdown_var.get()
#         selected_id = None
#         for item in self.downtime_data:
#             if item['DOWNTIME_TYPE'] == selected_text:
#                 selected_id = item['ID']
#                 break

#         if selected_id is not None:
#             print("Selected ID:", selected_id)
#             print("Selected Text:", selected_text)

# if __name__ == "__main__":
#     root = tk.Tk()
#     app = MyApp(root)
#     root.mainloop()



# import json
# import os
# import tkinter as tk
# import tkinter.font as tkFont
# import csv
# from datetime import datetime
# from io import BytesIO
# from tkinter import Toplevel
# from tkinter import messagebox
# from tkinter import simpledialog
# from tkinter import ttk
# from tkinter.messagebox import showinfo, showwarning, showerror

# import requests

# def getDownTimeType():
#     cmms_url = 'http://cmms.teamglac.com/main_downtime_type.php'
#     response = requests.get(cmms_url)
#     data = response.json()
#     result = data["result"]
#     id = []
#     downtime_type = []
#     if response.status_code == 200:
#         for item in result:
#             id.append(item['ID'])
#             downtime_type.append(item['DOWNTIME_TYPE'])
            
#     print(f"==>> id: {id}")
#     print(f"==>> downtime_type: {downtime_type}")
    
# getDownTimeType()


# import tkinter as tk
# import matplotlib.pyplot as plt
# from matplotlib.figure import Figure
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# from PIL import Image, ImageTk

# def create_donut_chart():
#     total = 100 - 17
#     data = [17, total]  # Example data
#     labels = ['Blue', 'Red']  # Example labels
#     colors = ['#3498db', '#e74c3c']  # Example colors
#     explode = (0.05, 0)  # "explode" the first slice for emphasis

#     figure = Figure(figsize=(5, 4), dpi=100)
#     plot = figure.add_subplot(1, 1, 1)
#     plot.pie(data, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90, pctdistance=0.85, explode=explode)

#     centre_circle = plt.Circle((0,0),0.70,fc='white')
#     plot.add_artist(centre_circle)
    
#     plot.axis('equal')

#     canvas = FigureCanvasTkAgg(figure, master=root)
#     canvas_widget = canvas.get_tk_widget()
    
#     # Convert FigureCanvasTkAgg to a PIL Image
#     canvas.draw()  # Render the canvas
#     pil_image = Image.frombytes('RGB', canvas.get_width_height(), canvas.tostring_rgb())
    
#     # Convert PIL Image to PhotoImage
#     img = ImageTk.PhotoImage(image=pil_image)
    
#     # Clear the previous contents of the Label (if any) and add the new chart
#     chart_label.config(image=img)
#     chart_label.image = img  # Keep a reference to prevent it from being garbage collected

# root = tk.Tk()
# root.title("Donut Chart in Tkinter")

# chart_label = tk.Label(root)
# chart_label.pack()

# create_donut_chart_button = tk.Button(root, text="Create Donut Chart", command=create_donut_chart)
# create_donut_chart_button.pack()

# root.mainloop()












# def show_input_dialog(self):
#     total_finished = simpledialog.askstring(
#         "Enter Total Number of finished",
#         "Please enter the total number of finish items",
#     )

#     if total_finished is not None and total_finished.strip() != "":
#         total_finished = int(total_finished)

#         with open("data/mo_logs.json", "r") as logs_file:
#             logs_data = json.load(logs_file)

#         wip_entity_name = self.extracted_wip_entity_name  # Assuming you have this value available

#         found_entry = None
#         for entry in logs_data:
#             if entry["wip_entity_name"] == wip_entity_name:
#                 found_entry = entry
#                 break

#         if found_entry:
#             found_entry["total_finished"] += total_finished
#         else:
#             new_entry = {
#                 "wip_entity_name": wip_entity_name,
#                 "running_qty": extracted_running_qty,
#                 "total_finished": total_finished
#             }
#             logs_data.append(new_entry)

#         with open("data/mo_logs.json", "w") as logs_file:
#             json.dump(logs_data, logs_file, indent=4)

#         self.start_btn["state"] = "normal"
#         self.log_event('START')

# from datetime import datetime

# data = [
#     "ONLINE,2023-08-23,17:14:43",
#     "OFFLINE,2023-08-25,20:19:14"
# ]

# total_available_hours = 0

# for i in range(0, len(data), 2):
#     online_data = data[i].split(",")
#     offline_data = data[i+1].split(",")

#     online_datetime = datetime.strptime(online_data[1] + " " + online_data[2], "%Y-%m-%d %H:%M:%S")
#     offline_datetime = datetime.strptime(offline_data[1] + " " + offline_data[2], "%Y-%m-%d %H:%M:%S")

#     time_difference = offline_datetime - online_datetime
#     total_available_hours += time_difference.total_seconds() / 3600

# print("Total available hours:", total_available_hours)

# import csv
# from datetime import datetime

# def format_time(seconds):
#     hours = int(seconds // 3600)
#     minutes = int((seconds % 3600) // 60)
#     seconds = int(seconds % 60)
#     return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

# def getAvailableHours():
#     data = []
#     with open('logs/logs.csv', 'r') as csvfile:
#         csvreader = csv.reader(csvfile)
#         for row in csvreader:
#             data.append(row)

#     total_available_seconds = 0
#     previous_event_time = None

#     for event in data:
#         event_type = event[0]
#         event_date = event[1]
#         event_time = event[2]
        
#         event_datetime = datetime.strptime(event_date + " " + event_time, "%Y-%m-%d %H:%M:%S")
        
#         if previous_event_time and event_type == "OFFLINE":
#             time_difference = event_datetime - previous_event_time
#             total_available_seconds += time_difference.total_seconds()
        
#         previous_event_time = event_datetime

#     if not any(event[0].startswith("OFFLINE") for event in data):
#         current_datetime = datetime.now()
#         if previous_event_time:
#             time_difference = current_datetime - previous_event_time
#         else:
#             time_difference = current_datetime - datetime.strptime("2000-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")
#         total_available_seconds += time_difference.total_seconds()

#     formatted_time = format_time(total_available_seconds)
#     return formatted_time

# total_available_time = getAvailableHours()
# print("Total available time:", total_available_time)














# Other methods and code for your class


# import json
# import requests

# def checking():
#     hris_url = 'http://lams.teamglac.com/lams/api/job_order/active_jo.php'
#     response = requests.get(hris_url)

#     if response.status_code == 200:
#         data = response.json()  # Parse JSON response
#         result = data['result']  # Access the 'result' key
#         res = ''
#         for x in result:
#             if x['MACH201_MACHNO'] == 'DAD 3350-01':
#                 res = x['MACH201_MACHNO']
#                 break
#         print(res)


#         # if result:
#         #     print('result: ', result)
#         #     target_value = "DAD 3350-01"
#         #     if target_value in result:
#         #         print(f'The value "{target_value}" is present in the result.')
#         #     else:
#         #         print(f'The value "{target_value}" is not present in the result.')
#         # else:
#         #     print('No data found in the result.')
#     else:
#         print('Request failed with status code:', response.status_code)

# checking()


# import csv
# from datetime import datetime, timedelta

# data = []
# # Read data from CSV file
# with open('data/time.csv', 'r') as csvfile:
#     csvreader = csv.reader(csvfile)
#     for row in csvreader:
#         data.append(tuple(row))

# productive_hours = {}
# start_time = None

# for action, date_str, time_str in data:
#     dt = datetime.strptime(date_str + " " + time_str, "%Y-%m-%d %H:%M:%S")

#     if action == "START":
#         start_time = dt
#     elif action == "STOP" and start_time is not None:
#         productive_time = dt - start_time
#         day = dt.date()
#         if day not in productive_hours:
#             productive_hours[day] = productive_time
#         else:
#             productive_hours[day] += productive_time
#         start_time = None

# total_productive_time = timedelta()

# for day, productive_time in productive_hours.items():
#     total_productive_time += productive_time

# print("Total productive time:", total_productive_time)


# import tkinter as tk
# from PIL import Image, ImageTk
# import requests
# from io import BytesIO

# class App:
#     def __init__(self, root):
#         root.title("Image Example")

#         # Fetch the image from a URL
#         image_url = "http://hris.teamglac.com/employeeInformation/photos/EMP2932/JOHN_RAYMARK_M._LLAVANES.JPG"  # Replace with your image URL
#         response = requests.get(image_url)

#         if response.status_code == 200:
#             pil_image = Image.open(BytesIO(response.content))
#             self.image = ImageTk.PhotoImage(pil_image)

#             # Create a label to display the image
#             self.image_label = tk.Label(root, image=self.image)
#             self.image_label.pack()
#         else:
#             print("Error fetching image:", response.status_code)

# if __name__ == "__main__":
#     root = tk.Tk()
#     app = App(root)
#     root.mainloop()

# import tkinter as tk
# from PIL import Image, ImageTk
# import requests
# from io import BytesIO
# import tkinter as tk
# import tkinter.font as tkFont

# class App:
#     def __init__(self, root):
#         #setting title
#         root.title("DASHBOARD")
#         #setting window size
#         width=1475
#         height=935
#         screenwidth = root.winfo_screenwidth()
#         screenheight = root.winfo_screenheight()
#         alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
#         root.geometry(alignstr)
#         root.resizable(width=False, height=False)

#         image_url = "http://hris.teamglac.com/employeeInformation/photos/EMP2932/JOHN_RAYMARK_M._LLAVANES.JPG"  # Replace with your image URL
#         response = requests.get(image_url)
#         pil_image = Image.open(BytesIO(response.content))
#         desired_width = 83
#         desired_height = 60
#         pil_image = pil_image.resize((desired_width, desired_height), Image.ANTIALIAS)

#         self.image = ImageTk.PhotoImage(pil_image)

#         GLabel_937=tk.Label(root)
#         GLabel_937["bg"] = "#ffffff"
#         ft = tkFont.Font(family='Times',size=10)
#         GLabel_937["font"] = ft
#         GLabel_937["fg"] = "#333333"
#         GLabel_937["justify"] = "center"
#         GLabel_937["text"] = "label"
#         GLabel_937.place(x=1190,y=0,width=281,height=60)

#         GLabel_831=tk.Label(root, image=self.image)
#         GLabel_831["bg"] = "#999999"
#         ft = tkFont.Font(family='Times',size=10)
#         GLabel_831["font"] = ft
#         GLabel_831["fg"] = "#333333"
#         GLabel_831["justify"] = "center"
#         GLabel_831["text"] = "label"
#         GLabel_831.place(x=1100,y=0,width=83,height=60)


# if __name__ == "__main__":
#     root = tk.Tk()
#     app = App(root)
#     root.mainloop()


# import os
# import json

# def checking_allowed_user():
#     script_directory = os.path.dirname(os.path.abspath(__file__))
#     log_folder = os.path.join(script_directory, "config")
#     log_file_path = os.path.join(log_folder, 'settings.json')
#     try:
#         with open(log_file_path) as json_file: 
#             data = json.load(json_file)
#             employee_departments = data["allowed_users"]["employee_department"]
#             employee_positions = data["allowed_users"]["employee_position"]
#     except FileNotFoundError as e:
#         print(e)

# checking_allowed_user()

# import requests

# def check_internet_connection():
#     try:
#         # Try making a simple HTTP GET request to a reliable website
#         response = requests.get("http://www.google.com", timeout=5)
#         return response.status_code == 200
#     except requests.ConnectionError:
#         return False

# if check_internet_connection():
#     print("Internet connection is active.")
# else:
#     print("No internet connection.")

# import json
# import os

# class UserPermissions:
#     def __init__(self, config_path):
#         self.config_path = config_path
#         self.employee_departments = []
#         self.employee_positions = []

#     def load_permissions(self):
#         try:
#             with open(self.config_path) as json_file:
#                 data = json.load(json_file)
#                 self.employee_departments = data["allowed_users"]["employee_department"]
#                 self.employee_positions = data["allowed_users"]["employee_position"]
#         except FileNotFoundError as e:
#             print(e)
#             self.employee_departments = []
#             self.employee_positions = []

#     def is_department_allowed(self, department):
#         return department in self.employee_departments

#     def is_position_allowed(self, position):
#         return position in self.employee_positions

# def check_employee_permissions(emp_id):
#     script_directory = os.path.dirname(os.path.abspath(__file__))
#     config_folder = os.path.join(script_directory, "config")
#     config_file_path = os.path.join(config_folder, 'settings.json')

#     permissions = UserPermissions(config_file_path)
#     permissions.load_permissions()

#     log_folder = os.path.join(script_directory, "config")
#     log_file_path = os.path.join(log_folder, 'hris.json')

#     with open(log_file_path, "r") as json_file:
#         data = json.load(json_file)['result']

#     matching_employee = None
#     for employee in data:
#         if employee.get('employee_id_no') == emp_id:
#             matching_employee = employee
#             break

#     if matching_employee:
#         user_department = matching_employee.get('employee_department')
#         user_position = matching_employee.get('employee_position')

#         if user_department and user_position:
#             if permissions.is_department_allowed(user_department) and permissions.is_position_allowed(user_position):
#                 return "User's department and position are allowed."
#             else:
#                 return "User's department or position is not allowed."
#         else:
#             return "User's department or position information missing."
#     else:
#         return "Employee not found."

# # Example usage
# employee_id = "003091"
# result = check_employee_permissions(employee_id)
# print(result)

# import tkinter as tk
# from tkinter import ttk
# from PIL import Image, ImageTk
# import requests
# from io import BytesIO
# import tkinter.font as tkFont
# import os
# import csv
# import json
# from tkinter import Toplevel
# from tkinter import messagebox
# from tkinter import simpledialog
# from tkinter.messagebox import showinfo, showwarning, showerror
# import logging
# import datetime



# class MO_Details:
#     def __init__(self,root,extracted_fullname,extracted_employee_no,extracted_photo_url,extracted_username,data):
#         #setting title
#         root.title("MO")
#         #setting window size
#         width=1264
#         height=675
#         screenwidth = root.winfo_screenwidth()
#         screenheight = root.winfo_screenheight()
#         alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
#         root.geometry(alignstr)
#         root.resizable(width=False, height=False)
        
#         self.root = root
#         self.extracted_employee_no = extracted_employee_no
#         self.extracted_photo_url = extracted_photo_url
#         self.extracted_username = extracted_username
#         self.root.title("MO DETAILS")
#         self.test_data = data

#         # self.remaining_qty = None
#         self.data_dict = {}
        
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

#         GLabel_932=tk.Label(root)
#         GLabel_932["bg"] = "#ffffff"
#         ft = tkFont.Font(family='Times',size=18)
#         GLabel_932["font"] = ft
#         GLabel_932["fg"] = "#333333"
#         GLabel_932["justify"] = "center"
#         GLabel_932["text"] = f"Device : {data[2]}"
#         GLabel_932.place(x=20,y=180,width=526,height=97)

#         GLabel_771=tk.Label(root)
#         GLabel_771["bg"] = "#ffffff"
#         ft = tkFont.Font(family='Times',size=18)
#         GLabel_771["font"] = ft
#         GLabel_771["fg"] = "#333333"
#         GLabel_771["justify"] = "center"
#         GLabel_771["text"] = f"Package : {data[4]}"
#         GLabel_771.place(x=20,y=300,width=526,height=97)

#         GLabel_146=tk.Label(root)
#         GLabel_146["bg"] = "#ffffff"
#         ft = tkFont.Font(family='Times',size=18)
#         GLabel_146["font"] = ft
#         GLabel_146["fg"] = "#333333"
#         GLabel_146["justify"] = "center"
#         GLabel_146["text"] = f"Customer : {data[1]}"
#         GLabel_146.place(x=20,y=420,width=526,height=97)

#         GLabel_915=tk.Label(root)
#         GLabel_915["bg"] = "#ffffff"
#         ft = tkFont.Font(family='Times',size=18)
#         GLabel_915["font"] = ft
#         GLabel_915["fg"] = "#333333"
#         GLabel_915["justify"] = "center"
#         GLabel_915["text"] = f"MO Quantity : {data[5]}"
#         GLabel_915.place(x=20,y=540,width=526,height=97)

#         GLabel_514=tk.Label(root)
#         ft = tkFont.Font(family='Times',size=24)
#         GLabel_514["font"] = ft
#         GLabel_514["fg"] = "#333333"
#         GLabel_514["justify"] = "center"
#         GLabel_514["text"] = extracted_fullname
#         GLabel_514.place(x=820,y=20,width=424,height=87)

#         GLabel_978=tk.Label(root, image=self.image)
#         ft = tkFont.Font(family='Times',size=10)
#         GLabel_978["font"] = ft
#         GLabel_978["fg"] = "#333333"
#         GLabel_978["justify"] = "center"
#         GLabel_978["text"] = "img"
#         GLabel_978.place(x=680,y=20,width=120,height=87)

#         self.start_btn=tk.Button(root)
#         self.start_btn["bg"] = "#5fb878"
#         ft = tkFont.Font(family='Times',size=23)
#         self.start_btn["font"] = ft
#         self.start_btn["fg"] = "#ffffff"
#         self.start_btn["justify"] = "center"
#         self.start_btn["text"] = "START"
#         self.start_btn.place(x=1000,y=540,width=245,height=97)
#         self.start_btn["command"] = self.start_command

#         self.stop_btn=tk.Button(root)
#         self.stop_btn["bg"] = "#cc0000"
#         ft = tkFont.Font(family='Times',size=23)
#         self.stop_btn["font"] = ft
#         self.stop_btn["fg"] = "#f9f9f9"
#         self.stop_btn["justify"] = "center"
#         self.stop_btn["text"] = "STOP"
#         self.stop_btn.place(x=1000,y=430,width=245,height=97)
#         self.stop_btn["state"] = "disabled"  
#         self.stop_btn["command"] = self.stop_command

#         GLabel_65=tk.Label(root)
#         GLabel_65["bg"] = "#ffffff"
#         GLabel_65["borderwidth"] = "2px"
#         ft = tkFont.Font(family='Times',size=58)
#         GLabel_65["font"] = ft
#         GLabel_65["fg"] = "#333333"
#         GLabel_65["justify"] = "center"
#         GLabel_65["text"] =  data[6]
#         GLabel_65.place(x=20,y=20,width=526,height=87)

#         GLabel_566=tk.Label(root)
#         ft = tkFont.Font(family='Times',size=11)
#         GLabel_566["font"] = ft
#         GLabel_566["fg"] = "#333333"
#         GLabel_566["justify"] = "center"
#         GLabel_566["text"] = "PERSON ASSIGNED"
#         GLabel_566.place(x=820,y=80,width=424,height=30)


#         lbl_remaining_qty=tk.Label(root)
#         lbl_remaining_qty["bg"] = "#ffffff"
#         ft = tkFont.Font(family='Times',size=18)
#         lbl_remaining_qty["font"] = ft
#         lbl_remaining_qty["fg"] = "#333333"
#         lbl_remaining_qty["justify"] = "center"
#         # lbl_remaining_qty["text"] = f"Remaining MO Quantity : "
#         # lbl_remaining_qty["text"] = f"Remaining MO Quantity : ", lbl_remaining_qty
#         self.lbl_remaining_qty = lbl_remaining_qty
#         lbl_remaining_qty.place(x=450,y=540,width=526,height=97)

#         self.get_remaining_qty_from_logs()

#     def get_remaining_qty_from_logs(self):
#         try:
#             with open("data/mo_logs.json", "r") as json_file:
#                 data = json.load(json_file)
#                 if "data" in data and isinstance(data["data"], list):
#                     remaining_qty = 0
#                     for entry in data["data"]:
#                         if "remaining_qty" in entry:
#                             remaining_qty += entry["remaining_qty"]
                    
#                     self.lbl_remaining_qty["text"] = f"Remaining MO Quantity: {remaining_qty}"
#                 else:
#                     self.lbl_remaining_qty["text"] = "Remaining MO Quantity: N/A"
#         except FileNotFoundError:
#             self.lbl_remaining_qty["text"] = "Remaining MO Quantity: N/A"


#     def log_event(self, msg):
#         current_time = datetime.datetime.now()
#         date = current_time.strftime('%Y-%m-%d')
#         time = current_time.strftime('%H:%M:%S')

#         with open(self.csv_file_path, mode='a', newline='') as csv_file:
#             csv_writer = csv.writer(csv_file)
#             csv_writer.writerow([msg, date, time ])

#     def start_command(self):
#         # self.checking()
#         print("START button clicked")
#         self.log_event('START')
#         self.start_btn["state"] = "disabled"  # Disable the START button
#         self.stop_btn["state"] = "normal"  # Enable the STOP button

#     def stop_command(self):
#         print("STOP button clicked")
#         self.show_input_dialog()



#     def read_machno(self):
#         with open("data\main.json", "r") as json_file:
#             data = json.load(json_file)
#             extracted_data = []
#             extracted_machno = data["machno"]
#         return extracted_machno
    
#     def checking(self):
#         hris_url = "http://lams.teamglac.com/lams/api/job_order/active_jo.php"
#         response = requests.get(hris_url)

#         if response.status_code == 200:
#             data = response.json()  # Parse JSON response
#             result = data["result"]  # Access the 'result' key
#             res = ""
#             for x in result:
#                 if x["MACH201_MACHNO"] == self.read_machno():
#                     res = 1
#                     break
#             if res == 1:
#                 showwarning("TICKET ALERT!", "Attention! The machine is temporarily unavailable.")
#                 self.stop_btn["state"] = "disabled"
#             else:
#                 self.start_btn["state"] = "normal"

#     def show_input_dialog(self):
#         total_finished = simpledialog.askstring(
#             "Enter Total Number of finished",
#             "Please enter the total number of finish items",
#         )

#         if total_finished is not None and total_finished.strip() != "":
#             total_finished = int(total_finished)

#             with open("data/main.json", "r") as json_file:
#                 data = json.load(json_file)

#                 for item in data["data"]:
#                     customer = item["customer"]
#                     device = item["device"]
#                     main_opt = item["main_opt"]
#                     package = item["package"]
#                     running_qty = item["running_qty"]
#                     wip_entity_name = item["wip_entity_name"]

#                     extracted_running_qty = int(running_qty)

#                 if wip_entity_name in self.data_dict:
#                     current_total_finished = self.data_dict[wip_entity_name]["total_finished"]
                    
#                     if current_total_finished + total_finished <= extracted_running_qty:
#                         if current_total_finished + total_finished == extracted_running_qty:
#                             print("DONE")
#                             self.start_btn["state"] = "disabled"
#                             self.stop_btn["state"] = "disabled"
#                         else:
#                             self.start_btn["state"] = "normal"
#                             self.stop_btn["state"] = "disabled"
#                         self.data_dict[wip_entity_name]["total_finished"] += total_finished
#                         self.data_dict[wip_entity_name]["remaining_qty"] -= total_finished
#                     else:
#                         messagebox.showinfo(title="Warning", message="Input exceeded the set running Quantity: " + str(extracted_running_qty))
#                         print("Total finished is not less than or equal to extracted running qty.")
#                 else:
#                     if total_finished <= extracted_running_qty:
#                         if total_finished == extracted_running_qty:
#                             print("DONE")
#                             self.start_btn["state"] = "disabled"
#                             self.stop_btn["state"] = "disabled"
#                         else:
#                             self.start_btn["state"] = "normal"
#                             self.stop_btn["state"] = "disabled"
#                         self.data_dict[wip_entity_name] = {
#                             "wip_entity_name": wip_entity_name,
#                             "running_qty": running_qty,
#                             "total_finished": total_finished,
#                             "remaining_qty": extracted_running_qty - total_finished
#                         }

#                     else:
#                         messagebox.showinfo(title="Warning", message="Input exceeded the set running Quantity: " + str(extracted_running_qty))
#                         print("Total finished is not less than or equal to extracted running qty.")

#         with open("data/mo_logs.json", "w") as json_output_file:
    #             json.dump({"data": list(self.data_dict.values())}, json_output_file, indent=4)
