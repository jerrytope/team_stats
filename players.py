


import plotly.graph_objs as go
import streamlit as st
import pandas as pd


document_id = '1EXllUu4dZ4YeNwNbS8J7qBZ3Q5bPLn-U1abawBP7CUQ'
sheet_name = 'sheet1'

# Construct the URL
url = f'https://docs.google.com/spreadsheets/d/{document_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'

# Read the data into a pandas DataFrame
df = pd.read_csv(url)

# Function to create radar chart
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

# Streamlit app
st.title('Player Comparison Radar Chart')

# Select players
player1 = st.selectbox('Select First Player', df['Player'])
player2 = st.selectbox('Select Second Player', df['Player'])

# Ensure two different players are selected
if player1 != player2:
    fig = create_radar_chart(df, player1, player2)
    st.plotly_chart(fig)
else:
    st.warning("Please select two different players.")
