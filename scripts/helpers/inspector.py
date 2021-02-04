import re
import signal

from pathlib import Path
from helpers.util import echo, execute_sys_command


LOG_DIR = Path("./logs/").resolve()

class Inspector:

    CPU = "cpu"
    MEMORY = "memory"
    DISK = "disk"
    POWER = "power"

    METRICS = [
        CPU,
        MEMORY,
        DISK
    ]

    COMMAND = {
        CPU : "sar -u 1",
        MEMORY : "sar -r 1",
        DISK : "sar -b 1",
        POWER : "powerstat -R -d 0"
    }

    OUTPUT_PATTERN_BY_METRIC = { 
        CPU : { "pattern" : r"Average:.*all\s+([0-9.]+)", "match_group" : 1 },
        MEMORY : { "pattern" : r"Average:(\s+[0-9]+){3}\s+([0-9.]+)", "match_group" : 2 },
        DISK : { "pattern" : r"Average:\s+([0-9]+.[0-9]+)", "match_group" : 1 },
        POWER : { "pattern" : r"CPU:(.*)Watts", "match_group" : 1 }
    }
    

    def __init__(self):
        super().__init__()
        self.procs = []

        # Prepare log storage directory if it doesn't already exist
        Path(LOG_DIR).mkdir(parents=True, exist_ok=True)


    def start(self, msg_queue, results_queue):
        echo("Starting system inspection")

        for metric in Inspector.METRICS:
            filename = self.__getLogFileNameFor(metric)

            with open(filename, "w") as f:
                self.procs.append(execute_sys_command("exec {}".format(Inspector.COMMAND[metric]), f))

        msg_queue.get() # wait for stop notification

        self.stop()
        echo ("Inspection stopped")

        msg_queue.task_done()

        echo ("Sending inspection result")
        results_queue.put(self.__stats())

    def stop(self):

        for proc in self.procs:
            proc.send_signal(signal.SIGINT) # can't call terminate() function; calling terminate will kill the process but we wan't the avg values that are returned after Ctrl + C

            proc.wait() # wait for the process to end

        # TODO : the new process spinned off is not getting terminated; have to look into ways to kill it
        # raise KeyboardInterrupt("Ctrl + C")

        
    def __stats(self):

        stats = {}

        for metric in Inspector.METRICS:
            stats[metric] = self._getStatFor(metric)

        return stats

    def _getStatFor(self, metric):

        filename = self.__getLogFileNameFor(metric)

        result = None
        
        with open(filename, "r") as f:
            data = f.read()

            match = re.search(Inspector.OUTPUT_PATTERN_BY_METRIC[metric]["pattern"], data)
            if match is None:
                echo ("Not enough statistics to gather {}".format(metric))
            else:
                result = match.group(Inspector.OUTPUT_PATTERN_BY_METRIC[metric]["match_group"]).strip()

        return result

    def __getLogFileNameFor(self, metric):
        return Path(LOG_DIR).joinpath("raw_{}_log.txt".format(metric)).resolve()
