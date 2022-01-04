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

class ImageSorter:
    def __init__(self, directory="images"):
        self.imageDirektory = directory
        self.filenames = []
        # self.run()
        self.searchForFilesInDirs()
    # def run():
    def searchForFilesInDirs(self):
        for root, dirs, files in os.walk(self.imageDirektory):
            # print("root:%s dirs:%s file:%s"%(root, dirs, files))
            for filename in files:
                logging.info("root:%s dirs:%s file:%s"%(root, dirs, os.path.join(root, filename)))
                self.filenames.append(os.path.join(root, filename))
                f = os.path.join(root, filename)
                # checking if it is a file
        print(self.filenames)
sorter = ImageSorter()


