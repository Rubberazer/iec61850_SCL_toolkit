#Script to extract variables from SCL files
import xml.etree.ElementTree as etree
import sys

# Auxiliary functions
def verify_if_none(x):
    if x is not None:
        return x
    else:
        return ''

# Arguments
file_name = ''
try:
    file_name = sys.argv[1]
except:
    print('SCL file name missing, please provide a file name')

# Opening & parsing SCL file
try:
    tree = etree.parse(file_name)
except:
    print('File not found, non existent,  wrong file name or path')
root = tree.getroot()

# Main variables
IEDs = []
IED_names = []
LDs_total = []
LN_total = []
DOs = []
variables_DO = []

# Find IEDs
print('-------IED NAMES AND COUNT--------')
IEDs = root.findall('.//{*}IED')

for IED in IEDs:
    IED_name = IED.get('name')
    IED_names.append(IED_name)
    print(IED_name)

IED_count = len(IEDs)
print('IED count:' + str(IED_count))

# Find Logical Devices
print('-------LOGICAL DEVICES--------')

for IED in IEDs:
    LDs = IED.findall('.//{*}LDevice')
    LDs_total.append(LDs)

for LDs in LDs_total:
    for LD in LDs:
        LD_name = LD.get('inst')
        print(LD_name)        

# Find Logical Nodes for each Logical Device
for LDs in LDs_total:
    for LD in LDs:
        LNs = LD.findall('./{*}LN')
        LNOs = LD.findall('./{*}LN0')
        LN_total.extend(LNs)
        LN_total.extend(LNOs)
        LNs.clear()
        LNOs.clear()

for LN in LN_total:
    if LN.get('prefix'):
        LN_prefix = LN.get('prefix')
        LN_name = LN.get('lnClass')
        LN_inst = LN.get('inst')
        print('-------LN PREFIX + LN CLASS + INSTANCE--------')
        print(LN_prefix + LN_name + LN_inst)

LN_number = len(LN_total)
print('--LN Number:' + str(LN_number))

# Find Logical Nodes data templates

templates = root.findall('.//{*}LNodeType')
templates_DO = root.findall('.//{*}DOType')

# Getting the template DOs
print('-------TEMPLATES ID--------')

for template in templates:
    template_id = template.get('id')
    print(template_id)
    DOs_template = template.findall('./{*}DO')
    DOs.append(DOs_template)

# Compare Logical Nodes lnType with the templates and add DOs
print('-------ADD DOs-------')

for LN in LN_total:
    for template in range (len(templates)):
        if LN.attrib['lnType'] == templates[template].attrib['id'] and LN.attrib['lnClass'] == templates[template].attrib['lnClass']:
            for DO in DOs[template]: 
                LN.append(DO)
            break
        else:
            continue

# Compare DOs type with the templates and add SDOs
for LN in LN_total:
    DOs = LN.findall('./{*}DO')
    for DO in DOs:
        for DO_type in templates_DO:
            if DO.get('type') == DO_type.get('id'):
                SDOs = DO_type.findall('./{*}SDO')
                if SDOs is not None:
                    for SDO in SDOs:
                        DO.append(SDO)

print('-------replacing DO template type by standard type--------')

for LN in LN_total:
    LN_DOs = LN.findall('./{*}DO')
    for DO in LN_DOs:
        for DO_type in templates_DO:
            if DO.get('type') == DO_type.get('id'): 
                DO.set('type', DO_type.get('cdc'))

print('-------replacing SDO template type by standard type--------')

for LN in LN_total:
    LN_DOs = LN.findall('./{*}DO')
    for DO in LN_DOs:
        SDOs = DO.findall('./{*}SDO')
        if SDOs is not None:
            for SDO in SDOs: 
                for DO_type in templates_DO:
                    if SDO.get('type') == DO_type.get('id'): 
                        SDO.set('type', DO_type.get('cdc'))

print('-------LN with standard DOs and SDOs--------')

for LN in LN_total:
    LN_DOs = LN.findall('./{*}DO')
    for DO in LN_DOs:
        SDOs = DO.findall('./{*}SDO')
        if SDOs:
            for SDO in SDOs:
                print(LN.get('prefix'), LN.get('lnType'), DO.get('name'), SDO.get('name'), SDO.get('type'), '<<----THIS ONE WITH SDO')
        else:
            print(LN.get('prefix'), LN.get('lnType'), DO.get('name'), DO.get('type'))


print('-------Find DOI objects--------')

for LN in LN_total:
    LN_DOs = LN.findall('./{*}DOI')
    for DO in LN_DOs:
        print(LN.tag, LN.get('prefix'), LN.get('lnType'), DO.tag, DO.get('name'))
      
print('-------Writing variable list--------')

#Opening file
f = open("variables_extract.csv", "w", encoding="utf-8")
f.write('NAME' + ',' + 'TYPE' + ',' + 'DESCRIPTION' + '\n')

