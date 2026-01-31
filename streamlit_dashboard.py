"""
Streamlit Dashboard for IoT Data Visualization
Real-time visualization of MQTT sensor data from PostgreSQL
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import psycopg2
from datetime import datetime, timedelta
import time

# Database Configuration - Using Unix socket (no host) for better compatibility
DB_CONFIG = {
    "dbname": "iot_course",
    "user": "iot_usr",
    "password": "upy_student_Admin1"
}

# Page configuration
st.set_page_config(
    page_title="IoT Data Dashboard",
    page_icon="📊",
    layout="wide"
)

def get_db_connection():
    """Create and return a fresh database connection"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except psycopg2.Error as e:
        st.error(f"Database connection failed: {e}")
        return None

def fetch_int_data(limit=100):
    """Fetch integer data from database"""
    conn = get_db_connection()
    if not conn:
        return pd.DataFrame()
    
    try:
        query = f"""
        SELECT id, topic, value, ts
        FROM lake_raw_data_int
        ORDER BY ts DESC
        LIMIT {limit}
        """
        df = pd.read_sql(query, conn)
        conn.close()
        return df.sort_values('ts')
    except Exception as e:
        st.error(f"Error fetching int data: {e}")
        if conn:
            conn.close()
        return pd.DataFrame()

def fetch_float_data(limit=100):
    """Fetch float data from database"""
    conn = get_db_connection()
    if not conn:
        return pd.DataFrame()
    
    try:
        query = f"""
        SELECT id, topic, value, ts
        FROM lake_raw_data_float
        ORDER BY ts DESC
        LIMIT {limit}
        """
        df = pd.read_sql(query, conn)
        conn.close()
        return df.sort_values('ts')
    except Exception as e:
        st.error(f"Error fetching float data: {e}")
        if conn:
            conn.close()
        return pd.DataFrame()

def get_statistics(df, data_type):
    """Calculate statistics for data"""
    if df.empty:
        return {}
    
    return {
        "Count": len(df),
        "Mean": df['value'].mean(),
        "Min": df['value'].min(),
        "Max": df['value'].max(),
        "Std Dev": df['value'].std(),
        "Latest": df['value'].iloc[-1] if len(df) > 0 else None
    }

