FIGS = ast_1.dot ast_2.dot
PNGS = ast_1.png ast_2.png
.SUFFIXES: .dot .png

figs : $(FIGS:.dot=.png)

.dot.png:
	dot -Tpng -o $*.png $*.dot

clean:
	-rm $(PNGS)


