"""
A scientific plotting convenience class called EasyPlotter.

You can choose between the styles:
- latex
- matlab

...as well as the formats:
- revtex
- a0poster

This choice can be given to the EasyPlotter class through the command line
arguments of your script (e.g. by using a Makefile) or "manually" by using
the default constructor.

The width of the plots is fixed and can be
- normal_figure
- wide_figure

with a variable height (there is also a default value).

When finished, there is a save function to save to plot to a file.

The central class is EasyClass - please also see its documentation below!
"""

from matplotlib.figure import Figure
from matplotlib.axes import Axes
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib import artist
import matplotlib
import sys
import inspect

# XXX: add additional formatting: 'latex,revtex', 'matplotlib,poster'...
# Smells like Builder pattern (at least the 'extended' version)

# XXX: introduce fct to save the data so that the script can either
# use the saved data (with possibly changed plot arrangement, line widths, ...)
# or recalculate it.

# XXX: Make properties private.

class SizesBase:
    """
    Base class for classes that contain the size and font specifications
    for a certain publication format (e.g. Revtex, A0 poster...). The subclasses
    only contain information about sizes and do not set a specific style (e.g.
    font type, other specifics).
    """
    def intensive_properties(self, format_name):
        """
        Return font size, title size and line width
        for a given format (e.g. 'matlab', 'latex')
        """
        return (self.fontsize[format_name],
                self.titlesize[format_name],
                self.linewidth[format_name])
    
class SizesRevtex(SizesBase):
    """
    Specify the plot format for Revtex plots.
    """
    size_name = 'revtex'
    normal_figure_width = 243./72.
    normal_figure_default_height = 2.
    wide_figure_width = 482./72.
    wide_figure_default_height = 4. 
    fontsize = {'matlab': 7,
                'latex': 8}
    titlesize = {'matlab': 8,
                 'latex': 9}
    linewidth = {'matlab': 0.4,
                 'latex': 0.4}      
    
class SizesA0poster(SizesBase):
    """
    Specify the plot format for A0 poster plots.
    """
    size_name = 'a0poster'
    normal_figure_width = 700./72.
    normal_figure_default_height = 500./72.
    wide_figure_width = 1400./72.
    wide_figure_default_height = 500./72.
    fontsize = {'matlab': 14,
                'latex': 16}
    titlesize = {'matlab': 16,
                 'latex': 18}
    linewidth = {'matlab': 1,
                 'latex': 1}
                                     
def get_size_class(size_name):
    """
    Get the size format class (subclass of SizesBase, e.g. SizesRevtex,
    SizesA0poster) by its name ('revtex', 'a0poster', etc.).
    It returns the class, if found.
    """
    for name, obj in inspect.getmembers(sys.modules[__name__]):
        if (inspect.isclass(obj) and issubclass(obj, SizesBase) and
            obj is not SizesBase):
            if obj.size_name == size_name:
                return obj
    raise KeyError('size_name %s not found' % size_name)
              
                     
class FormattingBase:
    """
    Base class for plot style parameter sets (e.g. Latex, Matlab,..)
    """
    pass
   
class FormattingLatex(FormattingBase):
    """
    Provides functions to set the Matplotlib global parameters to Latex
    formatting.
    """
    format_name = 'latex'
    def set_matplotlib_global_parameters(self, sizes):
        """
        Set default style parameters for matplotlib.
        """
        
        fontsize, titlesize, linewidth = \
            sizes.intensive_properties(self.format_name)
                    
        matplotlib.rcParams['lines.linewidth'] = linewidth
        matplotlib.rcParams['patch.linewidth'] = linewidth
        matplotlib.rcParams['axes.linewidth'] = linewidth
        matplotlib.rcParams['axes.titlesize'] = titlesize
        matplotlib.rcParams['grid.linewidth'] = linewidth
        matplotlib.rcParams['font.size'] = fontsize
        matplotlib.rcParams['font.family'] = 'serif'
        matplotlib.rcParams['xtick.major.width'] = linewidth
        matplotlib.rcParams['xtick.minor.width'] = linewidth
        matplotlib.rcParams['text.usetex'] = True
        matplotlib.rcParams['font.serif'] = ['Computer Modern Roman']
        matplotlib.rcParams['font.monospace'] = ['Computer Modern Typewriter']
        
class FormattingMatlab(FormattingBase):
    """
    Provides functions to set the Matplotlib global parameters to Matlab
    formatting.
    """
    format_name = 'matlab'
    def set_matplotlib_global_parameters(self, sizes):
        """
        Set default style parameters for matplotlib.
        """ 
        
        fontsize, titlesize, linewidth = \
            sizes.intensive_properties(self.format_name)
                        
        matplotlib.rcParams['lines.linewidth'] = linewidth
        matplotlib.rcParams['patch.linewidth'] = linewidth
        matplotlib.rcParams['axes.linewidth'] = linewidth
        matplotlib.rcParams['axes.titlesize'] = fontsize
        matplotlib.rcParams['grid.linewidth'] = linewidth
        matplotlib.rcParams['font.size'] = fontsize        
        matplotlib.rcParams['axes.titlesize'] = titlesize    
        
