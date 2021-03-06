"""
The graphics module contains functions to format scatter and time series 
plots for reporting.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import textwrap
import os
import logging

try:
    from nose.tools import nottest as _nottest
except ImportError:
    def _nottest(afunction):
        return afunction
        
logger = logging.getLogger(__name__)

def plot_scatter(x,y,xaxis_min=None, xaxis_max=None, yaxis_min=None, yaxis_max=None):
    """
    Create a scatter plot.  If x and y have the same number of columns, then 
    the columns of x are plotted against the corresponding columns of y, in order.
    If x (or y) has 1 column, then that column of data is plotted against all
    the columns in y (or x).
    
    Parameters
    ----------
    x : pd.DataFrame
        x data
    
    y : pd.DataFrame
        y data
    
    xaxis_min : float (optional)
        X-axis minimum        
        
    xaxis_max : float (optional)
        X-axis maximum    
        
    yaxis_min : float (optional)
        Y-axis minimum            
        
    yaxis_max : float (optional)
        Y-axis maximum         
    """
    
    ax = plt.gca()

    try:
        if x.shape[1] == y.shape[1]:
            for i in range(x.shape[1]):
                plt.plot(x.iloc[:,i],y.iloc[:,i], '.', markersize=3) #, color=next(colors))
                plt.xticks(rotation='vertical')
                plt.hold(True)
        elif x.shape[1] != y.shape[1]:
            if x.shape[1] == 1:
                for col in y.columns:
                    plt.plot(x,y[col], '.', markersize=3) #, color=next(colors))
                    plt.xticks(rotation='vertical')
                    plt.hold(True)
            elif y.shape[1] == 1:
                for col in x.columns:
                    plt.plot(x[col],y, '.', markersize=3) #, color=next(colors))
                    plt.xticks(rotation='vertical')
                    plt.hold(True)
    except:
        plt.text(0.3,0.5,'Insufficient Data', fontsize=8)
    
    # Format axis
    xmin_plt, xmax_plt = plt.xlim()
    ymin_plt, ymax_plt = plt.ylim()
    if xaxis_min is None:
        xaxis_min = xmin_plt
    if xaxis_max is None:
        xaxis_max = xmax_plt
    if yaxis_min is None:
        yaxis_min = ymin_plt
    if yaxis_max is None:
        yaxis_max = ymax_plt
    plt.xlim((xaxis_min, xaxis_max))
    plt.ylim((yaxis_min, yaxis_max))
    ax.tick_params(axis='both', labelsize=8)
    box = ax.get_position()
    ax.set_position([box.x0, box.y0+0.15, box.width, box.height*0.75])
    
def plot_timeseries(data, tfilter=None, test_results_group=None, xaxis_min=None, xaxis_max=None, yaxis_min=None, yaxis_max=None):
    """
    Create a time series plot using each column in the DataFrame.
    
    Parameters
    ----------
    data : pd.DataFrame
        Data, indexed by time
        
    tfilter : pd.Series (optional)
        Boolean values used to include time filter in the plot 
        
    test_results_group : pd.DataFrame (optional)
        Test results for a particular variable.  To group test results by variable, use
        grouped = pm.test_results.groupby(['System Name', 'Variable Name']).
    
    xaxis_min : float (optional)
        X-axis minimum        
        
    xaxis_max : float (optional)
        X-axis maximum    
        
    yaxis_min : float (optional)
        Y-axis minimum            
        
    yaxis_max : float (optional)
        Y-axis maximum   
    """
    
    ax = plt.gca()
    
    try:
        # plot timeseries
        if isinstance(data, pd.Series):
            data.plot(ax=ax, grid=False, legend=False, color='k', fontsize=8, rot=90, label='Data', x_compat=True)
        else:
            data.plot(ax=ax, grid=False, legend=False, fontsize=8, rot=90, label='Data')
    
        if tfilter is not None:
            # add tfilter        
            temp = np.where(tfilter - tfilter.shift())
            temp = np.append(temp[0],len(tfilter)-1)
            count = 0
            for i in range(len(temp)-1):
                if tfilter[temp[i]] == 0:
                    if count == 0:
                        ax.axvspan(data.index[temp[i]], data.index[temp[i+1]], facecolor='k', alpha=0.2, label='Time filter')
                        count = count+1
                    else:
                        ax.axvspan(data.index[temp[i]], data.index[temp[i+1]], facecolor='k', alpha=0.2)     
        
        # add errors 
        try:
            if test_results_group.empty:
                test_results_group = None
        except:
            pass
        if test_results_group is not None:
            key2 = test_results_group['Error Flag']
            grouped2 = test_results_group.groupby(key2)
            
            for error_flag in key2.unique():
                test_results_group2 = grouped2.get_group(error_flag)
                
                error_label = '\n'.join(textwrap.wrap(error_flag, 30))
                if len(test_results_group2.index.values) > 4:
                    warning_label = '\n'.join(textwrap.wrap('Warning ' + str(test_results_group2.index.values[0:4]).strip('[]') + '...', 30))
                else:
                    warning_label = '\n'.join(textwrap.wrap('Warning ' + str(test_results_group2.index.values).strip('[]'), 30))
                error_label = error_label + '\n' + warning_label
                
                date_idx2 = np.array([False]*len(data.index))
                for row2 in range(len(test_results_group2.index)):
                    date_idx2 = date_idx2 + ((data.index >= test_results_group2.iloc[row2,2]) & (data.index <= test_results_group2.iloc[row2,3]))
                
                if sum(date_idx2) == 0:
                    continue
                
                data2 = data[date_idx2]
                if error_flag in ['Duplicate timestamp', 'Missing data', 'Corrupt data', 'Nonmonotonic timestamp']:
                    continue
                if "Data <" in error_flag:
                    try:
                        ax.scatter(data2.index, data2.values, c='r', marker='+', label=error_label)   
                    except:
                        ax.scatter(data2.index[0], data2.values[0], c='r', marker='+', label=error_label) 
                elif "Data >" in error_flag:
                    try:
                        ax.scatter(data2.index, data2.values, c='r', marker='+', label=error_label) 
                    except:
                        ax.scatter(data2.index[0], data2.values[0], c='r', marker='+', label=error_label) 
                else:
                    try:
                        ax.scatter(data2.index, data2.values, c='g', marker='+', label=error_label)  
                    except:
                        ax.scatter(data2.index[0], data2.values[0], c='g', marker='+', label=error_label) 
        
        # Format axis
        xmin_plt, xmax_plt = plt.xlim()
        ymin_plt, ymax_plt = plt.ylim()
        if tfilter is not None:
            ymin_plt = np.nanmin(data[tfilter].values)
            ymax_plt = np.nanmax(data[tfilter].values)
        if np.abs(ymin_plt - ymax_plt) < 0.01:
            ymin_plt, ymax_plt = plt.ylim()
    except:
        plt.text(0.3,0.5,'Insufficient Data', fontsize=8)
        xmin_plt, xmax_plt = plt.xlim()
        ymin_plt, ymax_plt = plt.ylim()
    
    # Format axis
    y_range = (ymax_plt - ymin_plt)
    if xaxis_min is None:
        xaxis_min = xmin_plt
    if xaxis_max is None:
        xaxis_max = xmax_plt
    if yaxis_min is None:
        yaxis_min = ymin_plt-y_range/10
    if yaxis_max is None:
        yaxis_max = ymax_plt+y_range/10
    plt.xlim((xaxis_min, xaxis_max))
    plt.ylim((yaxis_min, yaxis_max))
    ax.get_yaxis().get_major_formatter().set_useOffset(False)
    ax.tick_params(axis='both', labelsize=8)
    plt.xlabel('Time', fontsize=8)
    box = ax.get_position()
    ax.set_position([box.x0, box.y0+0.15, box.width, box.height*0.75])

def plot_colorblock(values, vmin=0, vmax=1, nColors=12, colors=[(0.75, 0.15, 0.15), (1, 0.75, 0.15), (0.15, 0.75, 0.15)]):
    """ 
    Create a colorblock figure.  Default color scheme is red to yellow to green with 12 colors.  
    This function can be used to generate dashboards with simple color indicators in each cell.
    
    Parameters
    -----------
    values : 2D np.array
        Values to plot in the colorblock
    
    vmin : float (optional)
        Colomap minimum, default = 0
    
    vmax : float (optional)
        Colomap maximum, default = 1
    
    num_colors : int (optional)
        Number of colors in the colormap
    
    colors : list (optional)
        List of colors, colors can be specified in any way understandable by matplotlib.colors.ColorConverter.to_rgb().
        Default is red to yellow to green.
    """
    from matplotlib.colors import LinearSegmentedColormap
    cmap = LinearSegmentedColormap.from_list(name='custom', colors = colors, N=nColors)
    
    fig = plt.imshow(values, cmap=cmap, aspect='equal', vmin=vmin, vmax=vmax)
    plt.axis('off')
    fig.axes.get_xaxis().set_visible(False)
    fig.axes.get_yaxis().set_visible(False)
    
@_nottest
def plot_test_results(filename_root, pm, image_format='png', dpi=500, figsize=(7.0, 2.5)):
    """
    Create test results graphics which highlight data points that
    failed a quality control test.

    Parameters
    ----------
    filename : string
        Filename root, with full path.  
        Each grpahics filename is appended with an integer.
        For example, filename_root = 'C:\\\\pecos\\\\results\\\\test' will generate a file named 
        'C:\\\\pecos\\\\results\\\\test1.png'.
        The directory ''C:\\\\pecos\\\\results' must exist.

    pm : PerformanceMonitoring object
        Contains data (pm.df) and test results (pm.test_results)
        
    image_format : string  (optional)
        Image format, default = 'png'
    
    """
    
    filename_root = os.path.abspath(filename_root)
    
    # Colect file names
    test_results_graphics = []
    
    if pm.test_results.empty:
        return test_results_graphics

    graphic = 0

    tfilter = pm.tfilter

    grouped = pm.test_results.groupby(['System Name', 'Variable Name'])

    for name, test_results_group in grouped:
        if name[1] == ' ':
            continue
        elif name[0] == '':
            col_name = str(name[1])
        else:
            col_name = str(name[0]) + ":" + str(name[1])


        if test_results_group['Error Flag'].all() in ['Duplicate timestamp', 'Missing data', 'Corrupt data', 'Missing timestamp', 'Nonmonotonic timestamp']:
            continue
        logger.info("Creating graphic for " + col_name)
        plt.figure(figsize = figsize)
        plot_timeseries(pm.df[col_name], tfilter, test_results_group = test_results_group)

        ax = plt.gca()
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width*0.65, box.height])
        plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize=8)
        plt.title(col_name, fontsize=8)
        
        filename = filename_root + str(graphic) + '.' + image_format
        test_results_graphics.append(filename)
        plt.savefig(filename, format=image_format, dpi=dpi)
        
        graphic = graphic + 1
        plt.close()

    return test_results_graphics

