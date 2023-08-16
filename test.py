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

import tkinter as tk
from PIL import Image, ImageTk
import requests
from io import BytesIO
import tkinter as tk
import tkinter.font as tkFont

class App:
    def __init__(self, root):
        #setting title
        root.title("DASHBOARD")
        #setting window size
        width=1475
        height=935
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)
        
        image_url = "http://hris.teamglac.com/employeeInformation/photos/EMP2932/JOHN_RAYMARK_M._LLAVANES.JPG"  # Replace with your image URL
        response = requests.get(image_url)
        pil_image = Image.open(BytesIO(response.content))
        desired_width = 83
        desired_height = 60
        pil_image = pil_image.resize((desired_width, desired_height), Image.LANCZOS)
        
        self.image = ImageTk.PhotoImage(pil_image)
        
        GLabel_937=tk.Label(root)
        GLabel_937["bg"] = "#ffffff"
        ft = tkFont.Font(family='Times',size=10)
        GLabel_937["font"] = ft
        GLabel_937["fg"] = "#333333"
        GLabel_937["justify"] = "center"
        GLabel_937["text"] = "label"
        GLabel_937.place(x=1190,y=0,width=281,height=60)

        GLabel_831=tk.Label(root, image=self.image)
        GLabel_831["bg"] = "#999999"
        ft = tkFont.Font(family='Times',size=10)
        GLabel_831["font"] = ft
        GLabel_831["fg"] = "#333333"
        GLabel_831["justify"] = "center"
        GLabel_831["text"] = "label"
        GLabel_831.place(x=1100,y=0,width=83,height=60)
        
        
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()












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