def main():
    """Main dashboard function"""
    
    # Title
    st.title("📊 IoT Data Ingestion Dashboard")
    st.markdown("Real-time monitoring of MQTT sensor data")
    
    # Sidebar controls
    st.sidebar.header("⚙️ Dashboard Controls")
    
    # Auto-refresh toggle
    auto_refresh = st.sidebar.checkbox("Auto-refresh", value=True)
    if auto_refresh:
        refresh_interval = st.sidebar.slider("Refresh interval (seconds)", 1, 30, 5)
    
    # Data limit
    data_limit = st.sidebar.slider("Number of data points", 50, 500, 100, 50)
    
    # Time range filter
    st.sidebar.subheader("Time Filter")
    time_filter = st.sidebar.selectbox(
        "Show data from last:",
        ["All", "1 hour", "6 hours", "12 hours", "24 hours"]
    )
    
    # Manual refresh button
    if st.sidebar.button("🔄 Refresh Now"):
        st.rerun()
    
    # Create placeholder for auto-refresh
    placeholder = st.empty()
    
    while True:
        with placeholder.container():
            # Fetch data
            df_int = fetch_int_data(data_limit)
            df_float = fetch_float_data(data_limit)
            
            # Apply time filter
            if time_filter != "All":
                hours = int(time_filter.split()[0])
                cutoff_time = datetime.now() - timedelta(hours=hours)
                if not df_int.empty:
                    df_int = df_int[df_int['ts'] >= cutoff_time]
                if not df_float.empty:
                    df_float = df_float[df_float['ts'] >= cutoff_time]
            
            # Key metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Integer Records", len(df_int))
            with col2:
                st.metric("Total Float Records", len(df_float))
            with col3:
                if not df_int.empty:
                    st.metric("Latest Int Value", f"{df_int['value'].iloc[-1]}")
                else:
                    st.metric("Latest Int Value", "N/A")
            with col4:
                if not df_float.empty:
                    st.metric("Latest Float Value", f"{df_float['value'].iloc[-1]:.4f}")
                else:
                    st.metric("Latest Float Value", "N/A")
            
            # Main visualizations
            st.markdown("---")
            
            # Time series charts
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("🔢 Integer Data Stream")
                if not df_int.empty:
                    fig_int = go.Figure()
                    fig_int.add_trace(go.Scatter(
                        x=df_int['ts'],
                        y=df_int['value'],
                        mode='lines+markers',
                        name='Integer Values',
                        line=dict(color='#1f77b4', width=2),
                        marker=dict(size=6)
                    ))
                    fig_int.update_layout(
                        xaxis_title="Timestamp",
                        yaxis_title="Value",
                        hovermode='x unified',
                        height=400
                    )
                    st.plotly_chart(fig_int, use_container_width=True)
                    
                    # Statistics
                    stats_int = get_statistics(df_int, "int")
                    st.markdown("**Statistics:**")
                    stats_cols = st.columns(3)
                    stats_cols[0].metric("Mean", f"{stats_int['Mean']:.2f}")
                    stats_cols[1].metric("Min", stats_int['Min'])
                    stats_cols[2].metric("Max", stats_int['Max'])
                else:
                    st.info("No integer data available. Make sure the publisher and subscriber are running.")
            
            with col2:
                st.subheader("📈 Float Data Stream")
                if not df_float.empty:
                    fig_float = go.Figure()
                    fig_float.add_trace(go.Scatter(
                        x=df_float['ts'],
                        y=df_float['value'],
                        mode='lines+markers',
                        name='Float Values',
                        line=dict(color='#ff7f0e', width=2),
                        marker=dict(size=6)
                    ))
                    fig_float.update_layout(
                        xaxis_title="Timestamp",
                        yaxis_title="Value",
                        hovermode='x unified',
                        height=400
                    )
                    st.plotly_chart(fig_float, use_container_width=True)
                    
                    # Statistics
                    stats_float = get_statistics(df_float, "float")
                    st.markdown("**Statistics:**")
                    stats_cols = st.columns(3)
                    stats_cols[0].metric("Mean", f"{stats_float['Mean']:.4f}")
                    stats_cols[1].metric("Min", f"{stats_float['Min']:.4f}")
                    stats_cols[2].metric("Max", f"{stats_float['Max']:.4f}")
                else:
                    st.info("No float data available. Make sure the publisher and subscriber are running.")
            
            # Combined comparison chart
            st.markdown("---")
            st.subheader("📊 Combined Data Comparison")
            
            if not df_int.empty or not df_float.empty:
                # Create subplot with secondary y-axis
                fig_combined = make_subplots(specs=[[{"secondary_y": True}]])
                
                if not df_int.empty:
                    fig_combined.add_trace(
                        go.Scatter(
                            x=df_int['ts'],
                            y=df_int['value'],
                            name="Integer",
                            line=dict(color='#1f77b4')
                        ),
                        secondary_y=False
                    )
                
                if not df_float.empty:
                    fig_combined.add_trace(
                        go.Scatter(
                            x=df_float['ts'],
                            y=df_float['value'],
                            name="Float",
                            line=dict(color='#ff7f0e')
                        ),
                        secondary_y=True
                    )
                
                fig_combined.update_xaxes(title_text="Timestamp")
                fig_combined.update_yaxes(title_text="Integer Values", secondary_y=False)
                fig_combined.update_yaxes(title_text="Float Values", secondary_y=True)
                fig_combined.update_layout(height=400, hovermode='x unified')
                
                st.plotly_chart(fig_combined, use_container_width=True)
            else:
                st.info("No data available for comparison")
            
            # Distribution charts
            st.markdown("---")
            st.subheader("📉 Data Distribution")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if not df_int.empty:
                    fig_hist_int = px.histogram(
                        df_int,
                        x='value',
                        nbins=30,
                        title="Integer Value Distribution",
                        color_discrete_sequence=['#1f77b4']
                    )
                    fig_hist_int.update_layout(height=300)
                    st.plotly_chart(fig_hist_int, use_container_width=True)
                else:
                    st.info("No integer data for distribution")
            
            with col2:
                if not df_float.empty:
                    fig_hist_float = px.histogram(
                        df_float,
                        x='value',
                        nbins=30,
                        title="Float Value Distribution",
                        color_discrete_sequence=['#ff7f0e']
                    )
                    fig_hist_float.update_layout(height=300)
                    st.plotly_chart(fig_hist_float, use_container_width=True)
                else:
                    st.info("No float data for distribution")
            
            # Recent data table
            st.markdown("---")
            st.subheader("📋 Recent Data Records")
            
            tab1, tab2 = st.tabs(["Integer Data", "Float Data"])
            
            with tab1:
                if not df_int.empty:
                    st.dataframe(
                        df_int.tail(10)[['id', 'topic', 'value', 'ts']],
                        use_container_width=True,
                        hide_index=True
                    )
                else:
                    st.info("No integer data available")
            
            with tab2:
                if not df_float.empty:
                    st.dataframe(
                        df_float.tail(10)[['id', 'topic', 'value', 'ts']],
                        use_container_width=True,
                        hide_index=True
                    )
                else:
                    st.info("No float data available")
            
            # Footer
            st.markdown("---")
            st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        if not auto_refresh:
            break
        
        time.sleep(refresh_interval)
        st.rerun()

if __name__ == "__main__":
    main()
