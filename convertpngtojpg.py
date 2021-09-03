from PIL import Image
import numpy as np
import os

"""converts png images to jpg"""

#can set path to whatever
path = r"C:\Users\MarkScheble.Jr\Desktop\imagesnew\210830.131420"

for filename in os.listdir(path):
    if filename.endswith(".png"):
        filename = os.path.join(path, filename)
        im = Image.open(filename)
        description = filename.partition(".png")[0]
        description = description + '.jpg'
        print(description)
        im.save(description)