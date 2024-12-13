import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import plotly.graph_objects as go
import yaml
import streamlit_authenticator as stauth
from yaml.loader import SafeLoader
import time
from auth import setup_authentication



# Set up Streamlit page configuration
st.set_page_config(
    page_title="Homepage",
    page_icon="🌟",
    layout="wide"
)

authenticator = setup_authentication()

user_data = st.query_params.get("user_data", "dashboard1")

# Function to fetch data from the claims table
@st.cache_data
def fetch_claims_data():
    try:
        # Load data from CSV for now
        df = pd.read_csv('Claims.csv')
        
        # Ensure date columns are in the correct format
        date_columns = [
            'claim_received_date', 'claim_loss_date', 'claim_finalised_date',
            'original_verified_date_of_loss_time', 'last_verified_date_of_loss_time',
            'catastrophe_valid_from_date_time', 'catastrophe_valid_to_date_time', 'update_date'
        ]
        for col in date_columns:
            df[col] = pd.to_datetime(df[col], errors='coerce').dt.date
        
    except Exception as e:
        print(f"Error fetching data: {e}")
        df = pd.DataFrame()  # Return empty DataFrame on failure
    return df
# Define each dashboard (Dashboard 1 to Dashboard 6)
def dashboard1():
    if st.session_state['authentication_status']:
        if user_data == "dashboard1":

            st.markdown("""
            <style>
                /* Global font color and family */
                body {
                    font-family: 'Arial', sans-serif;
                    color: #333;
                }

                /* Styling for sidebar */
                .sidebar .sidebar-content {
                    background-color: #f4f4f4;
                    color: #5d3a9b;
                }
                
                /* Styling for filter options */
                .sidebar .widget > label {
                    color: #5d3a9b;
                    font-weight: bold;
                }

                /* Styling for cards */
                .metric-card {
                    border: 2px solid #5d3a9b;
                    border-radius: 8px;
                    background-color: #f0f0f0;
                    padding: 20px;
                    margin: 10px;
                    height: 200px;  
                    width: 160px;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                }

                .metric-card h3 {
                    color: #5d3a9b;
                    font-size: 18px;
                    margin-bottom: 10px;
                }

                .metric-card .value {
                    font-size: 36px;
                    font-weight: bold;
                    color: #333;
                    margin-bottom: 0px;
                }

                /* Styling for "Go Back to Home" button */
                .stButton button {
                    background-color: #5d3a9b;
                    color: white;
                    font-weight: bold;
                    border-radius: 8px;
                    padding: 10px 30px;
                    width: auto;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                    border: none;
                }

                .stButton button:hover {
                    background-color: #4a2a78;
                }

                /* Centering the "Go Back to Home" button */
                .go-back-btn {
                    display: flex;
                    justify-content: center;
                }
            </style>
            """, unsafe_allow_html=True)
            # Display logo
            # st.image("exl.png", width=150)  # Replace 'logo.png' with the path to your logo image file

            col1, col2, col3 = st.columns([0.7, 2.6, 0.7])
            with col2:
                st.title("Claim Report Dashboard Testing")

        

            # Load data only once per session
            if "data" not in st.session_state:
                st.session_state.data = fetch_claims_data()

            # Fetch data from the database
            data = st.session_state.data

            # st.title("Dashboard Navigation")
            # navigation = st.selectbox("Select a Dashboard", ["Homepage", "Dashboard 1", "Dashboard 2", "Dashboard 3"])

            if not data.empty:
                # Sidebar for filters
                st.sidebar.header("Filter Options")

                filtered_data = data.copy()  # Start with a copy for independent filtering

                claim_numbers = st.sidebar.text_input("Filter by Claim Number (comma-separated)")
                if claim_numbers:
                    claim_numbers = [num.strip() for num in claim_numbers.split(",") if num.strip()]
                    filtered_data = filtered_data[filtered_data['claim_number'].astype(str).isin(claim_numbers)]

                # Text-based filters with an "All" option for each relevant column
                text_columns = [
                    'source_system', 'general_nature_of_loss', 'line_of_business', 'claim_status', 
                    'fault_rating', 'fault_categorisation'
                ]
                for col in text_columns:
                    unique_values = data[col].dropna().unique().tolist()
                    unique_values.insert(0, "All")  # Add "All" option
                    selected_values = st.sidebar.multiselect(f"Filter by {col}", options=unique_values, default="All")
                    
                    # Apply filter only if "All" is not selected
                    if "All" not in selected_values:
                        filtered_data = filtered_data[filtered_data[col].isin(selected_values)]

                # Independent Date range filters
                date_columns = [
                    'claim_received_date', 'claim_loss_date', 'claim_finalised_date', 
                    'original_verified_date_of_loss_time', 'last_verified_date_of_loss_time', 
                    'catastrophe_valid_from_date_time', 'catastrophe_valid_to_date_time'
                ]
                for col in date_columns:
                    min_date, max_date = data[col].min(), data[col].max()
                    if pd.notnull(min_date) and pd.notnull(max_date):
                        date_range = st.sidebar.date_input(f"{col} Range", value=(min_date, max_date))
                        if date_range:
                            filtered_data = filtered_data[filtered_data[col].between(date_range[0], date_range[1])]
                            

                # Display filtered statistics
                st.markdown("""
                    <style>
                        h3 {
                            color: #5d3a9b !important;
                        }
                    </style>
                """, unsafe_allow_html=True)
                st.subheader("Filtered Claims Statistics")
                st.write("Total Claims:", filtered_data["claim_number"].nunique())
                def display_custom_metric(title, value, background_color="#f0f0f0"):
                    card_style = f"""
                    <style>
                    .metric-card {{
                        border: 2px solid #5d3a9b;
                        border-radius: 8px;
                        background-color: {background_color};
                        padding: 20px;
                        margin: 10px;
                        height: 200px;  
                        width: 160px;
                        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                    }}
                    .metric-card h3 {{
                        color: #5d3a9b;
                        font-size: 18px;
                        margin-bottom: 10px;
                    }}
                    .metric-card .value {{
                        font-size: 36px;
                        font-weight: bold;
                        color: #333;
                        margin-bottom: 0px;
                    }}
                    </style>
                    """

                    # HTML for the metric card
                    card_html = f"""
                    <div class="metric-card">
                        <h3>{title}</h3>
                        <div class="value">{value}</div>
                    </div>
                    """

                    # Render the card with custom styling
                    st.markdown(card_style + card_html, unsafe_allow_html=True)
                
                st.subheader("Metrics Overview")
                col1, col2, col3, col4, col5, col6 = st.columns(6)
                
                with col1:
                    display_custom_metric("Claims Monitored", "3,071")
        #             st.metric("**Claims Monitored**", "3,071")
                with col2:
                    display_custom_metric("Claims with Leakage Opportunity", "1,854")

                with col3:
                    display_custom_metric("Leakage Opportunity %", 60)

                with col4:
                    display_custom_metric("Potential Leakage $", "$51.2M")

                with col5:
                    display_custom_metric("Leakage Rate %", 100)

                with col6:
                    display_custom_metric("Opportunities Not Actioned", "3,063")
                    
                
                st.markdown("<br><br>", unsafe_allow_html=True)

                col1, col2 = st.columns(2, gap="small")

                # Claims by Status chart with customized colors
                with col1:
                    st.subheader("Claims by Status")
                    status_counts = filtered_data['claim_status'].value_counts().reset_index()
                    status_counts.columns = ['claim_status', 'count']
                    fig_status = px.bar(
                        status_counts, x='claim_status', y='count', title="Claims by Status", 
                        color='claim_status', color_discrete_sequence=px.colors.sequential.Plasma
                    )
                    fig_status.update_layout(
                        plot_bgcolor="#ffffff",
                        paper_bgcolor="#f0f2f6",
                    )
        #             st.markdown('<div class="graph-container">', unsafe_allow_html=True)
                    st.plotly_chart(fig_status)


                # Claims Over Time chart
                with col2:
                    st.subheader("Claims Over Time")
                    claims_over_time = filtered_data.groupby('claim_received_date').size().reset_index(name='claim_count')
                    fig_time = px.line(
                        claims_over_time, x='claim_received_date', y='claim_count', 
                        title="Claims Over Time", color_discrete_sequence=px.colors.sequential.Viridis
                    )
                    fig_time.update_layout(
                        plot_bgcolor="#ffffff",
                        paper_bgcolor="#f0f2f6",
                    )
                    st.plotly_chart(fig_time)

        #         # New side-by-side charts for Claim Status (Pie) and Line of Business (Horizontal Bar)
                col3, col4 = st.columns(2, gap="small")

                # Pie chart for Claim Status
                with col3:
                    st.subheader("Claim Status Distribution")
                    fig_pie = px.pie(filtered_data, names='claim_status', title="Claim Status Distribution", hole=0.3)
                    fig_pie.update_layout(
                        plot_bgcolor="#ffffff",
                        paper_bgcolor="#f0f2f6",
                    )
                    st.plotly_chart(fig_pie)

                # Horizontal bar chart for Line of Business
                with col4:
                    st.subheader("Claims by Line of Business")
                    line_of_business_counts = filtered_data['line_of_business'].value_counts().reset_index()
                    line_of_business_counts.columns = ['line_of_business', 'count']
                    fig_line_of_business = px.bar(
                        line_of_business_counts, 
                        y='line_of_business', 
                        x='count', 
                        orientation='h', 
                        title="Claims by Line of Business", 
                        color='line_of_business'
                    )
                    fig_line_of_business.update_layout(
                        plot_bgcolor="#ffffff",
                        paper_bgcolor="#f0f2f6",
                        showlegend=False,
                    )
                    fig_line_of_business.update_xaxes(title="Count")
                    fig_line_of_business.update_yaxes(title="Line of Business")
                    st.plotly_chart(fig_line_of_business)
                    
                
                # Trend graph for Claim Status (Open and Closed) by Year
                # Trend graph for Claim Status (Open and Closed) by Month
                st.subheader("Claim Status Trend Over Months")

                # Extract month and year from claim_received_date
                filtered_data['claim_received_date'] = pd.to_datetime(filtered_data['claim_received_date'], errors='coerce')
                filtered_data['month_year'] = filtered_data['claim_received_date'].dt.to_period('M').astype(str)
                monthly_status_counts = (
                    filtered_data.groupby(['month_year', 'claim_status'])
                    .size()
                    .reset_index(name='count')
                )

                # Create bar chart with a line trend for total claims per month
                fig_trend_monthly = px.bar(
                    monthly_status_counts, 
                    x='month_year', 
                    y='count', 
                    color='claim_status', 
                    title="Monthly Claim Status Trend (Open vs Closed)",
                    barmode='group'
                )

                # Add a line to show the overall trend of claims per month
                monthly_totals = monthly_status_counts.groupby('month_year')['count'].sum().reset_index()
                fig_trend_monthly.add_scatter(
                    x=monthly_totals['month_year'], 
                    y=monthly_totals['count'], 
                    mode='lines+markers', 
                    name='Total Claims Trend',
                    line=dict(color='blue', width=2)
                )

                # Update layout and background
                fig_trend_monthly.update_layout(
                    plot_bgcolor="#ffffff",
                    paper_bgcolor="#f0f2f6",
                    xaxis_title="Month-Year",
                    yaxis_title="Number of Claims",
                    xaxis_tickangle=-45
                )
                st.plotly_chart(fig_trend_monthly)

        #         # Display the styled dataframe with a subheader
                st.subheader("Filtered Claims Data")
                filtered_data = filtered_data.head(20)
        #         st.dataframe(styled_data)
                def style_alternate_rows(x):
                    # Create an empty style object
                    style = pd.DataFrame('', index=x.index, columns=x.columns)
        #             style = style.applymap(lambda v: 'border: 2px solid #5d3a9b')
                    # Apply background color for even rows
                    style.iloc[::2] = 'background-color: #f9f9f9'  # Light gray for even rows
                    style.iloc[1::2] = 'background-color: #e6e6e6'  # Slightly darker gray for odd rows
                    
                    
                    return style

                # Apply the styling to the dataframe
                styled_df = filtered_data.style.apply(style_alternate_rows, axis=None)
        #         filtered_data = filtered_data.head(20)
                st.dataframe(styled_df)

                # Option to download the filtered data
                csv = filtered_data.to_csv(index=False)
                st.download_button("Download as CSV", csv, "filtered_claims.csv", "text/csv")
                
            else:
                st.warning("No data available.")
            col1, col2, col3 = st.columns([2.8, 1.4, 2.8])
            with col2:
                authenticator.logout()
    else:
        st.warning("You must log in to access this page.")
        st.stop()


# Run the app
if __name__ == "__main__":
    dashboard1()