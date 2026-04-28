all:
	pdflatex Report.tex
	bibtex Report
	pdflatex Report.tex
	pdflatex Report.tex

clean:
	rm -f Report.aux Report.bbl Report.blg Report.log Report.toc Report.out
