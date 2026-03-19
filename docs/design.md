
## Main.py
The main file, handles argument parsing, main loop logic, starting and clean exiting.
This file is the project entry point.

### Arguments Parsing
The program has two keywords arguments:
 * Interval (float) - The amount of seconds between refreshes - Defaulting to 2.0, and values under 0.2 will be adjusted to 0.2
 * Log (str) - Path to log file. If not provided, logging is disabled.
The parser is written using the argparse library. 

### Starting
After creating the Display and Logger object, we use threading to display a progress bar while the data is gathered - To gather the cpu usage, we have to wait for interval seconds.
Note that the progress bar has to be in the main thread otherwise it don't fill up evenly and "skips" the animation, so we launch a thread to collect the data, and pass it back to the main thread using the DATA global variable.
Then we're ready to go into the main loop.

### Main Loop
Using the helper modules, the main loop is very clean and just consists of logging, updating and squaring new data.
Note that getting the new data, takes interval many seconds so there isn't an explicit call of sleep.

### Clean Exit
The entire loop is wrapped inside a try, except block to handle clean exit on Ctrl + C.
To make sure we free the resources, we call the shutdown function on app in a finally block, that called no matter what (even brutal exit). If the user excepts it using Ctrl + C then we first shutdown and than print exit cleanly message, and the shutdown function is called twice. This is harmless, and is used because it makes the exit look better in the terminal.

### Technical notes
In the specific use of threads in main, we don't have to use locks because the main thread access the global variable only after we join the thread.

## Data_classes.py
This file creates dataclasses used by all files for type hints and clarity.
CPUData is for the data related to the CPU.
MemoryData is for the data related to the memory.
DiskData is for the data related to a single disk. (mostly used in lists)
Data is nested dataclass, that contains all of above.

Before using dataclasses, I used dictionaries with specific keys, which was very messy and complicated. 



## Collector.py
This file contains static methods to gather required data using the psutil library.
All its functions return a specific dataclass as explained [here](#Data_classes.py)

### Insight
While writing collector.get_memory, i've noticed the the used + available is drastic different from the total amount of memory. (~ 5gb compared to ~8gb)

after researching specify about mac (which I am using) it is very common that apps like chrome have several GB of compressed data which isn't accounted for in the used/available fields.

## Display.py
This file uses the rich library to load all graphics including progress bar and in-place changing dashboard.
It contains a single class (Display) that lives through the entire lifespan of the program.
It's public function are called from main to control the graphics, and include ready,shutdown, update and load progress. All the rest of the functions are private and used to style the graphics.
Note that the Display class doesn't collect data on its own, on get it as arguments from the main file.

## Logger.py
This file is responsible for logging. 
It contains a single class (Logger) that lives through the entire lifespan of the program.
When the log function is called, it appends a new line to the path file with the json of the Data dataclass as a dictionary. If the file/path don't exist it creates them.
Note that the Logger class doesn't collect data on its own, on get it as arguments from the main file.

Problem - when writing the logger, i noticed that if i called the cpu_usage, it will halt. and the display will take twice as longer to update, because it calls cpu_usage twice (once from the logger and once from the display). 
Chosen Solution - 
* Change the architecture so that the main loop is in main, and the main file requests the data from the main file, and pass it as parameter to collector and logger. 

## Testing
For testing I am using pytest to inject mock function instead of the dependencies of the function that is being tested. 





sources:
https://stackoverflow.com/questions/48246674/group-multiple-pytest-cases-for-the-same-function - multiple tests with one function pytest
https://stackoverflow.com/questions/73098801/rich-center-a-renderable-in-layout - center object in rich using Align
https://docs.python.org/3/howto/argparse.html - argparse doc