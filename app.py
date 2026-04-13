import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans

st.set_page_config(layout="wide", initial_sidebar_state="expanded")

st.title("📊 Customer Segmentation Dashboard")

uploaded_file = st.file_uploader("Upload your dataset", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # 🔥 SIDEBAR
    st.sidebar.header("Filter Options")

    #gender = st.sidebar.selectbox("Select Gender", df["Gender"].unique()
    gender = st.sidebar.multiselect(
        "Select Gender",
        df["Gender"].unique(),
        default=df["Gender"].unique()
       )
    if gender:
            filtered_df = df[df["Gender"].isin(gender)]
    else:
            filtered_df = df

    age_range = st.sidebar.slider(
        "Select Age Range",
        int(df["Age"].min()),
        int(df["Age"].max()),
        (int(df["Age"].min()), int(df["Age"].max()))
    )
    income_range = st.sidebar.slider(
        "Select Income Range",
        int(df["Annual Income (k$)"].min()),
        int(df["Annual Income (k$)"].max()),
        (int(df["Annual Income (k$)"].min()), int(df["Annual Income (k$)"].max()))
    	)
    st.sidebar.markdown("Filters Applied")
    st.sidebar.write(f"Gender: {gender}")
    st.sidebar.write(f"Age: {age_range}")
    st.sidebar.write(f"Income: {income_range}")
	
    # 🔥 FILTER LOGIC
    filtered_df = df.copy()

    # Gender filter
    if gender:
        filtered_df = filtered_df[filtered_df["Gender"].isin(gender)]

    # Age filter
    filtered_df = filtered_df[
         (filtered_df["Age"] >= age_range[0]) &
         (filtered_df["Age"] <= age_range[1])
    ]

    # Income filter
    filtered_df = filtered_df[
         (filtered_df["Annual Income (k$)"] >= income_range[0]) &
         (filtered_df["Annual Income (k$)"] <= income_range[1])
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

    from sklearn.cluster import KMeans

    # Clustering on filtered data
    X = filtered_df[['Annual Income (k$)', 'Spending Score (1-100)']]
    
    #kmeans = KMeans(n_clusters=5, random_state=42)
    kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)
    filtered_df['Cluster'] = kmeans.fit_predict(X)
    st.subheader("🧠 Customer Segments (Income vs Spending)")

    fig, ax = plt.subplots(figsize=(6, 4))

    sns.scatterplot(
   	 x='Annual Income (k$)',
    	 y='Spending Score (1-100)',
    	 hue='Cluster',
   	 data=filtered_df,
          palette='Set2',   # softer colors
   	 s=80,             # bigger dots
          edgecolor='black'
	)

    plt.title("Customer Segmentation", fontsize=14)
    plt.xlabel("Annual Income")
    plt.ylabel("Spending Score")

    plt.legend(title="Cluster", bbox_to_anchor=(1.05, 1), loc='upper left')

    st.pyplot(fig)

    cluster_summary = filtered_df.groupby('Cluster')[
    [ 'Age','Annual Income (k$)', 'Spending Score (1-100)']
    ].mean()

    st.subheader("📊 Cluster Summary")

   
    st.dataframe(cluster_summary)
    st.subheader("🎯 Target Customer Strategy")

    for i in range(5):
       cluster_data = filtered_df[filtered_df['Cluster'] == i]

       avg_income = cluster_data['Annual Income (k$)'].mean()
       avg_spending = cluster_data['Spending Score (1-100)'].mean()

       if avg_income > 60 and avg_spending > 60:
         st.success(f"Cluster {i}: High value customers 💰")
       elif avg_income < 40 and avg_spending > 60:
         st.info(f"Cluster {i}: Discount seekers 🎯")
       elif avg_income > 60 and avg_spending < 40:
         st.warning(f"Cluster {i}: Needs engagement ⚠️")
       else:
         st.write(f"Cluster {i}: Average customers")

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