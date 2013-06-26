#This scripts expects all plotscripts to be in the src directory and creates an
#output directory with the files in the given file format (pdf, png, eps) and style.
#This is VERY convenient and you should definitely check it out when you are
#working on a paper or a thesis!

#STYLE can be latex or matlab. Use 'make pdf STYLE=matlab' to set the style.
#The default setting is latex.
#FLAG can be used to supply an additional setting to the plot script,
#e.g. FLAG=poster could make the script omit a legend.

#Tip: you can mask the style choice by creating a symlink, e.g. from the directory
#'poster' to the directory 'eps-matlab,revtex-default'
#Tip: common STYLE-FLAG combinations can be bookmarked by creating a make command.

STYLE = latex,revtex
FLAG = default

SRC = $(wildcard src/*.py)

PDF = $(patsubst src/%.py,pdf-$(STYLE)-$(FLAG)/%.pdf,$(SRC)) 
PNG = $(patsubst src/%.py,png-$(STYLE)-$(FLAG)/%.png,$(SRC)) 
EPS = $(patsubst src/%.py,eps-$(STYLE)-$(FLAG)/%.eps,$(SRC)) 

default: pdf

all: pdf png

pdf: $(PDF)

png: $(PNG)

eps: $(EPS)

pdf-$(STYLE)-$(FLAG)/%.pdf: src/%.py
	-mkdir pdf-$(STYLE)-$(FLAG)
	python $< $@ $(STYLE) $(FLAG)
	
eps-$(STYLE)-$(FLAG)/%.eps: src/%.py
	-mkdir eps-$(STYLE)-$(FLAG)
	python $< $@ $(STYLE) $(FLAG)	
	
png-$(STYLE)-$(FLAG)/%.png: src/%.py
	-mkdir png-$(STYLE)-$(FLAG)
	python $< $@ $(STYLE) $(FLAG)
	
clean:
	-rm -r png*
	-rm -r pdf*

#inkscape t.svg --export-pdf=t.pdf
