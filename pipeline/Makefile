execute_wrapper?=
plotter: carpenter 
	@echo -e "\n==== Running fast-plotter"
	mkdir -p plotter
	$(execute_wrapper) fast_plotter -y log -c ../plot_config.yml -o plotter/ carpenter/tbl_*.csv

carpenter: curator
	@echo -e "\n==== Running fast-carpenter"
	$(execute_wrapper) fast_carpenter --profile --outdir carpenter --ncores 4 curator/file_list.yml ../sequence_cfg.yml
	touch carpenter

curator: input_files
	@echo -e "\n==== Running fast-curator"
	mkdir -p curator
	rm -f curator/file_list.yml
	fast_curator -q xrootd -o curator/file_list.yml -t events -d data --data input_files/HEPTutorial/files/data.root
	fast_curator -q xrootd -o curator/file_list.yml -t events -d dy --mc input_files/HEPTutorial/files/dy.root
	fast_curator -q xrootd -o curator/file_list.yml -t events -d qcd --mc input_files/HEPTutorial/files/qcd.root
	fast_curator -q xrootd -o curator/file_list.yml -t events -d single_top --mc input_files/HEPTutorial/files/single_top.root
	fast_curator -q xrootd -o curator/file_list.yml -t events -d ttbar --mc input_files/HEPTutorial/files/ttbar.root
	fast_curator -q xrootd -o curator/file_list.yml -t events -d wjets --mc input_files/HEPTutorial/files/wjets.root
	fast_curator -q xrootd -o curator/file_list.yml -t events -d ww --mc input_files/HEPTutorial/files/ww.root
	fast_curator -q xrootd -o curator/file_list.yml -t events -d wz --mc input_files/HEPTutorial/files/wz.root
	fast_curator -q xrootd -o curator/file_list.yml -t events -d zz --mc input_files/HEPTutorial/files/zz.root

input_files:
	@echo -e "\n==== Downloading input files"
	mkdir input_files &&\
	cd input_files  && \
	wget ippog.org/sites/ippog.web.cern.ch/files/HEPTutorial_0.tar &&\
	tar -xf HEPTutorial_0.tar HEPTutorial/files/

clean: clean-plotter clean-carpenter clean-curator clean-input_files

clean-plotter:
	rm -rf plotter

clean-carpenter:
	rm -rf carpenter

clean-curator:
	rm -rf curator

clean-input_files:
	rm -rf input_files
