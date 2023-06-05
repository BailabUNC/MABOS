import multiprocessing
from multiprocessing.shared_memory import SharedMemory
import utils.data_manager as dm
import numpy as np


class MemoryManager:
    def __init__(self, grid_plot_flag=bool, shape=None, dtype=np.int64):
        self.shm = None
        self.generate_ef = None
        self.acquire_ef = None
        self.mutex = None
        self.grid_plot_flag = grid_plot_flag
        self.shape = shape
        self.dtype = dtype

    def create_event_flags(self):
        self.generate_ef = multiprocessing.Event()
        self.acquire_ef = multiprocessing.Event()
        return self.generate_ef, self.acquire_ef

    def create_mutex(self):
        self.mutex = multiprocessing.Lock()
        return self.mutex

    def acquire_mutex(self):
        self.mutex.acquire()

    def release_mutex(self):
        self.mutex.release()

    def create_shared_block(self):
        if self.grid_plot_flag:
            xs, ys = dm.DataManager.initialize_grid_plot_data()
            data = np.vstack((xs, ys))
        else:
            xs, ys = dm.DataManager.initialize_plot_data()
            data = np.vstack((xs, ys))
        self.shape = data.shape
        self.shm = SharedMemory(create=True, size=data.nbytes)
        data_shared = np.ndarray(shape=self.shape,
                                 dtype=self.dtype, buffer=self.shm.buf)
        data_shared[:] = data[:]
        return self.shm, data_shared
    def get_shm_data(self):
        data_shared = np.ndarray(shape=self.shape, dtype=self.dtype,
                                 buffer=self.shm.buf)
        return data_shared
