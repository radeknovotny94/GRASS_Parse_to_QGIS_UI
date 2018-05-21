from __future__ import print_function
import xml.etree.ElementTree


def print_name_desc(modul):
    if child.tag == 'flag':
        print('-' + modul.attrib['name'].strip() + '|', end='')
    elif child.tag == 'parameter':
        print(modul.attrib['name'].strip() + '|', end='')
    else:
        pass

    if modul.find("label") is not None:
        print(modul.find("label").text.strip() + '|', end='')
    elif modul.find("description") is not None:
        print(modul.find("description").text.strip() + '|', end='')
    else:
        pass


def check_default(parameter):
    for par in parameter:
        if par.tag == 'default':
            return True


def print_default(parameter):
    if check_default(parameter):
        for par in parameter:
            if par.tag == 'default':
                print(par.text.strip() + '|', end='')
    else:
        print('None|', end='')


def print_optional(parameter):
    if parameter.attrib['required'] == 'yes':
        print('False')
    else:
        print('True')


tree = xml.etree.ElementTree.parse("v_surf_rst.xml")
root = tree.getroot()

name = root.attrib['name']
print(name)

print(tree.find("description").text.strip())

if name[:5] == 'nviz.':  # ????
    print('Visualization(NVIZ)')  # ????
elif name[:2] == 'r.':
    print('Raster (r.*)')
elif name[:2] == 'i.':
    print('Imagery (i.*)')
elif name[:2] == 'v.':
    print('Vector (v.*)')
elif name[:2] == 'm.':
    print('Miscellaneous (m.*)')
else:
    print('Not in plugin')

for child in root:
    if child.tag == 'parameter':
        if child.attrib['multiple'] == 'yes':
            print('QgsProcessingParameterMultipleLayers|', end='')
            print_name_desc(child)
            for k in child:
                if k.tag == 'gisprompt':
                    if k.attrib['prompt'] == 'raster':
                        print('TypeRaster|', end='')
                    if k.attrib['prompt'] == 'vector':
                        print('TypeVector|', end='')
                print_default(child)
                print_optional(child)

        elif child.attrib['multiple'] == 'no':
            for k in child:
                if k.tag == 'gisprompt':
                    if k.attrib['age'] == 'old':
                        if k.attrib['prompt'] == 'raster':
                            print('QgsProcessingParameterRasterLayer|', end='')
                        elif k.attrib['prompt'] == 'vector':
                            print('QgsProcessingParameterVectorLayer|', end='')
                        elif k.attrib['prompt'] == 'dbcolumn':
                            print('QgsProcessingParameterField|', end='')
                        else:
                            print('Not recognized >>> ', end='')
                        print_name_desc(child)
                    elif k.attrib['age'] == 'new':
                        if k.attrib['prompt'] == 'raster':
                            print('QgsProcessingParameterRasterDestination|', end='')
                            print_name_desc(child)
                        elif k.attrib['prompt'] == 'vector':
                            print('QgsProcessingParameterVectorDestination|', end='')
                            print_name_desc(child)
                            print('TypeVector|', end='')
                        else:
                            print('Not recognized >>> ', end='')
                            print_name_desc(child)
                    print_default(child)
                    print_optional(child)

        elif child.attrib['type'] == 'string':
            promt = child.find('gisprompt')
            if promt is None:
                print('QgsProcessingParameterString|', end='')
                print_name_desc(child)
                print_default(child)
                print('True|', end='')
                print_optional(child)
            else:
                print('Not recognized >>> ', end='')
                print_name_desc(child)

        elif child.attrib['type'] == 'integer':
            print('QgsProcessingParameterNumber|', end='')
            print_name_desc(child)
            print('QgsProcessingParameterNumber.Integer|', end='')
            print_default(child)
            print_optional(child)

        elif child.attrib['type'] == 'float':
            print('QgsProcessingParameterNumber|', end='')
            print_name_desc(child)
            print('QgsProcessingParameterNumber.Double|', end='')
            print_default(child)
            print_optional(child)
        else:
            print('Not recognized >>> ', end='')
            print_name_desc(child)

    elif child.tag == 'flag':
        print('QgsProcessingParameterBoolean|', end='')
        print_name_desc(child)
        print_default(child)
        print('True')
