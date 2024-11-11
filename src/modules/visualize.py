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
    '''
    Sets legend parameters on a Matplotlib Axes object.
    
    args:
        ax: Matplotlib Axes object to extract artist information from and whose legend to modify.
        figure: None or Matplotlib Figure object, if None, this function works on the axis level. Otherwise,
            this function uses a figure level legend to allow manipulation of a single global legend. Default None.
        legend_params: dict of keyword arguments to pass to ax.legend() or figure.legend(), should include labels
            in its keys if custom labels are desired
    
    returns Matplotlib Legend object
    '''
    # Get arists from axis
    lines, labels = ax.get_legend_handles_labels()
    
    # Pop off the labels from the legend params dictionary to manually pass to matplotlib functions
    labels = legend_params.pop('labels', labels)
    
    # If a figure is given, work at the figure level; otherwise, work at the axis level
    if figure is None:
        legend = ax.legend(handles = lines, labels = labels, **legend_params)
    else:
        legend = figure.legend(handles = lines, labels = labels, **legend_params)
    
    return legend

def annotate_data(ax, orient = 'h', labelsize = 12, precision = 0):
    '''
    Annotates a seaborn/matplotlib barplot with the barplot values.
    
    args:
        ax: Matplotlib Axes object to modify.
        orient: 'h' or 'v', orientation of barchart, 'h' for horizontal, 'v' for vertical, defaults to 'h'
        labelsize: int, font size of labels to use for annotation
        precision: int, level of precision to pass to np.round() for annotation
    '''
    
    # If precision is less than 0, convert results to integers to remove ugly floating point decimals
    # Otherwise, use as floats
    if precision <= 0:
        dtype = int
    else:
        dtype = float
        
    # Extract labels from ax.containers and round to desired precision
    if orient == 'h':
        labels = [[f'{np.round(c.get_height(), precision).astype(dtype)}' for c in s] for s in ax.containers]
    else:
        labels = [[f'{np.round(c.get_width(), precision).astype(dtype)}' for c in s] for s in ax.containers]
    
    # Add bar labels to axis
    for i, s in enumerate(ax.containers):
        ax.bar_label(s, labels = labels[i], label_type = 'edge', size = labelsize)
                 
    return

def plot_data(func, data, groupby_cols, target_cols, agg_type,
              func_params, fig = None, ax = None, fig_width = 12, fig_height = 6,
              sharex = True, sharey = True, share_legend = True,
              annotate = True, annotate_params = {'labelsize': 12, 'precision': 0},
              text_params = [{}], legend_params = None,
              save = False, save_path = ''):
    '''
    Function to create a plot by melting or performing a groupby along specified columns using specified
        target columns. Can be used with any seaborn or matplotlib function which can take melted/groupbyed data.

    args:
        func: function signature, function to use for plotting
        data: Pandas DataFrame in ungrouped/unmelted form to use for plotting
        groupby_cols: list of str, to use to perform groupby/melting operation
        target_cols: list of str, to use as target variables for plotting
        agg_type: 'melt' or 'groupby', whether to melt or groupby the dataframe, melting is useful
            for one level of grouping, whereas groupby is more general for any level of grouping
        func_params: dict or list of dict of keyword arguments to pass to func, a list is used to control the
            function parameters for each subplot in the case of multiple plots when using agg_type groupby
        fig: None or Matplotlib Figure, figure to use for drawing the plot, if None, default to behavior defined
            by ax parameter. Has no effect if ax is None. Default None.
        ax: None or Matplotlib Axes, if None, then figure and axes objects are created using plt.subplots(),
            else, uses the passed in Axes object to plot the data. Default None.
        fig_width: int, inches for width of plot in plt.subplots(), ignored if ax is not None. Default 12.
        fig_height: int, inches for height of each subplot in plt.subplots(), ignored if ax is not None. Default 6.
        sharex: bool, whether the subplots should share the same x-axis, ignored if ax is not None. Default True.
        sharey: bool, whether the subplots should share the same y-axis, ignored if ax is not None. Default True.
        share_legend: bool, whether the subplots should use a single figure-level legend or should each have their
            own legend within their subplot. Default True.
        annotate: bool, whether to add annotations in the case of a bar plot, default True.
        annotate_params: dict of keyword arguments to pass to annotate_data() for controlling annotation formatting,
            default {'labelsize': 12, 'precision': 0}
        text_params: dict or list of dict of keyword arguments to pass to set_text_params() for controlling
            plot labels and ticks for each subplot, default list of empty dict (no modifications to plot)
        legend_params: dict of keyword arguments to pass to set_legend_params() for controlling legends,
            default None (no modifications to legends generated by func)
        save: bool, whether to save the figure to the location specified by save_path, default False
        save_path: str, path to save the figure
        
    returns: Matplotlib Figure and Matplotlib Axes with plotted data
    '''
    
    # Perform aggregation operation
    if agg_type == 'melt':
        tidy = data[groupby_cols + target_cols].melt(groupby_cols)
        n = 1
    else:
        tidy = data.groupby(groupby_cols).sum()[target_cols]
        n = len(target_cols)

    # If an Axes object was not passed in, create a new set of subplots
    if ax is None:
        fig, ax = plt.subplots(n, 1, figsize = (fig_width, n * fig_height), sharex = sharex, sharey = sharey)

    # If there is only one plot, write directly to Axes object (not subscriptable)
    if n == 1:
        func(data = tidy, ax = ax, **func_params)
        ax = set_text_params(ax, **text_params)
        if annotate:
            annotate_data(ax,**annotate_params)
        if legend_params is not None:
            set_legend_params(ax, legend_params = legend_params)
    # Else, loop through subplots and write to each subplot
    else:
        for i in range(n):
            func(data = tidy, ax = ax[i], **func_params[i])
            ax[i] = set_text_params(ax[i], **text_params[i])
            if annotate:
                annotate_data(ax[i], **annotate_params)
            if legend_params is not None:
                # If using a shared legend, remove legends from individual subplots
                if share_legend:
                        ax[i].legend().remove()
                else:
                    set_legend_params(ax[i], legend_params = legend_params[i])
        
        # Assumes that the shared legend is the same for all subplots, so extracts artists from subplot 0
        if share_legend and legend_params is not None:
            set_legend_params(ax[0], figure = fig, legend_params = legend_params)
            
        plt.tight_layout()
    
    # Saves figure to save_path
    if save:
        plt.savefig(save_path, bbox_inches = 'tight')
        
    return fig, ax