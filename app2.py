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

# Fetch data from both sheets
st.title("Match Day Team Stats")
df1 = fetch_data('sheet1')
df2 = fetch_data('sheet2')
df3 = fetch_data('sheet3')

# Display the dataframes in the app
# st.write("## Data from Sheet 1")
# st.write(df1.head())
# st.write("## Data from Sheet 2")
# st.write(df2.head())

# Create plots for both sheets
fig1 = create_plot(df1, f'{df1.columns[1]} vs {df1.columns[2]} - Sheet 1')
fig2 = create_plot(df2, f'{df2.columns[1]} vs {df2.columns[2]} - Sheet 2')
fig3 = create_plot(df3, f'{df2.columns[1]} vs {df2.columns[2]} - Sheet 3')


# Display the Plotly figures in the Streamlit app
st.plotly_chart(fig1)
st.plotly_chart(fig2)
st.plotly_chart(fig3)

# Run the Streamlit app
if __name__ == "__main__":
    st.write("MIAS")