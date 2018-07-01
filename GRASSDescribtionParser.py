from __future__ import print_function
import xml.etree.ElementTree

import os
import subprocess
import tempfile
import binascii

import sys

reload(sys)
sys.setdefaultencoding('utf8')

# os.environ['LC_ALL'] = 'C'

def findGRASS():
    """Find GRASS.

    Find location of GRASS.

    :todo: Avoid bat file calling.
    """
    ########### SOFTWARE
    if sys.platform == 'win32':
        # qgis_prefix_path = os.environ['QGIS_PREFIX_PATH'] # not working in OSGeo installation
        # bin_path = os.path.join(os.path.split(
        #     os.path.split(qgis_prefix_path)[0])[0],
        #     'bin'
        # )
        # grass7bin = None
        # for grass_version in ['74', '72', '70']:
        #     gpath = os.path.join(bin_path, 'grass{}.bat'.format(grass_version))
        #     if os.path.exists(gpath):
        #         grass7bin = gpath
        #         break
        grass7bin = r'C:\OSGeo4W\bin\grass74.bat'

        if grass7bin is None:
            raise ImportError("No grass74.bat, grass72.bat or grass70.bat found.")
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        si.wShowWindow = subprocess.SW_HIDE
    else:
        grass7bin = '/usr/bin/grass'
    startcmd = [grass7bin, '--config', 'path']

    try:
        p = subprocess.Popen(startcmd, shell=False,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
    except OSError as error:
        sys.exit("ERROR: Cannot find GRASS GIS start script"
                 " {cmd}: {error}".format(cmd=startcmd[0], error=error))
    if p.returncode != 0:
        sys.exit("ERROR: Issues running GRASS GIS start script"
                 " {cmd}: {error}"
                 .format(cmd=' '.join(startcmd), error=err))
    # p = subprocess.Popen(startcmd,
    #                      stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # out, err = p.communicate()
    #
    # if p.returncode != 0:
    #     raise ImportError("Reason: ({cmd}: {reason})".format(
    #         cmd=startcmd, reason=err)
    #     )

    str_out = out.decode("utf-8")
    gisbase = str_out.rstrip(os.linesep)

    # Set GISBASE environment variable
    os.environ['GISBASE'] = gisbase
    # set language to english
    os.environ['LC_ALL'] = 'C'
    # define GRASS-Python environment
    sys.path.append(os.path.join(gisbase, "etc", "python"))

    return grass7bin

try:
    grass7bin = findGRASS()
except (StandardError, ImportError) as e:
    raise ImportError('Unable to find GRASS installation. {}'.format(e))

temp_dir = None
import grass.script as gscript
from grass.script import setup as gsetup
from grass.exceptions import ScriptError

# def set_location():
#     """Set GRASS gisbase, location and mapset.
#     """

gisdb = os.path.join(tempfile.gettempdir(), 'grassdata')
if not os.path.isdir(gisdb):
    os.mkdir(gisdb)

# location/mapset: use random names for batch jobs
string_length = 16
location = binascii.hexlify(os.urandom(string_length))
mapset   = 'PERMANENT'

# GRASS session must be initialized first
gsetup.init(os.environ['GISBASE'], gisdb, location, mapset)
print(gisdb + location + mapset) # for debug

# Create temporal location
try:
    gscript.create_location(gisdb, location, overwrite=True)
except ScriptError as e:
    raise StandardError('{}'.format(e))




# def main():
#     set_location()
#     find_moduls()
# info = gtask.command_info('v.surf.rst')


#
#
# if __name__ == "__main__":
#     main()

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


def optional(parameter, output):
    if parameter.attrib['required'] == 'yes':
        print('', end='', file=output)
    else:
        print('*', end='', file=output)


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


def check_tag(tag, branch):
    elemList = []

    for elem in branch:
        elemList.append(elem.tag)

    # now I remove duplicities - by convertion to set and back to list
    elemList = list(set(elemList))
    if tag in elemList:
        return True
    else:
        return False

from grass.script import core as gcore


# def find_moduls():
#     """Find GRASS moduls.
#     """
cmds = list(gcore.get_commands()[0])
cmds.sort()
# file_names = [cmd.replace('.', '_') for cmd in cmds]

from grass.script import task as gtask

# try to call method get_interface_description, see Issue #7
if sys.platform == 'win32':
    gtask.get_interface_description('v.db.update')

for cmd in cmds:
    try:
        # def parser():

        root = xml.etree.ElementTree.fromstring(gtask.get_interface_description('{}'.format(cmd)))
        # print(tree)
        #
        # root = tree.getroot()

        name = root.attrib['name']

        if name[:2] == 'd.':
            continue
        elif name[:3] == 'db.':
            continue
        elif name[:3] == 'r3.':
            continue
        elif name[:2] == 't.':
            continue
        elif name[:3] == 'ps.':
            continue
        elif name[:2] == 'g.':
            continue
        elif name[:5] == 'test.':
            continue
        elif cmd == 'g.parser':
            continue

        desc_file = open('desc/{}.txt'.format(cmd), 'w+')
        xml_file = open('xml/{}.txt'.format(cmd), 'w+')
        # print(gtask.get_interface_description('v.surf.rst'), file=xml_file)
        print(gtask.get_interface_description('{}'.format(cmd)), file=xml_file)

        print(name, file=desc_file)
        print(name)

        for child in root:
            if child.tag == 'label':
                label = child.text.strip()
                label = label.replace('-', '')
                print(label, end=' ', file=desc_file)
            if child.tag == 'description':
                desc = child.text.strip()
                desc = desc.replace('-', '')
                print(desc, end=' ', file=desc_file)
        print('', file=desc_file)
        if name[:2] == 'r.':
            print('Raster (r.*)', file=desc_file)
        elif name[:2] == 'i.':
            print('Imagery (i.*)', file=desc_file)
        elif name[:2] == 'v.':
            print('Vector (v.*)', file=desc_file)
        elif name[:2] == 'm.':
            print('Miscellaneous (m.*)', file=desc_file)
        # elif name[:2] == 'd.':
        #     print('Display (d.*)', file=desc_file)
        # elif name[:3] == 'db.':
        #     print('Database (db.*)', file=desc_file)
        # elif name[:3] == 'r3.':
        #     print('Raster3D (r3.*)', file=desc_file)
        # elif name[:2] == 't.':
        #     print('Temporal (t.*)', file=desc_file)
        # elif name[:3] == 'ps.':
        #     print('Postscript (ps.*)', file=desc_file)
        # elif name[:2] == 'g.':
        #     print('General (g.*)', file=desc_file)
        else:
            print('Not in plugin - ' + name)

        for child in root:
            if child.tag == 'parameter':
                if check_tag('gisprompt', child):
                    for k in child:
                        if k.tag == 'gisprompt':
                            if 'prompt' in k.attrib:
                                if k.attrib['prompt'] == 'raster_3d':
                                    if child.attrib['required'] == 'yes':
                                        print('Need of 3D raster for module >>> ' + name)
                                        os.remove('desc/{}.txt'.format(cmd))
                                    else:
                                        pass
                if child.attrib['type'] == 'integer':
                    if check_default(child):
                        for k in child:
                            if k.tag == 'default':
                                if ',' not in k.text.strip():
                                    optional(child, desc_file)
                                    print('QgsProcessingParameterNumber|', end='', file=desc_file)
                                    print_name_desc(child, desc_file)
                                    print('QgsProcessingParameterNumber.Integer|', end='', file=desc_file)
                                    print_def_opt(child, desc_file)

                                else:
                                    optional(child, desc_file)
                                    print('QgsProcessingParameterRange|', end='', file=desc_file)
                                    print_name_desc(child, desc_file)
                                    print('QgsProcessingParameterNumber.Integer|', end='', file=desc_file)
                                    print_def_opt(child, desc_file)

                elif child.attrib['type'] == 'float':
                    optional(child, desc_file)
                    print('QgsProcessingParameterNumber|', end='', file=desc_file)
                    print_name_desc(child, desc_file)
                    print('QgsProcessingParameterNumber.Double|', end='', file=desc_file)
                    print_def_opt(child, desc_file)
                # else:
                #     print('Not recognized >>> ', end='')
                #     print(child.attrib['name'].strip())
                elif check_tag('values', child):
                    optional(child, desc_file)
                    print('QgsProcessingParameterEnum|', end='', file=desc_file)
                    print_name_desc(child, desc_file)
                    print('not selected', end='', file=desc_file)
                    for k in child:
                        if k.tag == 'values':
                            for value in k:
                                for name in value:
                                    if name.tag == 'name':
                                        print(';' + name.text.strip(), end='', file=desc_file)
                    if child.attrib['multiple'] == 'yes':
                        print('|True|', end='', file=desc_file)
                    else:
                        print('|False|', end='', file=desc_file)
                    print_def_opt(child, desc_file)
                elif child.attrib['multiple'] == 'yes':
                    if check_tag('gisprompt', child):
                        for k in child:
                            if k.tag == 'gisprompt':
                                # if k.tag == 'gisprompt':
                                if k.attrib['prompt'] == 'dbcolumn':
                                    optional(child, desc_file)
                                    print('QgsProcessingParameterField|', end='', file=desc_file)
                                    print_name_def_opt(child, desc_file)
                                else:
                                    optional(child, desc_file)
                                    print('QgsProcessingParameterMultipleLayers|', end='', file=desc_file)
                                    print_name_desc(child, desc_file)
                                    if k.attrib['prompt'] == 'raster':
                                        print('3|', end='', file=desc_file)
                                        print_def_opt(child, desc_file)
                                    elif k.attrib['prompt'] == 'vector':
                                        print('2|', end='', file=desc_file)
                                        print_def_opt(child, desc_file)
                                    else:
                                        print('33|', end='', file=desc_file)
                                        print_def_opt(child, desc_file)
                    else:
                        optional(child, desc_file)
                        print('QgsProcessingParameterString|', end='', file=desc_file)
                        print_name_def(child, desc_file)
                        print('True|', end='', file=desc_file)
                        print_optional(child, desc_file)

                        # else:
                        #     print('Input layers|TypeMapLayer|', end='', file=desc_file)
                        #     print_def_opt(child, desc_file)

                elif child.attrib['multiple'] == 'no':
                    if child.attrib['type'] == 'string':
                        if check_tag('gisprompt', child):
                            for k in child:
                                if k.tag == 'gisprompt':
                                    if k.attrib['age'] == 'old':
                                        if k.attrib['prompt'] == 'raster':
                                            optional(child, desc_file)
                                            print('QgsProcessingParameterRasterLayer|', end='', file=desc_file)
                                            print_name_def_opt(child, desc_file)
                                        elif k.attrib['prompt'] == 'vector':
                                            optional(child, desc_file)
                                            print('QgsProcessingParameterVectorLayer|', end='', file=desc_file)
                                            print_name_def_opt(child, desc_file)
                                        elif k.attrib['prompt'] == 'dbcolumn':
                                            optional(child, desc_file)
                                            print('QgsProcessingParameterField|', end='', file=desc_file)
                                            print_name_def_opt(child, desc_file)
                                        elif k.attrib['prompt'] == 'file' or k.attrib['prompt'] == 'sigfile' \
                                                or child.attrib['name'] == 'signature':
                                            optional(child, desc_file)
                                            print('QgsProcessingParameterFile|', end='', file=desc_file)
                                            print_name_desc(child, desc_file)
                                            print('QgsProcessingParameterFile.File|txt|', end='', file=desc_file)
                                            print_def_opt(child, desc_file)
                                        elif k.attrib['prompt'] == 'datasource':
                                            optional(child, desc_file)
                                            print('QgsProcessingParameterFolder|', end='', file=desc_file)
                                            print_name_desc(child, desc_file)
                                            print('QgsProcessingParameterFile.Folder|None|', end='', file=desc_file)
                                            print_def_opt(child, desc_file)
                                        elif k.attrib['prompt'] == 'group' and child.attrib['name'] != 'subgroup':
                                            if name == 'i.group':
                                                optional(child, desc_file)
                                                print('QgsProcessingParameterRasterDestination|group|Multiband raster', file=desc_file)
                                            else:
                                                optional(child, desc_file)
                                                print('QgsProcessingParameterMultipleLayers|input|', end='', file=desc_file)
                                                if name[:2] == 'r.':
                                                    print('Input rasters|3|', end='', file=desc_file)
                                                    print_def_opt(child, desc_file)
                                                elif name[:2] == 'v.':
                                                    print('Input vectors|2|', end='', file=desc_file)
                                                    print_def_opt(child, desc_file)
                                                else:
                                                    print('Input layers|3|', end='', file=desc_file)
                                                    print_def_opt(child, desc_file)
                                        elif k.attrib['prompt'] == 'separator' or k.attrib['prompt'] == 'color'   \
                                                or k.attrib['prompt'] == 'cats' or k.attrib['prompt'] == 'dbname' \
                                                or k.attrib['prompt'] == 'dbtable':
                                            optional(child, desc_file)
                                            print('QgsProcessingParameterString|', end='', file=desc_file)
                                            print_name_def(child, desc_file)
                                            print('False|', end='', file=desc_file)
                                            print_optional(child, desc_file)
                                        elif k.attrib['prompt'] == 'layer':
                                            pass
                                        elif k.attrib['prompt'] == 'subgroup' or child.attrib['name'] == 'subgroup':
                                            pass
                                        else:
                                            print('Not recognized >>> ', end='')
                                            print(child.attrib['name'].strip())
                                    elif k.attrib['age'] == 'new':
                                        if k.attrib['prompt'] == 'raster':
                                            optional(child, desc_file)
                                            print('QgsProcessingParameterRasterDestination|', end='', file=desc_file)
                                            print_name_def_opt(child, desc_file)
                                        elif k.attrib['prompt'] == 'vector':
                                            optional(child, desc_file)
                                            print('QgsProcessingParameterVectorDestination|', end='', file=desc_file)
                                            print_name_desc(child, desc_file)
                                            print('TypeVector|', end='', file=desc_file)
                                            print_def_opt(child, desc_file)
                                        elif k.attrib['prompt'] == 'file' or k.attrib['prompt'] == 'sigfile':
                                            optional(child, desc_file)
                                            print('QgsProcessingParameterFileDestination|', end='', file=desc_file)
                                            print_name_desc(child, desc_file)
                                            print('Txt files(*.txt)|', end='', file=desc_file)
                                            print_def_opt(child, desc_file)
                                        elif k.attrib['prompt'] == 'layer':
                                            pass
                        elif child.attrib['name'] == 'signature':
                            optional(child, desc_file)
                            print('QgsProcessingParameterFile|', end='', file=desc_file)
                            print_name_def(child, desc_file)
                            print('QgsProcessingParameterFile.File|txt|', end='', file=desc_file)
                            print_def_opt(child, desc_file)
                        else:
                            # print('Not recognized >>> ', end='')
                            # print(child.attrib['name'].strip())
                            optional(child, desc_file)
                            print('QgsProcessingParameterString|', end='', file=desc_file)
                            print_name_def(child, desc_file)
                            print('True|', end='', file=desc_file)
                            print_optional(child, desc_file)


                        # promt = child.find('gisprompt')
                        # if promt is None or promt == 'cats':
                        # print('QgsProcessingParameterString|', end='', file=desc_file)
                        # print_name_def(child, desc_file)
                        # print('True|', end='', file=desc_file)
                        # print_optional(child, desc_file)
                        # # else:
                        #     print('Not recognized >>> ', end='')
                        #     print(child.attrib['name'].strip())




                        # elif child.find('gisprompt') is None:
                        #     if child.attrib['type'] == 'string':
                        #     # promt = child.find('gisprompt')
                        #     # if promt is None or promt == 'cats':
                        #         print('QgsProcessingParameterString|', end='', file=desc_file)
                        #         print_name_def(child, desc_file)
                        #         print('True|', end='', file=desc_file)
                        #         print_optional(child, desc_file)
                        #     # else:
                        #     #     print('Not recognized >>> ', end='')
                        #     #     print(child.attrib['name'].strip())
                        #
                        #     elif child.attrib['type'] == 'integer':
                        #         print('QgsProcessingParameterNumber|', end='', file=desc_file)
                        #         print_name_desc(child, desc_file)
                        #         print('QgsProcessingParameterNumber.Integer|', end='', file=desc_file)
                        #         print_def_opt(child, desc_file)
                        #
                        #     elif child.attrib['type'] == 'float':
                        #         print('QgsProcessingParameterNumber|', end='', file=desc_file)
                        #         print_name_desc(child, desc_file)
                        #         print('QgsProcessingParameterNumber.Double|', end='', file=desc_file)
                        #         print_def_opt(child, desc_file)
                        #     else:
                        #         print('Not recognized >>> ', end='')
                        #         print(child.attrib['name'].strip())

            elif child.tag == 'flag':
                # optional(child, desc_file)
                print('*QgsProcessingParameterBoolean|', end='', file=desc_file)
                print_name_desc(child, desc_file)
                print('False|True', file=desc_file)
        if cmd == 'r.colors':
            print('QgsProcessingParameterFolderDestination|output_dir|Output Directory|None|False', file=desc_file)
    except Exception, e:
        print('{} - unable to create description, because: '.format(cmd) + str(e))

# print(gtask.get_interface_description('d.barscale'))