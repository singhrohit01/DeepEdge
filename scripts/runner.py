# main class

from pathlib import Path
from queue import Queue

from helpers.db_connector import Connection
from helpers.db_push import push_stats
from helpers.util import echo, import_script_from_filename, read_JSON, write_JSON
from helpers.inspector import Inspector

import threading


class Runner:
    """ 
        Class uses config.json to configure a system that executes ML models and captures real time statistics
        The statistics are then pushed to the database
    """

    def __init__(self, workload, inspector):
        self.workload = workload
        self.inspector = inspector

    def run(self, batch_size):

        stats = []

        msg_queue = Queue() # message queue to establish a communication channel between the threads

        workload_results_queue = Queue() # capture results from the workload thread

        inspector_results_queue = Queue() # capture results from the workload thread

        for run_number in range(batch_size):

            echo ("Run #{}".format(run_number + 1))

            workloadThread = threading.Thread(
                target=self.workload.start,
                name="workload_thread",
                args=[msg_queue, workload_results_queue])

            inspectorThread = threading.Thread(
                target=self.inspector.start,
                name="inspector_thread",
                args=[msg_queue, inspector_results_queue])

            try:

                workloadThread.start()

                msg_queue.get() # waits until the model starts running; we can ignore the msg for now

                inspectorThread.start()

                msg_queue.task_done()   # notifies model that inspection has been started

                workload_result = workload_results_queue.get()
                workload_results_queue.task_done()

                inspector_stats = inspector_results_queue.get()
                inspector_results_queue.task_done()

                if len(workload_result) > 0:
                    stat = { **workload_result, **inspector_stats }

                    echo (stat)

                    stats.append(stat)

                raise KeyboardInterrupt("Ctrl + C")

            except KeyboardInterrupt:
                pass                 
        
        return stats


ID_CACHE_FILE = Path("./cache/ids.json").resolve()

def getIdOrThrow(con, key, value, table):
    """ 
        Searches for the Id of the given key with the given value, ex. device="Atomic Pi" would return 1 as Id
        First searches in the local cache folder
        If not present, searches in the database
    """

    #  create cache directory if not present
    Path(ID_CACHE_FILE.parent).mkdir(parents=True, exist_ok=True)
    
    path_exists = Path(ID_CACHE_FILE).exists()

    cache = None
    if (path_exists):
        cache = read_JSON(ID_CACHE_FILE)
        if key in cache:
            return cache[key]

    query = "SELECT Id FROM {} WHERE {} = \"{}\"".format(table, key, value)

    result = con.execute_query(query).fetchone()

    if (result is None):
        raise LookupError("Could not find {} in table {}".format(value, table))

    if (path_exists == False):
        cache = {}

    cache[value] = result[0]

    write_JSON(cache, ID_CACHE_FILE)

    return str(cache[value])




### MAIN
if __name__ == "__main__":

    config_file = "config.json"
    config = read_JSON(config_file)

    db_credentials = config["credentials"]["database"][config["db_provider"]]

    db_connection = Connection(db_credentials["host"], db_credentials["username"], db_credentials["password"], db_credentials["db"])

    test_suite_info = {}

    # retrieve device id
    test_suite_info["device"] = getIdOrThrow(db_connection, "name", config["device_name"], "devices")

    # run each workload and push the results one by one
    for workload in config["workloads"]:

        batch_size = workload["batch_size"]
        workload_file = workload["file"]

        echo ("Executing workload from {}".format(workload_file))

        workload = import_script_from_filename(workload_file).Workload()
        inspector = Inspector()

        # look for ids
        test_suite_info["model"] = getIdOrThrow(db_connection, "name", workload.getModel(), "models")
        test_suite_info["framework"] = getIdOrThrow(db_connection, "name", workload.getFramework(), "frameworks")
        test_suite_info["application"] = getIdOrThrow(db_connection, "name", workload.getApplication(), "applications")

        # start execution
        stats = Runner(workload, inspector).run(batch_size)

        if len(stats) > 0:
            push_stats(con=db_connection, table="runs", test_suite=test_suite_info, stats=stats)
        else:
            echo ("Nothing to push")