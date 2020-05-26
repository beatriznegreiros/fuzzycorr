#!/usr/bin/python
# Filename: cPlotter.py
try:
    import os, logging    
except:
    print('ExceptionERROR: Missing fundamental packages (required: os, sys, logging).')

try:
    import numpy as np
    import matplotlib
    import matplotlib.pyplot as plt
    import matplotlib.font_manager as font_manager
    from mpl_toolkits.mplot3d import Axes3D  # imports 3D projection
    from matplotlib.ticker import LinearLocator, FormatStrFormatter
except:
    print('ExceptionERROR: Could not import matplotlib and/or numpy.')


class Plotter:
    def __init__(self, *args):
        # args[0] = full_file_name --  absolute path of a workbook
        self.set_default_parameters()
        self.dir = os.path.abspath(os.path.dirname(__file__)) + '/'
        logging.basicConfig(filename=self.dir+'logfile.log', format='%(asctime)s %(message)s', level=logging.DEBUG)
        
        
    def create_figure(self):
        try:
            self.update_fonts()
            return plt.figure(figsize=(self.width, self.height), dpi=self.resolution, facecolor=self.face_color, edgecolor=self.edge_color)
        except:
            logging.info('ERROR: Could not create figure.')
            return -1
    
    def get_color_map(self, plot_data_size):
        # plot_data_size = INT (for x-y plot -- typically the number of y-graphs, for surface plots: size(Z) elements)
        try:
            return plt.cm.get_cmap(self.color_map_type, plot_data_size + 1)  # +1 because lowest color is nearby white
        except:
            logging.info('WARNING: Could not create colormap.\n Valid color_map_types are: jet, Oranges,inferno, plasma, Greens, Blues, PuRd, RdPu, Reds, Greys')
            logging.info('         More options are available: http://matplotlib.org/users/colormaps.html')
    
    
    
    def annotate_heatmap(self, im, data=None, valfmt='{x:.2f}', textcolors=['black', 'white'], threshold=None, **textkw):
        '''
        Annotate a heatmap function from matplotlib.org
    
        Arguments:
            im         : The AxesImage to be labeled.
        Optional arguments:
            data       : Data used to annotate. If None, the image's data is used.
            valfmt     : The format of the annotations inside the heatmap.
                         This should either use the string format method, e.g.
                         '$ {x:.2f}', or be a :class:`matplotlib.ticker.Formatter`.
            textcolors : A list or array of two color specifications. The first is
                         used for values below a threshold, the second for those
                         above.
            threshold  : Value in data units according to which the colors from
                         textcolors are applied. If None (the default) uses the
                         middle of the colormap as separation.
        '''
    
        if not isinstance(data, (list, np.ndarray)):
            data = im.get_array()
    
        # Normalize the threshold to the images color range.
        if threshold is not None:
            threshold = im.norm(threshold)
        else:
            threshold = im.norm(data.max())/2.
    
        # Set default alignment to center, but allow it to be overwritten by textkw.
        kw = dict(horizontalalignment='center', verticalalignment='center')
        kw.update(textkw)
    
        # Get the formatter in case a string is supplied
        if isinstance(valfmt, str):
            valfmt = matplotlib.ticker.StrMethodFormatter(valfmt)
    
        # Loop over the data and create a `Text` for each 'pixel'. Change the text's color depending on the data.
        texts = []
        for i in range(data.shape[0]):
            for j in range(data.shape[1]):
                try:
                    kw.update(color=textcolors[im.norm(data[i, j]) > threshold])
                    text = im.axes.text(j, i, valfmt(data[i, j], None), **kw)
                    texts.append(text)
                except:
                    logging.info('WARNING: Heatmap annotation failed.')
        return texts
    
    def heatmap(self, data, row_labels, col_labels, ax=None, cbar_kw={}, cbarlabel='', **kwargs):
        '''
        Create a heatmap from a numpy array and two lists of labels (source: matplolib.org).
    
        Arguments:
            data       : A 2D numpy array of shape (N,M)
            row_labels : A list or array of length N with the labels
                         for the rows
            col_labels : A list or array of length M with the labels
                         for the columns
        Optional arguments:
            axe        : A matplotlib.axes.Axes instance to which the heatmap
                         is plotted. If not provided, use current axes or
                         create a new one.
            cbar_kw    : A dictionary with arguments to
                         :meth: matplotlib.Figure.colorbar.
            cbarlabel  : The label for the colorbar
        '''
        try:
            if not ax:
                ax = plt.gca()
        except:
            logging.info('WARNING: Heatmap axe identification failed.')
    
        # Plot the heatmap
        try:
            im = ax.imshow(data, **kwargs)  # uses vmin and vmax
        except:
            logging.info('ERROR: Heatmap creation failed (ax.imshow(data)).')
            return -1
    
        # Create colorbar
        try:
            cbar = ax.figure.colorbar(im, ax=ax, shrink=self.colorbar_shrink, aspect=self.colorbar_aspect, format=self.colorbar_format, **cbar_kw)
        except:
            logging.info('WARNING: Heatmap colorbar creation failed.')
        try:
            cbar.ax.set_ylabel(self.colorbar_label, rotation=-90, va='bottom', **self.hfont)
        except:
            logging.info('WARNING: Heatmap colorbar arrangement failed.')
    
        # We want to show all ticks...
        try:
            ax.set_xticks(np.arange(data.shape[1]))
            ax.set_yticks(np.arange(data.shape[0]))            
        except:
            logging.info('WARNING: Heatmap tick setting failed.')
    
        # Let the horizontal axes labeling appear on top
        try:
            # ... and label them with the respective list entries
            ax.set_xticklabels(col_labels, **self.hfont)
            ax.set_yticklabels(row_labels, **self.hfont)
            ax.tick_params(top=True, bottom=False, labeltop=True, labelbottom=False)
        except:
            logging.info('WARNING: Heatmap tick labeling and arrangement failed.')
    
        # Rotate the tick labels and set their alignment
        try:
            plt.setp(ax.get_xticklabels(), rotation=-30, ha='right', rotation_mode='anchor', **self.hfont)
        except:
            logging.info('WARNING: Heatmap tick label rotation failed.')
    
        # Turn spines off and create white grid
        try:
            for edge, spine in ax.spines.items():
                spine.set_visible(False)
        except:
            logging.info('WARNING: Heatmap spine and grid modifications failed.')
    
        try:
            ax.set_xticks(np.arange(data.shape[1]+1)-.5, minor=True)
            ax.set_yticks(np.arange(data.shape[0]+1)-.5, minor=True)
            ax.grid(which='minor', color='w', linestyle=self.data_line_style[0], linewidth=self.data_line_width)
            ax.tick_params(which='minor', bottom=False, left=False)
        except:
            logging.info('WARNING: Heatmap line-up failed.')
            
        if self.plot_title_mode:
            try:
                 ax.set_title(self.plot_title)
            except:
                logging.info('WARNING: Failed to make plot title.')
    
        return im, cbar

    def make_heatmap(self, Z, x_labels, y_labels, *args, **kwargs):
        # x_data = LIST of STR
        # y_data = LIST of STR
        # Z = NESTED LIST with size = (y_size, x_size) -- [y_size*[x_size elements]]
        # Documentation: https://matplotlib.org/gallery/images_contours_and_fields/image_annotated_heatmap.html
        
        self.update_fonts()
        
        try:
            fig, axe = plt.subplots(figsize=(self.width, self.height), dpi=self.resolution, facecolor=self.face_color, edgecolor=self.edge_color)
        except:
            logging.info('ERROR: Could not initiate figure.')
            return -1
        Z = np.array(Z)
        

        try:
            im, cbar = self.heatmap(Z, y_labels, x_labels, ax=axe, 
                                    vmin=self.colorbar_min_val, 
                                    vmax=self.colorbar_max_val, 
                                    cmap=self.color_map_type, 
                                    cbarlabel=self.colorbar_label)
        except:
            logging.info('ERROR: Could not create heatmap.')
            return -1
