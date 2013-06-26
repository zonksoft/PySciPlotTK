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

EasyPlotter provides a convenient plotting framework and assists in
style, size and saving of the plots.
You can either set the style parameters by getting them from the
command line (using EasyPlotter.from_argv()) or by setting them directly
(using the default constructor).
Example with format parameters from the command line (save the file to e.g. plot.py)::

    from pysciplottk.easyplotter import EasyPlotter
    import sys
    plotter = EasyPlotter.from_argv(sys.argv)
    ax = plotter.normal_figure_single_ax()
    ax.plot([1,2,3],[4,5,6])
    plotter.save()
    
Execute the script using "python plot.py output.pdf"
Example with format parameters directly given to the constructor::

    from pysciplottk.easyplotter import EasyPlotter
    plotter = EasyPlotter('output.pdf','matlab,revtex',flag='do_legend')
    fig = plotter.normal_figure(height=8)
    ax = fig.add_subplot(121)
    ax2 = fig.add_subplot(122)
    ax.plot([1,2,3],[4,5,6])
    ax2.plot([1,2,3],[4,5,6])
    if plotter.flag == 'do_legend'):
        ax.legend()
    plotter.save()
