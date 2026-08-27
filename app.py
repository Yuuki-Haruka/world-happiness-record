import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="World Happiness Analysis", layout="wide")

df = pd.read_csv("world_happiness_2015_2019_trend_data.csv")

st.sidebar.title("Data Selection")

option = st.sidebar.radio(
    "Select Year",
    ["All Years", 2015, 2016, 2017, 2018, 2019],
    label_visibility="collapsed"
)

if option == "All Years":
    data = df
else:
    data = df[df["Year"] == option]

st.title("World Happiness Analysis")
st.write("Explore happiness scores and factors across countries.")

# Summary
top = data.sort_values("score", ascending=False).iloc[0]

c1, c2, c3, c4 = st.columns(4)

c1.metric("Countries", data["Country"].nunique())
c2.metric("Average Score", f"{data['score'].mean():.2f}")
c3.metric("Top Country", top["Country"])
c4.metric("Highest Score", f"{top['score']:.2f}")

# Top countries
st.header("Top 10 Happiest Countries")

top10 = data.groupby("Country")["score"].mean().reset_index().round(2)
top10 = top10.sort_values("score", ascending=False).head(10)

fig = px.bar(
    top10,
    x="Country",
    y="score",
    text="score"
)

st.plotly_chart(fig, use_container_width=True)

# Bottom countries
st.header("Bottom 10 Countries")

bottom10 = data.groupby("Country")["score"].mean().reset_index().round(2)
bottom10 = bottom10.sort_values("score").head(10)

fig = px.bar(
    bottom10,
    x="Country",
    y="score",
    text="score"
)

st.plotly_chart(fig, use_container_width=True)

# Happiness trend
st.header("Happiness Trend")

trend = df.groupby("Year")["score"].mean().reset_index()

fig = px.line(
    trend,
    x="Year",
    y="score",
    markers=True
)

st.plotly_chart(fig, use_container_width=True)

# Country details
st.header("Country Details")

country = st.selectbox(
    "Choose Country",
    sorted(data["Country"].dropna().unique())
)

country_data = data[data["Country"] == country]

fig = px.line(
    country_data,
    x="Year",
    y="score",
    markers=True,
    title=f"Happiness Score: {country}"
)

st.plotly_chart(fig, use_container_width=True)

# Pie chart
st.header("Happiness Factors")

factors = [
    "gdp",
    "social_support",
    "healthy_life",
    "freedom",
    "generosity",
    "corruption"
]

factor_data = country_data[factors].mean().reset_index()
factor_data.columns = ["Factor", "Value"]

fig = px.pie(
    factor_data,
    names="Factor",
    values="Value",
    hole=0.4
)

st.plotly_chart(fig, use_container_width=True)

# Statistics
st.header("Statistical Description")

st.dataframe(
    data[["score"] + factors].describe(),
    use_container_width=True
)

# Dataset
st.header("Dataset")

st.dataframe(
    data.sort_values("score", ascending=False),
    use_container_width=True,
    hide_index=True
)