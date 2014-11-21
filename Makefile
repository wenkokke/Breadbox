DATA_DIR = semantic_space/data

all:
	$(MAKE) -C $(DATA_DIR) all

clean:
	$(MAKE) -C $(DATA_DIR) clean

clobber:
	$(MAKE) -C $(DATA_DIR) clobber

.phony: all clean clobber
