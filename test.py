import pandas as pd
import streamlit as st
import plotly.graph_objs as go

document_id = '1IywguYo1CI9iqJzIadlptexdyIAlVnlp'

def fetch_data(sheet_name):
    url = f'https://docs.google.com/spreadsheets/d/{document_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'
    return pd.read_csv(url)

# Fetch the data
df = fetch_data('Individual_Stats')

# Select relevant columns
df = df.iloc[:, 6:25]

# Streamlit App
st.title("Player Comparison - Radar Chart")

# Sidebar for Team Selection
st.sidebar.header("Select Teams")
team_options = df['Team'].unique()
team1 = st.sidebar.selectbox("Select Team 1", team_options)
team2 = st.sidebar.selectbox("Select Team 2", team_options)

# Filter the DataFrame based on selected teams
df_team1_filtered = df[df['Team'] == team1]
df_team2_filtered = df[df['Team'] == team2]

# Sidebar for Position Selection
st.sidebar.header("Select Position")
position_options_team1 = df_team1_filtered['POS'].unique()
position_options_team2 = df_team2_filtered['POS'].unique()

# Ensure positions are only selectable if they exist in both teams
common_positions = list(set(position_options_team1) & set(position_options_team2))
selected_position = st.sidebar.selectbox("Select Position", common_positions)

# Further filter the DataFrame based on the selected position
df_position_team1 = df_team1_filtered[df_team1_filtered['POS'] == selected_position]
df_position_team2 = df_team2_filtered[df_team2_filtered['POS'] == selected_position]

# Ensure players are uniquely filtered
players_team1 = df_position_team1['Player'].unique().tolist()
players_team2 = df_position_team2['Player'].unique().tolist()

# Select players from the filtered teams
player1 = st.sidebar.selectbox(f"Select Player from {team1}", players_team1, index=0)
player2 = st.sidebar.selectbox(f"Select Player from {team2}", players_team2, index=1)

# Define columns based on position
if selected_position == 'GK':
    columns_to_use = ['Player', 'Saves', 'Blocks']
elif selected_position == 'FW':
    columns_to_use = ['Player', 'Goals', 'Assists', 'Shots ON', 'Shots OFF']
elif selected_position == 'MF':
    columns_to_use = ['Player', 'Goals', 'Assists', 'Shots ON', 'Shots OFF', 'Crosses', 'Tackles']
elif selected_position == 'DF':
    columns_to_use = ['Player', 'Goals',  'Tackles', 'Fouls']

# Filter the DataFrame to include only the relevant columns
df_position_team1 = df_position_team1[columns_to_use]
df_position_team2 = df_position_team2[columns_to_use]

# Radar Chart Function
def create_radar_chart(df1, df2, player1, player2):
    metrics = df1.columns[1:].tolist()  # Exclude 'Player' column
    player1_data = df[df['Player'] == player1].iloc[:, 4:10].sum()
    player2_data = df[df['Player'] == player2].iloc[:, 4:10].sum()

    col1, col2 = st.columns(2)
    
    with col1:
        st.header(f"{player1} Stats")
        st.write(player1_data)
    
    with col2:
        st.header(f"{player2} Stats")
        st.write(player2_data) 

    player1_data = player1_data.iloc[:].tolist()
    player2_data = player2_data.iloc[:].tolist()





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
                range=[0, max(max(player1_data), max(player2_data))]  # Dynamic range
            )
        ),
        showlegend=True
    )

    fig = go.Figure(data=[trace1, trace2], layout=layout)
    return fig


import plotly.graph_objs as go

def create_plot(df, title):
    stats_column = 'stats'
    team1_column = df.iloc[0, 1]  # Extracting team name from first row, second column
    team2_column = df.iloc[1, 1]  # Extracting team name from second row, second column

    # Create a new DataFrame for plotting
    plot_df = pd.DataFrame({
        stats_column: df.columns[2:],  # Extract stats from column names starting from the 3rd column
        team1_column: df.iloc[0, 2:],  # Extract data for Team 1
        team2_column: df.iloc[1, 2:]   # Extract data for Team 2
    })

    trace1 = go.Bar(
        y=plot_df[stats_column],
        x=-plot_df[team1_column],  # Make x-values negative for one team
        name=team1_column,
        orientation='h',
        marker=dict(color='blue'),
        text=plot_df[team1_column],  # Add labels
        textposition='outside',  # Position labels outside the bars
        hoverinfo='x+text'  # Hover information
    )

    trace2 = go.Bar(
        y=plot_df[stats_column],
        x=plot_df[team2_column],
        name=team2_column,
        orientation='h',
        marker=dict(color='red'),
        text=plot_df[team2_column],  # Add labels
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
            categoryarray=list(plot_df[stats_column])[::-1]  # Use the order from the DataFrame and reverse it
        )
    )

    fig = go.Figure(data=[trace1, trace2], layout=layout)
    return fig




# Ensure the teams are different
if team1 != team2:
    if player1 and player2:
        # Create and display radar chart
        fig = create_radar_chart(df_position_team1, df_position_team2, player1, player2)
        st.plotly_chart(fig)
else:
    st.sidebar.write("Please select two different teams.")




df2 = fetch_data('Team_Stats')

st.title("Team Stats")


df2 = df2[['match_id','team_name','team_score','goal_attempt','shot_ON','shot_OFF', 'goalkeeper_saves', 'fouls_committed', 'fouls_drawn', 'possession %', 'pass_accuracy %' ]]
# 'shot_BLOCK', 'shot_accuracy', 'fouls_committed','fouls_drawn','pass_attempt','pass_complete','possession'


match_id = df2['match_id'].unique()
item = st.sidebar.selectbox("Select Team 1", match_id)

match_id_filtered = df2[df2['match_id'] == item]

st.write(match_id_filtered)
st.title("Match Day Team Stats")
fig1 = create_plot(match_id_filtered, f'{match_id_filtered.columns[1]} vs {match_id_filtered.columns[2]} ')
st.plotly_chart(fig1)


 
