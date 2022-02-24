CURDIR = $(shell pwd)
MAINDOCUMENT = $(shell basename $(CURDIR))
QRSRC = qrcode.txt

all: $(MAINDOCUMENT).tex
	xelatex $(MAINDOCUMENT).tex
	
qrcode:
	if [ -r $(QRSRC) ] ; then \
		qrencode -l L -v 1 -o qrcode.png `head -n 1 qrcode.txt` ; \
	fi
	
clean:
	rm -f $(MAINDOCUMENT).aux $(MAINDOCUMENT).log a0header.ps $(MAINDOCUMENT).pdf
	
.phony: clean
