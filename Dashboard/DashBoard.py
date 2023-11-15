from dash import Dash, html, dcc, dash_table
import plotly.express as px
import pandas as pd
from sqlalchemy import create_engine
import dash_bootstrap_components as dbc
from dash import html
from dash.dependencies import Input, Output, State
import time

# Configurar o tema Bootstrap
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Configuração da conexão com o banco de dados
server = 'localhost'
database = 'LINXPOS'
username = 'sa'
password = ''
driver = 'ODBC Driver 17 for SQL Server'

# Criação da string de conexão
connection_string = f'mssql+pyodbc://{username}:{password}@{server}/{database}?driver={driver}'

# Criação da conexão
engine = create_engine(connection_string)

# Função para executar a consulta do primeiro SELECT
def update_first_select(n):
    query = 'SELECT SERVICO, MEDIA_TEMPO_EXECUCAO_SEGUNDOS, HORA_EXECUCAO FROM W_DS_HERING_EXECUCAO order by MEDIA_TEMPO_EXECUCAO_SEGUNDOS DESC'
    df = pd.read_sql_query(query, engine)
    return df.to_dict('records')

# Função para executar a consulta do segundo SELECT
def update_second_select(n):
    query_second = 'SELECT SERVICO, DATA_INICIO, NIVEL_ALERTA, MENSAGEM FROM W_DS_EM_EXECUCAO_NIVEL_ALERTA ORDER BY DATA_INICIO'
    df_second = pd.read_sql_query(query_second, engine)
    return df_second.to_dict('records')

# Mapear cores com base no NIVEL_ALERTA
colors = {
    'ALERTA GRAVE': 'rgba(255, 0, 0, 0.6)',
    'ALERTA MAXIMA': 'rgba(255, 0, 0, 0.6)',
    'ALERTA': 'rgba(255, 165, 0, 0.6)',
    'ATENÇÃO': 'rgba(255, 255, 0, 0.6)',
    'NORMAL': 'rgba(0, 128, 0, 0.6)'
}

# Adicionar estilo condicional à tabela
conditional_styles = [
    {
        'if': {'filter_query': '{{NIVEL_ALERTA}} = "{}"'.format(level)},
        'backgroundColor': colors[level],
        'color': 'black'
    }
    for level in colors.keys()
]

# Layout do aplicativo
app.layout = dbc.Container(
    fluid=True,
    children=[
        html.H1(children='DS Dashboard', style={'textAlign': 'center', 'color': '#007BFF', 'marginBottom': 20}),
        
        html.Div(children='''
        ''', style={'textAlign': 'center', 'color': '#333', 'marginBottom': 30}),
        
        dbc.Row([
            dbc.Col(
                dbc.Card(
                    dbc.CardBody([
                        html.H4("Média de Tempo de Execução por Serviço", className="card-title"),
                        dcc.Graph(
                            id='bar-chart',
                            figure=px.bar()
                        ),
                    ]),
                    style={"marginBottom": "20px", "boxShadow": "0px 4px 8px rgba(0, 0, 0, 0.1)", "marginLeft": "auto"},
                ),
                width=6  # Ajuste o valor conforme necessário
            ),
            
            dbc.Col(
                dbc.Card(
                    dbc.CardBody([
                        html.H4("Distribuição do Tempo de Execução por Serviço", className="card-title"),
                        dcc.Graph(
                            id='pie-chart',
                            figure=px.pie()
                        ),
                    ]),
                    style={"marginBottom": "20px", "boxShadow": "0px 4px 8px rgba(0, 0, 0, 0.1)", "marginRight": "auto"},
                ),
                width=6  # Ajuste o valor conforme necessário
            ),
        ]),

        dcc.Interval(
            id='interval-component',
            interval=1 * 60 * 1000,  # em milissegundos (1 minuto)
            n_intervals=0
        ),

        dbc.Card(
            dbc.CardBody([
                html.H4("Serviços em execução", className="card-title"),
                dash_table.DataTable(
                    id='table',
                    columns=[
                        {'name': 'Serviço', 'id': 'SERVICO'},
                        {'name': 'Data de Início', 'id': 'DATA_INICIO'},
                        {'name': 'Alerta', 'id': 'NIVEL_ALERTA'},
                    ],
                    style_data_conditional=conditional_styles,
                    style_cell={'textAlign': 'center'},  # Centralizar células
                    tooltip_data=[
                        {
                            column: {'value': str(row[column]), 'type': 'markdown'}
                            for column in ['MENSAGEM']
                        }
                        for row in update_second_select(0)
                    ],
                ),
    ]),
    style={"marginBottom": "20px", "boxShadow": "0px 4px 8px rgba(0, 0, 0, 0.1)", "marginLeft": "auto", "marginRight": "auto", "width": "60%"},
),

    ]
)

# Callback para atualizar os dados do primeiro SELECT
@app.callback(
    Output('bar-chart', 'figure'),
    [Input('interval-component', 'n_intervals')]
)
def update_bar_chart(n):
    df = pd.DataFrame(update_first_select(n))
    fig = px.bar(
        df,
        x="SERVICO",
        y="MEDIA_TEMPO_EXECUCAO_SEGUNDOS",
        color="SERVICO",
        hover_data=["HORA_EXECUCAO"],
        labels={"MEDIA_TEMPO_EXECUCAO_SEGUNDOS": "Média Tempo de Execução (segundos)"},
    )
    fig.update_layout(
        showlegend=True,
        legend_title='Serviços',
        font=dict(family="Arial", size=14, color="RebeccaPurple"),
        height=600,  # Ajuste o valor conforme necessário
        width=900,   # Ajuste o valor conforme necessário
    )
    return fig

# Callback para atualizar os dados do segundo SELECT
@app.callback(
    Output('pie-chart', 'figure'),
    [Input('interval-component', 'n_intervals')]
)
def update_pie_chart(n):
    df_pie = pd.DataFrame(update_first_select(n))
    fig_pie = px.pie(
        df_pie,
        names="SERVICO",
        values="MEDIA_TEMPO_EXECUCAO_SEGUNDOS",
    )
    fig_pie.update_layout(
        showlegend=False,
        font=dict(family="Arial", size=14, color="RebeccaPurple"),
    )
    return fig_pie

# Callback para atualizar os dados da tabela
@app.callback(
    Output('table', 'data'),
    [Input('interval-component', 'n_intervals')]
)
def update_table_data(n):
    return update_second_select(n)

if __name__ == '__main__':
    app.run(debug=True)
