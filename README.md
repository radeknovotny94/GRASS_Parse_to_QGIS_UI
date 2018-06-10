# GRASS Parse To QGIS UI

This is one part of Google Summer of Code 2018 project - Improve GRASS GIS integration in QGIS 3.
For more information see Wiki page: https://trac.osgeo.org/grass/wiki/GSoC/2018/IntegrationInQGIS3
Or GitHub: https://github.com/radeknovotny94/GRASSIntegrationInQGIS3

First step is creating parser tool which create UI description for QGIS from GRASS description. This implementation is going on this GitHub page.

How run this script:
In this moment script not run on Windows > https://github.com/radeknovotny94/GRASS_Parse_to_QGIS_UI/issues/6

For test:
1. You have to create 'desc' and 'xml' folder in directory, where you run the script.

2. Just run script - GRASSDescribtionParser.py, it should find QGIS/GRASS installation, find GRASS moduls and create their description for QGIS Processing plugin in folder desc.


