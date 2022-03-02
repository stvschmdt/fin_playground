# functions to abstract away logging
# TODO make this more robust


import sys
import time
import datetime

#simple logging class, call the type of message, pass in a string
class Logging(object):
#TODO add filepath handling from sys
    def __init__(self, filepath=""):
        self.filepath = filepath
        if self.filepath == "":
            self.filepath = 'finlog.txt'
            self.writeable = 1
        self.start = datetime.datetime.utcnow()
        print("[log] started {}" .format(self.start))

    def error(self, msg):
        out = "[error] {}".format(datetime.datetime.utcnow()) +  msg
        print("[error] {}".format(datetime.datetime.utcnow()), msg)
        if self.writeable:
            with open(self.filepath,'a', newline='') as fd:
                fd.write(out+ '\n')

    def info(self, msg):
        out = "[info] {}".format(datetime.datetime.utcnow()) +  msg
        print("[info] {}".format(datetime.datetime.utcnow()), msg)
        if self.writeable:
            with open(self.filepath,'a', newline='') as fd:
                fd.write(out+ '\n')

    def warning(self, msg):
        out = "[warning] {}".format(datetime.datetime.utcnow()) +  msg 
        print("[warning] {}".format(datetime.datetime.utcnow()), msg)
        if self.writeable:
            with open(self.filepath,'a', newline='') as fd:
                fd.write(out+ '\n')

    def results(self, msg):
        out = "[results] {}".format(datetime.datetime.utcnow()) +  msg 
        print("[results] {}".format(datetime.datetime.utcnow()), msg)
        if self.writeable:
            with open(self.filepath,'a', newline='') as fd:
                fd.write(out+ '\n')
