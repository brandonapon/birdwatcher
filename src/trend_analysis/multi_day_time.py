import grid_analysis_md_time
import map_plotting

mp = map_plotting.Mapping()
rows_obj_list = []
for i in range(1,28):
    row_obj = grid_analysis_md_time.main('over', '2019_02_{}'.format(str(i).zfill(2)), 12)
    if(row_obj[0] != None):
        rows_obj_list.append(row_obj)
print('row_obj_list: {}'.format(rows_obj_list))
mp.generate_grid_gif('1-28_GIF_md_12pm', 4, rows_obj_list, 0.5, multi=True)