
all: cars

cars: car_black.svg
	@cat ../hda_colors.txt  | while read line ;\
	  do \
	  	color=`echo $$line | awk '{print $$1}'` ;\
	  	name=`echo $$line | awk '{print $$2}'` ;\
	  	if [ -z "$$color" ] ; then \
	  		continue ;\
	  	fi ;\
	  	echo ">>> creating car_$${name}.svg using colorcode $$color" ;\
	  	cat car_black.svg | sed "s/style=\"fill:#000000\"/style=\"fill:#$$color\"/g" > car_$${name}.svg ;\
	  	echo ">>> converting car_$${name}.svg to car_$${name}.pdf" ;\
	  	svg2pdf car_$${name}.svg car_$${name}.pdf ;\
	  done
