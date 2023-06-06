import numpy as np
from multiprocessing.shared_memory import SharedMemory
import utils.mem_manager as mm
import utils.ser_manager as sm
import time

def initialize_plot_data():
    xs = [np.linspace(0, 999, 1000)]
    ys = np.ones(1000) * np.linspace(0, 1, 1000)
    return xs, ys
def initialize_grid_plot_data():
    xs = [np.linspace(0, 999, 1000)]
    ys = np.array(np.random.randint(0, 1000, size=(3, 1000)))
    return xs, ys

def update_data(ser, window_length, shape, dtype, shm_name, mutex):
    while True:
        ys = sm.acquire_data(ser)
        mm.acquire_mutex(mutex)
        print('data acquire')
        # data_shared = mm.get_shm_data(shape, dtype, shm_name)
        shm = SharedMemory(shm_name)
        data_shared = np.ndarray(shape=shape, dtype=dtype,
                                 buffer=shm.buf)
        xs = data_shared[0][-window_length:]
        data_shared[0][:-window_length] = data_shared[0][window_length:] - [window_length]
        data_shared[0][-window_length:] = xs
        for i in range(shape[0] - 1):
            data_shared[i + 1][:-window_length] = data_shared[i + 1][window_length:]
            data_shared[i + 1][-window_length:] = ys

        mm.release_mutex(mutex)
        print('data release')
