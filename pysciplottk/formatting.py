import inspect
import sys
import matplotlib

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
                    
