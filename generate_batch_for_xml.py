import os
import sys
import subprocess

# https://gis.stackexchange.com/questions/203310/connecting-python-script-external-to-grass-gis-7-program-in-windows-10?noredirect=1&lq=1
# add grass.script
grass7bin = r'C:\Program Files (x86)\QGIS 3.0\bin\grass74.bat'
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
gisbase = out.strip(os.linesep)

os.environ['GISBASE'] = gisbase
grass_pydir = os.path.join(gisbase, "etc", "python")
sys.path.append(grass_pydir)

import grass.script.setup as gsetup

gisdb = os.path.join(os.path.expanduser("~"), "Documents/grassdata")
location = "nc_spm_08"
mapset = "user1"

rcfile = gsetup.init(gisbase, gisdb, location, mapset)

from grass.script import core as gcore

cmds = list(gcore.get_commands()[0])
cmds.sort()
file_names = [cmd.replace('.', '_') for cmd in cmds]
print len(cmds)
with open(os.path.join("C:\Users", "radek", "Desktop", "generate_xml.bat"), 'w') as file:
    file.write('@ECHO ON\n')
    for name, file_name in zip(cmds, file_names):
        file.write('{} --interface-description > C:\Users\\radek\Desktop\XML_grass\{}.xml\n'.format(name, file_name))

from grass.script import task as gtask
gtask.command_info('r.info')

# for name in cmds:
print gtask.parse_interface('C:\\Program Files (x86)\\QGIS 3.0\\apps\\grass\\grass-7.4.0\\scripts\\r.grow.py')


# r.univar --interface-description > C:\Users\radek\Desktop\r_univar.txt
os.remove(rcfile)
