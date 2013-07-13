import inspect
import sys

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
