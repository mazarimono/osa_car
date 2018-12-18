import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import os

df = pd.read_csv('./csv2/all_all.csv', index_col=0)

app = dash.Dash()
server = app.server

app.layout = html.Div(children=[
    html.H1(children='大阪自動車保有台数',
    style={
        'textAlign': 'center',
        'color': '#5882FA',
    }),
        dcc.Dropdown(
            id="selected_item",
            options=[{'label': i[0], 'value': i[1]} for i in zip(df.columns.unique(), df.columns.unique())],
            value=['自動車総数','電気自動車総数'],
            multi=True,
            style={
                'textAlign': 'center',
                'width': '50%'
            }
        ),
        html.Div(
            id='osa_car',
        )
    ]
)
@app.callback(
    dash.dependencies.Output('osa_car', 'children'),
    [dash.dependencies.Input('selected_item', 'value')]
)
def update_graph(syuruis):
    graphs = []

    if not syuruis:
        graphs.append(html.H3(
            "要素を選択してください！"
        ))
    else:
        for i, syurui in enumerate(syuruis):
            dff = df[syurui]
            chart = {
                'x': dff.index,
                'y': dff,
                'name': syurui,
            }
            graphs.append(dcc.Graph(
                id=syurui,
                figure={
                    'data': [chart],
                    'layout': {
                        'margin': {'b': 40, 'r':140, 'l':140, 't': 80},
                        'legend': {'x': 0},
                        'height':400,
                        'title': syurui,
                    }
                }
            ))

    return graphs

if __name__=='__main__':
    app.run_server(debug=True)