import streamlit as st
import pandas as pd
import psycopg2
import plotly.express as px
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import seaborn as sns
import sys

# Database Connection Details
db_name = "postgres"
username = "postgres"
password = "admin"
host = "localhost"
port = "5432"

# Connect to PostgreSQL
engine = create_engine(f'postgresql://{username}:{password}@{host}:{port}/{db_name}')

# Display in Streamlit
st.title("Sales Dashboard")

# Query Data
query = "SELECT * FROM emp_table;"  # Use your actual table name
df = pd.read_sql(query, con=engine)

st.markdown("This dashboard presents visualizations from the cleaned and transformed dataset. The goal is to derive insights and identify the main factors affecting sales—whether product type, price, location, or other influences.")
# Show Data Table
st.write("Sales Data", df)

# Compute correlation
correlation = df[['Price Each', 'Quantity Ordered']].corr().iloc[0, 1]
st.markdown("### Price vs Quantity Ordered")
st.markdown("The plot below explores the relationship between product prices and the quantity ordered. This helps us determine if pricing significantly affects purchasing behavior.")
# Scatter Plot
fig, ax = plt.subplots()
sns.regplot(x=df["Price Each"], y=df["Quantity Ordered"], ax=ax)
ax.set_title("Price vs Quantity Ordered")
st.pyplot(fig)

st.write(f"Correlation between Price and Quantity Ordered: {correlation:.2f}")



# Interpretation
if correlation > 0:
    st.write("🔼 Higher prices tend to increase quantity ordered.")
elif correlation < 0:
    st.write("🔽 Higher prices tend to decrease quantity ordered.")
else:
    st.write("⚖️ No strong relationship between price and quantity ordered.")

# Define a threshold (e.g., negative correlation)
if correlation < -0.5:
    df["Price Impact"] = "High Impact"
elif -0.5 <= correlation <= 0.5:
    df["Price Impact"] = "Moderate Impact"
else:
    df["Price Impact"] = "Low Impact"

# Show result
st.write(df[["Product", "Price Each", "Quantity Ordered", "Price Impact"]].head(10))
st.markdown("### Key Insight: Does Price Affect Sales?")
st.markdown("Although the chart suggests that higher prices tend to decrease the quantity ordered, the difference is minimal compared to the price gap. This suggests that quantity alone may not be a strong determinant of total sales. Let’s explore another factor.")

st.markdown("### Sales by City")
st.markdown("Here, we analyze the impact of location on purchasing power. Busier cities with stronger economies may contribute to higher sales. We compare sales across cities to determine whether location is an important factor for the company.")

# Group by City and Sum Sales
sales_by_city = df.groupby("City")["Sales"].sum().reset_index()

# Sort for better visualization
sales_by_city = sales_by_city.sort_values(by="Sales", ascending=False)

# Plot Bar Chart
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x="City", y="Sales", data=sales_by_city, palette="Blues", ax=ax)

ax.set_title("Total Sales by City", fontsize=14)
ax.set_ylabel("Total Sales ($)", fontsize=12)
ax.set_xlabel("City", fontsize=12)
plt.xticks(rotation=45)  # Rotate city names for readability

st.markdown("### Key Insight: Does Price Affect Sales?")
st.markdown("Although the chart suggests that higher prices tend to decrease the quantity ordered, the difference is minimal compared to the price gap. This suggests that quantity alone may not be a strong determinant of total sales. Let’s explore another factor.")


# Show in Streamlit
st.pyplot(fig)
st.markdown("### Sales Growth by City")
st.markdown("This chart illustrates how sales vary across cities. San Francisco emerges as the city with the highest sales. The next question is: Is this due to more customers in San Francisco or the popularity of specific products? Since we lack customer data, we will determine the top-selling product in each city.")

sales_by_product = df.groupby("Product")["Sales"].sum().reset_index()

# Sort by Sales for better visualization
sales_by_product = sales_by_product.sort_values(by="Sales", ascending=False)

# Display results
st.markdown("### Highest Selling Product")

# Sidebar Filter
st.sidebar.header("Filters")
selected_city = st.sidebar.selectbox("Select City", df["City"].unique())

# Filter Data
df_filtered = df[df["City"] == selected_city]

# Create a Sales Chart
fig_sales = px.bar(df_filtered, x="Product", y="Sales", 
                   title=f"Top Selling Products in {selected_city}",
                   color="Sales")

st.plotly_chart(fig_sales)

# Show Data Table
st.write("Filtered Data", df_filtered)
st.markdown("### Top-Selling Product by City")
st.markdown("The best-selling product overall is the **MacBook Pro Laptop**. The company generates more revenue from selling MacBooks than lower-priced items such as 'AAA Batteries (4-pack).'This suggests that San Francisco residents have higher purchasing power. Focusing on MacBook sales in this city could further increase revenue.")

