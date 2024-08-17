import matplotlib.pyplot as plt
from mplsoccer.pitch import Pitch
import streamlit as st
import pandas as pd

document_id = '1oCS-ubjn2FtmkHevCToSCfcgL6WpjgXA3qoGnsu8IWk'

def fetch_data(sheet_name):
    url = f'https://docs.google.com/spreadsheets/d/{document_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'
    return pd.read_csv(url)

def plot_pass_map_for_player(player_name, df_pass):
    # Filter the pass DataFrame for the selected player
    player_pass_df = df_pass[df_pass['player'] == player_name]

    # Create the pitch
    pitch = Pitch(pitch_type='statsbomb', pitch_color='#22312b', line_color='#c7d5cc')

    fig, ax = plt.subplots(figsize=(13.5, 8))
    fig.set_facecolor('#22312b')
    ax.patch.set_facecolor('#22312b')
    
    pitch.draw(ax=ax)
    plt.gca().invert_yaxis()

    # Plot each pass
    for _, row in player_pass_df.iterrows():
        if row['outcome'] == 'Successful':
            plt.plot((row['x'], row['endX']), (row['y'], row['endY']), color='green')
            plt.scatter(row['x'], row['y'], color='green')
        elif row['outcome'] == 'Unsuccessful':
            plt.plot((row['x'], row['endX']), (row['y'], row['endY']), color='red')
            plt.scatter(row['x'], row['y'], color='red')

    st.pyplot(fig)  # Use st.pyplot to display the plot in Streamlit

def plot_pass_maps(player1, player2, df_pass):
    st.subheader(f'Pass Map for {player1}')
    plot_pass_map_for_player(player1, df_pass)
    
    st.subheader(f'Pass Map for {player2}')
    plot_pass_map_for_player(player2, df_pass)

df_pass = fetch_data("Passes")
player_options = df_pass['player'].unique()
player1 = st.selectbox('Select First Player', player_options)
player2 = st.selectbox('Select Second Player', player_options)

plot_pass_maps(player1, player2, df_pass)
