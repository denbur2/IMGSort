from datetime import datetime
from sys import version_info
from PIL import Image
from PIL.ExifTags import TAGS
# import pandas as pd 
import os
# import matplotlib.pyplot as plt 
# import numpy as np
import time
import logging
import magic
import ffmpeg

# uncomment the next line if you did not add ffmpeg to path
# os.environ["path"] = "C:\\Users\\paulu\\Downloads\\ffmpeg-master-latest-win64-gpl-shared\\ffmpeg-master-latest-win64-gpl-shared\\bin"

startTime = time.time()
# print(TAGS)
logger = logging.getLogger('ImageSorter')
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)

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
            
    def make_dirs(self,head):
        head_backup = head
        if head == '' or os.path.isdir(head): return 0
        _path = []
        while head != '':
            try:
                _path.append(head)
                head = os.path.split(head)[0]
            except OSError as e:
                logging.error(e)
                return 0

        for i in range(len(_path)-1,-1,-1):
            # print(_path[i])
            try:
                os.mkdir(_path[i])
            except OSError as e:
                logging.error(e)
                # print(e)
                i = i
        logging.info('path: %s was created' %head_backup)
        return 1

# append all relative filepaths to filenames
    def searchForFilesInDirs(self):
        for root, dirs, files in os.walk(self.imageDirektory):
            for filename in files:
                # logger.debug("root:%s dirs:%s file:%s"%(root, dirs, os.path.join(root, filename)))
                self.filenames.append(os.path.join(root, filename))
                # f = os.path.join(root, filename)
                # self.checkFile(f)
                # checking if it is a file
        print(self.filenames)

    def linkFilesInDirs(self):
        for f in self.filenames:
            filetype = magic.from_file(f,mime=True).split("/")[0]
            # logger.debug("checking file: {}".format(os.path.relpath(f)))
            if os.path.isfile(f):
                if filetype == "video":
                    logger.info("processing Videofile: {}".format(os.path.relpath(f)))
                    self.sortVideo(f)
                elif filetype == "image":
                    logger.info("processing Imagefile: {}".format(os.path.relpath(f)))
                    # self.sortImage(f)
                    # print(self.createSortedImagePath(f))
                    print(self.getExifDate(f))
                else:
                    logger.error("{} is nor an imagefile or a videofile!".format(os.path.relpath(f)))
            else:
                logger.error("{} is nor an imagefile or a videofile!".format(os.path.relpath(f)))

    def sortImage(self, imageFilePath):
        with Image.open(imageFilePath) as im:
            exifData = im._getexif()
            foundExifData = False
            for id in exifData:
                data = exifData.get(id)
                if id == 36867: #36867 -> DateTimeOriginal
                    foundExifData = True
                    src = os.path.abspath(imageFilePath)
                    date = str(datetime.strptime(data,"%Y:%m:%d %H:%M:%S").year) + "-" + str(datetime.strptime(data,"%Y:%m:%d %H:%M:%S").month)
                    dest = os.path.join(self.create_path(date), os.path.split(imageFilePath)[1])
                    self.make_dirs(self.create_path(date))
                    logger.info("img src: %s dest: %s "%(src,dest))
                    try:
                        os.symlink(src, dest)
                    except Exception as e:
                        logger.error(e)
                    break                     
            if not foundExifData:
                logger.error("cant find exif date, linking files to dateless: {}".format(imageFilePath))                      
                try:
                    src = os.path.abspath(imageFilePath)
                    os.symlink(src, self.datelessPath)
                # except Exception as e:
                #     logger.error(e)                        
                    # print(e)
                except WindowsError as e:
                    # logger.error("lllll{}".format(e))
                    pass

    def sortVideo(self, videoFilePath):
        videoFilePath = os.path.abspath(videoFilePath)
        if not os.path.exists(videoFilePath): raise FileNotFoundError
        try:
            # logger.info(videoFilePath)
            src = os.path.abspath(videoFilePath)
            tempDate = datetime.strptime(ffmpeg.probe(videoFilePath)["format"]["tags"]["creation_time"],"%Y-%m-%dT%H:%M:%S.000000Z")
            date = "{}-{}".format(tempDate.year, tempDate.month) 
            dest = os.path.join(self.create_path(date), os.path.split(videoFilePath)[1])
            self.make_dirs(self.create_path(date))
            try:
                os.symlink(src, dest)
            except Exception as e:
                logger.error(e) 
        except Exception as e:
            logger.error(e)

    def createSortedImagePath(self, imageFilePath):
        with Image.open(imageFilePath) as im:
            exifData = im._getexif()
            foundExifData = False
            for id in exifData:
                data = exifData.get(id)
                if id == 36867: #36867 -> DateTimeOriginal
                    foundExifData = True
                    src = os.path.abspath(imageFilePath)
                    date = str(datetime.strptime(data,"%Y:%m:%d %H:%M:%S").year) + "-" + str(datetime.strptime(data,"%Y:%m:%d %H:%M:%S").month)
                    dest = os.path.join(self.create_path(date), os.path.split(imageFilePath)[1])
                    self.make_dirs(self.create_path(date))
                    logger.info("img src: %s dest: %s "%(src,dest))
                    try:
                        return dict({"src":src,"dest":dest})
                    except Exception as e:
                        logger.error(e)
                    break                     
            if not foundExifData:
                logger.error("cant find exif date, linking files to dateless: {}".format(imageFilePath))                      
                try:
                    src = os.path.abspath(imageFilePath)
                    return dict({"src":src,"dest":self.datelessPath})
                except WindowsError as e:
                    # logger.error("lllll{}".format(e))
                    pass
    def getExifDate(self, imageFilePath):
        with Image.open(imageFilePath) as im:
            exifData = im._getexif()
            foundExifData = False
            for id in exifData:
                data = exifData.get(id)
                if id == 36867: #36867 -> DateTimeOriginal
                    foundExifData = True
                    return str(datetime.strptime(data,"%Y:%m:%d %H:%M:%S").year) + "-" + str(datetime.strptime(data,"%Y:%m:%d %H:%M:%S").month)

sorter = ImageSorter()