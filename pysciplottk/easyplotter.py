from matplotlib.figure import Figure
from matplotlib.axes import Axes
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib import artist
import sys
from pysciplottk.formatting import get_formatting_class
from pysciplottk.sizes import get_size_class

# XXX: add additional formatting: 'latex,revtex', 'matplotlib,poster'...
# Smells like Builder pattern (at least the 'extended' version)

# XXX: introduce fct to save the data so that the script can either
# use the saved data (with possibly changed plot arrangement, line widths, ...)
# or recalculate it.

# XXX: Make properties private.
    
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
