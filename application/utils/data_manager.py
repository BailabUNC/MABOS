import numpy as np
import utils.mem_manager as mm
import utils.ser_manager as sm

class DataManager:
    def __init__(self, shape, dtype, window_length):
        self.shape = shape
        self.dtype = dtype
        self.window_length = window_length
    def initialize_plot_data(self):
        xs = [np.linspace(0, 999, 1000)]
        ys = np.ones(1000) * np.linspace(0, 1, 1000)
        return xs, ys
    def initialize_grid_plot_data(self):
        xs = [np.linspace(0, 999, 1000)]
        ys = np.array(np.random.randint(0, 1000, size=(3, 1000)))
        return xs, ys

    def update_data(self):
        while True:
            ys = sm.SerialManager.acquire_data()
            mm.MemoryManager.acquire_mutex()
            data_shared = mm.MemoryManager.get_shm_data()
            xs = data_shared[0][-self.window_length:]
            data_shared[0][:-self.window_length] = \
                data_shared[0][self.window_length:] - [self.window_length]
            data_shared[0][-self.window_length:] = xs
            for i in range(self.shape[0] - 1):
                data_shared[i + 1][:-self.window_length] = \
                    data_shared[i + 1][self.window_length:]
                data_shared[i + 1][-self.window_length:] = ys
            mm.MemoryManager.release_mutex()