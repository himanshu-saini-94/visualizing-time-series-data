# -*- coding: utf-8 -*-
'''
@author: Sapteru
'''
#importing all required libraries
import pandas as pd
import webbrowser
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import plotly.express as px
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

app = dash.Dash(__name__)

def load_data():
    dataset = 'global_terror.csv'
    global df
    df = pd.read_csv(dataset)
    
    global month_list
    month={'January':1,'February':2,'March':3,'April':4,'May':5,'June':6,'July':7,
           'August':8,'September':9,'October':10,'November':11,'December':12}
    month_list=[{'label':key,'value':values} for key,values in month.items()]
    
    global date_list
    date_list=[x for x in range(1,32)]
    
    global region_list
    region_list=[{'label':str(i),'value':str(i)} for i in sorted(df['region_txt'].unique().tolist())]
    
    global country_list
    country_list= df.groupby('region_txt')['country_txt'].unique().apply(list).to_dict()
    
    global  state_list
    state_list= df.groupby('country_txt')['provstate'].unique().apply(list).to_dict()
    
    global city_list
    city_list= df.groupby('provstate')['city'].unique().apply(list).to_dict()
    
    global attack_type_list
    attack_type_list=[{'label':str(i),'value':str(i)} for i in df['attacktype1_txt'].unique().tolist()]
    
    global year_list
    year_list= sorted(df['iyear'].unique().tolist())
    
    global year_dict
    year_dict={str(year):str(year) for year in year_list}
    
    global chart_dd_values
    chart_dd={'Terrorist Organisation':'gname','Target Nationality':'natlty1_txt','Target Type':'targtype1_txt',
                     'Type of Attack':'attacktype1_txt','Weapon Type':'weaptype1_txt','Region':'region_txt','Country Attacked':'country_txt'}
    
    chart_dd_values=[{'label':keys,'value':value} for keys,value in chart_dd.items()]

def app_dashboard_ui():
    main_output = html.Div([
        html.H1(children='Terrorism Analysis with Insights', id='main-tt', style={'textAlign':'center','font-family':'Arial, Helvetica, sans-serif'}),
        html.Br(),
        
        
        dcc.Tabs(id='tabs', value='Map',style={'font-family':'Arial, Helvetica, sans-serif'}, children=[
            dcc.Tab(label='Map Tool', id='map_tool', value='Map', children=[
                dcc.Tabs(id='subtabs1', value='WorldMap',style={'font-family':'Arial, Helvetica, sans-serif'}, children=[
                    dcc.Tab(label='World Map Tool', id='WorldM',style={'font-family':'Arial, Helvetica, sans-serif'}, value='WorldMap'),
                    dcc.Tab(label='India Map Tool', id='IndiaM',style={'font-family':'Arial, Helvetica, sans-serif'}, value='IndiaMap')
                    ]),
                html.Br(),
                
                
                dcc.Dropdown(id='month_dd', options=month_list,style={'font-family':'Arial, Helvetica, sans-serif'}, placeholder='Select Month', multi=True),
                dcc.Dropdown(id='date_dd', placeholder='Select Day',style={'font-family':'Arial, Helvetica, sans-serif'}, multi=True),
                dcc.Dropdown(id='region_dd', options=region_list,style={'font-family':'Arial, Helvetica, sans-serif'}, placeholder='Select Region', multi=True),
                dcc.Dropdown(id='country_dd', placeholder='Select Country',style={'font-family':'Arial, Helvetica, sans-serif'}, multi=True),
                dcc.Dropdown(id='state_dd', placeholder='Select State or Province',style={'font-family':'Arial, Helvetica, sans-serif'}, multi=True),
                dcc.Dropdown(id='city_dd',placeholder='Select City',style={'font-family':'Arial, Helvetica, sans-serif'}, multi=True),
                dcc.Dropdown(id='attacktype_dd', options=attack_type_list, placeholder='Select Attack Type',style={'font-family':'Arial, Helvetica, sans-serif'}, multi=True),
                html.H3('Select the year', id='year_tt',style={'font-family':'Arial, Helvetica, sans-serif'},),
                
                
                dcc.RangeSlider(id='year_sl', min=min(year_list), max=max(year_list), value=[min(year_list),max(year_list)], marks=year_dict, step=None),
                html.Br()
                ]),
            
            
            dcc.Tab(label = 'Chart Tool', id='chart_tool', value='Chart', children=[
                dcc.Tabs(id='subtabs2', value='WorldChart',style={'font-family':'Arial, Helvetica, sans-serif'}, children=[
                    dcc.Tab(label='World Chart Tool', id='WorldC',style={'font-family':'Arial, Helvetica, sans-serif'}, value='WorldChart'),
                    dcc.Tab(label='India Chart Tool', id='IndiaC',style={'font-family':'Arial, Helvetica, sans-serif'}, value="IndiaChart")
                    ]),
                html.Br(),
                
                
                dcc.Dropdown(id='chart_dd', options=chart_dd_values, placeholder='Select Option', value='region_txt'),
                html.Br(),
                html.Hr(),
                
                
                dcc.Input(id='search', placeholder='Search Filter',style={'font-family':'Arial, Helvetica, sans-serif'},),
                html.Hr(),
                html.H3('Select the year', id='c_year_tt',style={'font-family':'Arial, Helvetica, sans-serif'},),
                
                
                dcc.RangeSlider(id='c_year_sl',min=min(year_list), max=max(year_list), value=[min(year_list),max(year_list)],marks=year_dict, step=None),
                html.Br()
                ])
            ]),
        
        
        html.Div(id = 'result_object', children ='Output is loading...',style={'font-family':'Arial, Helvetica, sans-serif'},)], className = 'custom')
    
    return main_output

