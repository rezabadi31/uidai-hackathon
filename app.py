import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Page Configuration
st.set_page_config(page_title="UIDAI Aadhaar Update Analysis", layout="wide")

# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv("data/merged_data_clean.csv")
    df['month'] = pd.to_datetime(df['date']).dt.month
    return df

df = load_data()

# Compute Pressure Index
district_counts = df.groupby('district').size().reset_index(name='count')
mean_count = district_counts['count'].mean()
district_counts['pressure_index'] = district_counts['count'] / mean_count
district_counts = district_counts.sort_values('pressure_index', ascending=False)

# Header Section
with st.container():
    st.markdown("## UIDAI Aadhaar Update Analysis")
    st.markdown("Data-driven insights for update service planning")

# Quick Access Section
st.markdown("### Quick Access")
cols = st.columns(4)
sections = ["Overview", "Bivariate Analysis", "Trivariate Analysis", "Pressure Index"]
selected_section = st.radio("", sections, horizontal=True, label_visibility="collapsed")

# Sidebar Filters
st.sidebar.title("Filters & Selection")
selected_state = st.sidebar.selectbox("State", ["All"] + sorted(df['state'].unique()))
district_options = ["All"] + sorted(df[df['state'] == selected_state]['district'].unique()) if selected_state != "All" else ["All"] + sorted(df['district'].unique())
selected_district = st.sidebar.selectbox("District", district_options)
selected_month = st.sidebar.selectbox("Month", ["All"] + list(range(1, 13)))
top_n = st.sidebar.slider("Top N", 5, 20, 10)

# Filter Data
filtered_df = df.copy()
if selected_state != "All":
    filtered_df = filtered_df[filtered_df['state'] == selected_state]
if selected_district != "All":
    filtered_df = filtered_df[filtered_df['district'] == selected_district]
if selected_month != "All":
    filtered_df = filtered_df[filtered_df['month'] == selected_month]

# Compute Filtered Pressure Index
filtered_district_counts = filtered_df.groupby('district').size().reset_index(name='count')
if not filtered_district_counts.empty:
    filtered_mean_count = filtered_district_counts['count'].mean()
    filtered_district_counts['pressure_index'] = filtered_district_counts['count'] / filtered_mean_count
    filtered_district_counts = filtered_district_counts.sort_values('pressure_index', ascending=False)
else:
    filtered_district_counts = pd.DataFrame(columns=['district', 'count', 'pressure_index'])

# KPI Summary
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Records", len(filtered_df))
with col2:
    st.metric("Total States", filtered_df['state'].nunique())
with col3:
    st.metric("Total Districts", filtered_df['district'].nunique())
with col4:
    max_pressure = filtered_district_counts['pressure_index'].max() if not filtered_district_counts.empty else 0
    st.metric("Highest Pressure Index", f"{max_pressure:.2f}")

# Main Content
if selected_section == "Overview":
    with st.container():
        st.markdown("#### State vs Update Count")
        state_updates = filtered_df.groupby('state').size().reset_index(name='update_count').sort_values('update_count', ascending=False).head(top_n)
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x='update_count', y='state', data=state_updates, ax=ax)
        st.pyplot(fig)
        
        st.markdown("#### Month vs Update Count")
        month_updates = filtered_df.groupby('month').size().reset_index(name='update_count')
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.lineplot(x='month', y='update_count', data=month_updates, marker='o', ax=ax)
        ax.set_xticks(range(1, 13))
        st.pyplot(fig)

elif selected_section == "Bivariate Analysis":
    with st.container():
        st.markdown("#### State vs Updates")
        state_updates = filtered_df.groupby('state').size().reset_index(name='update_count').sort_values('update_count', ascending=False).head(top_n)
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x='update_count', y='state', data=state_updates, ax=ax)
        st.pyplot(fig)
        
        st.markdown("#### District vs Updates")
        district_updates = filtered_df.groupby('district').size().reset_index(name='update_count').sort_values('update_count', ascending=False).head(top_n)
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x='update_count', y='district', data=district_updates, ax=ax)
        st.pyplot(fig)

elif selected_section == "Trivariate Analysis":
    with st.container():
        st.markdown("#### Month vs Updates for Top Districts")
        top_districts = filtered_district_counts['district'].head(top_n).tolist()
        district_month = filtered_df[filtered_df['district'].isin(top_districts)].groupby(['district', 'month']).size().reset_index(name='update_count')
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.lineplot(x='month', y='update_count', hue='district', data=district_month, marker='o', ax=ax)
        ax.set_xticks(range(1, 13))
        st.pyplot(fig)

elif selected_section == "Pressure Index":
    with st.container():
        st.markdown("#### Top Districts Pressure Index")
        top_pressure = filtered_district_counts.head(top_n)
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x='pressure_index', y='district', data=top_pressure, ax=ax)
        st.pyplot(fig)
        
        st.markdown("#### High-Pressure Table")
        st.dataframe(top_pressure)