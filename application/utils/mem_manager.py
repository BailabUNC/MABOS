import multiprocessing
from multiprocessing.shared_memory import SharedMemory
import utils.data_manager as dm
import utils.plot_manager as pm
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


def create_shared_block(grid_plot_flag=False, dtype=np.int64):
    if grid_plot_flag:
        plot, data = pm.initialize_grid_plot()
    else:
        plot, data = pm.initialize_plot()

    shm = SharedMemory(create=True, size=data.nbytes)
    data_shared = np.ndarray(shape=data.shape,
                             dtype=dtype, buffer=shm.buf)
    data_shared[:] = data[:]
    return shm, data_shared, plot


def get_shm_data(shape, dtype, shm_name):
    print('request for shared data')
    shm = SharedMemory(shm_name)
    data_shared = np.ndarray(shape=shape, dtype=dtype,
                             buffer=shm.buf)
    print(data_shared)
    return data_shared
