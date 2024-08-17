import streamlit as st
import pandas as pd
from mplsoccer import VerticalPitch
import matplotlib.pyplot as plt

# Load data
df_new = pd.read_excel("shoot_data.xlsx")
df_new = df_new[df_new["period"] != 5].copy()

# Define team colors
team_colors = {
    "England": "#C8102E",
    "Italy": "#0000FF",
    # Add more teams and their colors if needed
}

# Streamlit interface
st.title("Team Shot Analysis")

# Team selection
team1 = st.selectbox("Select Team 1", df_new["team"].unique())
team2 = st.selectbox("Select Team 2", df_new["team"].unique())

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
