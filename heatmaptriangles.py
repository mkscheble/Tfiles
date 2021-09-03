import matplotlib.pyplot as plt
import matplotlib.tri as mtri
from planeequationcalculator import *
import numpy as np

"""Models the monolayer channels using offset data and colors according to spiky cells detected"""

#extract 'c' data, # of spiky cells detected for FOV from excel file
def getcdata(ws, column_num):
    row = 1
    numcells = -5
    extracted_data = []
    # iterates through each row in the column_num given of the excel sheet until no values are left, then returns the array
    while numcells != None:
        cellc = str(get_column_letter(column_num)) + str(row)
        numcells = ws[cellc].value
        if numcells != None:
            extracted_data += [numcells]
        row += 1
    return np.array(extracted_data)

def main(path_offset_data, path_spiky_data, sheetname):

    #for naming axis
    index_x, index_y, index_z = 0, 1, 2
    list_name_variables = ['x offset (mm)', 'y offset (mm)', 'z offset (mm)']
    name_color_map = 'hot'

    #paths for data
    ws_offsheet = load_wb(path_offset_data, sheetname)
    data = accessData(ws_offsheet)
    ws_spiky = load_wb(path_spiky_data, sheetname)


    row = 1
    #iterate through every monolayer run in dataset ~20 runs of data
    for run in data:
        x_arr = []
        y_arr = []
        z_arr = []
        c_arr = getcdata(ws_spiky, row)
        print(c_arr)

        #iterate through every offset in each run, put into x, y, z
        for offset in run:
            x, y, z = offset
            x_arr.append(x)
            y_arr.append(y)
            z_arr.append(z)

        #check if all offset data is same length, will through off 3D recreation if not
        if len(x_arr) == len(y_arr) and len(y_arr) == len(z_arr):

            #get index of end of channel 1 and switch to channel 2 in monolayer
            chan = find_channel_change(y_arr)
            print('channel', chan)

            #standard data case where len == 120, can just plot normally
            if chan and len(x_arr) == 120:
                # x is channel 1, x2 is channel 2
                x = np.array(x_arr)[0:chan]
                x2 = np.array(x_arr)[chan:]
                y = np.array(y_arr)[0:chan]
                y2 = np.array(y_arr)[chan:]
                z = np.array(z_arr)[0:chan]
                z2 = np.array(z_arr)[chan:]
                c = c_arr[0:chan]
                c2 = c_arr[chan:]

                fig = plt.figure()
                ax = fig.add_subplot(projection='3d')


                # comment for scatter plot

                # create triangles between points
                triangles = mtri.Triangulation(x, y).triangles
                triangles2 = mtri.Triangulation(x2, y2).triangles
                triang = mtri.Triangulation(x, y, triangles)
                triang2 = mtri.Triangulation(x2, y2, triangles2)

                # add colors
                colors = np.mean([c[triangles[:, 0]], c[triangles[:, 1]], c[triangles[:, 2]]], axis=0)
                colors2 = np.mean([c2[triangles2[:, 0]], c2[triangles2[:, 1]], c2[triangles2[:, 2]]], axis=0)

                surf = ax.plot_trisurf(triang, z, cmap=name_color_map, shade=False, linewidth=0.2)
                surf2 = ax.plot_trisurf(triang2, z2, cmap=name_color_map, shade=False, linewidth=0.2)
                surf.set_array(colors)
                surf.autoscale()
                surf2.set_array(colors2)
                surf2.autoscale()
                cbar = fig.colorbar(surf, shrink=0.5, aspect=10)
                cbar.ax.get_yaxis().labelpad = 15
                cbar.ax.set_ylabel("# of Spiky Cells Detected", rotation=270)

                # end of comment

                # uncomment for scatter plot
                # im = ax.scatter(x_arr, y_arr, z_arr, marker='s', s= 50, c=c_arr, cmap='hot')
                # fig.colorbar(im, ax=ax, shrink=0.5, aspect=10)
                # end of uncomment

                #add axis title and graph title
                ax.set_xlabel(list_name_variables[index_x])
                ax.set_ylabel(list_name_variables[index_y])
                ax.set_zlabel(list_name_variables[index_z])
                plt.title('Monolayer Morphology Heatmap')
                plt.show()

            else: #for the case when data is not uniform so just plot one data, means run errored half way through
                #split data into two channels
                x = np.array(x_arr)[0:60]
                x2 = np.array(x_arr)[60:]
                y = np.array(y_arr)[0:60]
                y2 = np.array(y_arr)[60:]
                z = np.array(z_arr)[0:60]
                z2 = np.array(z_arr)[60:]
                c = c_arr[0:60]
                c2 = c_arr[60:]

                fig = plt.figure()
                ax = fig.add_subplot(projection='3d')

                triangles = mtri.Triangulation(x, y).triangles;
                colors = np.mean([c[triangles[:, 0]], c[triangles[:, 1]], c[triangles[:, 2]]], axis=0)
                ax.scatter(x2, y2, z2, marker='s', s=50, c=c2, cmap='hot')
                triang = mtri.Triangulation(x, y, triangles)
                surf = ax.plot_trisurf(triang, z, cmap=name_color_map, shade=False, linewidth=0.2)
                surf.set_array(colors)
                cbar = fig.colorbar(surf, shrink=0.5, aspect=10)
                cbar.ax.get_yaxis().labelpad = 15
                cbar.ax.set_ylabel("# of Spiky Cells Detected", rotation=270)

                # im = ax.scatter(x_arr, y_arr, z_arr, marker='s', s=50, c=c_arr, cmap='hot')
                # fig.colorbar(im, ax=ax, shrink=0.5, aspect=10)


                # Add titles to the axes and a title in the figure.
                ax.set_xlabel(list_name_variables[index_x])
                ax.set_ylabel(list_name_variables[index_y])
                ax.set_zlabel(list_name_variables[index_z])
                plt.title('Monolayer Morphology Heatmap')
                plt.show()

            row += 1

if __name__ == "__main__":
    path_offset_data = r"C:\Users\MarkScheble.Jr\Desktop\cellclassifier\newrundataglassplastic.xlsx"
    path_spiky_data = r"C:\Users\MarkScheble.Jr\Desktop\cellclassifier\cdata.xlsx"
    sheetname = 'Sheet'
    main(path_offset_data, path_spiky_data, sheetname)