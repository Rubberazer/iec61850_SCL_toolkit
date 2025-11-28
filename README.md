# iec61850_SCL_toolkit

A few humble Python script that I use at work to extract variables from SCL files.
Put together in a rush and clunky as hell, but it seems to do the job. 


No external dependencies, only the Python standard lib.


Supports all the SCL formats e.g. .icd, .cid. iid and .scd, if there are several IEDs into an scd file, it will extract all of them. 

## USAGE

To extract the Data Objects (DO): 

	python icd_DO_extractor.py SCL_file_name
	
	
It is going to produce two files:

	
- variables_extract_DO.csv -> all the DOs in the IEDs
	
- variables_report.csv  -> only the DOs linked to the reports set up in the IEDs


To extract the Data Objects (DO) with all their Data Attributes (DA): 

	python icd_DA_extractor.py SCL_file_name
	
	
It is going to produce this file:

	
- variables_extract_DA.csv -> all the DOs with their DAs in the IEDs



