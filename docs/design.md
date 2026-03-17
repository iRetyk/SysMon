

Architecture dits:

the var data refers to a dict in this format, that is used to pass cleanly all the required data to other modules

    {"cpu": <cpu_data>, "mem":<mem_data>, "disk":<disk_data>}
        cpu_data: (<per_cpu_percent>,<total>)
            per_cpu_percent: list[float]
            total: float
        mem_data: {"used":<used>,"total":<total>,"percent":<percent>}
            used: str
            total: str
            percent: float
        disk_data: [<disk_dict0>,<disk_dict1>...]
            disk_dict: {"mountpoint":<mountpoint>, "device":<device>, "used":<used>,"total":<total>,"percent":<percent>}
                mountpoint: str
                device : str
                used: str
                total: str
                percent: float


If an error occurred while trying to log (no permission etc), will print error message and continue to display the stats just without the logging.


I've noticed that loading the table for the first takes a few (interval) seconds, becuase it sleeps before loading, so I've added a progress bar to load at the same time with threads 

Problem - when writing the logger, i noticed that if i called the cpu_usage, it will halt. and the display will take twice as longer to update, because it calls cpu_usage twice (once from the logger and once from the display). 
Chosen Solution - 
* Change the architecture so that the main loop is in main, and the main file requests the data from the main file, and pass it as parameter to collector and logger. 


insights:

While writing collector.get_memory, i've noticed the the used + available is drasticly different from the total amount of memory. (~ 5gb compared to ~8gb)
With a little research ive seen that the gap consists mainly of OS reserved memory,  buffers and caches.
I am not satisfied with this answer (the gap is too big), and more research is due.  
after researching specify about mac (which am i using) it is very common that apps like chrome have several GB of compressed data which isn't accounted for in the used/available fields.






sources:
https://stackoverflow.com/questions/48246674/group-multiple-pytest-cases-for-the-same-function - multiple tests with one function pytest
https://stackoverflow.com/questions/73098801/rich-center-a-renderable-in-layout - center object in rich using Align
https://docs.python.org/3/howto/argparse.html - argparse doc