from itertools import groupby

import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

from testing import load_samples


class Data(object):
    def __init__(self, filename):
        self.filename = filename

    def process(self):
        self.load()
        self.add_histogram()
        self.add_scatter()

    def load(self):
        self.samples = load_samples(self.filename)
        self.samples = list(sorted(self.samples, key=lambda x: x.start_time))
        self.by_service = {k: list(v) for k, v in groupby(
            sorted(self.samples, key=lambda x: (x.server, x.service)),
            key=lambda x: (x.server, x.service),
        )}

    def add_histogram(self):
        num_bins = 50
        fig = plt.figure()
        n_plots = len(self.by_service)
        axo = None
        for i, (k, service) in enumerate(self.by_service.items()):
            x = map(lambda x: x.duration, service)
            ax = fig.add_subplot(n_plots, 1, i + 1, sharey=axo)
            ax.hist(x, num_bins, normed=1, facecolor='green', alpha=0.5)
            if i < n_plots - 1:
                ax.axes.get_xaxis().set_ticks([])
            if not axo:
                axo = ax
            ax.yaxis.set_major_locator(plt.MaxNLocator(5))
            plt.xticks(fontsize=8)
            plt.yticks(fontsize=8)
        plt.savefig(self.filename + '.histogram.png')

    def add_scatter(self):
        plt.figure()
        items = self.by_service.items()
        colors = iter(cm.rainbow(np.linspace(0, 1, len(items))))
        for i, (k, service) in enumerate(items):
            x = map(lambda x: x.start_time, service)
            y = map(lambda x: x.duration, service)
            plt.scatter(x, y, s=2, color=next(colors))
        plt.xticks(fontsize=8)
        plt.yticks(fontsize=8)
        plt.savefig(self.filename + '.scatter.png')

data = Data('out.pkl')
data.process()
