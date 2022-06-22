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
import xml.etree.ElementTree as et
import pandas as pd
import plotly.express as px
import plotly.figure_factory as FF
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output


# ===============================================================================
# METHODS
# ===============================================================================
def tcx2cvs():
    istream = open("/Users/jean-marcbaubet/Downloads/Saint Jean Cimetière.tcx", 'r')
    xml = istream.read()

    xml = re.sub('xmlns=".*?"', '', xml)
    root = et.fromstringlist(xml)
    for name in root.findall('Courses/Course/Name'):
        print("Nom de la course : {}".format(name.text))
        nom_course = name.text

    nom_fichier = "/Users/jean-marcbaubet/Downloads/" + nom_course + ".cvs"
    fichier_cvs = open(nom_fichier, "w")
    fichier_cvs.write("Distance,Altitude,Latitude,Longitude\n")
    for trackPoint in root.findall('Courses/Course/Track/Trackpoint'):
        distance = float(trackPoint.find('DistanceMeters').text)
        altitude = float(trackPoint.find('AltitudeMeters').text)
        longitude = float(trackPoint.find('Position/LongitudeDegrees').text)
        latitude = float(trackPoint.find('Position/LatitudeDegrees').text)
        fichier_cvs.write("{:4.0f},{:5.0f},{},{}\n".format(distance, altitude, longitude, latitude))
    return nom_fichier

nom_fichier = tcx2cvs()



app = dash.Dash(__name__)

df = pd.read_csv(nom_fichier)


#df = df.groupby(['Distance'])[['Altitude']].mean()

print(df[:5])

app.layout = html.Div([
    html.H1('Mon premier Dash bord', style={'text-align' : 'center'}),
    html.Button('test', id='affiche', value='0'),
    dcc.Graph(id='profile', figure={})
])
# xaxis={'domain':[0,200]}, yaxis={'domain':[100, 120]}

@app.callback(
    Output('profile', 'figure'),
    Input('affiche', 'value')
)

def update_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))

    x, y = 'Distance', 'Altitude'
    fig = px.line(df, x=x, y=y)
#    fig.update_layout(xaxis_range=[0, 8000])
#    fig.update_layout(yaxis_range=[80, 150])
    return fig

# ===============================================================================
# MAIN METHOD AND TESTING AREA
# ===============================================================================


def main():
    """Description of main()"""

if __name__ == '__main__':
 #   main()
    app.run_server(debug=True)
