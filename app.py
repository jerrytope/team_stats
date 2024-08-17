import streamlit as st
import pandas as pd
import plotly.graph_objs as go
import mplsoccer
from mplsoccer.pitch import Pitch

# Google Sheets document ID


# st. set_page_config(layout="wide")
document_id = '1oCS-ubjn2FtmkHevCToSCfcgL6WpjgXA3qoGnsu8IWk'

def fetch_data(sheet_name):
    url = f'https://docs.google.com/spreadsheets/d/{document_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'
    return pd.read_csv(url)


import plotly.graph_objs as go

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
        text=[f"<b>{x}</b>" for x in df[team1_column]],  # Make text bold
        textposition='outside',  # Position labels outside the bars
        textfont=dict(color='black'),  # Set text color to black
        hoverinfo='x+text'  # Hover information
    )

    trace2 = go.Bar(
        y=df[stats_column],
        x=df[team2_column],
        name=team2_column,
        orientation='h',
        marker=dict(color='red'),
        text=[f"<b>{x}</b>" for x in df[team2_column]],  # Make text bold
        textposition='outside',  # Position labels outside the bars
        textfont=dict(color='black'),  # Set text color to black
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
            tickfont=dict(color='black'),  # Set stats values color to black
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

import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.pyplot as plt
from mplsoccer.pitch import Pitch
import seaborn as sns

def plot_pass_map_for_player(ax, player_name, df_pass):
    # Filter the pass DataFrame for the selected player
    player_pass_df = df_pass[df_pass['player'] == player_name]

    # Create the pitch
    pitch = Pitch(pitch_type='statsbomb', pitch_color='#22312b', line_color='#c7d5cc')
    pitch.draw(ax=ax)
    ax.set_title(f'Pass Map for {player_name}', color='white', fontsize=10, pad=20)
    ax.invert_yaxis()

    # Plot each pass
    for _, row in player_pass_df.iterrows():
        if row['outcome'] == 'Successful':
            ax.plot((row['x'], row['endX']), (row['y'], row['endY']), color='green')
            ax.scatter(row['x'], row['y'], color='green')
        elif row['outcome'] == 'Unsuccessful':
            ax.plot((row['x'], row['endX']), (row['y'], row['endY']), color='red')
            ax.scatter(row['x'], row['y'], color='red')

def plot_pass_maps(player1, player2, df_pass):
    fig, axs = plt.subplots(1, 2, figsize=(12, 6))  # Two plots side by side

    fig.set_facecolor('#22312b')
    axs[0].patch.set_facecolor('#22312b')
    axs[1].patch.set_facecolor('#22312b')

    plot_pass_map_for_player(axs[0], player1, df_pass)
    plot_pass_map_for_player(axs[1], player2, df_pass)

    st.pyplot(fig)


# Fetch data for three games
df1 = fetch_data('sheet1')
df2 = fetch_data('sheet2')
df3 = fetch_data('sheet3')


df_assists = fetch_data('Assist')  # Replace 'assist_sheet' with the actual name of the sheet
df_goals = fetch_data('Goals')  # Replace 'goal_sheet' with the actual name of the sheet
df_shots = fetch_data('SOT')  # Replace with the actual name of the sheet
df_saves = fetch_data('Save')

df_radar = fetch_data("FW_Rader")

df_pass = fetch_data("Passes")


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

# Filter by position
position_options_team = df_radar['Position'].unique()
selected_position = st.selectbox("Select Position", position_options_team)

if selected_position == 'GK':
    columns_to_use = ['Player', 'Save Percentage', 'Clean Sheets','Goal Conceded', 'Saves', 'Crosses Stopped', 'Penalty saves', 'Cross Clamed', 'Sweeper actions' ]                 
elif selected_position == 'FW':
    columns_to_use = ['Player', 'Goals', 'Shots on target', 'Conversion rate', 'Assists','Goal involvement', 'Penalties won', 'Attacking contribution', 'Minutes per goal']
elif selected_position == 'MF':
    columns_to_use = ['Player', 'Goals', 'Assists', 'Tackles', 'Interceptions', 'Chances created', 'Defensive errors','Fouls committed','Blocks','Goal involvement']      
elif selected_position == 'DF':
    columns_to_use = ['Player', 'Goals', 'Tackles', 'Fouls Won', 'Blocks', 'Minutes per card','Goal involvement', 'Defensive contribution', 'Defensive errors']        


# Filter the radar DataFrame by the selected position
filtered_df_radar = df_radar[df_radar['Position'] == selected_position]
filtered_df_radar = filtered_df_radar[columns_to_use]

# Select players from the filtered DataFrame
player_options = filtered_df_radar['Player'].unique()
player1 = st.selectbox('Select First Player', player_options)
player2 = st.selectbox('Select Second Player', player_options)




# Ensure two different players are selected
if player1 != player2:
    st.subheader('Player Stats')
    player1_value = filtered_df_radar[filtered_df_radar['Player'] == player1]
    player2_value = filtered_df_radar[filtered_df_radar['Player'] == player2]
    
    # Merge player data for display and plotting
    merged_df = pd.concat([player1_value, player2_value], ignore_index=True)
    st.write(merged_df)
    # st.dataframe(merged_df, use_container_width=True)  


    
    fig = create_radar_chart(filtered_df_radar, player1, player2)
    st.plotly_chart(fig)
else:
    st.warning("Please select two different players.")

plot_pass_maps(player1, player2, df_pass)

import streamlit as st
import pandas as pd
from mplsoccer import VerticalPitch
import matplotlib.pyplot as plt

# Load data

df_new = fetch_data("shoot")

# Streamlit interface
st.title("Team Shot Analysis")

# Get unique teams from the data
teams = df_new["team"].unique()

# Define team colors dynamically based on the teams in the data
team_colors = {team: f"C{i+1:02d}0{i+1:02d}" for i, team in enumerate(teams)}

# Team selection
team1 = st.selectbox("Select Team 1", teams)
team2 = st.selectbox("Select Team 2", teams)

# Split df into two parts, one for each team
team1_df = df_new[df_new["team"] == team1].copy()
team2_df = df_new[df_new["team"] == team2].copy()

# Split into goals and non-goals for each team
team1_df_g = team1_df[team1_df["outcome"] == "Goal"].copy()
team1_df_ng = team1_df[team1_df["outcome"] != "Goal"].copy()

team2_df_g = team2_df[team2_df["outcome"] == "Goal"].copy()
team2_df_ng = team2_df[team2_df["outcome"] != "Goal"].copy()

# Team stats
team1_tot_shots = team1_df.shape[0]
team1_tot_goals = team1_df_g.shape[0]
team1_tot_xg = team1_df["statsbomb_xg"].sum().round(2)

team2_tot_shots = team2_df.shape[0]
team2_tot_goals = team2_df_g.shape[0]
team2_tot_xg = team2_df["statsbomb_xg"].sum().round(2)

# Plotting
pitch = VerticalPitch(half=True)

fig, ax = plt.subplots(1, 2, figsize=(20, 8))

# Plot for Team 1
pitch.draw(ax=ax[0])
ax[0].set_title(f"{team1} Shots vs {team2}")

# Team 1 goals
pitch.scatter(team1_df_g["start_location_x"],
              team1_df_g["start_location_y"],
              s=team1_df_g["statsbomb_xg"]*500+100,
              marker="football",
              c=team_colors[team1],
              ax=ax[0],
              label=f"{team1} goals")
# Team 1 non-goals
pitch.scatter(team1_df_ng["start_location_x"],
              team1_df_ng["start_location_y"],
              s=team1_df_ng["statsbomb_xg"]*500+100,
              c=team_colors[team1],
              alpha=0.5,
              hatch="//",
              edgecolor="#101010",
              marker="s",
              ax=ax[0],
              label=f"{team1} non-goals")

# Plot for Team 2
pitch.draw(ax=ax[1])
ax[1].set_title(f"{team2} Shots vs {team1}")

# Team 2 goals
pitch.scatter(team2_df_g["start_location_x"],
              team2_df_g["start_location_y"],
              s=team2_df_g["statsbomb_xg"]*500+100,
              marker="football",
              c=team_colors[team2],
              ax=ax[1],
              label=f"{team2} goals")
# Team 2 non-goals
pitch.scatter(team2_df_ng["start_location_x"],
              team2_df_ng["start_location_y"],
              s=team2_df_ng["statsbomb_xg"]*500+100,
              c=team_colors[team2],
              alpha=0.5,
              hatch="//",
              edgecolor="#101010",
              marker="s",
              ax=ax[1],
              label=f"{team2} non-goals")

# Team 1 stats
basic_info_txt1 = f"Shots: {team1_tot_shots} | Goals: {team1_tot_goals} | xG: {team1_tot_xg}"
ax[0].text(0.5, -0.1, basic_info_txt1, size=15, ha="center", transform=ax[0].transAxes)

# Team 2 stats
basic_info_txt2 = f"Shots: {team2_tot_shots} | Goals: {team2_tot_goals} | xG: {team2_tot_xg}"
ax[1].text(0.5, -0.1, basic_info_txt2, size=15, ha="center", transform=ax[1].transAxes)

# Legends
ax[0].legend(labelspacing=1.5, loc="lower center")
ax[1].legend(labelspacing=1.5, loc="lower center")

# Display the plots
st.pyplot(fig)