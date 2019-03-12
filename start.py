import dash
import os
import configparser
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from tools.utils import *

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


app.layout = html.Div([
    html.H1(children=title,style={'textAlign': 'center','color': '#ff0000'}),
    html.Div([
        html.Button('开始', id='start',style={'marginRight': '20%'}),
        html.Button('左边', id='right'),
        html.Button('右边', id='left'),
    ], style={'columnCount': 3}),
    html.Div(id='output', style={'columnCount': 1}),
    dcc.Input(id='pair-id', type='text', value='', style={'display': 'none'})
], style={'columnCount': 1}
)


def get_clicked_button_name(value_1, value_2):
    if value_1 is None:
        value_1 = 0
    if value_2 is None:
        value_2 = 0
    if value_1 == 0 and value_2 == 0:
        return -1
    if value_1 > value_2:
        return 1
    else:
        return 0


@app.callback(
    Output('output', 'children'),
    [Input('right', 'n_clicks_timestamp'),
     Input('left', 'n_clicks_timestamp'),
     Input('start', 'n_clicks_timestamp')],
    [State('pair-id', 'value')
     ]
)

def update_data(value_1, value_2, value_3, value_4):
    if value_3 is None:
        logger.info('Not click start~')
        return ''
    logger.info('value_1:{}, value_2:{}, value_3:{}, value_4:{}'.format(value_1, value_2, value_3, value_4))
    label = get_clicked_button_name(value_1, value_2)
    if label != -1:
        save_label(int(value_4), label)
    # new pair
    my_pair = Pair()
    text_left, text_right = my_pair.get_text()

    output_data = html.Div([
        html.H1(my_pair.id, id='pair_id_des'),
        dcc.Input(id='pair-id', type='text', value=my_pair.id,
                  style={'display': 'none'}),
        html.Div([
            dcc.Markdown(children=text_left, id='text-left',),
            dcc.Markdown(children=text_right, id='text-right'),
        ], style={'columnCount': 2})
    ])
    return output_data


if __name__ == '__main__':
    app.run_server(debug=False)
