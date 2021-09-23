from PIL import Image
from PIL.ExifTags import TAGS
import pandas as pd 
import os
import matplotlib.pyplot as plt 
import numpy as np
directory = 'images'
 
# iterate over files in
# that directory
ypoints = np.array([] ,dtype=np.int_)
for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    # checking if it is a file
    if os.path.isfile(f):
        with Image.open(f) as im:
            # im = Image.open("testimg.jpg")
            # im.show()

            img_exif_data = im.getexif()

            # print(img_exif_data)

            buf = {f:[], "Data":[]}

            for id in img_exif_data:

                tag_name = TAGS.get(id, id)
                data = img_exif_data.get(id)
                # buf.append(tag_name)
                # buf.append(data)


                if id == 0x9003:
                        buf[f].append(tag_name)
                        buf["Data"].append(data)
                        # print(data.rsplit(" ")[0].rsplit(":"))
                        ypoints = np.append(ypoints, int(data.rsplit(" ")[1].rsplit(":")[1]))
                        # print(type(int(data.rsplit(" ")[1].rsplit(":")[1])))

            df = pd.DataFrame(buf)
            df.head(10).style.format({"BasePay": "${:20,.0f}", 
                          "OtherPay": "${:20,.0f}", 
                          "TotalPay": "${:20,.0f}",
                          "TotalPayBenefits":"${:20,.0f}"})
            df.style
            # print(df.to_string())
            # print(df)

print( os.getlogin()+' is logged in')

#countarr = np.bincount(ypoints)
#print(countarr)
#print(ypoints)
#plt.plot(countarr, 'X--r')
#plt.show()

src = 'images'
dst = 'symlinks'

# This creates a symbolic link on python in tmp directory
os.symlink(src, dst)
