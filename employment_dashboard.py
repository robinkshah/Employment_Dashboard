
!pip install dash pyngrok pandas plotly

#LINK TO LIVE SERVER:

import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd

################################################################################################################### Data Processing
cleaned_df = pd.read_csv('cleaned_data.csv')

cleaned_df = cleaned_df[~cleaned_df['Occupation'].str.startswith("Total")]
#major NOC
cleaned_df['NOC_Major'] = cleaned_df['Occupation'].str.extract(r'^(\d)').dropna()
cleaned_df['NOC_Major'] = cleaned_df['NOC_Major'].astype(str)
noc_titles = {
    '3': 'Health Occupations',
    '4': 'Education, Law, Social & Government Services',
    '7': 'Trades, Transport & Equipment Operators'
}

# Province population
province_population = {
    'Alberta': 3375130,
    'British Columbia': 4200425,
    'Manitoba': 1058410,
    'New Brunswick': 648250,
    'Newfoundland and Labrador': 433955,
    'Nova Scotia': 819315,
    'Ontario': 11782825,
    'Prince Edward Island': 126900,
    'Quebec': 6918730,
    'Saskatchewan': 882760,
    'Northwest Territories': 31915,
    'Yukon': 32775,
    'Nunavut': 24540,
    'Canada': 30335920
}

################################################################################################################### Initialise
app = dash.Dash(__name__)
server = app.server

provinces = sorted(cleaned_df['Province'].unique())
noc_categories = ['3', '4', '7']

app.layout = html.Div([
    html.H1("2023 Canadian Census - Employment Dashboard"),

################################################################################################################### Bar Chart: Essential Worker Distribution
    html.Div([
        html.H3("Essential Worker Distribution by Province"),
        html.P(
    "This bar chart visualizes the distribution of essential service workers across all Canadian provinces and territories. "
    "It focuses on three key occupational categories defined by the National Occupational Classification (NOC): NOC 3 (Health Occupations), NOC 4 (Education, Law, Social, Community and Government Services), and NOC 7 (Trades, Transport, and Equipment Operators)."
    "These occupations are critical to the functioning of society and public infrastructure. You may notice that larger provinces like Ontario, Quebec, and British Columbia consistently have higher numbers across all essential categories. "
    "However, when normalized by population, smaller provinces or territories may be under-resourced. "
    "Use the toggle above the chart to switch between categories and assess whether essential services are evenly distributed or whether certain regions may be under-resourced. "
    ),

        html.Div([
            html.Label("Display Mode:", style={'fontWeight': 'bold', 'marginRight': '10px'}),
            dcc.RadioItems(
                id='display-mode',
                options=[
                    {'label': 'Total Count', 'value': 'total'},
                    {'label': 'Per 1,000 Residents', 'value': 'normalized'}
                ],
                value='normalized',
                labelStyle={'display': 'inline-block', 'marginRight': '20px'}
            )
        ], style={'marginBottom': '15px'}),
        html.Label("Category Selection:", style={'fontWeight': 'bold', 'marginRight': '10px'}),
        dcc.RadioItems(
            id='essential-noc-selector',
            options=[{'label': f'NOC {n}', 'value': n} for n in noc_categories],
            value='3',
            labelStyle={'display': 'inline-block', 'marginRight': '10px'}
        ),
        dcc.Graph(id='essential-bar-chart')
    ]),
################################################################################################################### Butterfly Chart: Gender Distribution
    html.Div([
        html.H3("Gender Distribution by Occupation in Province"),
        html.P(
    "The butterfly chart offers a comparative view of male and female employment levels across various occupational groups within a selected province or territory. "
    "Each occupation is shown along the vertical axis, while the horizontal bars extend left for male employment and right for female employment. "
    "Health-related occupations may show higher female representation, while trades or engineering roles might skew male. "
    "Such patterns reflect broader societal trends and may help guide equity-based policy initiatives. "
    "If certain roles are heavily imbalanced, provinces may consider targeted recruitment or educational outreach."
    "This visualization helps identify gender imbalances in specific occupations, highlights trends in workforce participation, and can inform equity-driven hiring policies."
    "Use the dropdown menu to select a province or territory and explore its gender dynamics in employment."
    "You may also select each gender individually to see the distribution in occupations in each province."),

        dcc.Dropdown(
            id='province-dropdown',
            options=[{'label': p, 'value': p} for p in provinces],
            value='Ontario'
        ),
        html.Div([
            html.Label("Select Gender:", style={'fontWeight': 'bold', 'marginRight': '10px'}),
            dcc.RadioItems(
                id='gender-toggle',
                options=[
                    {'label': 'Both', 'value': 'both'},
                    {'label': 'Male Only', 'value': 'male'},
                    {'label': 'Female Only', 'value': 'female'}
                ],
                value='both',
                labelStyle={'display': 'inline-block', 'marginRight': '20px'}
            )
        ], style={'marginBottom': '20px'}),
        dcc.Graph(id='butterfly-chart')
    ]),
################################################################################################################### Horizontal Bar Chart: Manpower Threshold
    html.Div([
        html.H3("Occupations with Employment Above Threshold"),
        html.P(
    "This horizontal bar chart allows users to explore which occupations in each province or territory have a workforce size that meets or exceeds a user-defined threshold."
    "By adjusting the slider below the chart, decision-makers can filter the data to reveal only those occupations that have significant human resource availability. "
    "This feature is particularly useful for evaluating locations for new industrial projects, such as electric vehicle manufacturing plants, which require a minimum level of skilled labour (e.g., engineers, technicians, or tradespeople). "
    "If you're assessing potential locations for new industry—such as an electric vehicle factory, you'd look for high numbers in engineering, tech, or skilled trades. "
    "The chart updates in real time based on the selected threshold, helping users make data-driven location decisions."),

        dcc.Slider(
            id='manpower-threshold',
            min=0,
            max=10000000,
            step=1000000,
            value=10000,
            marks={i: str(i) for i in range(0, 10000000, 1000000)}
        ),
        dcc.Graph(id='manpower-bar-chart')
    ]),
################################################################################################################### Donut Chart: Occupational Composition
    html.Div([
        html.H3("National Occupational Composition"),
        html.P(
    "This donut chart provides a high-level overview of the occupational composition of Canada's workforce, or that of a specific province or territory. "
    "Each slice represents a major occupational group based on NOC codes, with the size corresponding to the proportion of total employment. "
    "This visualization helps policymakers and analysts understand which sectors dominate the labour market in a given region. "
    "Use the dropdown menu to toggle between a national view and province-specific views to compare how labour force composition varies regionally. "
    "Such insights can help whenthere is a need to align education and training initiatives with economic needs."),

        dcc.Dropdown(
            id='donut-province-dropdown',
            options=[{'label': 'All of Canada', 'value': 'Canada'}] + [{'label': p, 'value': p} for p in provinces],
            value='Canada'
        ),
        dcc.Graph(id='donut-chart')
    ])
])

