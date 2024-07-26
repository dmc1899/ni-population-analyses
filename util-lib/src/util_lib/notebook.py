import pandas as pd
from plotly import graph_objects as go

import graph


def print_full(x):
    pd.set_option('display.max_rows', len(x))
    print(x)
    pd.reset_option('display.max_rows')


def print_full_all_opts(x):
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 2000)
    pd.set_option('display.float_format', '{:20,.2f}'.format)
    pd.set_option('display.max_colwidth', None)
    print(x)
    pd.reset_option('display.max_rows')
    pd.reset_option('display.max_columns')
    pd.reset_option('display.width')
    pd.reset_option('display.float_format')
    pd.reset_option('display.max_colwidth')


def show_named_plotly_colours() -> None:
    df = graph.get_named_plotly_colours()

    fig = go.Figure(data=[go.Table(
        header=dict(
            values=["Plotly Named CSS colours"],
            line_color='black', fill_color='white',
            align='center', font=dict(color='black', size=14)
        ),
        cells=dict(
            values=[df.colour],
            line_color=[df.colour], fill_color=[df.colour],
            align='center', font=dict(color='black', size=11)
        ))
    ])

    fig.show()
