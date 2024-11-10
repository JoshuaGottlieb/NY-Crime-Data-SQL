import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def set_text_params(ax, title = '', xlabel = '', ylabel = '', tick_labels = None,
                    titlesize = 20, labelsize = 16, ticksize = 14, rotation = 0):
    '''
    Sets the title, x- and y-labels, and fontsizes for a Matplotlib Axes object.
    
    params:
        ax: Matplotlib Axes object to modify
        title: str to use as title for plot
        xlabel: str to use as x-label for plot
        ylabel: str to use as y-label for plot
        tick_labels: list of str to use as tick labels for plot
        titlesize: int to use as fontsize for title
        labelsize: int to use as fontsize for x- and y-labels
        ticksize: int to use as fontsize for tick labels
        rotation: int to use for rotating x-tick labels
    
    returns:
        ax: Matplotlib Axes modified object for further modification or display
    '''  
    
    ax.set_title(title, fontsize = titlesize);
    ax.set_xlabel(xlabel, fontsize = labelsize);
    ax.set_ylabel(ylabel, fontsize = labelsize);
    if tick_labels is not None:
        ax.set_xticklabels(tick_labels)
    
    ax.tick_params(axis = 'both', labelsize = ticksize)
    if rotation != 0:
        ax.tick_params(axis = 'x', rotation = rotation)
    
    return ax

def set_legend_params(ax, figure = None, legend_params = {}):
    lines, labels = ax.get_legend_handles_labels()
    
    labels = legend_params.pop('labels', labels)
    
    if figure is None:
        legend = ax.legend(handles = lines, labels = labels, **legend_params)
    else:
        legend = figure.legend(handles = lines, labels = labels, **legend_params)
    
    return legend

def annotate_data(ax, orient = 'h', labelsize = 12, precision = 0):
    if precision <= 0:
        dtype = int
    else:
        dtype = float
    if orient == 'h':
        labels = [[f'{np.round(c.get_height(), precision).astype(dtype)}' for c in s] for s in ax.containers]
    else:
        labels = [[f'{np.round(c.get_width(), precision).astype(dtype)}' for c in s] for s in ax.containers]
    
    for i, s in enumerate(ax.containers):
        ax.bar_label(s, labels = labels[i], label_type = 'edge', size = labelsize)
                 
    return

def plot_data(func, data, groupby_cols, target_cols, agg_type,
              func_params, fig = None, ax = None, fig_width = 12, fig_height = 6,
              sharex = True, sharey = True, share_legend = True,
              annotate = True, annotate_params = {'labelsize': 12, 'precision': 0},
              text_params = [{}], legend_params = None,
              save = False, save_path = ''):
    
    if agg_type == 'melt':
        tidy = data[groupby_cols + target_cols].melt(groupby_cols)
        n = 1
    else:
        tidy = data.groupby(groupby_cols).sum()[target_cols]
        n = len(target_cols)

    if ax is None:
        fig, ax = plt.subplots(n, 1, figsize = (fig_width, n * fig_height), sharex = sharex, sharey = sharey)

    if n == 1:
        func(data = tidy, ax = ax, **func_params)
        ax = set_text_params(ax, **text_params)
        if annotate:
            annotate_data(ax,**annotate_params)
        if legend_params is not None:
            set_legend_params(ax, legend_params = legend_params)
    else:
        for i in range(n):
            func(data = tidy, ax = ax[i], **func_params[i])
            ax[i] = set_text_params(ax[i], **text_params[i])
            if annotate:
                annotate_data(ax[i], **annotate_params)
            if legend_params is not None:
                if share_legend:
                        ax[i].legend().remove()
                else:
                    set_legend_params(ax[i], legend_params = legend_params[i])
                    
        if share_legend and legend_params is not None:
            set_legend_params(ax[0], figure = fig, legend_params = legend_params)
            
        plt.tight_layout()
    
    
                 
    if save:
        plt.savefig(save_path, bbox_inches = 'tight')
        
    return fig, ax