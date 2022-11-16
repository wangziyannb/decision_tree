import os
import tracemalloc
from datetime import datetime
import time


class Tracer:
    def __init__(self, path):
        self.start = time.time()
        self.end = None
        tracemalloc.start()
        self.log_path = "log/" + path[0:-4] + "_" + str(datetime.now())[0:19] + ".txt"
        self.log_path = self.log_path.replace(':', '-')
        self.info = {"dataset": path, "time_cons": "", "mem_cons": ""}

    def output(self, result):
        self.end = time.time()
        total = self.end - self.start
        mem_snapshot = tracemalloc.take_snapshot()
        stat = mem_snapshot.statistics('filename')
        sum = 0
        for s in stat:
            sum = sum + s.size
        self.info["time_cons"] = str(total) + " s"
        self.info["mem_cons"] = str(sum / 1024) + " KB"
        print("total time consumption:", self.info["time_cons"])
        print("total storage consumption:", self.info["mem_cons"])
        self.info = dict(self.info, **result)
        l = os.listdir()
        if "log" not in l:
            os.mkdir("log")
        with open(self.log_path, 'w', encoding='utf-8') as o:
            for i in self.info:
                if i == "result":
                    o.write(i + ": " + '\n')
                    for j in range(len(self.info[i])):
                        o.write(str(self.info[i][j]) + '\n')
                else:
                    o.write(i + ": " + str(self.info[i]) + '\n')
