from datetime import datetime
from sys import version_info
from PIL import Image
from PIL.ExifTags import TAGS
import pandas as pd 
import os
import matplotlib.pyplot as plt 
import numpy as np
import time
import logging
import magic
import ffmpeg

os.environ["path"] = "C:\\Users\\paulu\\Downloads\\ffmpeg-master-latest-win64-gpl-shared\\ffmpeg-master-latest-win64-gpl-shared\\bin"

startTime = time.time()
print(TAGS)
logging.basicConfig(level=logging.INFO)
# logging.basicConfig(level=logging.DEBUG)
class ImageSorter:
    def __init__(self, directory="images"):
        self.imageDirektory = directory
        self.filenames = []
        self.datelessPath = "sorted/dateless"
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
                # logging.info("root:%s dirs:%s file:%s"%(root, dirs, os.path.join(root, filename)))
                self.filenames.append(os.path.join(root, filename))
                # f = os.path.join(root, filename)
                # self.checkFile(f)
                # checking if it is a file
        print(self.filenames)

    # def checkFile(self, file):
    #     if os.path.isfile(file):
    #         # print(magic.from_file(file,mime=True).split("/"))
    #         filetype = magic.from_file(file,mime=True).split("/")[0]
    #         if filetype == "video":
    #             logging.info("ITS A VIDEO!")
    #         elif filetype == "image":
    #             logging.info("ITS AN IMAGE!")

    def linkFilesInDirs(self):
        for f in self.filenames:
            filetype = magic.from_file(f,mime=True).split("/")[0]
            # logging.debug("checking file: {}".format(os.path.relpath(f)))
            if os.path.isfile(f):
                if filetype == "video":
                    logging.info("processing Videofile: {}".format(os.path.relpath(f)))
                    self.sortVideo(f)
                elif filetype == "image":
                    logging.info("processing Imagefile: {}".format(os.path.relpath(f)))
                    self.sortImage(f)
                else:
                    logging.info("{} is nor an imagefile or a videofile!".format(os.path.relpath(f)))
            else:
                logging.info("{} is nor an imagefile or a videofile!".format(os.path.relpath(f)))

    def sortImage(self, imageFilePath):
        try:
            logging.info("sorting")
            with Image.open(imageFilePath) as im:
                exifData = im._getexif()
                
                foundExifData = False
                for id in exifData:
                    data = exifData.get(id)
                    tag_name = TAGS.get(id, id)
                    if id == 36867: #36867 -> DateTimeOriginal
                        foundExifData = True
                        src = os.path.abspath(imageFilePath)
                        date = str(datetime.strptime(data,"%Y:%m:%d %H:%M:%S").year) + "-" + str(datetime.strptime(data,"%Y:%m:%d %H:%M:%S").month)
                        dest = os.path.join(self.create_path(date), os.path.split(imageFilePath)[1])
                        logging.info("img src: %s dest: %s "%(src,dest))
                        try:
                            os.symlink(src, dest)
                        except Exception as e:
                            logging.error(e)                        
                if not foundExifData:
                    logging.error("cant find exif date, linking files to dateless: {}".format(imageFilePath))                      
                    try:
                        src = os.path.abspath(imageFilePath)
                        os.symlink(src, self.datelessPath)
                    except Exception as e:
                        logging.error(e)                        
                        # print(e)
        except Exception as e:
            logging.error(e)
    def sortVideo(self, videoFilePath):
        vdpath = os.path.abspath(videoFilePath)
        if not os.path.exists(vdpath): raise FileNotFoundError
        try:
            # logging.info(videoFilePath)
            if os.path.exists(vdpath): print("IST EIN FILE")
            probe = ffmpeg.probe(vdpath)
            print(probe["format"]["tags"]["creation_time"])
            # print(probe)


        except Exception as e:
            logging.error(e)
sorter = ImageSorter()


