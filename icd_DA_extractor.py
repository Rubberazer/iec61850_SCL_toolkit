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

print('-------Writing variable list--------')

#Opening file
f = open("variables_extract.csv", "w", encoding="utf-8")
f.write('NAME' + ',' + 'TYPE' + ',' + 'FC' + ',' + 'DESCRIPTION' + '\n')

desc = ''
LN_DOs = []
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
                    LN_DOs = template.findall('.//{*}DO')
                    for DO in LN_DOs:
                        for DOI in LN_DOIs:
                            if DO.get('name') == DOI.get('name'):
                                desc = DOI.get('desc')
                        for DO_type in templates_DO:
                            if DO.get('type') == DO_type.get('id'):
                                SDOs = DO_type.findall('./{*}SDO')
                                DAs = DO_type.findall('./{*}DA')
                                for SDO in SDOs:
                                    for SDO_type in templates_DO:
                                        if SDO.get('type') == SDO_type.get('id'):
                                            SDO.set('type', SDO_type.get('cdc'))
                                            variables_DO.append([IED.get('name') + LD.get('inst') + '/' + verify_if_none(LN.get('prefix'))
                                                 + LN.get('lnClass') + LN.get('inst') + '.' + DO.get('name') + '.' + SDO.get('name'), SDO.get('type'), '', verify_if_none(desc)])
                                            print(IED.get('name') + LD.get('inst') + '/' + verify_if_none(LN.get('prefix'))
                                                + LN.get('lnClass') + LN.get('inst') + '.' + DO.get('name') + '.' + SDO.get('name') + ',' + SDO.get('type') + ',' + '' + ',' + verify_if_none(desc))
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
                    LN_DOs = template.findall('.//{*}DO')
                    for DO in LN_DOs:
                        for DOI in LN_DOIs:
                            if DO.get('name') == DOI.get('name'):
                                desc = DOI.get('desc')
                        for DO_type in templates_DO:
                            if DO.get('type') == DO_type.get('id'):
                                SDOs = DO_type.findall('./{*}SDO')
                                DAs = DO_type.findall('./{*}DA')
                                for SDO in SDOs:
                                    for SDO_type in templates_DO:
                                        if SDO.get('type') == SDO_type.get('id'):
                                            SDO.set('type', SDO_type.get('cdc'))
                                            variables_DO.append([IED.get('name') + LD.get('inst') + '/' + verify_if_none(LN.get('prefix'))
                                                 + LN.get('lnClass') + LN.get('inst') + '.' + DO.get('name') + '.' + SDO.get('name'), SDO.get('type'), '', verify_if_none(desc)])
                                            print(IED.get('name') + LD.get('inst') + '/' + verify_if_none(LN.get('prefix'))
                                                + LN.get('lnClass') + LN.get('inst') + '.' + DO.get('name') + '.' + SDO.get('name') + ',' + SDO.get('type') + ',' + '' + ',' + verify_if_none(desc))
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

for column in variables_DO:
    f.write(column[0] + ',' + column[1] + ',' + column[2] + ',' + column[3] +'\n')

f.close()
