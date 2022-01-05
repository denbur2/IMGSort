from datetime import datetime
from PIL import Image
from PIL.ExifTags import TAGS
import pandas as pd 
import os
import matplotlib.pyplot as plt 
import numpy as np
import time
import logging
import magic
startTime = time.time()
logging.basicConfig(level=logging.INFO)
class ImageSorter:
    def __init__(self, directory="images"):
        self.imageDirektory = directory
        self.filenames = []
        # self.run()
        self.searchForFilesInDirs()
    # def run():

    def checkFile(self, file):
        if os.path.isfile(file):
            # print(magic.from_file(file,mime=True).split("/"))
            filetype = magic.from_file(file,mime=True).split("/")[0]
            if filetype == "video":
                logging.info("ITS A VIDEO!")
            elif filetype == "image":
                logging.info("ITS AN IMAGE!")

    def create_path(self, date):
        path = "sorted"
        path = os.path.join(path, date.rsplit("-")[0])
        switch={
            1:"Januar",
            2:"Februar",
            3:"Maerz",
            4:"April",
            5:"Mai",
            6:"Juni",
            7:"Juli",
            8:"August",
            9:"September",
            10:"Oktober",
            11:"November",
            12:"Dezember"
        }

        path = os.path.join(path, switch.get(int(date.rsplit("-")[1]),"0"))
        return path


    def searchForFilesInDirs(self):
        for root, dirs, files in os.walk(self.imageDirektory):
            # print("root:%s dirs:%s file:%s"%(root, dirs, files))
            for filename in files:
                logging.info("root:%s dirs:%s file:%s"%(root, dirs, os.path.join(root, filename)))
                self.filenames.append(os.path.join(root, filename))
                f = os.path.join(root, filename)
                self.checkFile(f)
                # checking if it is a file
        print(self.filenames)
sorter = ImageSorter()


