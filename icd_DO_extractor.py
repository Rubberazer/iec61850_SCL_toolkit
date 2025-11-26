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

# Change type SDOs
for DO_type in templates_DO:
    SDOs = DO_type.findall('./{*}SDO')
    for SDO in SDOs: 
        for type in templates_DO:
            if SDO.get('type') == type.get('id'): 
                SDO.set('type', type.get('cdc'))

# Insert SDOs in DOs
for template in templates:
    DOs = template.findall('.//{*}DO')
    for DO in DOs:
        for DO_type in templates_DO:
            if DO.get('type') == DO_type.get('id'):
                DO.set('type', DO_type.get('cdc'))
                SDOs = DO_type.findall('./{*}SDO')
                for SDO in SDOs:
                    DO.append(SDO)

print('-------Writing variable list--------')

#Opening file
f = open("variables_extract.csv", "w", encoding="utf-8")
f.write('NAME' + ',' + 'TYPE' + ',' + 'DESCRIPTION' + '\n')

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
                    LN_DOs = template.findall('./{*}DO')
                    for DO in LN_DOs:
                        SDOs = DO.findall('./{*}SDO')
                        for DOI in LN_DOIs:
                            if DO.get('name') == DOI.get('name'):
                                desc = DOI.get('desc')
                                break
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
                                break
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
                            
for column in variables_DO:
    f.write(column[0] + ',' + column[1] + ',' + column[2] +'\n')

f.close()
