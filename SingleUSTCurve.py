# -*- coding: utf-8 -*-
# Import required libraries
import os

import pandas as pd
import numpy as np
import chart_studio.plotly as py

import flask
from flask_cors import CORS
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html


# Setup the app
app = dash.Dash(__name__)
server = app.server


df = pd.read_csv("data/yield_curve.csv")

xlist = list(df["x"].dropna())
ylist = list(df["y"].dropna())

del df["x"]
del df["y"]
print(df)

zlist = []
for row in df.iterrows():
    index, data = row
    zlist.append(data.tolist())

print(zlist)

UPS = {
    0: dict(x=0, y=0, z=1),
    1: dict(x=0, y=0, z=1),
    2: dict(x=0, y=0, z=1),
    3: dict(x=0, y=0, z=1),
    4: dict(x=0, y=0, z=1),
    5: dict(x=0, y=0, z=1),
}

CENTERS = {
    0: dict(x=0.3, y=0.8, z=-0.5),
    1: dict(x=0, y=0, z=-0.37),
    2: dict(x=0, y=1.1, z=-1.3),
    3: dict(x=0, y=-0.7, z=0),
    4: dict(x=0, y=-0.2, z=0),
    5: dict(x=-0.11, y=-0.5, z=0),
}

EYES = {
    0: dict(x=2.7, y=2.7, z=0.3),
    1: dict(x=0.01, y=3.8, z=-0.37),
    2: dict(x=1.3, y=3, z=0),
    3: dict(x=2.6, y=-1.6, z=0),
    4: dict(x=3, y=-0.2, z=0),
    5: dict(x=-0.1, y=-0.5, z=2.66)
}

# Make 3d graph

def make_graph():
    z_secondary_beginning = [z[1] for z in zlist if z[0] == 'None']
    z_secondary_end = [z[0] for z in zlist if z[0] != 'None']
    z_secondary = z_secondary_beginning + z_secondary_end
    x_secondary = ['3-month'] * len(z_secondary_beginning) + ['1-month'] * len(z_secondary_end)
    y_secondary = ylist
    opacity = 0.7

    trace1 = dict(
        type="surface",
        x=xlist,
        y=ylist,
        z=zlist,
        hoverinfo='x+y+z',
        lighting={
            "ambient": 0.95,
            "diffuse": 0.99,
            "fresnel": 0.01,
            "roughness": 0.01,
            "specular": 0.01,
        },
        colorscale=[[0, "rgb(230,245,254)"], [0.4, "rgb(123,171,203)"], [
            0.8, "rgb(40,119,174)"], [1, "rgb(37,61,81)"]],
        opacity=opacity,
        showscale=False,
        zmax=9.18,
        zmin=0,
        scene="scene",
    )

    trace2 = dict(
        type='scatter3d',
        mode='lines',
        x=x_secondary,
        y=y_secondary,
        z=z_secondary,
        hoverinfo='x+y+z',
        line=dict(color='#444444')
    )

    data = [trace1, trace2]


    layout = dict(
        autosize=True,
        font=dict(
            size=12,
            color="#CCCCCC",
        ),
        margin=dict(
            t=5,
            l=5,
            b=5,
            r=5,
        ),
        showlegend=False,
        hovermode='closest',
        scene=dict(
            aspectmode="manual",
            aspectratio=dict(x=2, y=5, z=1.5),
            camera=dict(
                up=UPS[0],
                center=CENTERS[0],
                eye=EYES[0]
            ),
            annotations=[dict(
                showarrow=False,
                y="2015-03-18",
                x="1-month",
                z=0.046,
                text="Point 1",
                xanchor="left",
                xshift=10,
                opacity=0.7
            ), dict(
                y="2015-03-18",
                x="3-month",
                z=0.048,
                text="Point 2",
                textangle=0,
                ax=0,
                ay=-75,
                font=dict(
                    color="black",
                    size=12
                ),
                arrowcolor="black",
                arrowsize=3,
                arrowwidth=1,
                arrowhead=1
            )],
            xaxis={
                "showgrid": True,
                "title": "",
                "type": "category",
                "zeroline": False,
                "categoryorder": 'array',
                "categoryarray": list(reversed(xlist))
            },
            yaxis={
                "showgrid": True,
                "title": "",
                "type": "date",
                "zeroline": False,
            },
        )
    )

    figure_dict = dict(data=data, layout=layout)
    return figure_dict

fig = make_graph()
app.layout = html.Div(
    [
            dcc.Graph(
                id='graph',
                style={'height': '60vh'},
                figure = fig
            )

])

# Run the Dash app
if __name__ == '__main__':
    app.server.run()
