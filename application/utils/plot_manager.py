import numpy as np
import utils.data_manager as dm
import utils.mem_manager as mm
from multiprocessing.shared_memory import SharedMemory
from fastplotlib import Plot, GridPlot


def create_plot():
    plot = Plot()
    return plot


def create_grid_plot(channel_key):
    grid_shape = (len(channel_key), 1)
    names = [0]*len(channel_key)
    for i in range(len(channel_key)):
        names[i] = [channel_key[i]]

    grid_plot = GridPlot(
        shape=grid_shape,
        names=names
    )
    return grid_plot


def initialize_plot():
    plot = create_plot()
    xs, ys = dm.initialize_plot_data()
    plot_data = np.dstack([xs, ys])[0]
    plot.add_line(data=plot_data, name='data', cmap='jet')
    plot.auto_scale(maintain_aspect=False)
    data = np.vstack((xs, ys))
    return plot, data

def initialize_grid_plot(channel_key):
    grid_plot = create_grid_plot(channel_key)
    xs, ys = dm.initialize_grid_plot_data(len(channel_key))
    for i, subplot in enumerate(grid_plot):
        plot_data = np.dstack([xs, ys[i]])[0]
        subplot.add_line(data=plot_data, name='data', cmap='jet')
    data = np.vstack((xs, ys))
    return grid_plot, data


def obtain_plot_data(plot, mutex, shm_name, shape, dtype):
    mm.acquire_mutex(mutex)
    shm = SharedMemory(shm_name)
    data_shared = np.ndarray(shape=shape, dtype=dtype,
                             buffer=shm.buf)
    data = np.dstack([data_shared[0], data_shared[1]])[0]
    mm.release_mutex(mutex)
    plot['data'].data = data
    plot.auto_scale(maintain_aspect=False)


def obtain_grid_plot_data(args_dict):
    grid_plot = args_dict["plot"]
    mutex = args_dict["mutex"]
    shm_name = args_dict["shm_name"]
    shape = args_dict["shape"]
    dtype = args_dict["dtype"]
    mm.acquire_mutex(mutex)
    shm = SharedMemory(shm_name)
    data_shared = np.ndarray(shape=shape, dtype=dtype,
                             buffer=shm.buf)
    for i, subplot in enumerate(grid_plot):
        data = np.dstack([data_shared[0], data_shared[i + 1]])[0]
        subplot['data'].data = data
        subplot.auto_scale(maintain_aspect=False)
    mm.release_mutex(mutex)
