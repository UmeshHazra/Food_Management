import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# -----------------------------------------------------
# PAGE CONFIG
# -----------------------------------------------------

st.set_page_config(
    page_title="Food Wastage Management Dashboard",
    page_icon="🍲",
    layout="wide"
)

# -----------------------------------------------------
# CUSTOM CSS
# -----------------------------------------------------

st.markdown("""
<style>

.main{
    background-color:#F5F7FA;
}

.metric-card{
    padding:20px;
    border-radius:15px;
    color:white;
    text-align:center;
    font-size:18px;
    font-weight:bold;
}

.card1{
    background:linear-gradient(135deg,#667eea,#764ba2);
}

.card2{
    background:linear-gradient(135deg,#f093fb,#f5576c);
}

.card3{
    background:linear-gradient(135deg,#4facfe,#00f2fe);
}

.card4{
    background:linear-gradient(135deg,#43e97b,#38f9d7);
}

</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------
# LOAD DATA
# -----------------------------------------------------

# CHANGE PATHS IF REQUIRED

providers = pd.read_csv("clean_providers_data.csv")
receivers = pd.read_csv("clean_receivers_data.csv")
food = pd.read_csv("food_listings_data.csv")
claims = pd.read_csv("claims_data.csv")

# -----------------------------------------------------
# HEADER
# -----------------------------------------------------

st.markdown("""
<h1 style='text-align:center'>
🍲 Local Food Wastage Management System
</h1>

<h4 style='text-align:center;color:gray'>
Reduce Food Waste | Feed Communities | Data Analytics Dashboard
</h4>
""", unsafe_allow_html=True)

st.markdown("---")

# -----------------------------------------------------
# SIDEBAR
# -----------------------------------------------------

with st.sidebar.popover("🏙 Select Cities"):
    city_filter = st.multiselect(
        "Choose City",
        options=sorted(food["Location"].unique()),
        default=sorted(food["Location"].unique())
    )

provider_filter = st.sidebar.multiselect(
    "Provider Type",
    options=food["Provider_Type"].unique(),
    default=food["Provider_Type"].unique()
)

food_filter = st.sidebar.multiselect(
    "Food Type",
    options=food["Food_Type"].unique(),
    default=food["Food_Type"].unique()
)

meal_filter = st.sidebar.multiselect(
    "Meal Type",
    options=food["Meal_Type"].unique(),
    default=food["Meal_Type"].unique()
)

# -----------------------------------------------------
# FILTERED DATA
# -----------------------------------------------------

filtered_food = food[
    (food["Location"].isin(city_filter)) &
    (food["Provider_Type"].isin(provider_filter)) &
    (food["Food_Type"].isin(food_filter)) &
    (food["Meal_Type"].isin(meal_filter))
]

# -----------------------------------------------------
# KPIs
# -----------------------------------------------------

total_food = filtered_food["Quantity"].sum()
total_providers = providers["Provider_ID"].nunique()
total_receivers = receivers["Receiver_ID"].nunique()
total_claims = claims["Claim_ID"].nunique()

col1,col2,col3,col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card card1">
    🍛<br>
    Total Food<br>
    {total_food}
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card card2">
    🏢<br>
    Providers<br>
    {total_providers}
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card card3">
    🤝<br>
    Receivers<br>
    {total_receivers}
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card card4">
    📦<br>
    Claims<br>
    {total_claims}
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# -----------------------------------------------------
# TABS
# -----------------------------------------------------

tab1,tab2,tab3,tab4 = st.tabs(
    [
        "📊 Dashboard",
        "🍲 Food Listings",
        "📈 Analysis",
        "💡 Insights"
    ]
)

# =====================================================
# DASHBOARD TAB
# =====================================================

with tab1:

    col1,col2 = st.columns(2)

    with col1:

        fig1 = px.pie(
            filtered_food,
            names="Food_Type",
            hole=0.5,
            title="Food Type Distribution",
            color_discrete_sequence=px.colors.qualitative.Bold
        )

        st.plotly_chart(fig1,use_container_width=True)

    with col2:

        fig2 = px.pie(
            filtered_food,
            names="Meal_Type",
            hole=0.5,
            title="Meal Type Distribution",
            color_discrete_sequence=px.colors.qualitative.Set3
        )

        st.plotly_chart(fig2,use_container_width=True)

    city_food = filtered_food.groupby(
        "Location"
    ).size().reset_index(name="Listings")

    fig3 = px.bar(
    city_food,
    x="Location",
    y="Listings",
    color="Listings",
    text="Listings",
    title="Food Listings by City",
    color_continuous_scale="Turbo",
    hover_data={
        "Location": True,
        "Listings": ":,.0f"
    }
)

fig3.update_traces(
    textposition="outside"
)

fig3.update_layout(
    hovermode="x unified"
)

st.plotly_chart(fig3,use_container_width=True)

# =====================================================
# FOOD LISTINGS TAB
# =====================================================

with tab2:

    st.subheader("Available Food Listings")

    st.dataframe(
        filtered_food,
        use_container_width=True,
        height=500
    )

    st.subheader("Provider Contact Details")

    city_select = st.selectbox(
        "Select City",
        providers["City"].unique()
    )

    provider_contact = providers[
        providers["City"] == city_select
    ]

    st.dataframe(
        provider_contact,
        use_container_width=True
    )

# =====================================================
# ANALYSIS TAB
# =====================================================

with tab3:

    col1,col2 = st.columns(2)

    with col1:

        provider_qty = filtered_food.groupby(
            "Provider_Type"
        )["Quantity"].sum().reset_index()

        fig4 = px.bar(
            provider_qty,
            x="Provider_Type",
            y="Quantity",
            color="Quantity",
            title="Provider Type vs Quantity",
            color_continuous_scale="Viridis"
        )

        st.plotly_chart(fig4,use_container_width=True)

    with col2:

        meal_qty = filtered_food.groupby(
            "Meal_Type"
        )["Quantity"].sum().reset_index()

        fig5 = px.bar(
            meal_qty,
            x="Meal_Type",
            y="Quantity",
            color="Quantity",
            title="Meal Type vs Quantity",
            color_continuous_scale="Plasma"
        )

        st.plotly_chart(fig5,use_container_width=True)

    claim_status = claims.groupby(
        "Status"
    ).size().reset_index(name="Count")

    fig6 = px.bar(
        claim_status,
        x="Status",
        y="Count",
        color="Count",
        title="Claim Status Analysis"
    )

    st.plotly_chart(fig6,use_container_width=True)

    # Top Providers

    top_providers = filtered_food.groupby(
        "Provider_ID"
    )["Quantity"].sum().reset_index()

    top_providers = top_providers.sort_values(
        "Quantity",
        ascending=False
    ).head(10)

    fig7 = px.bar(
        top_providers,
        x="Provider_ID",
        y="Quantity",
        color="Quantity",
        title="Top 10 Providers"
    )

    st.plotly_chart(fig7,use_container_width=True)

# =====================================================
# INSIGHTS TAB
# =====================================================

with tab4:

    st.subheader("Business Insights")

    highest_food_city = city_food.sort_values(
        "Listings",
        ascending=False
    ).iloc[0]["Location"]

    highest_provider = top_providers.iloc[0]["Provider_ID"]

    col1,col2,col3 = st.columns(3)

    with col1:
        st.success(
            f"Highest Food Availability City: {highest_food_city}"
        )

    with col2:
        st.info(
            f"Top Provider ID: {highest_provider}"
        )

    with col3:
        st.warning(
            f"Total Claims: {total_claims}"
        )

    # Gauge Chart

    completed = len(
        claims[
            claims["Status"].astype(str).str.lower() == "completed"
        ]
    )

    total = len(claims)

    percentage = (
        completed / total * 100
        if total > 0 else 0
    )

    gauge = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=percentage,
            title={"text":"Completed Claims %"},
            gauge={
                "axis":{"range":[0,100]}
            }
        )
    )

    st.plotly_chart(
        gauge,
        use_container_width=True
    )

st.markdown("---")
st.caption("Built with Python | SQL | Streamlit | Plotly")