################################################################################################################### Callback: Essential Worker Distribution
@app.callback(
    Output('essential-bar-chart', 'figure'),
    Input('essential-noc-selector', 'value'),
    Input('display-mode', 'value')
)
def update_essential_chart(noc_value, mode):
    df_filtered = cleaned_df[
        (cleaned_df['NOC_Major'] == noc_value) &
        (cleaned_df['Gender'] == 'Total')
    ]
    df_grouped = df_filtered.groupby('Province')['Employment'].sum().reset_index()

    # Add population column
    df_grouped['Population'] = df_grouped['Province'].map(province_population)

    if mode == 'normalized':
        df_grouped['Value'] = (df_grouped['Employment'] / df_grouped['Population']) * 1000
        y_title = 'Essential Workers per 1,000 Residents'
        chart_title = f'NOC {noc_value} Essential Workers (Normalized)'
    else:
        df_grouped['Value'] = df_grouped['Employment']
        y_title = 'Total Number of Essential Workers'
        chart_title = f'NOC {noc_value} Essential Workers (Raw Count)'

    fig = px.bar(df_grouped, x='Province', y='Value', title=chart_title)
    fig.update_layout(
        yaxis_title=y_title,
        xaxis_title='Province',
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(size=12),
        title_font_size=18,
        margin=dict(t=50, b=50)
    )
    return fig
################################################################################################################### Callback: Butterfly Chart: Gender Distribution
@app.callback(
    Output('butterfly-chart', 'figure'),
    Input('province-dropdown', 'value'),
    Input('gender-toggle', 'value')
)
def update_butterfly_chart(selected_province, selected_gender):
    df = cleaned_df[cleaned_df['Province'] == selected_province]

    if selected_gender == 'male':
        df_male = df[df['Gender'] == 'Male']
        df_male = df_male[['Occupation', 'Employment']].copy()
        df_male['Employment'] *= -1
        fig = px.bar(df_male, x='Employment', y='Occupation', orientation='h', title=f'Male Employment in {selected_province}')
    elif selected_gender == 'female':
        df_female = df[df['Gender'] == 'Female']
        fig = px.bar(df_female, x='Employment', y='Occupation', orientation='h', title=f'Female Employment in {selected_province}')
    else:
        df_total = df[df['Gender'] != 'Total']
        df_pivot = df_total.pivot_table(index='Occupation', columns='Gender', values='Employment').fillna(0)
        df_pivot['Male'] *= -1
        fig = px.bar(df_pivot, x='Male', y=df_pivot.index, orientation='h', title=f'Gender Distribution in {selected_province}')
        fig.add_bar(x=df_pivot['Female'], y=df_pivot.index, name='Female', orientation='h')

    fig.update_layout(
        barmode='relative',
        xaxis_title='Employment (Male Negative)' if selected_gender == 'both' else 'Number of Workers',
        yaxis_title='Occupation',
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(size=12),
        title_font_size=18,
        margin=dict(t=50, b=50)
    )

    return fig
################################################################################################################### Callback: Manpower Threshold
@app.callback(
    Output('manpower-bar-chart', 'figure'),
    Input('manpower-threshold', 'value')
)
def update_threshold_chart(threshold):
    df_total = cleaned_df[cleaned_df['Gender'] == 'Total']
    df_grouped = df_total.groupby('Occupation')['Employment'].sum().reset_index()
    df_filtered = df_grouped[df_grouped['Employment'] >= threshold]
    fig = px.bar(df_filtered.sort_values('Employment'),
                 x='Employment', y='Occupation', orientation='h',
                 title=f'Occupations with ≥ {threshold} Employees')
    return fig
################################################################################################################### Callback: Occupational Composition
@app.callback(
    Output('donut-chart', 'figure'),
    Input('donut-province-dropdown', 'value')
)
def update_donut_chart(selected):
    if selected == 'Canada':
        df = cleaned_df[cleaned_df['Province'] == 'Canada']
    else:
        df = cleaned_df[cleaned_df['Province'] == selected]
    df = df[df['Gender'] == 'Total']
    df_grouped = df.groupby('Occupation')['Employment'].sum().reset_index()
    fig = px.pie(df_grouped, values='Employment', names='Occupation',
                 title=f'Occupational Composition in {selected}', hole=0.4)
    return fig

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=8050)
