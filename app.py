import dash
from dash import Dash, html, dcc, dash_table, callback
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc


df = pd.read_csv("./climatedashmonthly.csv")
df = df.sort_values(by = "yearmonth")

df_t = pd.DataFrame(df["country"].unique(), df["alpha-3"].unique())
df_t = df_t.reset_index()
df_t.columns = ["Alpha-3 ISO Code", "Country"]
df_t.sort_values(by="Country", inplace=True)

ani_map = px.choropleth(df,  
                         locations = "alpha-3", 
                         projection = "hammer",
                         animation_frame="yearmonth",
                         scope = "europe", 
                         color = "avg_temp",
                        range_color=(-30, 45),
                        width=900, height=700, 
                        fitbounds="locations")


ani_map.update_geos(fitbounds="locations", visible=True)

ani_map = ani_map.update_layout(
        #margin=dict(l=200, r=200, t=10, b=100),
        plot_bgcolor="#222222", paper_bgcolor="#222222", font_color="white", geo_bgcolor="#222222")

data_map = dcc.Graph(figure=ani_map)

temp_table = dash_table.DataTable(df.to_dict('records'),
                                  [{"name": i, "id": i} for i in df.columns], page_size=10,
                               style_data={'color': 'white','backgroundColor': 'black'},
                                  id="temperature_table",
                              style_header={
                                  'backgroundColor': 'rgb(210, 210, 210)',
                                  'color': 'black','fontWeight': 'bold'
    })


d_table = dash_table.DataTable(df_t.to_dict('records'),
                                  [{"name": i, "id": i} for i in df_t.columns],
                               page_size=10,
                               style_data={'color': 'white','backgroundColor': 'black'},
                              style_header={
                                  'backgroundColor': 'rgb(210, 210, 210)',
                                  'color': 'black','fontWeight': 'bold'
    })


linegraph = px.line(df, x='yearmonth', y='avg_temp', color="country", height=500, title="Average Temperatures in Europe", markers=True)
linegraph = linegraph.update_layout(
        legend=dict(orientation="h"),
        yaxis_range=[-15,38],
        plot_bgcolor="#222222", paper_bgcolor="#222222", font_color="white"
    )
linegraph = dcc.Graph(figure=linegraph)

app =dash.Dash(external_stylesheets=[dbc.themes.DARKLY])

#dropdowns:
server = app.server

dropdown_fulltable = dcc.Dropdown(df["country"], df["country"],  clearable=False)#,multi=True)

dropdown_iso =       dcc.Dropdown(df_t["Country"], [], clearable=False, multi=True)

isocountries =df_t['Country'].unique().tolist() 

# set app layout

app.layout = html.Div([
                        html.H1('Welcome to the superduperfuture Dashboard', style={'textAlign': 'center', 'color': 'coral'}), 
                        html.H2('European Countries Temperature Data', style ={'textAlign': 'center','font-weight': 'bold'}),
    
                        html.Div('Temperature Overview of Countries within the Timeframe', 
                                    style={'backgroundColor': 'coral', 'color': 'white','width': '900px', 'marginLeft': 'auto', 'marginRight': 'auto'}),
                        html.Div(temp_table, style={'backgroundColor': 'coral', 'color': 'white','width': '900px', 'marginLeft': 'auto', 'marginRight': 'auto'}),
                        
                        html.Br(),html.Br(),html.Br(),
    
                        html.Div('Temperature Datamap for Countries in Europe', 
                                    style={'backgroundColor': 'coral', 'color': 'white','width': '900px', 'marginLeft': 'auto', 'marginRight': 'auto'}),
                        #html.Div(data_map, style={'marginLeft': 'auto', 'marginRight': 'auto'}),
                        html.Div(data_map, style={'display':'flex', 'justify-content':'center'}),
    
                        html.Br(),html.Br(),html.Br(),
    
                        html.Div('Line Plots for Temperature Data in Europe', 
                                    style={'backgroundColor': 'coral', 'color': 'white','width': '900px', 'marginLeft': 'auto', 'marginRight': 'auto'}),
                        html.Br(),
                        html.Div("Filter by country:", style={'backgroundColor': '#222222', 'color': 'white','width': '300px', 'marginLeft': 'auto', 'marginRight':'auto'}),
                        html.Div(dropdown_fulltable, style={'backgroundColor': '#222222', 'color': 'red','width': '300px', 'marginLeft': 'auto', 'marginRight':'auto'}),
                        html.Div(linegraph, style={'marginLeft': 'auto', 'marginRight': 'auto'}),

                        html.Br(),html.Br(),html.Br(),
    
                        html.Div('ISO-Code Filter for Countries', 
                                    style={'backgroundColor': 'coral', 'color': 'white','width': '900px', 'marginLeft': 'auto', 'marginRight': 'auto'}),
                        html.Br(),
                        html.Div("Filter by country:", style={'backgroundColor': '#222222', 'color': 'white','width': '300px', 'marginLeft': 'auto', 'marginRight': 'auto'}),
                        html.Div(dropdown_iso, style={'backgroundColor': '#222222', 'color': 'red','width': '300px', 'marginLeft': 'auto', 'marginRight': 'auto'}),
                        html.Div(d_table, style={'title':'ISO-Code Table','width': '900px','marginLeft': 'auto', 'marginRight':'auto'}),
                        html.Br(),html.Br(),html.Br(),html.Br(),html.Br(),html.Br(),
                      ])

@callback(
    Output(temp_table, "data"),
    Output(linegraph, "figure"), 
    Input(dropdown_fulltable, "value"))




def update_line_graph(country): 
    mask = df["country"] == country # coming from the function parameter
    
    linegraph =px.line(df[mask], 
             x='yearmonth', 
             y='avg_temp',  
             color='country',
             #barmode='group',
             height=500, title = f"Average Temperatures for {country}",)
    linegraph = linegraph.update_layout(
        yaxis_range=[-15,38],
        legend=dict(orientation="h"),
        plot_bgcolor="#222222", paper_bgcolor="#222222", font_color="white"
   )    
    filtered_table = df[mask].to_dict('records')
    return filtered_table, linegraph


@callback(
    Output(d_table, "data"), 
    Input(dropdown_iso, "value"))

def update_iso_table(isocountries):
    mask2 = df_t["Country"].isin(isocountries)
    f_d_table = df_t[mask2].to_dict('records')
    return f_d_table



if __name__ == '__main__':
     app.run_server()
    


