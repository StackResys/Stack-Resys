DOC=midway
.PHONY: view clean

$(DOC).pdf: *.tex *.sty
	pdflatex $(DOC).tex

view:
	evince $(DOC).pdf&

clean:
	rm -rf $(DOC).aux $(DOC).pdf *.log
