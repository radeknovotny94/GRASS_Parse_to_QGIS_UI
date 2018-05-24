from __future__ import print_function
import xml.etree.ElementTree


def print_name_desc(modul, output):
    if child.tag == 'flag':
        print('-' + modul.attrib['name'].strip() + '|', end='', file=output)
    elif child.tag == 'parameter':
        print(modul.attrib['name'].strip() + '|', end='', file=output)
    else:
        pass

    if modul.find("label") is not None:
        print(modul.find("label").text.strip() + '|', end='', file=output)
    elif modul.find("description") is not None:
        print(modul.find("description").text.strip() + '|', end='', file=output)
    else:
        pass


def check_default(parameter):
    for par in parameter:
        if par.tag == 'default':
            return True


def print_default(parameter, output):
    if check_default(parameter):
        for par in parameter:
            if par.tag == 'default':
                print(par.text.strip() + '|', end='', file=output)
    else:
        print('None|', end='', file=output)


def print_optional(parameter, output):
    if parameter.attrib['required'] == 'yes':
        print('False', file=output)
    else:
        print('True', file=output)


def print_name_def(parameter, output):
    print_name_desc(parameter, output)
    print_default(parameter, output)


def print_def_opt(parameter, output):
    print_default(parameter, output)
    print_optional(parameter, output)


def print_name_def_opt(parameter, output):
    print_name_desc(parameter, output)
    print_default(parameter, output)
    print_optional(parameter, output)


desc_file = open('v_surf_rst.txt', 'w+')
tree = xml.etree.ElementTree.parse("v_surf_rst.xml")
root = tree.getroot()

name = root.attrib['name']
print(name, file=desc_file)

print(tree.find('description').text.strip(), file=desc_file)

if name[:5] == 'nviz.':  # ????
    print('Visualization(NVIZ)', file=desc_file)  # ????
elif name[:2] == 'r.':
    print('Raster (r.*)', file=desc_file)
elif name[:2] == 'i.':
    print('Imagery (i.*)', file=desc_file)
elif name[:2] == 'v.':
    print('Vector (v.*)', file=desc_file)
elif name[:2] == 'm.':
    print('Miscellaneous (m.*)', file=desc_file)
else:
    print('Not in plugin')

for child in root:
    if child.tag == 'parameter':
        if child.attrib['multiple'] == 'yes':
            print('QgsProcessingParameterMultipleLayers|', end='', file=desc_file)
            print_name_desc(child, desc_file)
            for k in child:
                if k.tag == 'gisprompt':
                    if k.attrib['prompt'] == 'raster':
                        print('TypeRaster|', end='', file=desc_file)
                    if k.attrib['prompt'] == 'vector':
                        print('TypeVector|', end='', file=desc_file)
                print_def_opt(child, desc_file)

        elif child.attrib['multiple'] == 'no':
            for k in child:
                if k.tag == 'gisprompt':
                    if k.attrib['age'] == 'old':
                        if k.attrib['prompt'] == 'raster':
                            print('QgsProcessingParameterRasterLayer|', end='', file=desc_file)
                            print_name_def_opt(child, desc_file)
                        elif k.attrib['prompt'] == 'vector':
                            print('QgsProcessingParameterVectorLayer|', end='', file=desc_file)
                            print_name_def_opt(child, desc_file)
                        elif k.attrib['prompt'] == 'dbcolumn':
                            print('QgsProcessingParameterField|', end='', file=desc_file)
                            print_name_def_opt(child, desc_file)
                        else:
                            print('Not recognized >>> ', end='')
                            print(child.attrib['name'].strip())
                    elif k.attrib['age'] == 'new':
                        if k.attrib['prompt'] == 'raster':
                            print('QgsProcessingParameterRasterDestination|', end='', file=desc_file)
                            print_name_def_opt(child, desc_file)
                        elif k.attrib['prompt'] == 'vector':
                            print('QgsProcessingParameterVectorDestination|', end='', file=desc_file)
                            print_name_desc(child, desc_file)
                            print('TypeVector|', end='', file=desc_file)
                            print_def_opt(child, desc_file)
                        else:
                            print('Not recognized >>> ', end='')
                            print(child.attrib['name'].strip())

        elif child.attrib['type'] == 'string':
            promt = child.find('gisprompt')
            if promt is None:
                print('QgsProcessingParameterString|', end='', file=desc_file)
                print_name_def(child, desc_file)
                print('True|', end='', file=desc_file)
                print_optional(child, desc_file)
            else:
                print('Not recognized >>> ', end='')
                print(child.attrib['name'].strip())

        elif child.attrib['type'] == 'integer':
            print('QgsProcessingParameterNumber|', end='', file=desc_file)
            print_name_desc(child, desc_file)
            print('QgsProcessingParameterNumber.Integer|', end='', file=desc_file)
            print_def_opt(child, desc_file)

        elif child.attrib['type'] == 'float':
            print('QgsProcessingParameterNumber|', end='', file=desc_file)
            print_name_desc(child, desc_file)
            print('QgsProcessingParameterNumber.Double|', end='', file=desc_file)
            print_def_opt(child, desc_file)
        else:
            print('Not recognized >>> ', end='')
            print(child.attrib['name'].strip())

    elif child.tag == 'flag':
        print('QgsProcessingParameterBoolean|', end='', file=desc_file)
        print_name_def(child, desc_file)
        print('True', file=desc_file)
