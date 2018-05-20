import os
import xml.etree.ElementTree

def print_name_desc(modul):
    print(modul.attrib['name'].strip() + '|' + \
          modul.find("description").text.strip() + '|'),

def print_default(parameter):
    if parameter.tag == 'default':
        print(parameter.find("default").text.strip() + '|'),
    else:
        print('None|'),

def print_optional(parameter):
    if parameter.attrib['required'] == 'yes':
        print('False')
    else:
        print('True')

file = open(os.path.join("C:\Users","radek","Desktop","r_covar.xml"), "r")
# print file.read()

tree = xml.etree.ElementTree.parse(os.path.join("C:\Users","radek","Desktop","r_covar.xml"))
root = tree.getroot()

name = root.attrib['name']
print name

print tree.find("description").text.strip()

if name[:5] == 'nviz.': # ????
    print 'Visualization(NVIZ)' # ????
elif name[:2] == 'r.':
    print 'Raster (r.*)'
elif name[:2] == 'i.':
    print 'Imagery (i.*)'
elif name[:2] == 'v.':
    print 'Vector (v.*)'
elif name[:2] == 'm.':
    print 'Miscellaneous (m.*)'
else:
    print 'Not in plugin'

for child in root:
    if child.tag == 'parameter':
        if child.attrib['multiple'] == 'yes':
            print('QgsProcessingParameterMultipleLayers|'),
            print_name_desc(child)
            for k in child:
                if k.tag == 'gisprompt':
                    if k.attrib['prompt'] == 'raster':
                        print('TypeRaster|'),
                        print_default(k)
                        print_optional(child)
                    if k.attrib['prompt'] == 'vector':
                        print('TypeVector|'),
                        print_default(k)
                        print_optional(child)

        if child.attrib['multiple'] == 'no':
            for k in child:
                if k.tag == 'gisprompt':
                    if k.attrib['prompt'] == 'raster':
                        print('QgsProcessingParameterRasterLayer|'),
                    if k.attrib['prompt'] == 'vector':
                        print('QgsProcessingParameterVectorLayer|'),
                print_name_desc(child)
                print_default(k)
                print_optional(child)

        if child.attrib['type'] == 'string':
            for k in child:
                if not k.tag.find('gisprompt'):
                    print(k.tag)
                    print('QgsProcessingParameterString|'),
                    print_name_desc(child)
                    print_default(k)
                    print('True|')



# for child in root:
#     for k in child:
#         if k.tag == 'gisprompt':
#             print(k.tag)
#             if k.attrib['prompt'] == 'raster':
#                 print('raster')
# print root.tag, root.attrib

# for atype in root.findall('name'):
#     print atype
