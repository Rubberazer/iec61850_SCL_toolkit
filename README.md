# iec61850_SCL_toolkit

A humble Python script that I use at work to extract variables from SCL files.
Put together in a rush and clunky as hell, but it seem to do the job. It doesnt use any external dependencies, only the Python standard lib.
Supports all the SCL formats e.g. .icd, .cid. iid and .scd, if there are several IED into an scd file it will extract all of them. 

## USAGE

The usual: 

	python icd_DO_extractor.py SCL_file_name
	
	
It is going to produce two files:

	-variables_extract.csv -> all the DOs in the IEDs
	
	-variables_report.csv  -> only the DOs linked to the reports set up in the IEDs
	
	

