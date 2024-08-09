


import streamlit as st
import pandas as pd
import plotly.graph_objs as go

# Set page configuration
# st.set_page_config(layout="wide")

# Google Sheets document ID
document_id = '1oCS-ubjn2FtmkHevCToSCfcgL6WpjgXA3qoGnsu8IWk'

def fetch_data(sheet_name):
    url = f'https://docs.google.com/spreadsheets/d/{document_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'
    return pd.read_csv(url)

def create_plot(df, title):
    stats_column = df.columns[0]
    team1_column = df.columns[1]
    team2_column = df.columns[2]

    trace1 = go.Bar(
        y=df[stats_column],
        x=-df[team1_column],  # Make x-values negative for one team
        name=team1_column,
        orientation='h',
        marker=dict(color='blue'),
        text=df[team1_column],  # Add labels
        textposition='outside',  # Position labels outside the bars
        hoverinfo='x+text'  # Hover information
    )

    trace2 = go.Bar(
        y=df[stats_column],
        x=df[team2_column],
        name=team2_column,
        orientation='h',
        marker=dict(color='red'),
        text=df[team2_column],  # Add labels
        textposition='outside',  # Position labels outside the bars
        hoverinfo='x+text'  # Hover information 
    )

    layout = go.Layout(
        title=title,
        barmode='overlay',
        bargap=0.1,
        bargroupgap=0,
        xaxis=dict(
            title='Values',
            showgrid=False,  # Hide x-axis grid lines
            zeroline=True,
            showline=True,
            showticklabels=False  # Hide x-axis ticks
        ),
        yaxis=dict(
            title='Stats',
            showgrid=False,  # Hide y-axis grid lines
            showline=True,
            showticklabels=True,
            categoryorder='array',  # Order by the values in the DataFrame
            categoryarray=list(df[stats_column])[::-1]  # Use the order from the DataFrame and reverse it
        )
    )

    fig = go.Figure(data=[trace1, trace2], layout=layout)
    return fig

def create_player_stat_plot(df, title):
    player_column = df.columns[0]
    stat_column = df.columns[1]
    team_column = df.columns[2]

    trace = go.Bar(
        y=df[player_column],
        x=df[stat_column],
        name=title,
        orientation='h',
        marker=dict(color='red'),
        text=df[team_column],  # Add labels
        textposition='outside',  # Position labels outside the bars
        hoverinfo='x+text'  # Hover information
    )

    layout = go.Layout(
        title=title,
        barmode='group',
        bargap=0.5,
        bargroupgap=0,
        xaxis=dict(
            title=title,
            showgrid=False,  # Hide x-axis grid lines
            zeroline=True,
            showline=True,
            showticklabels=True  # Show x-axis ticks
        ),
        yaxis=dict(
            title='Player',
            showgrid=False,  # Hide y-axis grid lines
            showline=True,
            showticklabels=True,
            categoryorder='array',  # Order by the values in the DataFrame
            categoryarray=list(df[player_column])[::-1]  # Use the order from the DataFrame and reverse it
        ),
        width=900,  # Set the figure width
        height=500  # Set the figure height
    )

    fig = go.Figure(data=[trace], layout=layout)
    return fig

# Fetch data from sheets
st.title("Match Day Team Stats")
df1 = fetch_data('sheet1')
df2 = fetch_data('sheet2')
df3 = fetch_data('sheet3')
df_assists = fetch_data('Assist')  # Replace 'assist_sheet' with the actual name of the sheet
df_goals = fetch_data('Goals')  # Replace 'goal_sheet' with the actual name of the sheet
df_shots = fetch_data('SOT')  # Replace with the actual name of the sheet
df_saves = fetch_data('Save')  # Replace with the actual name of the sheet

# Create plots for team stats
fig1 = create_plot(df1, f'{df1.columns[1]} vs {df1.columns[2]}')
fig2 = create_plot(df2, f'{df2.columns[1]} vs {df2.columns[2]}')
fig3 = create_plot(df3, f'{df3.columns[1]} vs {df3.columns[2]}')

# Create plots for individual player stats
fig_assists = create_player_stat_plot(df_assists, 'Player Assists')
fig_goals = create_player_stat_plot(df_goals, 'Player Goals')
fig_shots = create_player_stat_plot(df_shots, 'Shots on Target')
fig_saves = create_player_stat_plot(df_saves, 'Player Saves')

# Display the Plotly figures in the Streamlit app
st.plotly_chart(fig1)
st.plotly_chart(fig2)
st.plotly_chart(fig3)
st.plotly_chart(fig_assists)
st.plotly_chart(fig_goals)
st.plotly_chart(fig_shots)
st.plotly_chart(fig_saves)

# Run the Streamlit app
if __name__ == "__main__":
    st.write("MIAS")
