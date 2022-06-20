#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
summary

description

:REQUIRES:

:TODO:

:AUTHOR:
:ORGANIZATION:
:CONTACT:
:SINCE: %(date)s
:VERSION: 0.1
"""
# ===============================================================================
# PROGRAM METADATA
# ===============================================================================
__author__ = ''
__contact__ = ''
__copyright__ = ''
__license__ = ''
__date__ = '%(date)s'
__version__ = '0.1'

# ===============================================================================
# IMPORT STATEMENTS
# ===============================================================================
import re
import sys
import xml.etree.ElementTree as ET
import pandas as pd
import plotly.express as px
import dash


# ===============================================================================
# METHODS
# ===============================================================================
def tcx2cvs():
    istream = open("/Users/jean-marcbaubet/Downloads/Saint Jean Cimetière.tcx", 'r')
    xml = istream.read()

    xml = re.sub('xmlns=".*?"', '', xml)
    root = ET.fromstringlist(xml)
    for name in root.findall('Courses/Course/Name'):
        print("Name : {}".format(name.text))

    nomFichier = "/Users/jean-marcbaubet/Downloads/" + name.text + ".cvs"
    fichierCvs = open(nomFichier, "w")
    fichierCvs.write("Distance,Altitude,Latitude,Longitude\n")
    for trackPoint in root.findall('Courses/Course/Track/Trackpoint'):
        distance = float(trackPoint.find('DistanceMeters').text)
        altitude = float(trackPoint.find('AltitudeMeters').text)
        longitude = float(trackPoint.find('Position/LongitudeDegrees').text)
        latitude = float(trackPoint.find('Position/LatitudeDegrees').text)
        fichierCvs.write("{:4.0f},{:5.2f},{},{}\n".format(distance, altitude, longitude, latitude))


# ===============================================================================
# MAIN METHOD AND TESTING AREA
# ===============================================================================
def main():
    """Description of main()"""
    tcx2cvs()


if __name__ == '__main__':
    main()
