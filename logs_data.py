import os
import json

class LogsData:
    def __init__(self):
        self.total_running_qty()
        self.total_remaining_qty()

    def get_script_directory(self):
        return os.path.dirname(os.path.realpath(__file__))

    def total_running_qty(self):
        log_file_path = os.path.join(self.get_script_directory(), "data", 'mo_logs.json')

        with open(log_file_path, "r") as json_file:
            data = json.load(json_file)['data']
        
        total_running_qty = 0

        for item in data:
            running_qty = int(item['running_qty'])
            total_running_qty += running_qty
        
        # print("Total Running Quantity:", total_running_qty)
        return total_running_qty
        
    def total_remaining_qty(self):
        log_file_path = os.path.join(self.get_script_directory(), "data", 'mo_logs.json')

        with open(log_file_path, "r") as json_file:
            data = json.load(json_file)['data']
        
        total_remaining_qty = 0

        for item in data:
            total_finished = int(item['total_finished'])
            total_remaining_qty += total_finished
            
        # print("Total Running Quantity:", total_remaining_qty)
        return total_remaining_qty

if __name__ == "__main__":
    LogsData()
