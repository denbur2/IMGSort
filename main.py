from datetime import datetime
from PIL import Image
from PIL.ExifTags import TAGS
import pandas as pd 
import os
import matplotlib.pyplot as plt 
import numpy as np
import time

startTime = time.time()

# os.symlink(os.path.abspath("IMG_20200725_184755.jpg"), "sorted/test.jpg")

directory = 'images'
dates = []
filenames = []
# iterate over files in
# that directory
ypoints = np.array([] ,dtype=np.int_)

for root, dirs, files in os.walk(directory):
    # print("root:%s dirs:%s file:%s"%(root, dirs, files))
    for filename in files:
        print("root:%s dirs:%s file:%s"%(root, dirs, os.path.join(root, filename)))
        filenames.append(os.path.join(root, filename))
        f = os.path.join(root, filename)
        # checking if it is a file

# def extractDataFromImages(f):
        if os.path.isfile(f):
            print(f)
            try:
                with Image.open(f) as im:
                    img_exif_data = im.getexif()
                    # for plotting results
                    buf = {f:[], "Data":[]}

                    for id in img_exif_data:

                        tag_name = TAGS.get(id, id)
                        data = img_exif_data.get(id)
                        # buf.append(tag_name)
                        # buf.append(data)

                        if id == 0x9003:
                                buf[f].append(tag_name)
                                buf["Data"].append(data)
                                dates.append(str(datetime.strptime(data,"%Y:%m:%d %H:%M:%S").year) + "-" + str(datetime.strptime(data,"%Y:%m:%d %H:%M:%S").month))
                                ypoints = np.append(ypoints, int(data.rsplit(" ")[1].rsplit(":")[1]))

                    df = pd.DataFrame(buf)
                    df.head(10).style.format({"BasePay": "${:20,.0f}", 
                                "OtherPay": "${:20,.0f}", 
                                "TotalPay": "${:20,.0f}",
                                "TotalPayBenefits":"${:20,.0f}"})
                    # df.style
                    # print(df.to_string())
                    # print(df)
            except Exception as e:
                print(e)
print("filenames:%s"%(filenames))
# countarr = np.bincount(ypoints)
# plt.plot(countarr, 'X--r')
# plt.show()


def make_dirs(head):
    head_backup = head
    if head == '' or os.path.isdir(head): return 0
    _path = []
    while head != '':
        try:
            _path.append(head)
            head = os.path.split(head)[0]
        except OSError as e:
            print(e)
            return 0

    for i in range(len(_path)-1,-1,-1):
        # print(_path[i])
        try:
            os.mkdir(_path[i])
        except OSError as e:
            # print(e)
            i = i
    print('path: %s was created' %head_backup)
    return 1

def create_path(date):
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

def createDirsFromDates(dates):
    for i in range(len(dates)):
        try:
            os.makedirs(create_path(dates[i]),exist_ok=True)
            print(create_path(dates[i]))
        except OSError as e:
            print(e)

def linkFilesInDirs(unsortedImagesPath):
    print("==================")
    for f in filenames:
        # checking if it is a file
        if os.path.isfile(f):
            with Image.open(f) as im:
                img_exif_data = im.getexif()
                buf = {f:[], "Data":[]}
                print(f)
                for id in img_exif_data:

                    tag_name = TAGS.get(id, id)
                    data = img_exif_data.get(id)

                    if id == 0x9003:
                        src = os.path.abspath(f)
                        date = str(datetime.strptime(data,"%Y:%m:%d %H:%M:%S").year) + "-" + str(datetime.strptime(data,"%Y:%m:%d %H:%M:%S").month)
                        dest = os.path.join(create_path(date), os.path.split(f)[1])
                        print("img src: %s dest: %s "%(src,dest))
                        try:
                            os.symlink(src, dest)
                        except Exception as e:
                            print(e)

dates = list(set(dates))
dates.sort()
print(dates)
createDirsFromDates(dates)
linkFilesInDirs(directory)



print('Execution time in seconds: ' + str((time.time() - startTime)))