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
    ys = np.ones((3, 1000)) * np.linspace(0, 1, 1000)
    # ys = np.array(np.random.randint(0, 1000, size=(3, 1000)))
    return xs, ys


def update_data(ser, shm_name, mutex, window_length, shape, dtype):
    idx = 0
    channel_key = ["Red", "IR", "Violet"]
    while True:
        ys = sm.acquire_data(ser)
        shm = SharedMemory(shm_name)
        mm.acquire_mutex(mutex)
        data_shared = np.ndarray(shape=shape, dtype=dtype,
                                 buffer=shm.buf)
        # data_shared = mm.get_shm_data(shape, dtype, shm_name)
        xs = data_shared[0][-window_length:]
        data_shared[0][:-window_length] = data_shared[0][window_length:] - [window_length]
        data_shared[0][-window_length:] = xs
        if idx < 1000:
            for i in range(shape[0] - 1):
                data_shared[i + 1][:-window_length] = data_shared[i + 1][window_length:]
                data_shared[i + 1][-window_length:] = ys[i]
            idx += 1
        else:
            for i in range(shape[0] - 1):
                data_shared[i + 1][:-window_length] = data_shared[i + 1][window_length:]
                data_shared[i + 1][-window_length:] = ys[i]
                mm.save_data(key=channel_key[i], value=data_shared[i+1])
            idx = 0

        mm.release_mutex(mutex)

