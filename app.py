import dash
from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import plotly.express as px
from dash import dash_table
import dash_bootstrap_components as dbc

df = pd.read_csv("./climatedashdata.csv")
df = df.drop(columns = "Unnamed: 0")
df = df.sort_values(by = "date")

df_avg = df.drop(columns= ["date", "alpha-3", "region"])


ani_map = px.choropleth(df,  
                         locations = "alpha-3", 
                         projection = "mercator",
                         animation_frame="date",
                         scope = "europe", 
                         color = "avg_temp",
                        range_color=(-30, 45),
                        width=1000, height=1080, 
                        center =dict(lon=52.21,lat=9.55),
                        fitbounds="locations")

ani_map.update_geos(fitbounds="locations", visible=True)

ani_map = ani_map.update_layout(
        plot_bgcolor="#222222", paper_bgcolor="#222222", font_color="white", geo_bgcolor="#222222")

data_map = dcc.Graph(figure=ani_map)


app =dash.Dash(external_stylesheets=[dbc.themes.DARKLY])

server = app.server

# set app layout

app.layout = html.Div([html.H1('My First Spicy Dash', style={'textAlign': 'center', 'color': 'coral'}), 
                       html.H2('Welcome', style ={'paddingLeft': '30px'}),
                       html.H3('These are the Graphs'),
                       #html.Div(dash_table),
                       html.Div([
                           html.Div('Germany',
                                    style={'backgroundColor': 'coral', 'color': 'white','width': '900px', 'marginLeft': 'auto', 'marginRight': 'auto'}),
                                 data_map])
                      ])



if __name__ == '__main__':
     app.run_server()