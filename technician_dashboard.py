import json
import os
import tkinter as tk
import tkinter.font as tkFont
from io import BytesIO
from tkinter import messagebox

import requests
from PIL import Image, ImageTk


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

        data = dataJson['data']
        extracted_user_department = data[0]
        extracted_fullname = data[1]
        extracted_employee_no = data[2]
        extracted_employee_department = data[3]
        extracted_photo_url = data[4]
        extracted_possition = data[5]
        self.root = root
        self.checking()
        root.title(
            f"TECHNICIAN DASHBOARD - {extracted_employee_no} -- POSSITION - {extracted_possition}")

        root.title("undefined")

        width = 1663
        height = 986
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height,
                                    (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        if extracted_photo_url == False or extracted_photo_url is None:
            image_url = "https://www.freeiconspng.com/uploads/no-image-icon-15.png"
        else:

            image_url = f"http://hris.teamglac.com/{extracted_photo_url}"

        response = requests.get(image_url)
        pil_image = Image.open(BytesIO(response.content))
        desired_width = 83
        desired_height = 60
        pil_image = pil_image.resize(
            (desired_width, desired_height), Image.ANTIALIAS)

        self.image = ImageTk.PhotoImage(pil_image)

        ft = tk.font.Font(family='Times', size=14)

        self.operator_name = tk.Label(root)
        ft = tkFont.Font(family='Times', size=24)
        self.operator_name["font"] = ft
        self.operator_name["fg"] = "#333333"
        self.operator_name["justify"] = "center"
        self.operator_name["text"] = extracted_fullname
        self.operator_name.place(x=1220, y=20, width=424, height=87)

        self.operator_img = tk.Label(root, image=self.image)
        ft = tkFont.Font(family='Times', size=24)
        self.operator_img["font"] = ft
        self.operator_img["fg"] = "#333333"
        self.operator_img["justify"] = "center"
        self.operator_img["text"] = "img"
        self.operator_img.place(x=1070, y=20, width=120, height=87)

        self.ticket_show = tk.Message(root)
        self.ticket_show["bg"] = "#ffffff"
        ft = tkFont.Font(family='Times', size=23)
        self.ticket_show["font"] = ft
        self.ticket_show["fg"] = "#333333"
        self.ticket_show['width'] = 600
        self.ticket_show["text"] = f"Ticket: {self.ticket} : Status {self.ticket_status}"
        self.ticket_show["justify"] = "left"
        self.ticket_show.place(x=20, y=320, width=800, height=547)

        GButton_19 = tk.Button(root)
        GButton_19["bg"] = "#cc0000"
        ft = tkFont.Font(family='Times', size=18)
        GButton_19["font"] = ft
        GButton_19["fg"] = "#ffffff"
        GButton_19["justify"] = "center"
        GButton_19["text"] = "LOGOUT"
        GButton_19.place(x=1530, y=140, width=115, height=56)
        GButton_19["command"] = self.logout

        GMessage_474 = tk.Message(root)
        GMessage_474["bg"] = "#ffffff"
        ft = tkFont.Font(family='Times', size=23)
        GMessage_474["font"] = ft
        GMessage_474["fg"] = "#333333"
        GMessage_474["justify"] = "center"
        GMessage_474["text"] = "TICKET"
        GMessage_474.place(x=840, y=320, width=800, height=547)

    def read_machno(self):
        with open("data\main.json", "r") as json_file:
            data = json.load(json_file)
            extracted_data = []
            extracted_machno = data["machno"]
        return extracted_machno

    def checking(self):
        hris_url = "http://lams.teamglac.com/lams/api/job_order/active_jo.php"
        response = requests.get(hris_url)
        if response.status_code == 200:
            data = response.json()
            result = data["result"]
            res = 0
            machno_alerts = []
            machno_status = []
            for x in result:
                if x.get("MACH201_MACHNO") == self.read_machno():
                    res = 1

                    machno_alerts.append(x["DTNO"])

                    machno_status.append(x["STATUS"])
                    break
            if res == 1:

                self.machno_string = ", ".join(machno_alerts)
                self.machno_string_status = ", ".join(machno_status)
                print(
                    f"==>> machno_string_status: {self.machno_string_status}")
                print(f"==>> machno_string: {self.machno_string}")
                self.ticket = self.machno_string
                self.ticket_status = self.machno_string_status
                # if self.machno_status == False or self.machno_status is None and self.machno_alerts == False or self.machno_alerts is None:
                #     self.ticket = ''
                #     self.ticket_status = ''
                # else:
                #     self.ticket = self.machno_string
                #     self.ticket_status = self.machno_string_status

        self.root.after(15000, self.checking)

    def GButton_19_command(self):
        print("command")

    def logout(self):
        response = messagebox.askyesno(
            "Logout", "Are you sure you want to logout?")
        if response:
            self.root.destroy()  # Close the current root window
            os.system("python main.py")  # Start the login.py file


if __name__ == "__main__":
    root = tk.Tk()
    dashboard = TechnicianDashboard(
        root, user_department, user_position, dataJson)
    root.mainloop()
