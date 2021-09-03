from planeequationcalculator import load_wb, find_channel_change, accessData
import numpy as np

def ranges(x_arr, y_arr, z_arr):
    xmax = np.max(x_arr)
    ymax = np.max(y_arr)
    zmax = np.max(z_arr)
    xmin = np.min(x_arr)
    ymin = np.min(y_arr)
    zmin = np.min(z_arr)
    return [[xmin, xmax, np.abs(xmax-xmin)], [ymin, ymax, np.abs(ymax-ymin)], [zmin, zmax, np.abs(zmax-zmin)]]



path = r"C:\Users\MarkScheble.Jr\Desktop\cellclassifier\newrundataglassplastic.xlsx"
sheetname = 'Sheet'
ws = load_wb(path, sheetname)
data = accessData(ws)

count = 1
for item in data:
    x_arr = []
    y_arr = []
    z_arr = []
    for location in item:
        x, y, z = location
        x_arr.append(x)
        y_arr.append(y)
        z_arr.append(z)
    if len(x_arr) == len(y_arr) and len(y_arr) == len(z_arr):
        chan = find_channel_change(y_arr)
        print('channel', chan)
        if chan:
            x = np.array(x_arr)[0:chan]
            x2 = np.array(x_arr)[chan:]
            y = np.array(y_arr)[0:chan]
            y2 = np.array(y_arr)[chan:]
            z = np.array(z_arr)[0:chan]
            z2 = np.array(z_arr)[chan:]
        else:
            x = np.array(x_arr)
            x2 = np.array(x_arr)
            y = np.array(y_arr)
            y2 = np.array(y_arr)
            z = np.array(z_arr)
            z2 = np.array(z_arr)
        valuesx1, valuesy1, valuesz1 = ranges(x, y, z)
        valuesx2, valuesy2, valuesz2 = ranges(x2, y2, z2)
        minx = min(valuesx1[0], valuesx2[0])
        maxx = max(valuesx1[1], valuesx2[1])
        miny = min(valuesy1[0], valuesy2[0])
        maxy = max(valuesy1[1], valuesy2[1])
        minz = min(valuesz1[0], valuesz2[0])
        maxz = max(valuesz1[1], valuesz2[1])
        print("Run: ", count)
        print(round(valuesx1[0], 4), round(valuesx2[0], 4), round(valuesx1[1],4), round(valuesx2[1],4), round(valuesx1[2],4), round(valuesx2[2],4), round(np.abs(minx-maxx),4))
        print(round(valuesy1[0], 4), round(valuesy2[0], 4), round(valuesy1[1], 4), round(valuesy2[1], 4),
              round(valuesy1[2], 4), round(valuesy2[2], 4), round(np.abs(miny - maxy), 4))
        print(round(valuesz1[0], 4), round(valuesz2[0], 4), round(valuesz1[1], 4), round(valuesz2[1], 4),
              round(valuesz1[2], 4), round(valuesz2[2], 4), round(np.abs(minz - maxz), 4))
        count +=1