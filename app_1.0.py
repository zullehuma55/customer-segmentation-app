import streamlit as st
import pandas as pd

st.set_page_config(layout="wide", initial_sidebar_state="expanded")

st.title("📊 Customer Segmentation Dashboard")

uploaded_file = st.file_uploader("Upload your dataset", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # 🔥 SIDEBAR
    st.sidebar.header("Filter Options")

    gender = st.sidebar.selectbox("Select Gender", df["Gender"].unique())

    age_range = st.sidebar.slider(
        "Select Age Range",
        int(df["Age"].min()),
        int(df["Age"].max()),
        (int(df["Age"].min()), int(df["Age"].max()))
    )

    # 🔥 FILTER LOGIC
    filtered_df = df[
        (df["Gender"] == gender) &
        (df["Age"] >= age_range[0]) &
        (df["Age"] <= age_range[1])
    ]

    # 🔥 KPI SECTION
    st.markdown("## 📌 Key Insights")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Customers", len(filtered_df))
    col2.metric("Average Age", round(filtered_df["Age"].mean(), 1))
    col3.metric("Avg Spending Score", round(filtered_df["Spending Score (1-100)"].mean(), 1))

    # 🔥 CHART SECTION (side by side)
    st.markdown("## 📊 Visual Analysis")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Age Distribution")
        #age_counts = filtered_df["Age"].value_counts().sort_index()
        #st.bar_chart(age_counts)

        bins = [0, 20, 30, 40, 50, 60, 100]
        labels = ["0-20", "20-30", "30-40", "40-50", "50-60", "60+"]

        filtered_df["Age Group"] = pd.cut(filtered_df["Age"], bins=bins, labels=labels)
        age_group_counts = filtered_df["Age Group"].value_counts().sort_index()
        st.bar_chart(age_group_counts)

    with col2:
        st.subheader("Income vs Spending")
        st.scatter_chart(
            filtered_df,
            x="Annual Income (k$)",
            y="Spending Score (1-100)"
        )

    # 🔥 DATA SECTION
    st.markdown("## 📄 Data Preview")
    st.dataframe(filtered_df)

    # 🔥 DOWNLOAD BUTTON
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        "Download Filtered Data",
        data=csv,
        file_name="filtered_data.csv",
        mime="text/csv"
    )

else:
    st.info("Please upload a CSV file to continue")