import tkinter as tk
import tkinter.font as tkFont
import logging
import os
import datetime
import csv

class App:
    def __init__(self, root):
        root.title("undefined")
        width = 235
        height = 190
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        script_directory = os.path.dirname(os.path.abspath(__file__))
        self.log_folder = os.path.join(script_directory, "logs")
        if not os.path.exists(self.log_folder):
            os.makedirs(self.log_folder)
        self.csv_file_path = os.path.join(self.log_folder, 'logs.csv')

        self.log_event('ONLINE')

        root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        self.log_event('OFFLINE')
        root.destroy()

    def log_event(self, message):
        current_time = datetime.datetime.now()
        date = current_time.strftime('%Y-%m-%d')
        time = current_time.strftime('%H:%M:%S')

        with open(self.csv_file_path, mode='a', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([message, date, time ])

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
