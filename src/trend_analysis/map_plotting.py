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
from datetime import datetime
import time
from mapsplotlib.google_static_maps_api import GoogleStaticMapsAPI
from multiprocessing import Pool, Lock, Queue

MAX_SIZE = 600
PIXEL_LENGTH = 1200
global global_frame_list

class Mapping:
    def __init__(self):
        self.base_map = None
        self.side_length = 0
        self.grid_list_list = None
        self.opacity = 1
        self.show = True
        self.max_val = 0
        self.total_frames = 0
        self.frame_list = None # list of np array frames

    def import_data(self, filename):
        pass

    def register_api_key(self):
        # register api key
        mplt.register_api_key('AIzaSyBmjHKY0e0z090bBg4-qXFpKW4XbdBr2RM')
    
    def generate_base_map(self, coordinate_tuple=(34.412446,-119.855400), size = MAX_SIZE, zoom=15, maptype='roadmap'):
        # testing locked background map
        self.register_api_key()
        print("Generating Base Map...")
        coordinate_dict = {'latitudes': [coordinate_tuple[0]], 'longitudes': [coordinate_tuple[1]]}
        coordinate_df = pd.DataFrame(coordinate_dict)
        img, pixels = mplt.background_and_pixels_zoom(coordinate_df['latitudes'], coordinate_df['longitudes'], MAX_SIZE, maptype, zoom)
        # plt.figure(figsize=(15, 15))
        plt.imshow(np.array(img))
        self.base_map = img
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
            print('side_length = {} \ngrid_list = {}'.format(side_length, grid_list))
            return
        spacing = int(PIXEL_LENGTH/side_length)
        final_array_grid = np.array([])
        grid_list_list = []
        for val in grid_list:
            grid_list_list.append([val for i in range(spacing)])
        # create duplicating row
        for j in range(side_length):
            print('{}% complete'.format((j/side_length)*100))
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
        print('100% complete')
        print('Color Grid Generation Complete!')
        return final_array_grid

    def generate_color_grid_multi(self, side_length, grid_list):
        if side_length*side_length != len(grid_list):
            print("MISMATCH: BOXES TO PROVIDED GRID")
            print('side_length = {} \ngrid_list = {}\nlen = {}'.format(side_length, grid_list, len(grid_list)))
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
        return final_array_grid

    def init_background(self):
        plt.clf()

    def output_plot(self, filename):
        plt.savefig(filename)

    def generate_grid_plot(self, side_length, grid_obj, opacity, show=False):
        print('Starting Plot...')
        if self.base_map != None:
            print('Using prev rendered map')
            plt.imshow(np.array(self.base_map))
        else:
            self.generate_base_map()
        self.max_val = max(grid_obj[0])
        # print('max = {}'.format(self.max_val))
        array = self.generate_color_grid(side_length, grid_obj[0], opacity)
        plt.imshow(array, alpha=opacity, cmap=plt.get_cmap('Reds'))
        if len(plt.gcf().axes) == 1: 
            plt.clim(vmin = 0, vmax = self.max_val)
            plt.colorbar()
        plt.title(datetime.fromtimestamp(int(grid_obj[1])))
        if show == True:
            plt.show()
        print('Plotting Complete!')


    def initialize_grid(self, side_length, grid_obj_list, opacity):
        print('Init Grid Vals')
        self.side_length = side_length
        self.grid_obj_list = grid_obj_list
        self.opacity = opacity
        self.total_frames = len(grid_obj_list)
        for grid_obj in grid_obj_list:
            print(grid_obj[0])
            if self.max_val < max(grid_obj[0]):
                self.max_val = max(grid_obj[0])

    def generate_grid_plot_update(self, frame):
        print('################################################')
        print("Frame: {}/{}".format(frame+1, self.total_frames))
        print('side: {}, grid: {}, opacity: {}'.format(self.side_length, self.grid_obj_list[frame], self.opacity))
        self.generate_grid_plot(self.side_length, self.grid_obj_list[frame], self.opacity)
    
    def generate_grid_plot_update_multi(self, frame):
        print('Generating GIF frame {}'.format(frame))
        if self.base_map != None:
            # print('Using prev rendered map')
            plt.imshow(np.array(self.base_map))
        else:
            self.generate_base_map()
        plt.imshow(self.frame_list[frame][0], alpha=self.opacity, cmap=plt.get_cmap('Reds'))
        plt.title(datetime.fromtimestamp(int(self.frame_list[frame][1])))
        if len(plt.gcf().axes) == 1: 
            plt.clim(vmin = 0, vmax = self.max_val)
            plt.colorbar()

    # Type: activity/heatmap vs density
    def generate_grid_gif(self, filename, side_length, grid_obj_list, opacity, multi=False, show=False):
        print('Num Frames: {}'.format(len(grid_obj_list)))
        self.initialize_grid(side_length, grid_obj_list, opacity)
        fig = plt.figure()
        # dpi = fig.get_dpi()
        dpi = 200
        # print(dpi)
        if multi:
            print('Running multiprocessed GIF generation')
            self.generate_frames()
            func = self.generate_grid_plot_update_multi
            print('Starting Gif Creation...')
        else:
            func = self.generate_grid_plot_update
        anim = FuncAnimation(fig, func, frames=np.arange(0, len(grid_obj_list)), init_func = self.init_background, interval=500)
        print('Saving GIF...')
        anim.save('../../images/{}.gif'.format(filename), dpi=dpi, writer='imagemagick')
        print('GIF creation complete!')
        if show == True:
            plt.show()

    def init_multi(self, l, side_length, data, frame_list):
        global lock
        lock = l
        global global_side_length
        global_side_length = side_length
        global global_grid_obj_list
        global_grid_obj_list = data

    def generate_frames(self):
        l = Lock()
        results = []
        self.generate_base_map()
        pool = Pool(initializer=self.init_multi, initargs=(l, self.side_length, self.grid_obj_list, self.frame_list,  ))
        self.frame_list = [np.array([]) for i in range(self.total_frames)]
        # self.frame_list = pool.map(self.frame_worker, self.frame_list)
        print('Num frames to generate: {}'.format(self.total_frames))
        for i in range(0, self.total_frames):
            # print('Starting Frame Worker {}'.format(i))
            results.append(pool.apply_async(self.frame_worker, args=(i,)))
        pool.close()
        pool.join()
        print('Pool Joined - Processing Queue')
        results = [r.get() for r in results]
        for item in results:
            self.frame_list[item[1]] = (item[0],item[2])
        print('Queue Processing Completed - Generate Frames Complete')
        # print(self.frame_list)

    def frame_worker(self, frame):
        print('Frame Worker {} Started'.format(frame))
        result_frame = self.generate_color_grid_multi(self.side_length, global_grid_obj_list[frame][0])
        # lock.acquire()
        # try:
        #     print('Frame Worker {} Lock Aquired - Accesing Frame List'.format(frame))
        #     global_frame_list[frame] = result_frame
        # finally:
        #     print('Frame worker {} Lock Released'.format(frame))
        #     lock.release()
        print('Frame Worker {} Done'.format(frame))
        # queue.put((result_frame, frame))
        return(result_frame, frame, global_grid_obj_list[frame][1]) 
    

if __name__ == "__main__":
    base_map = Mapping()
    grid_obj_list = [([1,2,6,1,0,4,8,1,0,1,2,1,0,8,1,1], '1'),
                    ([1,2,6,1,0,4,0,1,0,1,2,1,10,0,1,1], '2')]
    # base_map.initialize_grid(4, grid_obj_list, 0.75)
    # base_map.generate_frames()
    # base_map.generate_grid_plot(4, grid_obj_list[0], 0.5, True)
    base_map.generate_grid_gif('multi', 4, grid_obj_list, 0.75, multi=True)
    # latitude = pd.Series(34.42397)
    # longitude = pd.Series(-119.86839)
    # center_lat = 34.413112
    # center_long = -119.855395
    # zoom = 15
    # size = MAX_SIZE
    # scale = 2
    # print(GoogleStaticMapsAPI.to_tile_coordinates(latitude, longitude, center_lat, center_long, zoom, size, scale))