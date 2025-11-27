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
    exit()

# Opening & parsing SCL file
try:
    tree = etree.parse(file_name)
except:
    print('File not found, non existent,  wrong file name or path')
    exit()

root = tree.getroot()

# Main variables
variables_DO = []

# Find Logical Nodes data templates
templates = root.findall('.//{*}LNodeType')
templates_DO = root.findall('.//{*}DOType')
templates_DA = root.findall('.//{*}DAType')

# Insert SDOs in DOs
for template in templates:
    DOs = template.findall('.//{*}DO')
    for DO in DOs:
        for DO_type in templates_DO:
            if DO.attrib['type'] == DO_type.attrib['id']:
                SDOs = DO_type.findall('./{*}SDO')
                if SDOs:
                    for SDO in SDOs:
                        DO.append(SDO)

# Insert DAs in SDOs

for template in templates:
    SDOs = template.findall('.//{*}SDO')
    for SDO in SDOs:
        for DO_type in templates_DO:
            if SDO.attrib['type'] == DO_type.attrib['id']:
                DAs = DO_type.findall('./{*}DA')
                if DAs:
                    for DA in DAs:
                        SDO.append(DA)

# Insert DAs in DOs

for template in templates:
    DOs = template.findall('.//{*}DO')
    for DO in DOs:
        for DO_type in templates_DO:
            if DO.attrib['type'] == DO_type.attrib['id']:
                DAs = DO_type.findall('./{*}DA')
                if DAs:
                    for DA in DAs:
                        DO.append(DA)

# Insert BDAs in DAs

for template in templates:
    DAs = template.findall('.//{*}DA')
    for DA in DAs:
        for DA_type in templates_DA:
            if DA.get('type') == DA_type.get('id'): #DA.attrib['type'] == DA_type.attrib['id']:
                BDAs = DA_type.findall('./{*}BDA')
                if BDAs:
                    for BDA in BDAs:
                        DA.append(BDA)

print('-------Writing variable list--------')

#Opening file
f = open("variables_extract_DA.csv", "w", encoding="utf-8")
f.write('NAME' + ',' + 'TYPE' + ',' + 'FC' + ',' + 'DESCRIPTION' + '\n')

desc = ''
IEDs = root.findall('.//{*}IED')

