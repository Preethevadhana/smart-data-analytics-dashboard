
    import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from io import BytesIO

---------------- PAGE CONFIG ----------------

st.set_page_config(
page_title="Smart Data Analytics Dashboard",
layout="wide",
initial_sidebar_state="expanded"
)

---------------- CUSTOM CSS ----------------

st.markdown("""

<style>  
.main {  
    padding-top: 1rem;  
}  
.stMetric {  
    border-radius: 10px;  
    padding: 10px;  
}  
</style>  """, unsafe_allow_html=True)

---------------- TITLE ----------------

st.title("📊 Smart Data Analytics Dashboard")
st.markdown(
"Upload any CSV file and perform data analysis instantly using "
"Python, Pandas, NumPy, Plotly, and Streamlit."
)

---------------- SIDEBAR ----------------

with st.sidebar:
st.header("📁 Upload Dataset")

uploaded_file = st.file_uploader(  
    "Choose a CSV File",  
    type=["csv"]  
)  

st.markdown("---")  

st.header("🧹 Data Cleaning")  

remove_duplicates = st.checkbox("Remove Duplicate Rows")  

drop_missing = st.checkbox("Drop Missing Values")  

st.markdown("---")  
st.info("Supports any CSV dataset.")

---------------- MAIN ----------------

if uploaded_file is not None:

try:  
    df = pd.read_csv(uploaded_file)  

except Exception as e:  
    st.error(f"Error reading CSV file: {e}")  
    st.stop()  

# ---------- DATA CLEANING ----------  
if remove_duplicates:  
    before = len(df)  
    df = df.drop_duplicates()  
    after = len(df)  
    st.success(f"Removed {before - after} duplicate rows")  

if drop_missing:  
    before = len(df)  
    df = df.dropna()  
    after = len(df)  
    st.success(f"Removed {before - after} rows containing missing values")  

# ---------- TABS ----------  
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(  
    [  
        "📋 Data Preview",  
        "🔍 Search",  
        "🧹 Missing Values",  
        "📈 Statistics",  
        "📊 Visualizations",  
        "⬇️ Download"  
    ]  
)  

# ====================================================  
# TAB 1 - DATA PREVIEW  
# ====================================================  
with tab1:  

    st.subheader("Dataset Overview")  

    c1, c2, c3 = st.columns(3)  

    c1.metric("Rows", df.shape[0])  
    c2.metric("Columns", df.shape[1])  

    memory = df.memory_usage(deep=True).sum() / (1024 ** 2)  

    c3.metric("Memory Usage", f"{memory:.2f} MB")  

    st.markdown("---")  

    st.subheader("First 100 Rows")  

    st.dataframe(  
        df.head(100),  
        use_container_width=True  
    )  

    st.markdown("---")  

    col1, col2 = st.columns(2)  

    with col1:  
        st.subheader("Data Types")  

        dtype_df = pd.DataFrame(  
            df.dtypes,  
            columns=["Type"]  
        )  

        st.dataframe(  
            dtype_df,  
            use_container_width=True  
        )  

    with col2:  
        st.subheader("Null Count")  

        null_df = pd.DataFrame(  
            df.isnull().sum(),  
            columns=["Null Count"]  
        )  

        st.dataframe(  
            null_df,  
            use_container_width=True  
        )  

# ====================================================  
# TAB 2 - SEARCH  
# ====================================================  
with tab2:  

    st.subheader("Search Dataset")  

    search_term = st.text_input(  
        "Enter keyword to search"  
    )  

    if search_term:  

        filtered = df[  
            df.astype(str)  
            .apply(  
                lambda x: x.str.contains(  
                    search_term,  
                    case=False,  
                    na=False  
                )  
            )  
            .any(axis=1)  
        ]  

        st.write(f"Found {len(filtered)} matching rows")  

        st.dataframe(  
            filtered,  
            use_container_width=True  
        )  

# ====================================================  
# TAB 3 - MISSING VALUES  
# ====================================================  
with tab3:  

    st.subheader("Missing Value Analysis")  

    missing_count = df.isnull().sum()  

    missing_percent = (  
        df.isnull().mean() * 100  
    ).round(2)  

    missing_df = pd.DataFrame({  
        "Missing Count": missing_count,  
        "Missing %": missing_percent  
    })  

    missing_df = missing_df[  
        missing_df["Missing Count"] > 0  
    ]  

    if len(missing_df) > 0:  

        st.dataframe(  
            missing_df,  
            use_container_width=True  
        )  

        fig = px.bar(  
            missing_df.reset_index(),  
            x="index",  
            y="Missing %",  
            title="Missing Percentage by Column",  
            labels={"index": "Column"}  
        )  

        fig.update_layout(  
            xaxis_tickangle=-45  
        )  

        st.plotly_chart(  
            fig,  
            use_container_width=True  
        )  

    else:  
        st.success(  
            "✅ No Missing Values Found"  
        )  

