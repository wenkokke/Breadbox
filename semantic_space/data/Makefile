all: EN-wform.w.5.cbow.neg10.400.subsmpl.pkl


clean:
	rm -f EN-wform.w.5.cbow.neg10.400.subsmpl.txt.gz
	rm -f EN-wform.w.5.cbow.neg10.400.subsmpl.txt


clobber:
	rm -f EN-wform.w.5.cbow.neg10.400.subsmpl.pkl


EN-wform.w.5.cbow.neg10.400.subsmpl.txt:
	wget http://clic.cimec.unitn.it/composes/materials/EN-wform.w.5.cbow.neg10.400.subsmpl.txt.gz
	gunzip EN-wform.w.5.cbow.neg10.400.subsmpl.txt.gz


EN-wform.w.5.cbow.neg10.400.subsmpl.pkl: EN-wform.w.5.cbow.neg10.400.subsmpl.txt
	python -c '$(PICKLE_SPACE)'


.phony: all clean clobber


define PICKLE_SPACE
from composes.semantic_space.space import Space;from composes.utils import io_utils;io_utils.save(Space.build(data = "./EN-wform.w.5.cbow.neg10.400.subsmpl.txt", format = "dm"), "./EN-wform.w.5.cbow.neg10.400.subsmpl.pkl")
endef
