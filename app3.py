import streamlit as st
import pandas as pd
import plotly.graph_objs as go

# Google Sheets document ID
document_id = '1oCS-ubjn2FtmkHevCToSCfcgL6WpjgXA3qoGnsu8IWk'

def fetch_data(sheet_name):
    url = f'https://docs.google.com/spreadsheets/d/{document_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'
    return pd.read_csv(url)





def create_team_plot(df, title):
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

def create_radar_chart(df, player1, player2):
    metrics = df.columns[1:].tolist()
    
    player1_data = df[df['Player'] == player1].iloc[0, 1:].tolist()
    player2_data = df[df['Player'] == player2].iloc[0, 1:].tolist()

    trace1 = go.Scatterpolar(
        r=player1_data,
        theta=metrics,
        fill='toself',
        name=player1,
        marker=dict(color='blue')
    )

    trace2 = go.Scatterpolar(
        r=player2_data,
        theta=metrics,
        fill='toself',
        name=player2,
        marker=dict(color='red')
    )

    layout = go.Layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )
        ),
        showlegend=True
    )

    fig = go.Figure(data=[trace1, trace2], layout=layout)
    return fig


# Fetch data for three games
df1 = fetch_data('sheet1')
df2 = fetch_data('sheet2')
df3 = fetch_data('sheet3')


df_assists = fetch_data('Assist')  # Replace 'assist_sheet' with the actual name of the sheet
df_goals = fetch_data('Goals')  # Replace 'goal_sheet' with the actual name of the sheet
df_shots = fetch_data('SOT')  # Replace with the actual name of the sheet
df_saves = fetch_data('Save')

df_rader = fetch_data("rader")

# Create a dictionary for easy access
game_data = {
    'Game 1': df1,
    'Game 2': df2,
    'Game 3': df3
}

# Streamlit app
st.title("Match Day Team Stats")

# Game selection filter
selected_game = st.selectbox('Select Game', list(game_data.keys()))

# Create plot for the selected game
selected_df = game_data[selected_game]
fig = create_team_plot(selected_df, f'{selected_df.columns[1]} vs {selected_df.columns[2]}')

# Display the Plotly figure for the selected game
st.plotly_chart(fig)

fig_assists = create_player_stat_plot(df_assists, 'Player Assists')
fig_goals = create_player_stat_plot(df_goals, 'Player Goals')
fig_shots = create_player_stat_plot(df_shots, 'Shots on Target')
fig_saves = create_player_stat_plot(df_saves, 'Player Saves')


st.plotly_chart(fig_assists)
st.plotly_chart(fig_goals)
st.plotly_chart(fig_shots)
st.plotly_chart(fig_saves)

st.title('Player Comparison Radar Chart')

# Select players
player1 = st.selectbox('Select First Player', df_rader['Player'])
player2 = st.selectbox('Select Second Player', df_rader['Player'])

# Ensure two different players are selected
if player1 != player2:

    st.subheader(f'Stats for {player1}')
    st.write(df_rader[df_rader['Player'] == player1])
    
    st.subheader(f'Stats for {player2}')
    st.write(df_rader[df_rader['Player'] == player2])
    
    fig = create_radar_chart(df_rader, player1, player2)
    st.plotly_chart(fig)
else:
    st.warning("Please select two different players.")