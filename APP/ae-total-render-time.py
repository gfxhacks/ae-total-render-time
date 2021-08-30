#!/usr/bin/env python3

# Command Line Usage: python3 ae-total-render-time.py /path/to/AERenderLogsFolder/

# Title: ae-total-render-time.py
# Version: 1.0.0
# Description: Calculate the Total Render Time of your completed After Effects renders.
# Author: gfxhacks.com
# More Info: https://gfxhacks.com/ae-render-logs-total-render-time

import os
import sys
import datetime

class Main:

    def __init__(self):
        print("\nRunning...\n\n---\n")

        # get folder path as passed to the command in Terminal
        self.directory = sys.argv[1]
        # set initial total time
        self.totalTime = 0;
        # set count for read log files
        self.logCount = 0;

        # check if folder exists, then walk
        if os.path.exists(self.directory):
             self.__walkDir__()
        else:
            sys.exit('Error: {} does not exist.\nExiting...'.format(self.directory))

    def __walkDir__(self):

        # walk the directory recursively
        for root, subdirs, files in os.walk(self.directory):

            # filter for txt files only
            files = list(filter(lambda file: file.endswith('.txt'), files))

            # iterate through txt files
            for filename in files:
                self.filename = filename
                self.file_path = os.path.join(root, filename)
                self.__getElapsedTime__()

        else:
            # when loop ends, print total time
            if self.totalTime > 0:
                print("\n---\n\nTotal Render Time: {}\n\n---\n".format(str(datetime.timedelta(seconds=self.totalTime))))
            else:
                print("No render times found here. Choose another location.\n\n---\n")

            sys.exit()

    def __getElapsedTime__(self):
        with open (self.file_path, 'rt') as myfile:
            # iterate line by line: if elapsed time exists, extract it
            for line in myfile:
                if "Elapsed" in line:
                    elapsedTime = line[line.rfind(":")+1:].strip()
                    self.logCount += 1
                    print("{}. {} reported in log file: {}".format(self.logCount, elapsedTime, self.filename))
                    self.__extractTime__(elapsedTime)

    def __extractTime__(self, et):
        # extract the elapsed time, split values by commas
        if "," in et:
            et = et.split(',')
            for i in et:
                self.__formatTime__(i.strip())
        else:
            self.__formatTime__(et.strip())

    def __formatTime__(self, t):

        # get strings
        s = [s for s in t.split() if not s.isdigit()][0]

        # get digits
        d = [int(s) for s in t.split() if s.isdigit()][0]

        # return seconds
        def sc():
            return d

        # convert minutes to seconds
        def mn():
            return d*60

        # convert hours to seconds
        def hr():
            return d*3600

        f = {
            "Sec": sc,
            "Seconds": sc,
            "Second": sc,
            "Min": mn,
            "Minutes": mn,
            "Minute": mn,
            "Hr": hr,
            "Hours": hr,
            "Hour": hr
        }

        # find whether value is Hours, Minutes, or Seconds
        # convert all to seconds, then accumulate
        self.totalTime += f[s]()

if __name__ == "__main__":
    Main()
