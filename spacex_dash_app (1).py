# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
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
                                dcc.Dropdown(id='site-dropdown',
                                options=[
                                            {'label': 'All Sites', 'value': 'ALL'},
                                            {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                            {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                            {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                            {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
                                        ],
                                        value='ALL',
                                        placeholder="Select a launch site",
                                        searchable=True
                                                ),  
                                        html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                # Function decorator to specify function input and output

        # return the outcomes piechart for a selected site
                                
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider', 
                                min = 0, max = 10000,step =1000,
                                marks={0: '0',
                                        2500: '2500',
                                        5000: '5000',
                                        7500: '7500',
                                        10000: '10000'},
                                value = [0,10000]
                                
                                ),






                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output

@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
            [Input(component_id='site-dropdown', component_property='value')])
def update_pie_chart(selected_site):
    if selected_site == 'ALL':
        pie_data = spacex_df.groupby('Launch Site')['class'].value_counts().reset_index(name='counts')
        fig = px.pie(pie_data, values='counts', names='Launch Site', title='Total Successful Launches in All Sites')
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]
        #print(selected_site)
    
        pie_data = filtered_df['class'].value_counts().reset_index(name='counts')
        #print(pie_data)
        
        fig = px.pie(pie_data, values='counts', names='class', title=f'Success Launches for Site {selected_site}')
    return fig
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'), 
    Input(component_id="payload-slider", component_property="value")]
)

def update_scatter_chart(selected_site, payload_range):
    low,high = payload_range
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= low) & 
    (spacex_df['Payload Mass (kg)'] <= high)]
    if selected_site == 'ALL':
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', 
        color='Booster Version Category', 
        title='Payload vs. Outcome for All Sites')
    else:
        filtered_site_df = filtered_df[filtered_df['Launch Site'] 
        == selected_site]
        fig = px.scatter(filtered_site_df, x='Payload Mass (kg)', 
        y='class', color='Booster Version Category', 
        title=f'Payload vs. Outcome for Site {selected_site}')
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()


""" 
Which site has the largest successful launches?
CCAFS-LC40 

Which site has the highest launch success rate?
 CCAFS -SLC 40
Which payload range(s) has the highest launch success rate?
3000 -4000 kgs 7/10 
0-5300kgs better than 5000-10000
Which payload range(s) has the lowest launch success rate?
0-2000 
5300 -10000
Which F9 Booster version (v1.0, v1.1, FT, B4, B5, etc.) has the highest
launch success rate?
B5 - 100%
Followed by FT 
then B4
"""
