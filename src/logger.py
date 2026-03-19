"""
File Logging
"""
import json
import datetime
from dataclasses import asdict

from data_classes import Data, CPUData, MemoryData, DiskData

class Logger:
    def __init__(self,path: str) -> None:
        self.__path = path


    def log(self,data: Data):
        # Change the order so that time shows first in json
        new_data = {}
        new_data["time"] = datetime.datetime.now().isoformat()
        for k,v in asdict(data).items():
            new_data[k] = v
        # Possibly support more than one file format
        self.log_json(new_data)
    

    
    def log_json(self,data):
        with open(self.__path,'a') as f:
            json.dump(data,f) 
            f.write("\n")