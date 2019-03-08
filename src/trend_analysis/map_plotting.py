import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from datetime import datetime
from math import sin, cos, sqrt, atan2
from mapsplotlib import mapsplot as mplt
from matplotlib import colors
from matplotlib.animation import FuncAnimation

MAX_SIZE = 640
PIXEL_LENGTH = 1280

class Mapping:
    def __init__(self):
        self.base_map = None
        self.side_length = 0
        self.grid_list_list = None
        self.opacity = 1
        self.show = True
        self.max_val = 0
        self.timestamp = None

    def import_data(self, filename):
        pass

    def register_api_key(self):
        # register api key
        mplt.register_api_key('AIzaSyBmjHKY0e0z090bBg4-qXFpKW4XbdBr2RM')
    
    def generate_base_map(self, coordinate_tuple=(34.413112,-119.855395), size = MAX_SIZE, zoom=15, maptype='roadmap'):
        # testing locked background map
        print("Generating Base Map...")
        coordinate_dict = {'latitudes': [coordinate_tuple[0]], 'longitudes': [coordinate_tuple[1]]}
        coordinate_df = pd.DataFrame(coordinate_dict)
        img, pixels = mplt.background_and_pixels_zoom(coordinate_df['latitudes'], coordinate_df['longitudes'], MAX_SIZE, maptype, zoom)
        # plt.figure(figsize=(15, 15))
        plt.imshow(np.array(img))
        print('Base Map Generation Complete!')
        # major_ticks = np.arange(0, 1280, 320)
        # ax.set_xticks(major_ticks)
        # ax.set_yticks(major_ticks)
        # minor_ticks = np.arange(0, 101, 5)
        # plt.grid()
        # plt.axis('off')

    # This makes the assumption that the list a representation of the list as if reading it L->R, Top to Bottom
    def generate_color_grid(self, side_length, grid_list, opacity):
        print("Generating Color Grid...")
        if side_length*side_length != len(grid_list):
            print("MISMATCH: BOXES TO PROVIDED GRID")
            return
        spacing = int(PIXEL_LENGTH/side_length)
        final_array_grid = np.array([])
        grid_list_list = []
        for val in grid_list:
            grid_list_list.append([val for i in range(spacing)])
        # create duplicating row
        for j in range(side_length):
            # print('j = {}'.format(j))
            row = []
            for i in range(side_length):
                # print (len(grid_list_list))
                row = row + grid_list_list[0]
                del grid_list_list[0]
            for repeat in range(spacing):
                # print(final_array_grid)
                if final_array_grid.size == 0:
                    final_array_grid = np.array(row)
                else:
                    final_array_grid = np.vstack((final_array_grid, np.array(row)))
        plt.imshow(final_array_grid, alpha = opacity, cmap=plt.get_cmap('Reds'))
        # plt.clim(vmin = 0, vmax = self.max_val)
        if len(plt.gcf().axes) == 1: 
            plt.colorbar()
        print('Color Grid Generation Complete!')
        # major_ticks = np.arange(0, PIXEL_LENGTH, spacing)
        # ax = plt.axes()
        # ax.set_xticks(major_ticks)
        # ax.set_yticks(major_ticks)
        # plt.grid()

    def init_background(self):
        plt.clf()

    def output_plot(self, filename):
        plt.savefig(filename)
    
    def generate_bird_plot(self):
        pass

    def generate_bird_plot_gif(self):
        pass

    def generate_grid_plot(self, side_length, grid_list, opacity, timestamp, show=False):
        print('Starting Plot...')
        self.register_api_key()
        self.generate_base_map()
        self.generate_color_grid(side_length, grid_list, opacity)
        plt.title(timestamp)
        if show == True:
            plt.show()
        print('Plotting Complete!')

    def initialize_grid(self, side_length, grid_list_list, opacity, timestamp):
        print('Init Grid Vals')
        self.side_length = side_length
        self.grid_list_list = grid_list_list
        self.opacity = opacity
        self.timestamp = timestamp
        for grid_list in grid_list_list:
            if self.max_val < max(grid_list):
                self.max_val = max(grid_list)

    def generate_grid_plot_update(self, frame):
        print("Frame: {}".format(frame))
        print('side: {}, grid: {}, opacity: {}'.format(self.side_length, self.grid_list_list[frame], self.opacity))
        self.generate_grid_plot(self.side_length, self.grid_list_list[frame], self.opacity, self.timestamp)

    # Type: activity/heatmap vs density
    def generate_grid_gif(self, side_length, grid_list_list, opacity, timestamp, show=False):
        print('Num Frames: {}'.format(len(grid_list_list)))
        self.initialize_grid(side_length, grid_list_list, opacity, timestamp)
        fig = plt.figure()
        dpi = fig.get_dpi()
        anim = FuncAnimation(fig, self.generate_grid_plot_update, frames=np.arange(0, len(grid_list_list)), init_func = self.init_background, interval=500)
        anim.save('../../images/line.gif', dpi=dpi, writer='imagemagick')
        if show == True:
            plt.show()

if __name__ == "__main__":
    base_map = Mapping()
    grid_list_list = [[1,2,6,1,0,4,8,1,0,1,2,1,0,8,1,1],
                    [1,2,6,1,0,4,0,1,0,1,2,1,0,0,1,1]]
    # base_map.generate_grid_plot(4, grid_list_list[0], 0.5)
    base_map.generate_grid_gif(4, grid_list_list, 0.75)