desc = ''

for IED in IEDs:
    LDs = IED.findall('.//{*}LDevice')
    for LD in LDs:
        LNs = LD.findall('./{*}LN')
        LNOs = LD.findall('./{*}LN0')
        for LN in LN_total:
            LN_DOs = LN.findall('./{*}DO')
            LN_DOIs = LN.findall('./{*}DOI')
            if (LN in LNs) or (LN in LNOs):
                for DO in LN_DOs:
                    SDOs = DO.findall('./{*}SDO')
                    for DOI in LN_DOIs:
                        if DO.get('name') == DOI.get('name'):
                            desc = DOI.get('desc')
                    if SDOs:
                        for SDO in SDOs:          
                            variables_DO.append([IED.get('name') + LD.get('inst') + '/' + verify_if_none(LN.get('prefix'))
                                                 + LN.get('lnClass') + LN.get('inst') + '.' + DO.get('name') + '.' + SDO.get('name'), SDO.get('type'), verify_if_none(desc)])
                            print(IED.get('name') + LD.get('inst') + '/' + verify_if_none(LN.get('prefix'))
                                  + LN.get('lnClass') + LN.get('inst') + '.' + DO.get('name') + '.' + SDO.get('name') + ',' + SDO.get('type') + ',' + verify_if_none(desc))
                    else:
                        variables_DO.append([IED.get('name') + LD.get('inst') + '/' + verify_if_none(LN.get('prefix'))
                                             + LN.get('lnClass') + LN.get('inst') + '.' + DO.get('name'), DO.get('type'), verify_if_none(desc)])
                        print(IED.get('name') + LD.get('inst') + '/' + verify_if_none(LN.get('prefix'))
                              + LN.get('lnClass') + LN.get('inst') + '.' + DO.get('name') + ',' + DO.get('type') + ',' + verify_if_none(desc))
                       
print('--------REMOVE DUPLICATES-------')

variables_DO_clean = []
for line in variables_DO:
    if line not in variables_DO_clean:
        variables_DO_clean.append(line)

for line in variables_DO_clean:
    f.write(line[0] + ',' + line[1] + ',' + line[2] + '\n')

f.close()

print(variables_DO_clean)

Variables_report = [['NAME', 'TYPE', 'DESCRIPTION']]

# Find Reports
print('-------REPORTS NAMES AND COUNT--------')

for IED in IEDs:
    REPORTS = IED.findall('.//{*}ReportControl')
    for report in REPORTS:
        report_desc = report.get('desc')
        report_name = report.get('name')
        print(report_name + '  ' + verify_if_none(report_desc))

REPORT_count = len(REPORTS)
print('Report count:' + str(REPORT_count))

# Find Datasets
print('-------DATASET NAMES AND COUNT--------')

for IED in IEDs:
    DATASETS = IED.findall('.//{*}DataSet')
    for dataset in DATASETS:
        dataset_name = dataset.get('name')
        dataset_desc = dataset.get('desc')
        print(dataset_name + '  ' + verify_if_none(dataset_desc))

DATASET_count = len(DATASETS)
print('Dataset count:' + str(DATASET_count))

# Find FCDAs
print('------FCDAs---------')
#Opening file
f = open("variables_report.csv", "w", encoding="utf-8")

for IED in IEDs:
    REPORTS = IED.findall('.//{*}ReportControl')
    for report in REPORTS:
        DATASETS = IED.findall('.//{*}DataSet')
        for dataset in DATASETS:
            if report.get('datSet') == dataset.get('name'):        
                FCDAs = dataset.findall('./{*}FCDA')
                for  fcda in FCDAs:
                    Variables_report.append([IED.get('name') + fcda.get('ldInst') + '/' + fcda.get('prefix')
                                             + fcda.get('lnClass') + fcda.get('lnInst') + '.' + fcda.get('doName'),'',''])
                    print(verify_if_none(IED.get('name')) + verify_if_none(fcda.get('ldInst')) + '/' + verify_if_none(fcda.get('prefix'))
                          + verify_if_none(fcda.get('lnClass')) + verify_if_none(fcda.get('lnInst')) + '.' + verify_if_none(fcda.get('doName')) + ',' + ',')

f.write(Variables_report[0][0] + ',' + Variables_report[0][1] + ',' + Variables_report[0][2] + '\n')
for R in range(1, len(Variables_report)):       
    for D in range(len(variables_DO_clean)):
        if  Variables_report[R][0] == variables_DO_clean[D][0]:
            Variables_report[R][1] = variables_DO_clean[D][1]
            Variables_report[R][2] = verify_if_none(variables_DO_clean[D][2])
    f.write(Variables_report[R][0] + ',' + Variables_report[R][1] + ',' + Variables_report[R][2] + '\n')
    print(Variables_report[R][0] + ',' + Variables_report[R][1] + ',' + Variables_report[R][2])
    
f.close()