@app.callback(Output("date_dd", "options"),Input("month_dd", "value"))
def date_check(month):
    option = []
    if month:
        option= [{"label":m, "value":m} for m in date_list]
    return option

@app.callback([Output('region_dd','value'),Output('region_dd','disabled'),
               Output('country_dd','value'),Output('country_dd','disabled')],
              Input('subtabs1','value'))
def tabs_check(tab):
    region=None
    temp_dr= False
    country=None
    temp_cr=False
    if tab == 'WorldMap':
        pass
    elif tab == 'IndiaMap':
        region=['South Asia']
        temp_dr=True
        country=['India']
        temp_cr=True
    return region,temp_dr,country,temp_cr

@app.callback(Output('country_dd','options'),Input('region_dd','value'))
def country_check(region):
    option=[]
    if region is None:
        pass
    else:
        for i in region:
            if i in country_list.keys():
                option.extend(country_list[i])
    return [{'label':country,'value':country} for country in option]

@app.callback(Output('state_dd','options'),Input('country_dd','value'))
def state_check(country):
    option=[]
    if country is None:
        pass
    else:
        for i in country:
            if i in state_list.keys():
                option.extend(state_list[i])
    return [{'label':state,'value':state} for state in option]

@app.callback(Output('city_dd','options'),Input('state_dd','value'))
def city_check(state):
    option=[]
    if state is None:
        pass
    else:
        for i in state:
            if i in city_list.keys():
                option.extend(city_list[i])
    return [{'label':city,'value':city} for city in option]

@app.callback(Output('result_object','children'),[Input('tabs','value'),Input('month_dd','value'),
               Input('date_dd','value'),Input('region_dd','value'),Input('country_dd','value'),
               Input('state_dd','value'),Input('city_dd','value'),Input('attacktype_dd','value'),
               Input('year_sl','value'),Input('c_year_sl','value'),Input('chart_dd','value'),
               Input('search','value'),Input('subtabs2','value')])
def update_app_ui(tabs,month,date,region,country,state,city,attack,year,year_c,chart_dd,search,child_tab):
    fig = None
    
    if tabs == 'Map':
        print('Data type and data of Month = \n' + str(type(month)))
        print(month)
        print('Data type and data of Region = \n' + str(type(region)))
        print(region)       
        print('Data type and data of Attacktype = \n' + str(type(attack)))
        print(attack)        
      
        year_range = range(year[0], year[1]+1)
        dff = df[df['iyear'].isin(year_range)]
        
        if month==[] or month is None:
            pass
        else:
            if date==[] or date is None:
                dff = dff[dff['imonth'].isin(month)]
            else:
                dff = dff[dff['imonth'].isin(month)
                                & (dff['iday'].isin(date))]

        if region==[] or region is None:
            pass
        else:
            if country==[] or country is None :
                dff = dff[dff['region_txt'].isin(region)]
            else:
                if state == [] or state is None:
                    dff = dff[(dff['region_txt'].isin(region))&(dff['country_txt'].isin(country))]
                else:
                    if city == [] or city is None:
                        dff = dff[(dff['region_txt'].isin(region))&(dff['country_txt'].isin(country)) &(dff['provstate'].isin(state))]
                    else:
                        dff = dff[(dff['region_txt'].isin(region))&(dff['country_txt'].isin(country)) &(dff['provstate'].isin(state))&(dff['city'].isin(city))]
                        
        if attack==[] or attack is None:
            pass
        else:
            dff = dff[dff['attacktype1_txt'].isin(attack)] 

        mapFigure = go.Figure()
        if dff.shape[0]:
            pass
        else: 
            dff = pd.DataFrame(columns = ['iyear', 'imonth', 'iday', 'country_txt', 'region_txt', 'provstate',
               'city', 'latitude', 'longitude', 'attacktype1_txt', 'nkill'])
            
            dff.loc[0] = [0, 0 ,0, None, None, None, None, None, None, None, None]
            
        
        mapFigure = px.scatter_mapbox(dff,lat='latitude', lon='longitude',color='attacktype1_txt',hover_name='city', hover_data=['region_txt', 'country_txt', 'provstate','city', 'attacktype1_txt','nkill','iyear','imonth', 'iday'],zoom=1)                       
        mapFigure.update_layout(mapbox_style='open-street-map',autosize=True,margin=dict(l=0, r=0, t=25, b=20),)
          
        fig = mapFigure

    elif tabs=='Chart':
        fig = None
        
        year_range_c = range(year_c[0], year_c[1]+1)
        chart_df = df[df['iyear'].isin(year_range_c)]
        
        if child_tab == 'WorldChart':
            pass
        elif child_tab == 'IndiaChart':
            chart_df = chart_df[(chart_df['region_txt']=='South Asia') &(chart_df['country_txt']=='India')]
        if chart_dd is not None and chart_df.shape[0]:
            if search is not None:
                chart_df = chart_df.groupby('iyear')[chart_dd].value_counts().reset_index(name = 'count')
                chart_df  = chart_df[chart_df[chart_dd].str.contains(search, case=False)]
            else:
                chart_df = chart_df.groupby('iyear')[chart_dd].value_counts().reset_index(name='count')

        if chart_df.shape[0]:
            pass
        else: 
            chart_df = pd.DataFrame(columns = ['iyear', 'count', chart_dd])
            
            chart_df.loc[0] = [0, 0,'No data']
        
        fig = px.area(chart_df, x='iyear', y ='count', color = chart_dd)

    return dcc.Graph(figure = fig)
                   
def main():
    load_data()
    
    global app
    app.layout = app_dashboard_ui()
    app.title = 'Terrorism Analysis with Insights'
    app.run_server()

if __name__ == '__main__':
    main()