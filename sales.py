import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
file_path = r"C:\Users\gowth\OneDrive\Desktop\streamlit tut\sales_dataset_with_items.xlsx"
df = pd.read_excel(file_path)

# Set page configuration
st.set_page_config(page_title="Corporate Sales Dashboard", page_icon="🏢", layout="wide")

# Styling for the dashboard
st.markdown("""
<style>
    .button-style {
        background-color: #2C3E50;
        color: white;
        font-size: 18px;
        padding: 10px 20px;
        margin: 10px;
        border-radius: 8px;
        text-align: center;
        width: 200px;
        cursor: pointer;
    }
    .selected-button {
        background-color: #1ABC9C;
        color: white;
        font-size: 18px;
        padding: 10px 20px;
        margin: 10px;
        border-radius: 8px;
        text-align: center;
        width: 200px;
        cursor: pointer;
    }
</style>
""", unsafe_allow_html=True)

# Define buttons for multipage navigation
col1, col2, col3 = st.columns(3)

with col1:
    intro_button = st.button("Introduction")
with col2:
    viz_button = st.button("Visualizations")
with col3:
    insights_button = st.button("Insights & Ideas")

# Default to Introduction page
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Introduction"

# Update page based on button click
if intro_button:
    st.session_state.current_page = "Introduction"
elif viz_button:
    st.session_state.current_page = "Visualizations"
elif insights_button:
    st.session_state.current_page = "Insights & Ideas"

# Display content based on selected page
if st.session_state.current_page == "Introduction":
    st.markdown('<div class="selected-button">Introduction</div>', unsafe_allow_html=True)
    st.title("Corporate Sales Dashboard - Introduction")
    st.subheader("Gowtham J | Reg. No: 24MAI0104")
    st.markdown("<hr>", unsafe_allow_html=True)

    # Detailed dataset description
    st.write("""
    ### Dataset Description
    This dataset provides an overview of corporate sales across regions, years, and items. It includes:
    
    - **State & District Information**
    - **Item Sales**: Different categories like fresh goods, packed goods, and more.
    - **Sales Metrics**: Total sales, demand, items purchased, profit margins.
    
    The goal is to explore patterns in sales, compare trends over time, and gain insights into product and customer behavior.
    """)
    
    # Dataset quick stats
    st.write("**Quick Stats**")
    st.write(f"Total Records: {len(df)}")
    st.write(f"Total Unique States: {df['State'].nunique()}")
    st.write(f"Total Unique Items: {df['Items Name'].nunique()}")

elif st.session_state.current_page == "Visualizations":
    st.markdown('<div class="selected-button">Visualizations</div>', unsafe_allow_html=True)
    st.title("Sales Visualizations")

    # Sidebar filters
    state = st.selectbox("Select State", df['State'].unique())
    district = st.selectbox("Select District", df[df['State'] == state]['District'].unique())
    item = st.selectbox("Select Item", df[df['District'] == district]['Items Name'].unique())
    year = st.selectbox("Select Year", df['Year'].unique())

    # Filter dataset
    filtered_df = df[(df['State'] == state) & (df['District'] == district) & 
                     (df['Items Name'] == item) & (df['Year'] == year)]

    st.subheader(f"Data for {state}, {district}, Item: {item}, Year: {year}")
    st.dataframe(filtered_df)

    # Sales Trend over the years
    st.subheader("Sales Trend over the Years")
    yearly_sales = df[(df['State'] == state) & (df['District'] == district) & 
                      (df['Items Name'] == item)].groupby('Year')['Counts'].sum().reset_index()
    
    # Reduced size of the plot
    plt.figure(figsize=(6, 3))  # Adjusted size
    sns.lineplot(x='Year', y='Counts', data=yearly_sales, marker='o', color='#1f77b4', lw=2)
    plt.title(f'Sales Trend for {item} in {state} - {district}', fontsize=12, color="#2C3E50")
    st.pyplot(plt)

    # More visualizations can go here

elif st.session_state.current_page == "Insights & Ideas":
    st.markdown('<div class="selected-button">Insights & Ideas</div>', unsafe_allow_html=True)
    st.title("Insights & Additional Ideas")

    # Heatmap for regional comparison
    st.subheader("Sales Performance by Region")
    region_sales = df.groupby(['State', 'District'])['Counts'].sum().unstack()
    
    # Reduced size of the plot
    plt.figure(figsize=(6, 4))  # Adjusted size
    sns.heatmap(region_sales, cmap='coolwarm', annot=True, fmt=".0f", linewidths=0.5)
    plt.title("Heatmap of Sales by Region", fontsize=12, color="#2C3E50")
    st.pyplot(plt)

    # Top performing products bar chart
    st.subheader("Top Performing Products")
    top_products = df.groupby('Items Name')['Counts'].sum().nlargest(5).reset_index()
    
    # Reduced size of the plot
    plt.figure(figsize=(6, 3))  # Adjusted size
    sns.barplot(x='Items Name', y='Counts', data=top_products, palette='Blues_d')
    plt.title("Top 5 Selling Products", fontsize=12, color="#2C3E50")
    st.pyplot(plt)

    st.markdown("""
    ### Further Ideas
    - **Predictive Modeling**: Use machine learning to forecast future sales trends.
    - **Regional Analysis**: Compare sales trends between regions to optimize supply decisions.
    - **Customer Behavior**: Analyze customer purchase patterns to enhance product recommendations.
    """)

# Footer
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<footer style='color: #7f8c8d; font-size: 12px;'>© 2024 Corporate Sales Insights | All rights reserved</footer>", unsafe_allow_html=True)
