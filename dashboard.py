import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load the Excel data
xls = pd.ExcelFile("summary_analysis.xlsx")
df = xls.parse("Filtered Selected")

st.title("Interactive Dashboard - Cooperation and Risk")

# Sidebar filters
st.sidebar.header("Filters")
participant = st.sidebar.selectbox("Select participant", options=["All"] + sorted(df['code'].dropna().unique().tolist()))
game = st.sidebar.selectbox("Select game type", options=["All"] + sorted(df['current_game'].dropna().unique().tolist()))
vote = st.sidebar.selectbox("Select vote (Matrix B = 1, A = 0)", options=["All"] + sorted(df['Chose_Risk'].dropna().unique().tolist()))

# Filter data based on sidebar selections
filtered = df.copy()
if participant != "All":
    filtered = filtered[filtered['code'] == participant]
if game != "All":
    filtered = filtered[filtered['current_game'] == game]
if vote != "All":
    filtered = filtered[filtered['Chose_Risk'] == vote]

# Round range filter
round_range = st.sidebar.slider("Select round range",
                                 int(df['round_number'].min()),
                                 int(df['round_number'].max()),
                                 (int(df['round_number'].min()), int(df['round_number'].max())))
filtered = filtered[filtered['round_number'].between(*round_range)]

# Summary stats
st.subheader("Summary Statistics")
st.write("**Overall Means (Filtered)**")
st.dataframe(filtered[['Cooperated', 'Chose_Risk']].mean().rename("Mean").to_frame())

# Grouped means
st.write("**Means by Game Type and Vote**")
grouped = filtered.groupby(['current_game', 'Chose_Risk'])[['Cooperated']].mean().reset_index()
st.dataframe(grouped)

# Custom graph builder
st.subheader("Custom Line Graph")

# Select axes
y_axis = st.selectbox("Y-axis variable", options=['Cooperated', 'Chose_Risk'])
x_axis = st.selectbox("X-axis variable", options=['round_number', 'current_game', 'Chose_Risk'])

# Optional group-by
group_by = st.multiselect("Group by (optional)", options=[col for col in df.columns if col not in [x_axis, y_axis]])

# Build chart data
if group_by:
    chart_data = (filtered.groupby([x_axis] + group_by)[y_axis]
                           .mean()
                           .reset_index()
                           .pivot(index=x_axis, columns=group_by[0], values=y_axis))
else:
    chart_data = filtered.groupby(x_axis)[y_axis].mean()

# Plot
st.line_chart(chart_data)

# Expanded data view
with st.expander("See filtered raw data"):
    st.dataframe(filtered)

# Optional insights
st.subheader("Notable Insights")
if y_axis == 'Cooperated':
    high_coop_rounds = filtered.groupby('round_number')['Cooperated'].mean().reset_index()
    top = high_coop_rounds[high_coop_rounds['Cooperated'] >= 0.95]
    if not top.empty:
        st.write("⚠️ Rounds with 95%+ cooperation:")
        st.dataframe(top)
if y_axis == 'Chose_Risk':
    high_risk = filtered.groupby('current_game')['Chose_Risk'].mean()
    st.write("Average risk-taking by game type:")
    st.dataframe(high_risk.rename("Risk Mean").to_frame())