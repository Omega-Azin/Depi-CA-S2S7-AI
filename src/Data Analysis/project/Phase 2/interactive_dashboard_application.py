import dash
from dash import html, dcc, Input, Output
import plotly.express as px
import pandas as pd
import os

# 1. Dataset Verification & Loading
clean_csv = 'cleaned_fordgobike_tripdata.csv'
raw_csv = '201902-fordgobike-tripdata.csv'

if not os.path.exists(clean_csv):
    if os.path.exists(raw_csv):
        import preprocessing
        preprocessing.clean_and_engineer_data(raw_csv, clean_csv)
    else:
        raise FileNotFoundError("Dataset not found. Please ensure '201902-fordgobike-tripdata.csv' is present.")

df = pd.read_csv(clean_csv)
df['start_time'] = pd.to_datetime(df['start_time'])
df['start_date'] = pd.to_datetime(df['start_date']).dt.date

min_date = df['start_date'].min()
max_date = df['start_date'].max()

# 2. App Initialization
app = dash.Dash(__name__, title="Ford GoBike Analytics Dashboard")
server = app.server

# Style Constants
SIDEBAR_STYLE = {
    'width': '280px',
    'min-width': '280px',
    'background-color': '#ffffff',
    'padding': '24px 20px',
    'border-right': '1px solid #e2e8f0',
    'box-shadow': '0 4px 6px -1px rgba(0, 0, 0, 0.05)',
    'font-family': 'Inter, system-ui, -apple-system, sans-serif'
}

MAIN_STYLE = {
    'flex': '1',
    'padding': '26px 32px',
    'background-color': '#f8fafc',
    'font-family': 'Inter, system-ui, -apple-system, sans-serif',
    'overflow-y': 'auto'
}

CARD_STYLE = {
    'background': '#ffffff',
    'padding': '18px 22px',
    'border-radius': '12px',
    'box-shadow': '0 1px 3px rgba(0,0,0,0.06)',
    'border': '1px solid #edf2f7',
    'flex': '1',
    'margin': '0 8px'
}

