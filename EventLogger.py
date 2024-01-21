import time
import csv
from pathlib import Path

# event are stored in ./logs with name $filename-YYYYMMDD.csv
# It will create a new csv file per day

def currentFileName (filename, ltime):
    dateStr = time.strftime("%Y%m%d", ltime)
    return filename + "-" + dateStr + ".csv"

class EventLogger ():
    def __init__(self, filename, columns = None):
        self.filename = filename
        self.currentFileName = currentFileName(self.filename, time.localtime())
        self.heads = ["time"]
        self.heads.extend(columns)
        if Path(self.currentFileName).is_file():
            self.fw = open(self.currentFileName, "a", encoding="utf-8")
            self.csvLogger = csv.writer(self.fw)
        else:
            self.fw = open(self.currentFileName, "w", encoding="utf-8")
            self.csvLogger = csv.writer(self.fw)
            self.csvLogger.writerow(self.heads)

    def log (self, values):
        ltime = time.localtime()
        c = currentFileName(self.filename, ltime)
        if c != self.currentFileName:
            self.currentFileName = c
            self.fw.close()
            self.fw = open(self.currentFileName, "w", encoding="utf-8")
            self.csvLogger.writerow(self.heads)
            self.csvLogger = csv.writer(self.fw)
        fields = [time.strftime("%Y-%m-%d %H:%M:%S %Z",ltime)]
        fields.extend(values)
        self.csvLogger.writerow(fields)
        self.fw.flush()

    def __del__(self):
        self.fw.close()

if __name__ == "__main__":
    el = EventLogger("./logs/test",["A","B","C"])
    el.log(["aaa","bbb","ccc"])