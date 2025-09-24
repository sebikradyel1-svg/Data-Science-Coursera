# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
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
                                               {'label': 'All Sites', 'value': 'ALL'}
                                           ] + [{'label': site, 'value': site} for site in spacex_df['Launch Site'].unique()],
                                           value='ALL',
                                           placeholder="Select a Launch Site here",
                                           searchable=True
                                           ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                              min=0, max=10000, step=1000,
                                              marks={0: '0',
                                                     100: '100',
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
                                              value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        # Return the outcomes piechart for all sites
        # Use all rows in the spacex_df dataframe to render and return a pie chart graph 
        # to show the total success launches (i.e., the total count of class column)
        fig = px.pie(spacex_df, values='class', 
                     names='Launch Site', 
                     title='Total Success Launches By Site')
        return fig
    else:
        # Return the outcomes piechart for a selected site
        # Filter the dataframe spacex_df first to include only data for the selected site
        # Then render a pie chart to show success (class=1) count and failed (class=0) count
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        success_counts = filtered_df['class'].value_counts().reset_index()
        success_counts.columns = ['class', 'count']
        success_counts['outcome'] = success_counts['class'].map({1: 'Success', 0: 'Failure'})
        
        fig = px.pie(success_counts, values='count', 
                     names='outcome', 
                     title=f'Total Success Launches for site {entered_site}')
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
               Input(component_id='payload-slider', component_property='value')])
def get_scatter_chart(entered_site, payload_range):
    # Filter data based on payload range first
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= payload_range[0]) &
                           (spacex_df['Payload Mass (kg)'] <= payload_range[1])]
    
    if entered_site == 'ALL':
        # Render scatter plot for all sites
        # Display all values for Payload Mass (kg) and class, color-coded by Booster Version Category
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class',
                        color='Booster Version Category',
                        title='Correlation between Payload and Success for all Sites')
        return fig
    else:
        # Render scatter plot for selected site
        # Filter by site and render scatter plot showing Payload Mass (kg) vs class
        # Color-label points using Booster Version Category
        site_filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        fig = px.scatter(site_filtered_df, x='Payload Mass (kg)', y='class',
                        color='Booster Version Category',
                        title=f'Correlation between Payload and Success for site {entered_site}')
        return fig

# Run the app
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8050)