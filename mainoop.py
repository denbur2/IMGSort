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
# logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.DEBUG)
class ImageSorter:
    def __init__(self, directory="images"):
        self.imageDirektory = directory
        self.filenames = []
        # self.run()
        self.searchForFilesInDirs()
        self.linkFilesInDirs()
    # def run():


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

# append all relative filepaths to filenames
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

    def checkFile(self, file):
        if os.path.isfile(file):
            # print(magic.from_file(file,mime=True).split("/"))
            filetype = magic.from_file(file,mime=True).split("/")[0]
            if filetype == "video":
                logging.info("ITS A VIDEO!")
            elif filetype == "image":
                logging.info("ITS AN IMAGE!")

    def linkFilesInDirs(self):
        for f in self.filenames:
            filetype = magic.from_file(f,mime=True).split("/")[0]
            logging.debug("checking file: {}".format(os.path.relpath(f)))
            if os.path.isfile(f):
                if filetype == "video":
                    logging.info("processing Videofile: {}".format(os.path.relpath(f)))
                elif filetype == "image":
                    logging.info("processing Imagefile: {}".format(os.path.relpath(f)))
                    self.sortImage(f)
                else:
                    logging.info("{} is nor an imagefile or a videofile!".format(os.path.relpath(f)))


            else:
                logging.info("{} is nor an imagefile or a videofile!".format(os.path.relpath(f)))

    def sortImage(self, imageFile):
        try:
            with Image.open(imageFile) as im:
                exifData = im.getexif()
                for id in exifData:
                    data = exifData.get(id)
                    print(exifData)
                    if id == 0x9003:
                        src = os.path.abspath(imageFile)
                        date = str(datetime.strptime(data,"%Y:%m:%d %H:%M:%S").year) + "-" + str(datetime.strptime(data,"%Y:%m:%d %H:%M:%S").month)
                        dest = os.path.join(self.create_path(date), os.path.split(imageFile)[1])
                        logging.info("img src: %s dest: %s "%(src,dest))
                        try:
                            os.symlink(src, dest)
                        except Exception as e:
                            logging.error(e)                        
                            print(e)                      
        except Exception as e:
            logging.error(e)
    def sortVideo(self, videoFilePath)
        try:
            pass
        except Exception as e:
            logging.error(e)
sorter = ImageSorter()


