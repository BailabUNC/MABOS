import multiprocessing
from multiprocessing.shared_memory import SharedMemory
import utils.data_manager as dm
import numpy as np
def create_event_flags():
    generate_ef = multiprocessing.Event()
    acquire_ef = multiprocessing.Event()
    return generate_ef, acquire_ef

def create_mutex():
    mutex = multiprocessing.Lock()
    return mutex

def acquire_mutex(mutex):
    mutex.acquire()

def release_mutex(mutex):
    mutex.release()

def create_shared_block(grid_plot_flag = False, dtype = np.int64, data = None):
    if data is None:
        if grid_plot_flag:
            xs, ys = dm.initialize_grid_plot_data()
            data = np.vstack((xs, ys))
        else:
            xs, ys = dm.initialize_plot_data()
            data = np.vstack((xs, ys))

    shape = data.shape
    shm = SharedMemory(create=True, size=data.nbytes)
    data_shared = np.ndarray(shape=shape,
                             dtype=dtype, buffer=shm.buf)
    data_shared[:] = data[:]
    return shm, data_shared
def get_shm_data(shape, dtype, shm_name):
    print('request for shared data')
    shm = SharedMemory(shm_name)
    data_shared = np.ndarray(shape=shape, dtype=dtype,
                             buffer=shm.buf)
    print(data_shared)
    return data_shared