def get_formatting_class(format_name):
    """
    Get the style format class (subclass of Formatting, e.g. FormattingMatlab,
    FormattingLatex) by its name ('latex', 'matlab' etc.).
    It returns the class, if found.
    """
    for name, obj in inspect.getmembers(sys.modules[__name__]):
        if (inspect.isclass(obj) and issubclass(obj, FormattingBase) and
            obj is not FormattingBase):
            if obj.format_name == format_name:
                return obj
    raise KeyError('format_name %s not found' % format_name)  
                    
    
class EasyPlotter:
    """
    EasyPlotter provides a convenient plotting framework and assists in
    style, size and saving of the plots.
    
    You can either set the style parameters by getting them from the
    command line (using EasyPlotter.from_argv()) or by setting them directly
    (using the default constructor).
    
    Example with format parameters from the command line (save the file to e.g. plot.py):
    
    >>> from pysciplottk.easyplotter import EasyPlotter
    >>> import sys
    >>> plotter = EasyPlotter.from_argv(sys.argv)
    >>> ax = plotter.normal_figure_single_ax()
    >>> ax.plot([1,2,3],[4,5,6])
    >>> plotter.save()
    
    Execute the script using "python plot.py output.pdf"
    
    Example with format parameters directly given to the constructor:
    >>> from pysciplottk.easyplotter import EasyPlotter
    >>> plotter = EasyPlotter('output.pdf','matlab,revtex',flag='do_legend')
    >>> fig = plotter.normal_figure(height=8)
    >>> ax = fig.add_subplot(121)
    >>> ax2 = fig.add_subplot(122)    
    >>> ax.plot([1,2,3],[4,5,6])
    >>> ax2.plot([1,2,3],[4,5,6])    
    >>> if plotter.flag == 'do_legend'):
    ...     ax.legend()
    >>> plotter.save()
    """
    def __init__(self, output_fname, output_formatting='latex,revtex', flag='default'):
        """
        output_fname: Output filename. The ending determines the format.
        output_formatting: output format and output size, separated by comma.
                           E.g. 'latex,revtex', 'matlab,a0poster'
        flag: can be anything. Used by the plot script (not the class!!!) 
              to do something differently.
              E.g.:
              - omit a legend or curve
              - different plot arrangement
              
        If you check output_format, output_size and flag in your script,
        we suggest only to use flag to change the contents and the others
        only to change custom formatting (e.g. inset font).
        """
        self.output_format, self.output_size = output_formatting.split(',')
        self.output_fname = output_fname
        self.flag = flag
        self.figure = None
        
        self.formatting = get_formatting_class(self.output_format)()
        self.size = get_size_class(self.output_size)()
        
        self.formatting.set_matplotlib_global_parameters(self.size)

    @classmethod 
    def from_argv(cls, argv, default_formatting = 'latex', default_type='pdf',
                  default_flag='default'):
        """
        Expects a script call like this:
        
        python scriptname.py output_fname output_formatting flag
        
        or:
        
        python scriptname.py output_fname output_formatting 
        
        or:
        
        python scriptname.py output_fname
        
        or:
        
        python scriptname.py
        """
        
        if len(argv) == 4:
            _, output_fname, output_formatting, flag = argv
        if len(argv) == 3:
            _, output_fname, output_formatting = argv
            flag = default_flag
        if len(argv) == 2:
            _, output_fname = argv
            output_formatting = default_formatting
            flag = default_flag
        if len(argv) == 1:
            output_fname = argv[0] + '.' + default_type
            flag = default_flag
            output_formatting = default_formatting
            
        return cls(output_fname, output_formatting, flag)
        
    def set_font_size(self, fontsize):
        """
        Set the default font size manually.
        """
        if output_formatting == 'latex':
            self.set_matplotlib_global_latex_parameters(fontsize=fontsize)
        elif output_formatting == 'matlab':
            self.set_matplotlib_global_matlab_parameters(fontsize=fontsize)         
        
    def normal_figure(self, height=None):
        """
        Returns a figure of normal size. You can change the
        setting here once, and all plotscripts where you
        use the function will follow.

        Example:
        >>> fig = plotutility.normal_figure()
        >>> ax = fig.add_subplot(111)
        >>> ax.plot(x,y)
        """
        
        width = self.size.normal_figure_width
        if height is None:
            height = self.size.normal_figure_default_height      

        self.figure = Figure(figsize=(width, height))
        return self.figure
        
    def normal_figure_single_ax(self, height=None):
        """
        Creates a normal figure with one axes and returns
        the axes object.
        """
        fig = self.normal_figure(height)
        ax = fig.add_subplot(111)
        return ax

    def wide_figure(self, height=None):
        """
        Returns a wide figure.
        """
        width = self.size.wide_figure_width
        if height is None:
            height = self.size.wide_figure_default_height      
        self.figure = Figure(figsize=(width, height))
        return self.figure
        
    def save(self, dpi=300):
        """
        Save the figure.
        """
        canvas = FigureCanvasAgg(self.figure)
        canvas.print_figure(self.output_fname,dpi=dpi)        
