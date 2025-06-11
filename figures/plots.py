import pandas as pd
import plotly.express as px
import dash_ag_grid as dag
from plotly.graph_objects import Figure

def create_grid(
        df:             pd.DataFrame)->dag.AgGrid:
    '''
    Create an AgGrid component
    '''

    grid = dag.AgGrid(
                id              = {"type": "grid", "index": "main_grid"},
                rowData         = df.to_dict("records"),
                columnDefs      = [{"field": i, 'filter': True, 'sortable': True} for i in df.columns],
                dashGridOptions = {"pagination": True},
                columnSize      = "sizeToFit")

    return grid


def create_choropleth(
        df:             pd.DataFrame,
        color_column:   str,
        color_scale:    str = '')->Figure:
    '''
    Create a Choropleth plot
    '''

    # Average values or counts by division (if needed)
    divisions           = df['Location (Census Region)'].value_counts().reset_index()
    divisions.columns   = ['Census Division', 'Count']

    # Map divisions to their states
    division_to_states = {
        'New England':          ['CT', 'ME', 'MA', 'NH', 'RI', 'VT'],
        'Middle Atlantic':      ['NJ', 'NY', 'PA'],
        'East North Central':   ['IL', 'IN', 'MI', 'OH', 'WI'],
        'West North Central':   ['IA', 'KS', 'MN', 'MO', 'NE', 'ND', 'SD'],
        'South Atlantic':       ['DE', 'FL', 'GA', 'MD', 'NC', 'SC', 'VA', 'DC', 'WV'],
        'East South Central':   ['AL', 'KY', 'MS', 'TN'],
        'West South Central':   ['AR', 'LA', 'OK', 'TX'],
        'Mountain':             ['AZ', 'CO', 'ID', 'MT', 'NV', 'NM', 'UT', 'WY'],
        'Pacific':              ['AK', 'CA', 'HI', 'OR', 'WA']
    }

    # Expand division counts to states
    expanded_rows       = []

    for i, row in divisions.iterrows():
        division        = row['Census Division']
        count           = row['Count']

        for state in division_to_states[division]:
            expanded_rows.append({'State': state, 'Census Division': division, 'Count': count})

    state_df            = pd.DataFrame(expanded_rows)

    if color_scale == '':
        choropleth_fig      = px.choropleth(
                        data_frame      = state_df,
                        locations       = "State",
                        locationmode    = "USA-states",
                        scope           = "usa",
                        color           = color_column,
                        hover_name      = "Census Division",
                        title           = "Census Divisions Regions")
        
    else:
        choropleth_fig      = px.choropleth(
                        data_frame      = state_df,
                        locations       = "State",
                        locationmode    = "USA-states",
                        scope           = "usa",
                        color           = color_column,
                        hover_name      = "Census Division",
                        color_continuous_scale  = color_scale,
                        hover_data      = {"State": False, "Census Division": True, "Count": True},
                        title           = "Survey Response Count by Census Division")

    # Remove state borders
    choropleth_fig.update_geos(
                    showlakes       = False,
                    showland        = True,
                    showcountries   = False,
                    showframe       = False,
                    visible         = False)
    
    choropleth_fig.update_traces(marker_line_width=0)

    return choropleth_fig