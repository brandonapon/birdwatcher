import grid_analysis_md_freq
import map_plotting

mp = map_plotting.Mapping()
res_obj_list = []
freq_obj_list = []
for i in range(1,28):
    res_list, freq_list = grid_analysis_md_freq.main('over', '2019_02_{}'.format(str(i).zfill(2)))
    res_obj_list.append(res_list)
    freq_obj_list.append(freq_list)
print('freq_obj_list: {}'.format(freq_obj_list))
mp.generate_grid_gif('01-28_GIF_Freq_600_600', 4, freq_obj_list, 0.5, multi=True)