import json
from helpers.db_connector import Connection
from helpers.util import echo

def push_stats(con, table, test_suite, stats):

    for stat in stats:

        # keys = ",".join(stat.keys())
        complete_stat = { **test_suite, **stat }

        # some renaming of col names
        complete_stat["cpu_usage(%)"] = complete_stat.pop("cpu") if "cpu" in complete_stat else None
        complete_stat["memory_usage(%)"] = complete_stat.pop("memory") if "memory" in complete_stat else None
        complete_stat["disk_io(tps)"] = complete_stat.pop("disk") if "disk" in complete_stat else None
        complete_stat["power_usage(Watts)"] = complete_stat.pop("power") if "power" in complete_stat else None
        complete_stat["inference_time(seconds)"] = complete_stat.pop("inference_time") if "inference_time" in complete_stat else None
        complete_stat["accuracy(%)"] = complete_stat.pop("accuracy") if "accuracy" in complete_stat else None

        # espace key names
        keys = ["`{}`".format(_) for _ in complete_stat.keys()]

        # for string values like datetime, add extra quotes
        # replace None with null
        values = []
        for _ in complete_stat.values():
            if _ is None:
                _ = "NULL"
            elif isinstance(_, str):
                if ":" in _:
                    _ = "'{}'".format(_)
            values.append(str(_))

        keys_str = ",".join(keys)
        values_str = ",".join(values)

        query = "INSERT INTO {table} ({keys}) values({values}) ON DUPLICATE KEY UPDATE id=id".format_map({ "table" : table,"keys" : keys_str, "values" : values_str })
        echo (query)
        con.execute_query(query)
        
        # con.execute_query("INSERT INTO {table} values({values}) ON DUPLICATE KEY UPDATE id=id".format_map({ "table" : table, "values" : values }))

    con.commit()

    echo ("Logs pushed to database")