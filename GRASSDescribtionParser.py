import os
import xml.etree.ElementTree

module_names = open(os.path.join("C:\Users","radek","Desktop","grass_modules_names.txt"), "r").read()
file = open(os.path.join("C:\Users","radek","Desktop","r_covar.xml"), "r")
# print file.read()
list_modules = module_names.split()
print list_modules

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
        if child.attrib['type'] == 'string' and \
           child.attrib['required'] == 'yes' and \
           child.attrib['multiple'] == 'yes':
            print 'QgsProcessingParameterMultipleLayers|'
        print child.attrib['name'] + '|'
        print child.find("description").text.strip()


# print root.tag, root.attrib

# for atype in root.findall('name'):
#     print atype
