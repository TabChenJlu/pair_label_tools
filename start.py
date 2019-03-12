import dash
import os
import configparser
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from tools.utils import *

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = title

app.layout = html.Div([
    html.H1(children=title, style={'textAlign': 'center', 'color': '#ff0000'}),
    html.Div([
        html.Span('输入你的用户名:'),
        dcc.Input(id='user', type='text', value='',
                  style={'width': '10%'}),
        html.Button('开始(请点击一次)', id='start', style={
                    'width': '10%', 'marginLeft': '2%'}),
        html.Button('左边', id='right', style={
                    'width': '25%', 'marginLeft': '2%'}),
        html.Button('右边', id='left', style={
                    'width': '25%', 'marginLeft': '2%'}),
    ], style={"width": '100%'}),
    html.Div(id='output', style={'columnCount': 1}),
    dcc.Input(id='pair-id', type='text', value='', style={'display': 'none'})
], style={'columnCount': 1,'margin':'2%'}
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


def process_pargraph(raw_text):
    p_list = []
    for text in raw_text.strip().split('\n'):
        who, content = text.split(':')
        if who == '老师':
            p_list.append(html.Strong(
                who, style={'color': teacher_font_color}))
            p_list.append(
                html.Span(':' + content, style={'color': teacher_font_color}))
            p_list.append(html.Br())
        else:
            p_list.append(html.Strong(
                who, style={'color': student_font_colot}))
            p_list.append(
                html.Span(':' + content, style={'color': student_font_colot}))
            p_list.append(html.Br())
    return p_list


@app.callback(
    Output('output', 'children'),
    [Input('right', 'n_clicks_timestamp'),
     Input('left', 'n_clicks_timestamp'),
     Input('start', 'n_clicks_timestamp')],
    [State('pair-id', 'value'),
     State('user', 'value')
     ]
)
def update_data(value_1, value_2, value_3, value_4, user):
    if value_3 is None:
        logger.info('Not click start~')
        return ''
    logger.info('value_1:{}, value_2:{}, value_3:{}, value_4:{}'.format(
        value_1, value_2, value_3, value_4))
    label = get_clicked_button_name(value_1, value_2)
    if label != -1 and value_4 != '':
        save_label(int(value_4), label, user)
    # new pair
    my_pair = Pair()
    # my_pair.i = 102
    # my_pair.j = 183
    text_left, text_right = my_pair.get_text()
    text_left = process_pargraph(text_left)
    text_right = process_pargraph(text_right)
    output_data = html.Div([
        html.H3('ID:{}'.format(my_pair.id), id='pair_id_des'),
        dcc.Input(id='pair-id', type='text', value=my_pair.id,
                  style={'display': 'none'}),
        html.Div([
            html.Div(text_left, style={
                     'columnCount': 1, 'float': 'left', 'width': '48%'}),
            html.Div(text_right,
                     style={'columnCount': 1, 'float': 'right', 'width': '48%'}),
        ],)
    ])
    return output_data


if __name__ == '__main__':
    app.run_server(debug=eval(config['server']['debug']),
                   host=config['server']['host'], port=int(config['server']['port']))