for IED in IEDs:
    LDs = IED.findall('.//{*}LDevice')
    for LD in LDs:
        LNs = LD.findall('./{*}LN')
        LNOs = LD.findall('./{*}LN0')
        for LN in LNs:
            LN_DOIs = LN.findall('./{*}DOI')
            for template in templates:
                if LN.attrib['lnType'] == template.attrib['id'] and LN.attrib['lnClass'] == template.attrib['lnClass']:
                    LN_DOs = template.findall('./{*}DO')
                    for DO in LN_DOs:
                        SDOs = DO.findall('./{*}SDO')
                        for DOI in LN_DOIs:
                            if DO.get('name') == DOI.get('name'):
                                desc = DOI.get('desc')
                        if SDOs:
                            for SDO in SDOs:
                                DAs = SDO.findall('./{*}DA')
                                if DAs:
                                    for DA in DAs:
                                        variables_DO.append([IED.get('name') + LD.get('inst') + '/' + verify_if_none(LN.get('prefix'))
                                            + LN.get('lnClass') + LN.get('inst') + '.' + DO.get('name') + '.' + SDO.get('name') + '.' + DA.get('name'), DA.get('bType'), DA.get('fc'), verify_if_none(desc)])
                                        print(IED.get('name') + LD.get('inst') + '/' + verify_if_none(LN.get('prefix'))
                                              + LN.get('lnClass') + LN.get('inst') + '.' + DO.get('name') + '.' + SDO.get('name') + '.' + DA.get('name') + ',' + DA.get('bType') + ',' + DA.get('fc') + ',' + verify_if_none(desc))
                                else:
                                    if DAs:
                                        variables_DO.append([IED.get('name') + LD.get('inst') + '/' + verify_if_none(LN.get('prefix'))
                                            + LN.get('lnClass') + LN.get('inst') + '.' + DO.get('name') + '.' + SDO.get('name'), SDO.get('type'), '', verify_if_none(desc)])
                                        print(IED.get('name') + LD.get('inst') + '/' + verify_if_none(LN.get('prefix'))
                                            + LN.get('lnClass') + LN.get('inst') + '.' + DO.get('name') + '.' + SDO.get('name') + ',' + SDO.get('type') + ',' + '' + ',' + verify_if_none(desc))
                        else:
                            DAs = DO.findall('./{*}DA')
                            for DA in DAs:
                                BDAs = DA.findall('./{*}BDA')
                                if BDAs:
                                    for BDA in BDAs:
                                        variables_DO.append([IED.get('name') + LD.get('inst') + '/' + verify_if_none(LN.get('prefix'))
                                                + LN.get('lnClass') + LN.get('inst') + '.' + DO.get('name') + '.' + DA.get('name') + '.' + BDA.get('name'), BDA.get('bType'), DA.get('fc'), verify_if_none(desc)])
                                        print([IED.get('name') + LD.get('inst') + '/' + verify_if_none(LN.get('prefix'))
                                                + LN.get('lnClass') + LN.get('inst') + '.' + DO.get('name') + '.' + DA.get('name') + '.' + BDA.get('name') + ',' + BDA.get('bType') + ',' + DA.get('fc') + ',' + verify_if_none(desc)])
                                else:
                                    variables_DO.append([IED.get('name') + LD.get('inst') + '/' + verify_if_none(LN.get('prefix'))
                                        + LN.get('lnClass') + LN.get('inst') + '.' + DO.get('name') + '.' + DA.get('name') , DA.get('bType'), DA.get('fc'), verify_if_none(desc)])
                                    print([IED.get('name') + LD.get('inst') + '/' + verify_if_none(LN.get('prefix'))
                                        + LN.get('lnClass') + LN.get('inst') + '.' + DO.get('name') + '.' + DA.get('name') + ',' + DA.get('bType') + ',' + DA.get('fc') + ',' + verify_if_none(desc)])
                       
        for LN in LNOs:
            LN_DOIs = LN.findall('./{*}DOI')
            for template in templates:
                if LN.attrib['lnType'] == template.attrib['id'] and LN.attrib['lnClass'] == template.attrib['lnClass']:
                    LN_DOs = template.findall('./{*}DO')
                    for DO in LN_DOs:
                        SDOs = DO.findall('./{*}SDO')
                        for DOI in LN_DOIs:
                            if DO.get('name') == DOI.get('name'):
                                desc = DOI.get('desc')
                        if SDOs:
                            for SDO in SDOs:
                                DAs = SDO.findall('./{*}DA')
                                if DAs:
                                    for DA in DAs:
                                        variables_DO.append([IED.get('name') + LD.get('inst') + '/' + verify_if_none(LN.get('prefix'))
                                            + LN.get('lnClass') + LN.get('inst') + '.' + DO.get('name') + '.' + SDO.get('name') + '.' + DA.get('name'), DA.get('bType'), DA.get('fc'), verify_if_none(desc)])
                                        print(IED.get('name') + LD.get('inst') + '/' + verify_if_none(LN.get('prefix'))
                                              + LN.get('lnClass') + LN.get('inst') + '.' + DO.get('name') + '.' + SDO.get('name') + '.' + DA.get('name') + ',' + DA.get('bType') + ',' + DA.get('fc') + ',' + verify_if_none(desc))
                                else:
                                    if DAs:
                                        variables_DO.append([IED.get('name') + LD.get('inst') + '/' + verify_if_none(LN.get('prefix'))
                                            + LN.get('lnClass') + LN.get('inst') + '.' + DO.get('name') + '.' + SDO.get('name'), SDO.get('type'), '', verify_if_none(desc)])
                                        print(IED.get('name') + LD.get('inst') + '/' + verify_if_none(LN.get('prefix'))
                                            + LN.get('lnClass') + LN.get('inst') + '.' + DO.get('name') + '.' + SDO.get('name') + ',' + SDO.get('type') + ',' + '' + ',' + verify_if_none(desc))
                        else:
                            DAs = DO.findall('./{*}DA')
                            for DA in DAs:
                                BDAs = DA.findall('./{*}BDA')
                                if BDAs:
                                    for BDA in BDAs:
                                        variables_DO.append([IED.get('name') + LD.get('inst') + '/' + verify_if_none(LN.get('prefix'))
                                                + LN.get('lnClass') + LN.get('inst') + '.' + DO.get('name') + '.' + DA.get('name') + '.' + BDA.get('name'), BDA.get('bType'), DA.get('fc'), verify_if_none(desc)])
                                        print([IED.get('name') + LD.get('inst') + '/' + verify_if_none(LN.get('prefix'))
                                                + LN.get('lnClass') + LN.get('inst') + '.' + DO.get('name') + '.' + DA.get('name') + '.' + BDA.get('name') + ',' + BDA.get('bType') + ',' + DA.get('fc') + ',' + verify_if_none(desc)])
                                else:
                                    variables_DO.append([IED.get('name') + LD.get('inst') + '/' + verify_if_none(LN.get('prefix'))
                                        + LN.get('lnClass') + LN.get('inst') + '.' + DO.get('name') + '.' + DA.get('name') , DA.get('bType'), DA.get('fc'), verify_if_none(desc)])
                                    print([IED.get('name') + LD.get('inst') + '/' + verify_if_none(LN.get('prefix'))
                                        + LN.get('lnClass') + LN.get('inst') + '.' + DO.get('name') + '.' + DA.get('name') + ',' + DA.get('bType') + ',' + DA.get('fc') + ',' + verify_if_none(desc)])

variables_DA = []
for line in variables_DO:
    if line not in variables_DA:
        variables_DA.append(line)

for column in variables_DA:
    f.write(column[0] + ',' + column[1] + ',' + column[2] + ',' + column[3] +'\n')

f.close()
