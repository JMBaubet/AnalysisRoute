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
from xml.etree.ElementTree import fromstringlist

import dash
import pandas as pd
import plotly.express as px
from dash import dcc
from dash import html
from dash.dependencies import Input, Output


# ===============================================================================
# METHODS
# ===============================================================================


def lecture_tcx():
    nom_course = ""
    istream = open("/Users/jean-marcbaubet/Downloads/Saint Jean Cimetière.tcx", 'r')
    xml = istream.read()

    xml = re.sub('xmlns=".*?"', '', xml)
    root = fromstringlist(xml)
    for name in root.findall('Courses/Course/Name'):
        print("Nom de la course : {}".format(name.text))
        nom_course = name.text

    tags = {"tags": []}
    distance_precedente = 0
    altitude_precedente = 0
    for elem in root.findall('Courses/Course/Track/Trackpoint'):
        distance = float(elem.find('DistanceMeters').text)
        altitude = float(elem.find('AltitudeMeters').text)
        # Calcul de la pente
        try:
            pente = format(100 * (altitude_precedente - altitude) / (distance_precedente - distance), '.1f')
        except ZeroDivisionError:
            pente = 0.0

        tag = {"Distance": distance,
               "Altitude": altitude,
               "Pente": pente,
               "Latitude": float(elem.find('Position/LongitudeDegrees').text),
               "Longitude": float(elem.find('Position/LatitudeDegrees').text)}
        tags["tags"].append(tag)
        distance_precedente = distance
        altitude_precedente = altitude

    print(tags["tags"][0])
    data_frame = pd.DataFrame(tags["tags"])
    print(data_frame.head())
    return data_frame, nom_course


app = dash.Dash(__name__)

df, nom = lecture_tcx()

app.layout = html.Div([
    html.H1('Parcours: {}'.format(nom), style={'text-align': 'left'}),
    html.Button('test', id='affiche', value='0', style={'width': '1080px'}),
    dcc.Graph(id='profile', figure={}, style={'width': '1080px', 'height': '480px'})
])


# xaxis={'domain':[0,200]}, yaxis={'domain':[100, 120]}
@app.callback(
    Output('profile', 'figure'),
    Input('affiche', 'value')
)
def update_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))

    fig = px.line(df, x='Distance', y='Altitude', hover_data=['Pente'])
    fig.update_layout(xaxis_range=[0, 90000])
    fig.update_layout(yaxis_range=[0, 1000])
    return fig


# ===============================================================================
# MAIN METHOD AND TESTING AREA
# ===============================================================================


def main():
    """Description of main()"""


if __name__ == '__main__':
    #   main()
    app.run_server(debug=True)
