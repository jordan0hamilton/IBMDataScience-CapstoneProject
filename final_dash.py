# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv')
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                html.Div(dcc.Dropdown(id='site-dropdown',
                                            options=[
                                                    {'label': 'All Sites', 'value': 'ALL'},
                                                    {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                    {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                                    {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                    {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                                ],
                                                value='ALL',
                                                placeholder='Select Launch Site',
                                                searchable=True
                                                )),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                html.Div(dcc.RangeSlider(id='payload-slider',
                                min=0, max=10000, step=1000,
                                marks={0: '0',
                                       1000: '1000',
                                       2000: '2000',
                                       3000: '3000',
                                       4000: '4000',
                                       5000: '5000',
                                       6000: '6000',
                                       7000: '7000',
                                       8000: '8000',
                                       9000: '9000',
                                       10000: '10000'},
                                value=[min_payload, max_payload])
                                ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])
                            


@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        all_fig = px.pie(spacex_df, values='class', 
        names='Launch Site', 
        title='Launch Success Rate for All Sites')
        return all_fig
    else:
        each_df = spacex_df[spacex_df['Launch Site'] == entered_site].groupby(['Launch Site', 'class']).size().reset_index(name='class count')
        fig = px.pie(each_df, values='class count', names='class', title='Success Rate for' + ' ' + entered_site + ' ' + 'Site')
        return fig
        

@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
                [Input(component_id='site-dropdown', component_property='value'), Input(component_id='payload-slider', component_property='value')])
def scatter(entered_site,payload):
    low, high = (payload[0],payload[1])
    all_scat=spacex_df[spacex_df['Payload Mass (kg)'].between(low,high)]
    if entered_site=='ALL':
        all_fig=px.scatter(all_scat,x='Payload Mass (kg)',y='class',color='Booster Version Category',title='Success Count by Payload Mass (kg) for All Sites')
        return all_fig
    else:
        each_scat=all_scat[all_scat['Launch Site']==entered_site]
        fig=px.scatter(each_scat, x='Payload Mass (kg)', y='class',color='Booster Version Category',title='Success Count by Payload Mass (kg) for' + ' ' + entered_site + ' ' + 'Site')
        return fig

if __name__ == '__main__':
    app.run_server()
