
## build all poster and create links in dir './build"

ROOT=$(shell pwd)
DIRPREFIX=20
LOGDIR=$(ROOT)/logs
POSTERDIR=$(ROOT)/build

all: images
	@mkdir -p $(LOGDIR)
	@mkdir -p $(POSTERDIR)
	@ls | grep "$(DIRPREFIX).*" | while read line ; \
		do \
			echo ">>> build poster           $$line" ; \
			$(MAKE) -C $$line  > $(ROOT)/logs/$${line}.log 2>&1 ; \
			echo ">>> create link for poster $$line.pdf" ; \
			ln -sf $(ROOT)/$${line}/$${line}.pdf $(POSTERDIR)/$${line}.pdf ; \
			echo "----------------------------------------------------" ; \
		done

images:
	$(MAKE) -C images

clean:
	rm -rf $(LOGIDR) $(POSTERDIR)
	@echo "----------------------------------------------------"
	@ls | grep "$(DIRPREFIX).*" | while read line ; \
		do \
			echo ">>> clean poster           $$line" ; \
			$(MAKE) -C $$line clean  ; \
			echo "----------------------------------------------------" ; \
		done
	@$(MAKE) -C images clean
	