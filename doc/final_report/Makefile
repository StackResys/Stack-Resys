DOC=final
.PHONY: view clean

$(DOC).pdf: $(DOC).dvi
	dvipdf $(DOC).dvi

$(DOC).dvi: *.tex *.sty *.bib
	latex $(DOC).tex
	bibtex $(DOC)
	latex $(DOC).tex
	latex $(DOC).tex

view:
	evince $(DOC).pdf&

clean:
	 \rm -f *.dvi *.bbl *.aux *.log *.blg *.toc
