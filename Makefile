DATA_DIR      = data
DATA_TXT_GZ   = $(DATA_DIR)/EN-wform.w.5.cbow.neg10.400.subsmpl.txt.gz
DATA_TXT      = $(DATA_DIR)/EN-wform.w.5.cbow.neg10.400.subsmpl.txt
DATA_TXT_NOUN = $(DATA_DIR)/noun_space.txt
DATA_PKL_NOUN = $(DATA_DIR)/noun_space.pkl


$(DATA_TXT):
	wget -x -nc -P $(DATA_DIR) http://clic.cimec.unitn.it/composes/materials/EN-wform.w.5.cbow.neg10.400.subsmpl.txt.gz
	gunzip $(DATA_TXT_GZ)

$(DATA_TXT_NOUN): | $(DATA_TXT)
	python -c "import main; main.create_noun_only('$(DATA_TXT)','$(DATA_TXT_NOUN)')"

$(DATA_PKL_NOUN): | $(DATA_TXT_NOUN)
	python -c "import main; main.create_pickle('$(DATA_TXT_NOUN)','$(DATA_PKL_NOUN)')"

build: $(DATA_PKL_NOUN)

dependencies:
	# install dissect
	pip install numpy scipy cython sparsesvd
	git submodule update --init --recursive
	cd dissect; python setup.py install
	# install auxiliary dependencies
	pip install future names enum

serve: $(DATA_PKL_NOUN)
	@python -c "import main; main.serve('$(DATA_PKL_NOUN)')"

play:
	python -c "import main; main.play()"

.phony: build dependencies serve play
