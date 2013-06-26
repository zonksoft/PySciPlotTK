### Introduction

The **PySciPlotTK** (Python Scientific Plotting Toolkit) provides a workflow
for the creation of plots for papers, theses, posters and presentation.
Naturally, it uses the congenial [matplotlib](http://www.matplotlib.org).

The features are:

- There are **style presets** available from which you can choose 
  (e.g. Latex and Matlab). All system settings (font size, line width etc.)
  are already set so that the plots look really nice.
- **Presets for plot sizes** are available (e.g. Revtex, A0 poster, PowerPoint
  presentation, standard Latex document). The plot width is restricted
  to one (=normal size) or two (=wide size) text columns, because most 
  journals are restrictive concerning plot widths. Also, it looks better
  anyway if you don't have 50 different plot sizes in your thesis.
- It is very easy to **replot many plots in a different style, size or file format**,
  e.g. if you want to recreate diagrams for a different journal or a presentation.
- You can supply **style/size/file format parameters in the plot script or as command line
  arguments**.
- It works well together with **Makefiles**, so you can integrate it into your preexisting
  Latex Makefile workflow.


### Available styles/sizes

- Styles: *matlab* (sans-serif fonts), *latex* (serif fonts)
- Sizes: *revtex*, *a0poster*, *presentation*, *latexa4*
- File formats: whatever [matplotlib supports](http://stackoverflow.com/questions/7608066/in-matplotlib-is-there-a-way-to-know-the-list-of-available-output-format)

### Use EasyPlotter

The main functionality is contained in the EasyPlotter class. You need to supply
the output filename and the style. The style has the syntax 'style,size', e.g.
'matlab,revtex', 'latex,revtex', 'matlab,a0poster', 'latex,presentation' etc.

*Example 1*: Plot a one-column ('normal') figure as PDF for a revtex document in Matlab style.

```python
    from pysciplottk.easyplotter import EasyPlotter
    plotter = EasyPlotter('output.pdf','latex,revtex')
    fig = plotter.normal_figure()
    ax = fig.add_subplot(111)
    ax.plot([1,2,3],[4,5,6])
    plotter.save()
```

*Example 2*: Plot a two-column ('wide') figure as PNG for a presentation in Latex style.

```python
    from pysciplottk.easyplotter import EasyPlotter
    plotter = EasyPlotter('output.png','matlab,presentation')
    fig = plotter.wide_figure(height=3)
    ax = fig.add_subplot(111)
    ax.plot([1,2,3],[4,5,6])
    plotter.save()
```

### Use command line arguments

Suppose you have a Python script whose only job is to create a plot.
You can easily change file format, style and size by supplying different command
line arguments.

Plot script *plot.py*:

```python
    import sys
    from pysciplottk.easyplotter import EasyPlotter
    plotter = EasyPlotter.from_argv(sys.argv)
    ax = plotter.normal_figure_single_ax()
    ax.plot([1,2,3],[4,5,6])
    if plotter.flag == 'plot_more':
        ax.plot([4],[19])
    plotter.save()
```

By invoking the script with various command line arguments, you can change
the result:

    python plot.py
    python plot.py output.pdf
    python plot.py output.pdf latex,revtex plot_more
    python plot.py output.png matlab,presentation do_not_plot_more

### Use a Makefile

The most convenient way is to put a lot of plot scripts which use the
*EasyPlotter.from_argv* function into a *src* directory
and use a Makefile to replot changed files or to replot everything with a
different style. You can either write your own Makefile that uses the EasyPlotter
command line interface or use the one in the *tools* directory that we wrote for you.

1. Copy the supplied Makefile to a directory.
2. Copy/create all plot scripts in a subdirectory *src* and make sure that they all
   use the *EasyPlotter.from_argv* constructor.
3. Run the Makefile.

Example make commands:

    make
    make pdf
    make eps
    make pdf STYLE=latex,revtex
    make png STYLE=matlab,a0poster
    make eps STYLE=matlab,revtex FLAG=plot_more

All of those commands execute all new/changed plot scripts in the *src* directory,
so that you end up with an up-to-date set of output files.

Every combination of file format, size, style and flag will be created in a different
subdirectory, e.g. the last line will create the directory *eps-matlab,revtex-plot_more*.

**Pro tip**: A trick to mask the actual style from the perspective of a Latex document is to create a
symlink:

    ln -s eps-matlab,revtex-plot_more eps
    
In the Latex document, you can access the files through *eps/file.eps*. If you decide later
that you e.g. like the *latex* style better than the *matlab* style and you want to add a flag,
you can change the symlink with 

    ln -s eps-matlab,revtex-do_not_plot_more eps
    
and just rerun the Latex compiler without having to change the document.
