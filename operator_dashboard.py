import json
import os
import tkinter as tk
import tkinter.font as tkFont
import csv
from datetime import datetime
from io import BytesIO
from tkinter import Toplevel
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import ttk
from tkinter.messagebox import showinfo, showwarning, showerror

import requests
from PIL import Image, ImageTk

from mo_details import MO_Details
from request_ticket import RequestTicket
from move_mo import MOData

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
            current_rows = current_content.strip().split("\n")
            previous_rows = self.previous_content.strip().split("\n")

            new_rows = len(current_rows) - len(previous_rows)
            if new_rows > 0:
                self.new_data_count += new_rows
                print(self.new_data_count)

            self.previous_content = current_content

        return self.new_data_count


class OperatorDashboard:
    def __init__(self, root, user_department, user_position, dataJson):
        data = dataJson["data"]
        self.extracted_user_department = data[0]
        self.extracted_fullname = data[1]
        self.extracted_employee_no = data[2]
        self.extracted_employee_department = data[3]
        self.extracted_photo_url = data[4]
        self.extracted_possition = data[5]
        self.extracted_username = data[6]
        self.root = root
        # setting title


        root.title(
            f"OPERATOR DASHBOARD - {self.extracted_employee_no} -- POSSITION - {self.extracted_possition}"
        )

        width = 1705
        height = 1000
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = "%dx%d+%d+%d" % (
            width,
            height,
            (screenwidth - width) / 2,
            (screenheight - height) / 2,
        )
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

        ft = tk.font.Font(family="Times", size=14)  # Use tk.font instead of tkFont

        request_ticket_btn = tk.Button(root)
        request_ticket_btn["bg"] = "#cc0000"
        request_ticket_btn["font"] = ft
        request_ticket_btn["fg"] = "#ffffff"
        request_ticket_btn["justify"] = "center"
        request_ticket_btn["text"] = "REQUEST TICKET"
        request_ticket_btn.place(x=10, y=0, width=172, height=44)
        request_ticket_btn["command"] = self.tickets_command

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

        logout_btn = tk.Button(root)
        logout_btn["bg"] = "#999999"
        logout_btn["cursor"] = "tcross"
        ft = tkFont.Font(family="Times", size=10)
        logout_btn["font"] = ft
        logout_btn["fg"] = "#333333"
        logout_btn["justify"] = "center"
        logout_btn["text"] = "LOGOUT"
        logout_btn["command"] = self.logout  # Use the logout method directly
        logout_btn.place(x=1620, y=70, width=66, height=37)

        self.tree = ttk.Treeview(
            root,
            show="headings",
            columns=(
                "ROW NUMBER",
                "CUSTOMER",
                "DEVICES",
                "MAIN OPERATION",
                "PACKAGE",
                "MO QUANTITY",
                "MO",
            ),
        )
        self.tree.heading("ROW NUMBER", text="ROW NUMBER")
        self.tree.heading("CUSTOMER", text="CUSTOMER")
        self.tree.heading("DEVICES", text="DEVICES")
        self.tree.heading("MAIN OPERATION", text="MAIN OPERATION")
        self.tree.heading("PACKAGE", text="PACKAGE")
        self.tree.heading("MO QUANTITY", text="MO QUANTITY")
        self.tree.heading("MO", text="MO")
        self.tree.pack(pady=120)

        self.populate_table()
        self.root.after(5000, self.update_table)

        self.update_status()

        self.tree.bind("<Double-1>", self.double_click_handler)




    def double_click_handler(self, event):
        if not self.getLastOfflineEntry():
            self.show_popup_view(event)
        # else:
        #     showinfo("Offline Alert", "Cannot perform action while offline.")

    def getLastOfflineEntry(self):
        last_offline_entry = None
        with open('logs/logs.csv', 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                if row[0] == "OFFLINE":
                    last_offline_entry = row

        if last_offline_entry:
            event_type, event_date, event_time = last_offline_entry[:3]
            event_datetime = datetime.strptime(
                f"{event_date} {event_time}", "%Y-%m-%d %H:%M:%S")
            print('last_offline_entry: ', last_offline_entry)
            showwarning(
                    "MACHINE OFFLINE!",
                    "Attention! The machine is currently OFFLINE",
                )
            return {
                "event_type": event_type,
                "event_datetime": event_datetime
            }
        else:
            return None


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
                    self.logs_message = tk.Message(self.root)
                    self.logs_message["bg"] = "#e0bdbd"
                    self.ft = tkFont.Font(family='Times', size=10)
                    self.logs_message["font"] = self.ft
                    self.logs_message["fg"] = "#333333"
                    self.logs_message["justify"] = "center"
                    self.logs_message['width'] = 200
                    self.logs_message["text"] = last_value
                    # self.logs_message.place(x=20, y=20, width=284, height=51)
                    self.logs_message.place(x=756, y=0, width=172, height=44)

                else:
                    pass
        except FileNotFoundError as e:
            print(e)
        self.root.after(5000, self.update_status)

    def populate_table(self):
        
        data = self.read_json_file()

        for i, (customer, device, main_opt, package, running_qty, wip_entity_name) in enumerate(data, start=1):
            self.tree.insert(
                "", "end", iid=i, text=str(i),
                values=(i, customer, device, main_opt, package, running_qty, wip_entity_name)
            )

    def update_table(self):
        # Clear existing data from the treeview
        self.tree.delete(*self.tree.get_children())
        
        # Call the populate_table function to fill the treeview with updated data
        self.populate_table()
        
        # Schedule the next update
        self.root.after(5000, self.update_table)

    def read_json_file(self):
        with open("data\main.json", "r") as json_file:
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

        return extracted_data

    def show_popup_view(self, event):
        selected_item = self.tree.selection()

        if not selected_item:
            showinfo(title="Error", message="No data selected.")
            return

        item = self.tree.item(selected_item)
        data = item["values"]

        if selected_item[0] == "1":
            # self.root.withdraw()
            self.show_mo_details(data)

        else:
            self.validate_offline_employee()

    def validate_offline_employee(self):
        log_file_path = os.path.join(self.get_script_directory(), "config", "hris.json")
        employee_number = simpledialog.askstring(
            "Employee ID", "Please enter your Employee ID."
        )
        with open(log_file_path, "r") as json_file:
            data = json.load(json_file)["result"]

        matching_employee = None
        for employee in data:
            if int(employee.get("employee_id_no")) == int(employee_number):
                matching_employee = employee
                break

        if matching_employee:
            user_department = matching_employee.get("employee_department")
            self.validate_permissions(user_department)
        else:
            print("Employee not found.")

    def validate_permissions(self, user_department):
        print(user_department)
        permissions = self.load_permissions()
        if permissions.is_department_allowed(user_department):
            selected_item = self.tree.selection()
            self.swap_position(selected_item)

            print("User allowed.")
        else:
            showerror(
                title="Login Failed",
                message=f"User's department or position is not allowed. {user_department}",
            )

    def swap_position(self, selected_item):
        print('selected_item: ', selected_item)

        selected_id = self.tree.item(selected_item, "text")
        first_id = "1"

        selected_data = self.tree.item(selected_item, "values")
        first_data = self.tree.item(first_id, "values")

        # Load data from the JSON file
        with open("data/main.json", "r") as json_file:
            data = json.load(json_file)

        # Swap data within the dictionaries
        data_list = data["data"]
        (
            data_list[int(selected_id) - 1]["customer"],
            data_list[int(first_id) - 1]["customer"],
        ) = (first_data[1], selected_data[1])
        (
            data_list[int(selected_id) - 1]["device"],
            data_list[int(first_id) - 1]["device"],
        ) = (first_data[2], selected_data[2])
        (
            data_list[int(selected_id) - 1]["main_opt"],
            data_list[int(first_id) - 1]["main_opt"],
        ) = (first_data[3], selected_data[3])
        (
            data_list[int(selected_id) - 1]["package"],
            data_list[int(first_id) - 1]["package"],
        ) = (first_data[4], selected_data[4])
        (
            data_list[int(selected_id) - 1]["running_qty"],
            data_list[int(first_id) - 1]["running_qty"],
        ) = (first_data[5], selected_data[5])
        (
            data_list[int(selected_id) - 1]["wip_entity_name"],
            data_list[int(first_id) - 1]["wip_entity_name"],
        ) = (first_data[6], selected_data[6])

        # Update the JSON data
        data["data"] = data_list

        # Save the updated JSON data
        with open("data/main.json", "w") as json_file:
            json.dump(data, json_file, indent=4)

        # Update the values of the Treeview rows
        self.tree.item(
            selected_item,
            values=(
            selected_id, first_data[1], first_data[2], first_data[3], first_data[4], first_data[5], first_data[6]),
        )
        self.tree.item(
            first_id,
            values=(first_id, selected_data[1], selected_data[2], selected_data[3], selected_data[4], selected_data[5],
                    selected_data[6]),
        )

        # Show a success message
        showinfo("Success", "Data swapped successfully!")

    def load_permissions(self):
        log_file_path = os.path.join(
            self.get_script_directory(), "config", "settings.json"
        )
        permissions = UserPermissions(log_file_path)
        permissions.load_permissions()
        return permissions

    def get_script_directory(self):
        return os.path.dirname(os.path.abspath(__file__))

    def tickets_command(self):
        # self.root.withdraw()
        self.ticket_dashboard = Toplevel(self.root)
        show_ticket_dashboard = RequestTicket(
            self.ticket_dashboard, self.extracted_fullname, self.extracted_employee_no
        )

    def show_mo_details(self, data):
        self.details_window = Toplevel(self.root)
        show_mo_details_window = MO_Details(self.details_window, self.extracted_fullname, self.extracted_employee_no,
                                            self.extracted_photo_url, self.extracted_username, data)

    def logout(self):
        response = messagebox.askyesno("Logout", "Are you sure you want to logout?")
        if response:
            self.root.destroy()  # Close the current root window
            os.system("python main.py")  # Start the login.py file


if __name__ == "__main__":
    root = tk.Tk()
    dashboard = OperatorDashboard(root, user_department, user_position, dataJson)
    root.mainloop()  # Start the Tkinter main loop
