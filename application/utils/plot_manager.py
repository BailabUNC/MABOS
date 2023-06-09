import numpy as np
import utils.data_manager as dm
import utils.mem_manager as mm
from multiprocessing.shared_memory import SharedMemory
from fastplotlib import Plot, GridPlot


def create_plot():
    plot = Plot()
    return plot


def create_grid_plot():
    grid_shape = (1, 3)
    controllers = [
        [0, 1, 2]
    ]
    names = [
        ["red", "IR", "violet"]
    ]
    grid_plot = GridPlot(
        shape=grid_shape,
        controllers=controllers,
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


def initialize_grid_plot():
    grid_plot = create_grid_plot()
    xs, ys = dm.initialize_grid_plot_data()
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


def obtain_grid_plot_data(grid_plot, mutex, shm_name, shape, dtype):
    mm.acquire_mutex(mutex)
    shm = SharedMemory(shm_name)
    data_shared = np.ndarray(shape=shape, dtype=dtype,
                             buffer=shm.buf)
    for i, subplot in enumerate(grid_plot):
        data = np.dstack([data_shared[0], data_shared[i + 1]])[0]
        subplot['data'].data = data
    mm.release_mutex(mutex)
