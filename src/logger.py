"""
File Logging
"""
import os
import time
import json
import datetime


class Logger:
    def __init__(self,path: str) -> None:
        self.__path = path


    def log(self,data: dict):
        # Change the order so that time shows first in json
        new_data = {}
        new_data["time"] = datetime.datetime.now().isoformat()
        for k,v in data.items():
            new_data[k] = v
        # Possibly support more than one file format
        self.log_json(new_data)
    

    
    def log_json(self,data):
        with open(self.__path,'a') as f:
            json.dump(data,f) 
            f.write("\n")