# ====================================================  
# TAB 4 - STATISTICS  
# ====================================================  
with tab4:  

    st.subheader("Descriptive Statistics")  

    st.dataframe(  
        df.describe(include="all").T,  
        use_container_width=True  
    )  

    st.markdown("---")  

    st.subheader("Correlation Heatmap")  

    numeric_df = df.select_dtypes(  
        include=[np.number]  
    )  

    if numeric_df.shape[1] > 1:  

        corr = numeric_df.corr()  

        fig = px.imshow(  
            corr,  
            text_auto=".2f",  
            aspect="auto",  
            color_continuous_scale="RdBu",  
            title="Correlation Matrix"  
        )  

        st.plotly_chart(  
            fig,  
            use_container_width=True  
        )  

    else:  
        st.warning(  
            "Need at least 2 numeric columns."  
        )  

# ====================================================  
# TAB 5 - VISUALIZATIONS  
# ====================================================  
with tab5:  

    st.subheader("Interactive Visualizations")  

    num_cols = df.select_dtypes(  
        include=[np.number]  
    ).columns.tolist()  

    cat_cols = df.select_dtypes(  
        include=["object", "category"]  
    ).columns.tolist()  

    # HISTOGRAM  
    st.markdown("### Histogram")  

    if num_cols:  

        hist_col = st.selectbox(  
            "Select Numeric Column",  
            num_cols,  
            key="hist"  
        )  

        bins = st.slider(  
            "Number of Bins",  
            10,  
            100,  
            30  
        )  

        fig = px.histogram(  
            df,  
            x=hist_col,  
            nbins=bins,  
            title=f"Distribution of {hist_col}"  
        )  

        st.plotly_chart(  
            fig,  
            use_container_width=True  
        )  

    # BOX PLOT  
    st.markdown("### Box Plot")  

    if num_cols:  

        box_col = st.selectbox(  
            "Box Plot Column",  
            num_cols,  
            key="box"  
        )  

        fig = px.box(  
            df,  
            y=box_col,  
            title=f"Box Plot - {box_col}"  
        )  

        st.plotly_chart(  
            fig,  
            use_container_width=True  
        )  

    # SCATTER PLOT  
    st.markdown("### Scatter Plot")  

    if len(num_cols) >= 2:  

        x_col = st.selectbox(  
            "X Axis",  
            num_cols,  
            key="scatterx"  
        )  

        y_col = st.selectbox(  
            "Y Axis",  
            num_cols,  
            key="scattery"  
        )  

        fig = px.scatter(  
            df,  
            x=x_col,  
            y=y_col,  
            title=f"{x_col} vs {y_col}"  
        )  

        st.plotly_chart(  
            fig,  
            use_container_width=True  
        )  

    # BAR CHART  
    if cat_cols:  

        st.markdown("### Bar Chart")  

        bar_col = st.selectbox(  
            "Categorical Column",  
            cat_cols,  
            key="bar"  
        )  

        top_n = st.slider(  
            "Top Categories",  
            5,  
            50,  
            10  
        )  

        vc = df[bar_col].value_counts().head(top_n)  

        fig = px.bar(  
            x=vc.index,  
            y=vc.values,  
            title=f"Top {top_n} Categories"  
        )  

        fig.update_layout(  
            xaxis_tickangle=-45  
        )  

        st.plotly_chart(  
            fig,  
            use_container_width=True  
        )  

    # PIE CHART  
    if cat_cols:  

        st.markdown("### Pie Chart")  

        pie_col = st.selectbox(  
            "Pie Chart Column",  
            cat_cols,  
            key="pie"  
        )  

        pie_top = st.slider(  
            "Top Categories for Pie",  
            3,  
            20,  
            10  
        )  

        pie_data = (  
            df[pie_col]  
            .value_counts()  
            .head(pie_top)  
        )  

        fig = px.pie(  
            values=pie_data.values,  
            names=pie_data.index,  
            title=f"Pie Chart - {pie_col}"  
        )  

        st.plotly_chart(  
            fig,  
            use_container_width=True  
        )  

# ====================================================  
# TAB 6 - DOWNLOAD  
# ====================================================  
with tab6:  

    st.subheader("Download Processed Dataset")  

    csv = df.to_csv(  
        index=False  
    ).encode("utf-8")  

    st.download_button(  
        label="📥 Download CSV",  
        data=csv,  
        file_name="processed_data.csv",  
        mime="text/csv"  
    )  

    buffer = BytesIO()  

    with pd.ExcelWriter(  
        buffer,  
        engine="openpyxl"  
    ) as writer:  

        df.to_excel(  
            writer,  
            index=False,  
            sheet_name="Data"  
        )  

    st.download_button(  
        label="📥 Download Excel",  
        data=buffer.getvalue(),  
        file_name="processed_data.xlsx",  
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"  
    )

else:

st.info(  
    "👈 Upload a CSV file from the sidebar to begin."  
)  

st.markdown(  
    """

Features Included

✅ CSV Upload

✅ Dataset Preview

✅ Search Records

✅ Missing Value Analysis

✅ Remove Duplicates

✅ Drop Missing Values

✅ Descriptive Statistics

✅ Correlation Heatmap

✅ Histogram

✅ Box Plot

✅ Scatter Plot

✅ Bar Chart

✅ Pie Chart

✅ CSV Download

✅ Excel Download

✅ Responsive Dashboard
"""
)