# 3. Application Layout
app.layout = html.Div([
    # Top Navbar
    html.Div([
        html.Div([
            html.H2("🚴 Ford GoBike", style={'color': '#ffffff', 'margin': '0', 'font-size': '20px', 'font-weight': '700'}),
            html.Span("Trip Analytics Dashboard", style={'color': '#94a3b8', 'font-size': '13px', 'margin-left': '12px'})
        ], style={'display': 'flex', 'align-items': 'center'}),
        html.Div([
            html.Span("Data: Feb 01, 2019 – Feb 28, 2019", style={'color': '#cbd5e1', 'font-size': '12px', 'background': '#1e293b', 'padding': '6px 14px', 'border-radius': '20px'})
        ])
    ], style={'background-color': '#0f172a', 'padding': '14px 32px', 'display': 'flex', 'justify-content': 'space-between', 'align-items': 'center'}),

    # Main Body Grid
    html.Div([
        # Sidebar Controls
        html.Div([
            html.H3("Filters", style={'color': '#0f172a', 'font-size': '17px', 'font-weight': '700', 'margin-top': '0', 'margin-bottom': '4px'}),
            html.P("Every chart updates instantly.", style={'color': '#64748b', 'font-size': '12px', 'margin-bottom': '18px'}),

            html.Label("Date range", style={'font-size': '13px', 'font-weight': '600', 'color': '#334155'}),
            dcc.DatePickerRange(
                id='date-range-filter',
                min_date_allowed=min_date,
                max_date_allowed=max_date,
                start_date=min_date,
                end_date=max_date,
                display_format='YYYY-MM-DD',
                style={'width': '100%', 'margin-bottom': '16px'}
            ),

            html.Label("User type", style={'font-size': '13px', 'font-weight': '600', 'color': '#334155'}),
            dcc.Dropdown(
                id='user-type-filter',
                options=[{'label': ut, 'value': ut} for ut in sorted(df['user_type'].unique())],
                value=list(df['user_type'].unique()),
                multi=True,
                clearable=False,
                style={'margin-bottom': '16px', 'font-size': '13px'}
            ),

            html.Label("Gender", style={'font-size': '13px', 'font-weight': '600', 'color': '#334155'}),
            dcc.Dropdown(
                id='gender-filter',
                options=[{'label': g, 'value': g} for g in sorted(df['member_gender'].unique())],
                value=list(df['member_gender'].unique()),
                multi=True,
                clearable=False,
                style={'margin-bottom': '16px', 'font-size': '13px'}
            ),

            html.Label("Age group", style={'font-size': '13px', 'font-weight': '600', 'color': '#334155'}),
            dcc.Checklist(
                id='age-group-filter',
                options=[
                    {'label': ' Young (< 25)', 'value': 'Young'},
                    {'label': ' Adult (25 - 45)', 'value': 'Adult'},
                    {'label': ' Senior (> 45)', 'value': 'Senior'}
                ],
                value=['Young', 'Adult', 'Senior'],
                labelStyle={'display': 'block', 'margin-bottom': '6px', 'color': '#475569', 'font-size': '13px'},
                style={'margin-bottom': '18px'}
            ),

            html.Label("Trip duration (minutes)", style={'font-size': '13px', 'font-weight': '600', 'color': '#334155'}),
            dcc.RangeSlider(
                id='duration-slider',
                min=1,
                max=80,
                step=1,
                value=[1, 80],
                marks={1: '1m', 20: '20m', 40: '40m', 60: '60m', 80: '80m+'},
                tooltip={"placement": "bottom", "always_visible": False}
            ),

            html.Div([
                html.Span("💡 Tip: ", style={'font-weight': 'bold', 'color': '#0284c7'}),
                html.Span("Combine the age, gender, and duration filters to spot niche riding patterns.", style={'color': '#0369a1', 'font-size': '11px'})
            ], style={'background': '#f0f9ff', 'border': '1px solid #bae6fd', 'border-radius': '8px', 'padding': '12px', 'margin-top': '25px'})
        ], style=SIDEBAR_STYLE),

        # Content Area
        html.Div([
            # Section 1: Overview KPIs
            html.Div([
                html.Div([
                    html.H2(id='kpi-total-trips', style={'color': '#0f172a', 'margin': '0', 'font-size': '26px', 'font-weight': '800'}),
                    html.P("Total trips", style={'color': '#64748b', 'margin': '4px 0 0 0', 'font-weight': '600', 'font-size': '13px'}),
                    html.Span(id='kpi-trips-subtext', style={'color': '#059669', 'font-size': '11px', 'font-weight': '500'})
                ], style=CARD_STYLE),

                html.Div([
                    html.H2(id='kpi-avg-duration', style={'color': '#0f172a', 'margin': '0', 'font-size': '26px', 'font-weight': '800'}),
                    html.P("Avg. duration", style={'color': '#64748b', 'margin': '4px 0 0 0', 'font-weight': '600', 'font-size': '13px'}),
                    html.Span("across selected trips", style={'color': '#0284c7', 'font-size': '11px', 'font-weight': '500'})
                ], style=CARD_STYLE),

                html.Div([
                    html.H2(id='kpi-active-riders', style={'color': '#0f172a', 'margin': '0', 'font-size': '26px', 'font-weight': '800'}),
                    html.P("Active riders", style={'color': '#64748b', 'margin': '4px 0 0 0', 'font-weight': '600', 'font-size': '13px'}),
                    html.Span("unique riders in view", style={'color': '#d97706', 'font-size': '11px', 'font-weight': '500'})
                ], style=CARD_STYLE),

                html.Div([
                    html.H2(id='kpi-top-station', style={'color': '#0f172a', 'margin': '0', 'font-size': '16px', 'font-weight': '700', 'white-space': 'nowrap', 'overflow': 'hidden', 'text-overflow': 'ellipsis'}),
                    html.P("Most popular station", style={'color': '#64748b', 'margin': '4px 0 0 0', 'font-weight': '600', 'font-size': '13px'}),
                    html.Span("most frequent trip start", style={'color': '#dc2626', 'font-size': '11px', 'font-weight': '500'})
                ], style=CARD_STYLE)
            ], style={'display': 'flex', 'justify-content': 'space-between', 'margin-bottom': '24px'}),

            # Section 2: Time Analysis
            html.Div([
                html.H4("Time Analysis", style={'color': '#1e293b', 'font-size': '15px', 'font-weight': '700', 'margin-bottom': '10px'}),
                html.Div([
                    html.Div([
                        dcc.Graph(id='graph-trips-weekday', config={'displayModeBar': False})
                    ], style={'width': '58%', 'background': '#ffffff', 'padding': '14px', 'border-radius': '12px', 'box-shadow': '0 1px 3px rgba(0,0,0,0.06)', 'margin-right': '14px'}),
                    html.Div([
                        dcc.Graph(id='graph-trips-hourly', config={'displayModeBar': False})
                    ], style={'width': '42%', 'background': '#ffffff', 'padding': '14px', 'border-radius': '12px', 'box-shadow': '0 1px 3px rgba(0,0,0,0.06)'})
                ], style={'display': 'flex', 'margin-bottom': '22px'})
            ]),

            # Section 3: User Analysis
            html.Div([
                html.H4("User Analysis", style={'color': '#1e293b', 'font-size': '15px', 'font-weight': '700', 'margin-bottom': '10px'}),
                html.Div([
                    html.Div([
                        dcc.Graph(id='graph-user-type', config={'displayModeBar': False})
                    ], style={'width': '34%', 'background': '#ffffff', 'padding': '14px', 'border-radius': '12px', 'box-shadow': '0 1px 3px rgba(0,0,0,0.06)', 'margin-right': '14px'}),
                    html.Div([
                        dcc.Graph(id='graph-gender-dist', config={'displayModeBar': False})
                    ], style={'width': '34%', 'background': '#ffffff', 'padding': '14px', 'border-radius': '12px', 'box-shadow': '0 1px 3px rgba(0,0,0,0.06)', 'margin-right': '14px'}),
                    html.Div([
                        dcc.Graph(id='graph-age-dist', config={'displayModeBar': False})
                    ], style={'width': '32%', 'background': '#ffffff', 'padding': '14px', 'border-radius': '12px', 'box-shadow': '0 1px 3px rgba(0,0,0,0.06)'})
                ], style={'display': 'flex', 'margin-bottom': '22px'})
            ]),

            # Section 4: Station & Trip Analysis
            html.Div([
                html.H4("Station & Trip Analysis", style={'color': '#1e293b', 'font-size': '15px', 'font-weight': '700', 'margin-bottom': '10px'}),
                html.Div([
                    html.Div([
                        dcc.Graph(id='graph-top-stations', config={'displayModeBar': False})
                    ], style={'width': '50%', 'background': '#ffffff', 'padding': '14px', 'border-radius': '12px', 'box-shadow': '0 1px 3px rgba(0,0,0,0.06)', 'margin-right': '14px'}),
                    html.Div([
                        dcc.Graph(id='graph-top-routes', config={'displayModeBar': False})
                    ], style={'width': '50%', 'background': '#ffffff', 'padding': '14px', 'border-radius': '12px', 'box-shadow': '0 1px 3px rgba(0,0,0,0.06)'})
                ], style={'display': 'flex'})
            ])
        ], style=MAIN_STYLE)
    ], style={'display': 'flex', 'min-height': 'calc(100vh - 60px)'})
])

