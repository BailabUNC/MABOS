import numpy as np
import utils.data_manager as dm
import utils.mem_manager as mm
from fastplotlib import Plot, GridPlot


class PlotManager:
    def __init__(self):
        self.plot = None
        self.grid_plot = None

    def create_plot(self):
        self.plot = Plot()
        return self.plot
    def create_grid_plot(self):
        grid_shape = (1, 3)
        controllers = [
            [0, 1, 2]
        ]
        names = [
            ["red", "IR", "violet"]
        ]
        self.grid_plot = GridPlot(
            shape=grid_shape,
            controllers=controllers,
            names=names
        )
        return self.grid_plot
    def initialize_plot(self):
        xs, ys = dm.DataManager.initialize_plot_data()
        plot_data = np.dstack([xs, ys])[0]
        self.plot.add_line(data=plot_data, name='data', cmap='jet')
        self.plot.auto_scale(maintain_aspect=False)
        data = np.vstack((xs, ys))
        return data
    def initialize_grid_plot(self):
        xs, ys, data = dm.DataManager.initialize_grid_plot_data()
        for i, subplot in enumerate(self.grid_plot):
            plot_data = np.dstack([xs, ys[i]])[0]
            subplot.add_line(data = plot_data, name='data', cmap='jet')
        data = np.vstack((xs, ys))
        return data

    def obtain_plot_data(self):
        mm.MemoryManager.acquire_mutex()
        data_shared = mm.MemoryManager.get_shm_data()
        data = np.dstack([data_shared[0], data_shared[1]])[0]
        mm.MemoryManager.release_mutex()
        self.plot['data'].data = data
        self.plot.auto_scale(maintain_aspect=False)

    def obtain_grid_plot_data(self):
        mm.MemoryManager.acquire_mutex()
        data_shared = mm.MemoryManager.get_shm_data()
        for i, subplot in enumerate(self.grid_plot):
            data = np.dstack([data_shared[0], data_shared[i + 1]])[0]
            subplot['data'].data = data
        mm.MemoryManager.release_mutex()
