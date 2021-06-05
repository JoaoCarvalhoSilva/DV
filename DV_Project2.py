import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd
import plotly.express as px

# Dataset Processing

path = 'https://raw.githubusercontent.com/TheGroovyPanda/DV/main/'

df = pd.read_csv(path + 'DV_Data.csv', sep=";")


# Dash Core Components

# requirement for countries dropdown

country_options = [
    dict(label=country, value=country)
    for country in df['COUNTRY'].unique()]

week_slider = dcc.RangeSlider(
        id='week_slider',
        min=1,
        max=20,
        value=[1, 20],
        marks={1: 'Week 1',
               2: '2',
               3: '3',
               4: '4',
               5: '5',
               6: '6',
               7: '7',
               8: '8',
               9: '9',
               10: '10',
               11: '11',
               12: '12',
               13: '13',
               14: '14',
               15: '15',
               16: '16',
               17: '17',
               18: '18',
               19: '19',
               20: '20'},
        step=None,
    )

radio_country = dcc.RadioItems(
    id='country_radio',
    options=country_options,
    value='Portugal',
    labelStyle={'display': 'block','font-size': '1.4rem'}
)

# Start the app

app = dash.Dash(__name__)

# App layout

app.layout = html.Div([

    html.H1("Covid 19 - Europe's overview in 2021", style={'text-align': 'center'}),


    html.Div([
            html.H2("New Cases and Deaths per Week", style={'text-align': 'center'}),
            html.Br(),
            dcc.Graph(id='scatter_plot'),
            html.Br(),
            week_slider,
            html.Br()
          ], style={'width': '96%', 'height': '100%', 'display': 'inline-block'}, className='box'),

    html.H3("How is the number of ICU Patients evolving Throughout Europe?", style={'text-align': 'center'}),
        html.Div([
            html.H4("Select Country", style={'text-align': 'left'}),
            radio_country,
        ], style={'width': '15%','height': '50%', 'display': 'inline-block'}, className='box'),

        html.Div([
            dcc.Graph(id='bar_plot'),
        ], style={'width': '77%', 'height': '100%', 'display': 'inline-block'}, className='box'),


html.Div([
    html.H2("How is Vaccination evolving in Europe?", style={'text-align': 'center','width': '96%'}, className='box'),
        html.Div([
            dcc.Graph(id='choropleth_plot'),
        ], style={'width': '96%', 'display': 'inline-block'}, className='box'),
    ]),

html.Div([
    html.H6("Daniela Domingues Ferreira - m20200395"),
    html.H6("David Pedro - m20200344"),
    html.H6("João Silva - m20200333"),
    ]),
], className='body')

# Connecting the Plotly graphs with Dash components


@app.callback(
    Output('scatter_plot', 'figure'),
    [Input('week_slider', 'value')]
)
def update_graph(weeks_chosen):
    filtered_by_week_df = df[(df['WEEK'] >= weeks_chosen[0]) & (df['WEEK'] <= weeks_chosen[1])]

    dff = filtered_by_week_df.groupby(["COUNTRY"], as_index=False)[["NEW_CASES_PER_MILLION", "NEW_DEATHS_PER_MILLION", "GDP_PER_CAPITA","NEW_TESTS_PER_THOUSAND"]].mean()

    scatterplot = px.scatter(
        data_frame=dff,
        x="NEW_CASES_PER_MILLION",
        y="NEW_DEATHS_PER_MILLION",
        hover_data=["GDP_PER_CAPITA","NEW_TESTS_PER_THOUSAND"],
        size="GDP_PER_CAPITA",
        text="COUNTRY",
        color="NEW_TESTS_PER_THOUSAND",
        color_continuous_scale = "Inferno",
        range_color = (0, 50)
    )

    scatterplot.update_traces(textposition='top center')

    return scatterplot


@app.callback(
    Output('bar_plot', 'figure'),
    [Input('country_radio', 'value')]
)
def update_graph(country_chosen):
    filtered_by_country_df = df.loc[df['COUNTRY'] == country_chosen]

    bar = px.bar(
        data_frame=filtered_by_country_df,
        x="WEEK",
        y="ICU_PATIENTS_PER_MILLION",
        color="HOSP_PATIENTS_PER_MILLION",
        color_continuous_scale="Inferno",
        range_color = (500, 0)
    )

    return bar

@app.callback(
    Output('choropleth_plot', 'figure'),
    [Input('country_radio', 'value')]
)
def update_graph(country_chosen):
    filtered_by_country_df = df.loc[df['COUNTRY'] == df['COUNTRY']]

    choropleth = px.choropleth(
                data_frame=filtered_by_country_df,
                locations='CODE',
                color="TOTAL_VACCINATIONS_PER_HUNDRED",
                animation_frame="WEEK",
                color_continuous_scale="Inferno",
                locationmode='ISO-3',
                scope="europe",
                range_color=(0, 20),
                height=900
    )

    return choropleth


if __name__ == '__main__':
    app.run_server(debug=True, port=8888)