#        try:
#            texts = self.annotate_heatmap(im, valfmt=self.heatmap_annotation)
#        except:
#            logging.info('WARNING: Heatmap annotation failed.')

        try:
            fig.tight_layout()
            fig.savefig(self.save_fig_dir)
            logging.info('   Figure saved as: ' + self.save_fig_dir)
        except:
            logging.info('ERROR: Could not save figure.')
        


    def make_surface_plot(self, x_data, y_data, Z, *args, **kwargs):
        # x_data = LIST
        # y_data = LIST
        # Z = NESTED LIST with size = (y_size, x_size) -- [y_size*[x_size elements]]
        # **kwargs: 
        #       plot_type = STR: 'surface', 'scatter3D', 'trisurf', 'contour', 'contourf', 'pcolormesh', 'streamplot'
        #       projection_type = STR: '2D' or '3D'
        
        # parse optional arguments
        
        try:
            for opt_var in kwargs.items():
                if 'plot_type' in opt_var[0]:
                    # type of 3D/2D plot - default= 2D
                    plot_type = opt_var[1]

        except:
            pass

        if not ('plot_type' in locals()):
            plot_type = 'surface'
            
        three_d_plot_types = ['surface', 'trisurf', 'scatter3D']
        if plot_type in three_d_plot_types:
            projection_type = '3D'
        else:
            projection_type = '2D'     
        
        fig = self.create_figure()        
        
        try:
            if projection_type == '2D':
                axe = fig.add_subplot(self.subplot_rows, self.subplot_cols, self.subplot_index)
            else:
                axe = fig.gca(projection='3d')
        except:
            logging.info('ERROR: Could not create axe (fig.gca(projection=3d) failed).')
            return -1

        color_map = self.get_color_map(Z.__len__())

        try:
            X, Y = np.meshgrid(x_data, y_data)
        except:
            logging.info('ERROR: Could not create np.meshgrid with x_data and y_data.')

        try:
            if plot_type == 'surface':  # verified
                surf = axe.plot_surface(X, Y, Z, cmap=color_map, linewidth=self.data_line_width, antialiased=False)
            if plot_type == 'contour':  # verified
                surf = axe.contour(X, Y, Z, cmap=color_map, linewidths=self.data_line_width, linestyles=self.data_line_style[0], alpha=self.alpha_value, antialiased=False)
            if plot_type == 'contourf':  # verified
                surf = axe.contourf(X, Y, Z, self.contour_interval_no, cmap=color_map, alpha=self.alpha_value, antialiased=False)
            if plot_type == 'pcolormesh':  # not yet verified
                surf = axe.pcolormesh(X, Y, Z, cmap=color_map, linewidth=self.data_line_width, antialiased=False, alpha=self.alpha_value)
            if plot_type == 'trisurf':  # not yet verified
                surf = axe.plot_trisurf(X, Y, Z, cmap=color_map, linewidth=self.data_line_width)            
            if plot_type == 'scatter3D':  # not yet verified
                surf = axe.scatter3D(X, Y, Z)
            if plot_type == 'streamplot':  # plot vectors of velocities -- not yet verified
                # Z[1] = 2D array of x-velocites (u)
                # Z[2] = 2D array of y-velocites (v)
                surf = axe.streamplot(X, Y, Z[1], Z[2], cmap=color_map, linewidth=self.data_line_width, arrowsize=self.stream_arrow_size, arrowstyle=self.stream_arrows_style)
        except:
            logging.info('WARNING: Plotting failed.')
        
        
        if projection_type == '3D':
            axe.zaxis.set_major_formatter(FormatStrFormatter(self.number_format))

        # Labels
        try:
            axe.set_xlabel(self.x_label, **self.hfont)
            axe.set_ylabel(self.y_label, **self.hfont)
            if projection_type == '3D':
                axe.set_zlabel(self.z_label, **self.hfont)
        except:
            logging.info('WARNING: Undefined x, y and/or z axis labels.')
        
        if self.legend_active:
            fig.colorbar(surf, shrink=self.colorbar_shrink, aspect=self.colorbar_aspect)            
        
        self.setup_figure(fig, axe)
        if projection_type == '3D':
            self.save_figure(fig, 'xyz')
        else:
            self.save_figure(fig, 'xy')
        


    def make_x_y_plot(self, x_data, y_data, *args, **kwargs):
        # x_data = LIST
        # y_data = NESTED LIST: [[y_series1], [y_series2], ... ]
        # **kwargs: 
        #       plot_type = STR: 'plot', 'bar', 'barh', 'hist', 'scatter'
        
        # parse optional arguments
        try:
            for opt_var in kwargs.items():
                if 'plot_type' in opt_var[0]:
                    # type of 3D/2D plot
                    plot_type = opt_var[1]

        except:
            pass
        if not ('plot_type' in locals()):
            plot_type = 'plot'
        
        
        fig = self.create_figure()
        
        try:
            axe = fig.add_subplot(self.subplot_rows, self.subplot_cols, self.subplot_index)#, sharex=self.subplot_share_x, sharey=self.subplot_share_y)
        except:
            logging.info('ERROR: Could not create axe (add_subplot failed).')
            return -1

        color_map = self.get_color_map(y_data.__len__())


        graph_no = 0
        for y in y_data:
            try:
                if plot_type == 'plot':  # verified
                    axe.plot(x_data, y, linestyle=self.data_line_style[graph_no], color=color_map(graph_no + 1), label=self.data_labels[graph_no])
                if plot_type =='bar':  # not yet verified
                    axe.bar(x_data, y, color=self.bar_color, yerr=self.y_err_type, label=self.data_labels[graph_no])
                if plot_type =='barh':  # horizontal bar plot -- not yet verified
                    axe.barh(x_data, y, color=self.bar_color, xerr=self.x_err_type, label=self.data_labels[graph_no])
                if plot_type == 'hist':  # histogram -- not yet verified
                    axe.hist(x_data, self.hist_class_numbers)
                if plot_type == 'scatter':  # histogram -- not yet verified
                    axe.scatter(x_data, y, color=color_map(graph_no + 1), label=self.data_labels[graph_no])
            except:
                try:
                    axe.plot(x_data, y, linestyle='-', color=color_map(graph_no + 1), label='series' + str(graph_no))
                    logging.info('WARNING: Used default graph labels. Consider setting as many data_line_styles and data_labels as there are graphs.')
                except:
                    logging.info('ERROR: Plotting of graph no. ' + str(graph_no) + ' failed.')
            graph_no += 1

        # Labels
        try:
            axe.set_xlabel(self.x_label, **self.hfont)
            axe.set_ylabel(self.y_label, **self.hfont)
        except:
            logging.info('WARNING: Undefined x and/or y axis labels.')
        
        if self.legend_active:
            axe.legend(loc=self.legend_loc, prop=self.font, facecolor=self.legend_face_color, edgecolor=self.legend_edge_color, framealpha=self.legend_frame_alpha, fancybox=0)
        
        self.setup_figure(fig, axe)
        self.save_figure(fig, 'xy')
        
    def save_figure(self, fig, plot_type):
        # plot_type = STR (x-y plot: 'xy', 3D: 'xyz')
        if self.save_fig:
            try:
                if plot_type == 'xy':
                    plt.savefig(self.save_fig_dir, bbox_inches=self.fig_boxes)
                    logging.info(' * Saved plot as: ' + self.save_fig_dir)
                if plot_type == 'xyz':
                    fig.savefig(self.save_fig_dir, bbox_inches=self.fig_boxes) 
                    logging.info(' * Saved figure as: ' + self.save_fig_dir)
            except:
                logging.info('WARNING: Could not save figure as path:\n  ' + self.save_fig_dir)
                logging.info('         Hint: .JPG is not supported (use .pdf or .png).')
        
    def set_default_parameters(self):
        # FONT DEFINITIONS
        self.font_family = 'sans-serif'
        self.font_name = 'Arial'        
        self.font_size = 10.0
        self.font_style = 'normal'        
        self.font_weight = 'medium'
        self.update_fonts()      
        self.number_format = '%02f'
        
        # AXES DEFINITIONS
        self.grid_line_color = 'gray'
        self.grid_line_style = '-'
        self.grid_line_width = 0.5
        
        self.x_label = 'undefined x-label'
        self.x_lim = (0, 1)
        self.x_lim_mode = False
        self.x_tick_mode = False
        self.x_ticks = []
        self.x_err_type = []  # list of numbers corresponding to no. of x-points
        
        self.y_label = 'undefined y-label'
        self.y_lim = (0, 1)
        self.y_lim_mode = False
        self.y_ticks = []
        self.y_tick_mode = False
        self.y_err_type = []  # list of numbers corresponding to no. of y-points
        
        self.z_label = 'undefined z-label'
        self.z_lim = (0, 1)
        self.z_lim_mode = False
        self.z_ticks = []
        self.z_tick_mode = False
        
        # DATA LABELLING AND LAYOUT        
        self.data_labels = ['']  # list of strings
        self.data_line_style = ['-']
        self.data_line_width = 0.5
        self.plot_title = 'Title'
        self.plot_title_mode = False
        
        # COLOR DEFINITIONS
        self.alpha_value = 1.0  # FLOAT between 0 and 1
        self.face_color = 'w'
        self.edge_color = 'k'
        # define colormap -- more options: http://matplotlib.org/users/colormaps.html
        # alternative cmaps: jet, Oranges,inferno, plasma, Greens, Blues, PuRd, RdPu, Reds, Greys
        self.color_map_type = 'Greys'
        self.bar_color = 'green'
        
        
        # LEGEND SETTINGS
        # more legend options: https://matplotlib.org/api/_as_gen/matplotlib.pyplot.legend.html#matplotlib.pyplot.legend
        self.legend_active = False
        self.legend_edge_color = 'gray'
        self.legend_face_color = 'w'
        self.legend_frame_alpha = 1
        self.legend_loc = 'upper_right'
        
        # FIGURE CONFIGURATION
        self.width = 6.0      # FLOAT defining inches
        self.height = 4.0     # FLOAT defining inches
        self.resolution = 300  # INT defining dpi
        self.fig_boxes = 'tight' # or INT in inches
        self.save_fig = True
        self.save_fig_dir = os.path.abspath(os.path.dirname(__file__)) + '/figure.png'
        self.show_fig = False
        
        self.subplot_cols = 1
        self.subplot_rows = 1
        self.subplot_index = 1
        self.subplot_share_x = False
        self.subplot_share_y = False
        
        # COLORBAR SETTINGS
        # https://matplotlib.org/api/_as_gen/matplotlib.pyplot.colorbar.html#matplotlib.pyplot.colorbar
        self.colorbar_aspect = 10
        self.colorbar_draw_edges = False
        self.colorbar_format = '%.2f'
        self.colorbar_label = ''
        self.colorbar_shrink = 1.0
        self.colorbar_ticks = None # LIST of ticks
        self.colorbar_min_val = 0
        self.colorbar_max_val = 1
       
        
        # PLOT SPECIFIC
        self.contour_interval_no = 10
        
        self.heatmap_annotation = ''  # STR of format: '{x:.1f} t'
        
        self.hist_class_numbers = 10  # INT required for histogram plots
        
        self.stream_arrow_size = 2
        self.stream_arrow_style = '-|>'  # other options: ->, -, -[, <-, <->, <|-|>, ]-, ]-[, |-| (Bar)
       
        
    def setup_figure(self, fig, axe):
        # Ticks
        if self.x_tick_mode:
            try:
                plt.xticks(self.x_ticks, **self.hfont)
            except:
                logging.info('WARNING: x_tick_mode active but no valid x_ticks and/or hfont set.')
        if self.y_tick_mode:
            try:
                plt.yticks(self.y_ticks, **self.hfont)
            except:
                logging.info('WARNING: y_tick_mode active but no valid y_ticks and/or hfont set.')
        if self.z_tick_mode:
            try:
                plt.yticks(self.z_ticks, **self.hfont)
            except:
                logging.info('WARNING: z_tick_mode active but no valid z_ticks and/or hfont set.') 


        # control grid
        axe.grid(color=self.grid_line_color, linestyle=self.grid_line_style, linewidth=self.grid_line_width)
        if self.x_lim_mode:
            try:
                axe.set_xlim(self.x_lim)
            except:
                logging.info('WARNING: x_lim_mode active but no valid x_lim (tuple= (min, max)) defined.')
        if self.y_lim_mode:
            try:
                axe.set_ylim(self.y_lim)
            except:
                logging.info('WARNING: y_lim_mode active but no valid y_lim (tuple= (min, max)) defined.')
        if self.z_lim_mode:
            try:
                axe.set_zlim(self.z_lim)
            except:
                logging.info('WARNING: z_lim_mode active but no valid z_lim (tuple= (min, max)) defined.')
                
        if self.plot_title_mode:
            axe.set_title(self.plot_title)
                
        if self.show_fig:
            fig.show()
            plt.show()
            
    def update_fonts(self):
        self.hfont = {'family': self.font_family, 'weight': self.font_weight, 
                      'size': self.font_size, 'style': self.font_style, 
                      'fontname': self.font_name}
        self.font = font_manager.FontProperties(family=self.hfont['fontname'],
                                                weight=self.hfont['weight'],
                                                style=self.hfont['style'],
                                                size=self.hfont['size'])
        matplotlib.rcParams.update({'font.family': self.font_family})
        matplotlib.rcParams.update({'font.weight': self.font_weight})
        matplotlib.rcParams.update({'font.size': self.font_size})
        matplotlib.rcParams.update({'font.style': self.font_style})
        matplotlib.rcParams.update({'font.sans-serif': self.font_name})
        matplotlib.rcParams.update({'font.serif': 'Times'})
        # more font settings: https://matplotlib.org/users/customizing.html
 

    def __call__(self):
        print('Class Info: <type> = Plotter (uses matplotlib library)')

