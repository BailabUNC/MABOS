import utils.data_manager as dm
import utils.mem_manager as mm
import utils.ser_manager as sm
import utils.plot_manager as pm
from functools import partial
import multiprocessing

class CentralManger:
    def __init__(self, channel_key, commport, window_length=1, baudrate=115200):
        self.channel_key = channel_key
        self.commport = commport
        self.baudrate = baudrate
        self.window_length = window_length

        self.mutex = mm.create_mutex()
        self.ser = sm.setup_serial(self.commport, self.baudrate)
        self.shm, data_shared, self.plot = mm.create_shared_block(grid_plot_flag=True, channel_key=channel_key)
        self.shape, self.dtype = data_shared.shape, data_shared.dtype

    def update_process(self):
        p1 = multiprocessing.Process(name='update',
                                     target=dm.update_data,
                                     args=(self.ser, self.shm.name, self.mutex, self.window_length, self.shape, self.dtype, self.channel_key,))
        return p1
    def plotting_process(self):
        self.plot.add_animations(partial(pm.obtain_grid_plot_data, self.plot, self.mutex, self.shm.name, self.shape, self.dtype, ))
        self.plot.show()