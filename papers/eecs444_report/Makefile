DOC = paper
INCLUDE_BIB = yes

%.pdf : %.dot
	dot -Tpdf $*.dot -o $*.pdf

build: $(FIGS)
ifeq ($(INCLUDE_BIB),yes)
	pdflatex $(DOC) > /dev/null
	bibtex $(DOC) > /dev/null
endif
	pdflatex $(DOC) > /dev/null
	pdflatex $(DOC) > /dev/null

kde: build
	kpdf $(DOC).pdf

kde4: build
	okular $(DOC).pdf

mac: build
	open $(DOC).pdf

all: build

clean:
	rm -f *.aux *.bbl *.blg *.log *.pdf

