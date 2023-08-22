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
from request_ticket import RequestTicket
from tkinter import messagebox
from tkinter import simpledialog
from tkinter.messagebox import showinfo, showwarning, showerror


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
                print(new_data_count)

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
                "MAIN OPERATION",
                "SUB-OPERATION",
                "WIP ENTITY NAME",
            ),
        )
        self.tree.heading("ROW NUMBER", text="ROW NUMBER")
        self.tree.heading("MAIN OPERATION", text="MAIN OPERATION")
        self.tree.heading("SUB-OPERATION", text="SUB-OPERATION")
        self.tree.heading("WIP ENTITY NAME", text="WIP ENTITY NAME")
        self.tree.pack(pady=120)

        self.populate_table()

        self.tree.bind("<Double-1>", self.show_popup_view)

    def populate_table(self):
        data = self.read_json_file()

        for i, (main_op, sub_op, wip_entity) in enumerate(data, start=1):
            self.tree.insert(
                "", "end", iid=i, text=str(i), values=(i, main_op, sub_op, wip_entity)
            )

    def read_json_file(self):
        with open("data\main.json", "r") as json_file:
            data = json.load(json_file)
            extracted_data = []

            for item in data["data"]:
                main_op = item["main_opt"]
                sub_op = item["sub_opt"]
                wip_entity = item["wip_entity_name"]
                extracted_data.append((main_op, sub_op, wip_entity))

        return extracted_data
    
    def show_popup_view(self, event):
                #setting title
        self.root.title("undefined")
        #setting window size
        width=985
        height=482
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.root.geometry(alignstr)
        self.root.resizable(width=False, height=False)

        GButton_715=tk.Button(self.root)
        GButton_715["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        GButton_715["font"] = ft
        GButton_715["fg"] = "#000000"
        GButton_715["justify"] = "center"
        GButton_715["text"] = "Button"
        GButton_715.place(x=820,y=390,width=155,height=77)
        GButton_715["command"] = self.GButton_715_command

        GLabel_690=tk.Label(self.root)
        GLabel_690["bg"] = "#ffffff"
        ft = tkFont.Font(family='Times',size=10)
        GLabel_690["font"] = ft
        GLabel_690["fg"] = "#333333"
        GLabel_690["justify"] = "center"
        GLabel_690["text"] = "label"
        GLabel_690.place(x=20,y=110,width=487,height=65)

        GLabel_898=tk.Label(self.root)
        GLabel_898["bg"] = "#fbfbfb"
        ft = tkFont.Font(family='Times',size=10)
        GLabel_898["font"] = ft
        GLabel_898["fg"] = "#333333"
        GLabel_898["justify"] = "center"
        GLabel_898["text"] = "label"
        GLabel_898.place(x=20,y=210,width=487,height=65)

        GLabel_961=tk.Label(self.root)
        GLabel_961["bg"] = "#ffffff"
        ft = tkFont.Font(family='Times',size=10)
        GLabel_961["font"] = ft
        GLabel_961["fg"] = "#333333"
        GLabel_961["justify"] = "center"
        GLabel_961["text"] = "label"
        GLabel_961.place(x=20,y=310,width=487,height=65)

        GLabel_417=tk.Label(self.root)
        GLabel_417["bg"] = "#fbfbfb"
        ft = tkFont.Font(family='Times',size=10)
        GLabel_417["font"] = ft
        GLabel_417["fg"] = "#333333"
        GLabel_417["justify"] = "center"
        GLabel_417["text"] = "label"
        GLabel_417.place(x=600,y=10,width=82,height=50)

        GLabel_593=tk.Label(self.root)
        GLabel_593["bg"] = "#fefefe"
        ft = tkFont.Font(family='Times',size=10)
        GLabel_593["font"] = ft
        GLabel_593["fg"] = "#333333"
        GLabel_593["justify"] = "center"
        GLabel_593["text"] = "label"
        GLabel_593.place(x=700,y=10,width=273,height=50)

    def GButton_715_command(self):
        print("command")
    # def show_popup_view(self, event):
        selected_item = self.tree.selection()

        if not selected_item:
            showinfo(title="Error", message="No data selected.")
            return

        item = self.tree.item(selected_item)
        data = item["values"]

        if selected_item[0] == "1":
            data_details_window = tk.Toplevel(self.root)
            data_details_window.title("Item Details")
            # setting window size
            data_details_window.geometry("500x500")

            label_mo = tk.Label(
                data_details_window,
                text=f"Main Operation: {data[1]}",
                font=("Helvetica 12"),
            )
            label_mo.pack(pady=5)

            label_customer = tk.Label(
                data_details_window,
                text=f"Sub-Operation: {data[2]}",
                font=("Helvetica 12"),
            )
            label_customer.pack(pady=5)

            label_device = tk.Label(
                data_details_window,
                text=f"WIP Entity Name: {data[3]}",
                font=("Helvetica 12"),
            )
            label_device.pack(pady=5)

            # Create a frame for buttons
            button_frame = tk.Frame(data_details_window)
            # button_frame.pack(side="right", padx=10)
            button_frame.pack(pady=10)

            # Create the "Start" button
            self.start = tk.Button(button_frame)
            self.start["bg"] = "#4f9c64"
            ft = tkFont.Font(family="Times", size=13)
            self.start["font"] = ft
            self.start["fg"] = "#ffffff"
            self.start["justify"] = "center"
            self.start["text"] = "START"
            self.start["relief"] = "flat"
            self.start["command"] = self.start_command
            self.start.grid(row=0, column=0, padx=10)  # Use grid instead of pack

            # Create the "Stop" button
            self.stop = tk.Button(button_frame)
            self.stop["bg"] = "#e04949"
            ft = tkFont.Font(family="Times", size=13)
            self.stop["font"] = ft
            self.stop["fg"] = "#ffffff"
            self.stop["justify"] = "center"
            self.stop["text"] = "STOP"
            self.stop["relief"] = "flat"
            self.stop["command"] = lambda: self.stop_command(data)
            self.stop.grid(row=0, column=1, padx=10)  # Use grid instead of pack
            self.stop.grid_remove()

            # self.creator.grab_set()

            data_details_window.mainloop()

        else:
            self.validate_offline_employee()
            self.swap_position(selected_item)

    def start_command(self):
        self.checking()
        print("Stop button displayed")

    def stop_command(self, data):
        print(data)
        self.stop.grid_remove()  # Remove the stop button
        self.start.grid()  # Display the start button
        print("Start button displayed")

        total_finished_str = simpledialog.askstring(
            "Enter Total Number of finished",
            "Please enter the total number of finish items",
        )

        # if total_finished_str is not None and total_finished_str.strip() != "":
        #     total_finished = int(total_finished_str)
        #     self.start.grid_remove()
        #     self.stop.grid()
        #     dataPass = data[4]

        #     # Ensure dataPass is an integer
        #     dataPass = int(dataPass)

        #     if total_finished > dataPass:
        #         print('True')
        #     else:
        #         print('False')

        #     showinfo('Notice', f'Total Finished.. inputted by {self.employee_number}')
        # else:
        #     showwarning('Error', 'Invalid input. Buttons not changed.')

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
            print("User allowed.")
        else:
            showerror(
                title="Login Failed",
                message=f"User's department or position is not allowed. Please check, Current Department / Possition  {user_department}",
            )

    def swap_position(self, selected_item):
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
            data_list[int(selected_id) - 1]["main_opt"],
            data_list[int(first_id) - 1]["main_opt"],
        ) = (first_data[1], selected_data[1])
        (
            data_list[int(selected_id) - 1]["sub_opt"],
            data_list[int(first_id) - 1]["sub_opt"],
        ) = (first_data[2], selected_data[2])
        (
            data_list[int(selected_id) - 1]["wip_entity_name"],
            data_list[int(first_id) - 1]["wip_entity_name"],
        ) = (first_data[3], selected_data[3])

        # Update the JSON data
        data["data"] = data_list

        # Save the updated JSON data
        with open("data/main.json", "w") as json_file:
            json.dump(data, json_file, indent=4)

        # Update the values of the Treeview rows
        self.tree.item(
            selected_item,
            values=(selected_id, first_data[1], first_data[2], first_data[3]),
        )
        self.tree.item(
            first_id,
            values=(first_id, selected_data[1], selected_data[2], selected_data[3]),
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

    def logout(self):
        response = messagebox.askyesno("Logout", "Are you sure you want to logout?")
        if response:
            self.root.destroy()  # Close the current root window
            os.system("python main.py")  # Start the login.py file


if __name__ == "__main__":
    root = tk.Tk()
    dashboard = OperatorDashboard(root, user_department, user_position, dataJson)
    root.mainloop()  # Start the Tkinter main loop