# 4. Interactive Callbacks
@app.callback(
    [
        Output('kpi-total-trips', 'children'),
        Output('kpi-trips-subtext', 'children'),
        Output('kpi-avg-duration', 'children'),
        Output('kpi-active-riders', 'children'),
        Output('kpi-top-station', 'children'),
        Output('graph-trips-weekday', 'figure'),
        Output('graph-trips-hourly', 'figure'),
        Output('graph-user-type', 'figure'),
        Output('graph-gender-dist', 'figure'),
        Output('graph-age-dist', 'figure'),
        Output('graph-top-stations', 'figure'),
        Output('graph-top-routes', 'figure')
    ],
    [
        Input('date-range-filter', 'start_date'),
        Input('date-range-filter', 'end_date'),
        Input('user-type-filter', 'value'),
        Input('gender-filter', 'value'),
        Input('age-group-filter', 'value'),
        Input('duration-slider', 'value')
    ]
)
def update_dashboard(start_date, end_date, user_types, genders, age_groups, duration_range):
    if not user_types or not genders or not age_groups:
        empty = px.bar(title="No matching records")
        return "0", "0% of all trips", "0 min", "0", "N/A", empty, empty, empty, empty, empty, empty, empty

    f_df = df[
        (df['start_date'] >= pd.to_datetime(start_date).date()) &
        (df['start_date'] <= pd.to_datetime(end_date).date()) &
        (df['user_type'].isin(user_types)) &
        (df['member_gender'].isin(genders)) &
        (df['age_group'].isin(age_groups)) &
        (df['duration_min'] >= duration_range[0]) &
        (df['duration_min'] <= duration_range[1])
    ]

    total_all = len(df)
    total_filtered = len(f_df)
    pct = (total_filtered / total_all * 100) if total_all > 0 else 0
    kpi_trips = f"{total_filtered:,}"
    kpi_subtext = f"{pct:.1f}% of all {total_all:,} trips"

    avg_dur = f"{f_df['duration_min'].mean():.1f} min" if total_filtered > 0 else "0.0 min"
    active_users = f"{f_df['bike_id'].nunique():,}" if total_filtered > 0 else "0"
    top_stat = f_df['start_station_name'].mode()[0] if total_filtered > 0 else "N/A"

    # Chart 1: Trips per day of week
    order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    wk_counts = f_df['day_of_week'].value_counts().reindex(order).fillna(0).reset_index()
    wk_counts.columns = ['Day', 'Trips']
    fig_weekday = px.line(wk_counts, x='Day', y='Trips', title="Trips per day of week", markers=True)
    fig_weekday.update_traces(line=dict(color='#0284c7', width=3), marker=dict(size=7, color='#0369a1'))
    fig_weekday.update_layout(plot_bgcolor='#ffffff', paper_bgcolor='#ffffff', height=240, margin=dict(t=35, b=20, l=30, r=20))

    # Chart 2: Hourly rides
    hr_counts = f_df['hour'].value_counts().sort_index().reset_index()
    hr_counts.columns = ['Hour', 'Trips']
    fig_hourly = px.bar(hr_counts, x='Hour', y='Trips', title="Trips by hour of day (Peak hours)")
    fig_hourly.update_traces(marker_color='#0d9488')
    fig_hourly.update_layout(plot_bgcolor='#ffffff', paper_bgcolor='#ffffff', height=240, margin=dict(t=35, b=20, l=30, r=20))

    # Chart 3: User type donut
    u_counts = f_df['user_type'].value_counts().reset_index()
    u_counts.columns = ['Type', 'Count']
    fig_user = px.pie(u_counts, names='Type', values='Count', hole=0.6, title="Subscriber vs Customer",
                      color_discrete_sequence=['#0284c7', '#f97316'])
    fig_user.update_layout(height=240, margin=dict(t=35, b=20, l=20, r=20))

    # Chart 4: Gender breakdown
    g_counts = f_df['member_gender'].value_counts().reset_index()
    g_counts.columns = ['Gender', 'Count']
    fig_gender = px.bar(g_counts, x='Gender', y='Count', title="Trips by Gender", color='Gender',
                        color_discrete_sequence=['#3b82f6', '#ec4899', '#8b5cf6'])
    fig_gender.update_layout(plot_bgcolor='#ffffff', paper_bgcolor='#ffffff', height=240, showlegend=False, margin=dict(t=35, b=20, l=30, r=20))

    # Chart 5: Age group breakdown
    ag_counts = f_df['age_group'].value_counts().reset_index()
    ag_counts.columns = ['Age Group', 'Count']
    fig_age = px.bar(ag_counts, x='Age Group', y='Count', title="Age Groups", color_discrete_sequence=['#6366f1'])
    fig_age.update_layout(plot_bgcolor='#ffffff', paper_bgcolor='#ffffff', height=240, margin=dict(t=35, b=20, l=30, r=20))

    # Chart 6: Top Departure Stations
    top_st = f_df['start_station_name'].value_counts().head(8).reset_index()
    top_st.columns = ['Station', 'Trips']
    top_st = top_st.sort_values(by='Trips', ascending=True)
    fig_top_st = px.bar(top_st, y='Station', x='Trips', orientation='h', title="Top 8 Departure Stations")
    fig_top_st.update_traces(marker_color='#3b82f6')
    fig_top_st.update_layout(plot_bgcolor='#ffffff', paper_bgcolor='#ffffff', height=280, margin=dict(t=35, b=20, l=160, r=20))

    # Chart 7: Top Routes
    top_rt = f_df['route'].value_counts().head(8).reset_index()
    top_rt.columns = ['Route', 'Trips']
    top_rt = top_rt.sort_values(by='Trips', ascending=True)
    fig_top_rt = px.bar(top_rt, y='Route', x='Trips', orientation='h', title="Top 8 Popular Routes")
    fig_top_rt.update_traces(marker_color='#8b5cf6')
    fig_top_rt.update_layout(plot_bgcolor='#ffffff', paper_bgcolor='#ffffff', height=280, margin=dict(t=35, b=20, l=200, r=20))

    return kpi_trips, kpi_subtext, avg_dur, active_users, top_stat, fig_weekday, fig_hourly, fig_user, fig_gender, fig_age, fig_top_st, fig_top_rt

if __name__ == '__main__':
    print("==========================================================")
    print("🚀 Ford GoBike Dash Server running on http://127.0.0.1:8050/")
    print("==========================================================")
    app.run(debug=True, port=8050)