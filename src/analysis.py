import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# -----------------------------------------
# 1. CREATE VISUALIZATION FOLDER
# -----------------------------------------

os.makedirs("visualizations", exist_ok=True)


# -----------------------------------------
# 2. LOAD DATASET
# -----------------------------------------

file_path = "data/retail_sales.csv"

df = pd.read_csv(file_path)

print("\n========== DATASET LOADED ==========")
print(df.head())


# -----------------------------------------
# 3. BASIC DATASET INFORMATION
# -----------------------------------------

print("\n========== DATASET SHAPE ==========")
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])

print("\n========== COLUMN NAMES ==========")
print(df.columns.tolist())

print("\n========== DATA TYPES ==========")
print(df.dtypes)

print("\n========== DATASET INFO ==========")
print(df.info())


# -----------------------------------------
# 4. CHECK MISSING VALUES
# -----------------------------------------

print("\n========== MISSING VALUES ==========")

missing_values = df.isnull().sum()

print(missing_values)


# -----------------------------------------
# 5. CHECK DUPLICATES
# -----------------------------------------

print("\n========== DUPLICATE ROWS ==========")

duplicates = df.duplicated().sum()

print("Duplicate rows:", duplicates)


# -----------------------------------------
# 6. REMOVE DUPLICATES
# -----------------------------------------

df = df.drop_duplicates()


# -----------------------------------------
# 7. CONVERT DATE COLUMN
# -----------------------------------------

if "Date" in df.columns:
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")


# -----------------------------------------
# 8. HANDLE MISSING VALUES
# -----------------------------------------

numeric_columns = df.select_dtypes(include=np.number).columns

for column in numeric_columns:
    df[column] = df[column].fillna(df[column].median())


categorical_columns = df.select_dtypes(include="object").columns

for column in categorical_columns:
    if not df[column].mode().empty:
        df[column] = df[column].fillna(df[column].mode()[0])


# -----------------------------------------
# 9. STATISTICAL SUMMARY
# -----------------------------------------

print("\n========== STATISTICAL SUMMARY ==========")

print(df.describe())


# -----------------------------------------
# 10. TOTAL SALES
# -----------------------------------------

if "Total Amount" in df.columns:

    total_sales = df["Total Amount"].sum()

    average_sales = df["Total Amount"].mean()

    maximum_sale = df["Total Amount"].max()

    minimum_sale = df["Total Amount"].min()

    print("\n========== SALES SUMMARY ==========")

    print("Total Sales:", total_sales)
    print("Average Transaction:", average_sales)
    print("Highest Transaction:", maximum_sale)
    print("Lowest Transaction:", minimum_sale)


# -----------------------------------------
# 11. SALES BY PRODUCT CATEGORY
# -----------------------------------------

if "Product Category" in df.columns:

    category_sales = (
        df.groupby("Product Category")["Total Amount"]
        .sum()
        .sort_values(ascending=False)
    )

    print("\n========== SALES BY CATEGORY ==========")

    print(category_sales)


    plt.figure(figsize=(10, 6))

    category_sales.plot(kind="bar")

    plt.title("Total Sales by Product Category")

    plt.xlabel("Product Category")

    plt.ylabel("Total Sales")

    plt.xticks(rotation=45)

    plt.tight_layout()

    plt.savefig(
        "visualizations/sales_by_category.png",
        dpi=300
    )

    plt.show()


# -----------------------------------------
# 12. SALES BY GENDER
# -----------------------------------------

if "Gender" in df.columns:

    gender_sales = (
        df.groupby("Gender")["Total Amount"]
        .sum()
        .sort_values(ascending=False)
    )

    print("\n========== SALES BY GENDER ==========")

    print(gender_sales)


    plt.figure(figsize=(8, 6))

    gender_sales.plot(
        kind="pie",
        autopct="%1.1f%%"
    )

    plt.title("Sales Distribution by Gender")

    plt.ylabel("")

    plt.tight_layout()

    plt.savefig(
        "visualizations/sales_by_gender.png",
        dpi=300
    )

    plt.show()


# -----------------------------------------
# 13. AGE DISTRIBUTION
# -----------------------------------------

if "Age" in df.columns:

    plt.figure(figsize=(10, 6))

    plt.hist(
        df["Age"],
        bins=10
    )

    plt.title("Customer Age Distribution")

    plt.xlabel("Age")

    plt.ylabel("Number of Customers")

    plt.tight_layout()

    plt.savefig(
        "visualizations/customer_age_distribution.png",
        dpi=300
    )

    plt.show()


# -----------------------------------------
# 14. QUANTITY DISTRIBUTION
# -----------------------------------------

if "Quantity" in df.columns:

    plt.figure(figsize=(10, 6))

    sns.histplot(
        df["Quantity"],
        bins=10,
        kde=True
    )

    plt.title("Quantity Distribution")

    plt.xlabel("Quantity Purchased")

    plt.ylabel("Frequency")

    plt.tight_layout()

    plt.savefig(
        "visualizations/quantity_distribution.png",
        dpi=300
    )

    plt.show()


# -----------------------------------------
# 15. SALES BY AGE
# -----------------------------------------

if "Age" in df.columns and "Total Amount" in df.columns:

    age_sales = (
        df.groupby("Age")["Total Amount"]
        .sum()
    )

    plt.figure(figsize=(12, 6))

    age_sales.plot()

    plt.title("Sales by Customer Age")

    plt.xlabel("Age")

    plt.ylabel("Total Sales")

    plt.grid(True)

    plt.tight_layout()

    plt.savefig(
        "visualizations/sales_by_age.png",
        dpi=300
    )

    plt.show()


# -----------------------------------------
# 16. MONTHLY SALES TREND
# -----------------------------------------

if "Date" in df.columns and "Total Amount" in df.columns:

    df["Month"] = df["Date"].dt.to_period("M")

    monthly_sales = (
        df.groupby("Month")["Total Amount"]
        .sum()
    )

    print("\n========== MONTHLY SALES ==========")

    print(monthly_sales)


    plt.figure(figsize=(12, 6))

    monthly_sales.plot(
        marker="o"
    )

    plt.title("Monthly Sales Trend")

    plt.xlabel("Month")

    plt.ylabel("Total Sales")

    plt.xticks(rotation=45)

    plt.grid(True)

    plt.tight_layout()

    plt.savefig(
        "visualizations/monthly_sales_trend.png",
        dpi=300
    )

    plt.show()


# -----------------------------------------
# 17. CORRELATION ANALYSIS
# -----------------------------------------

numeric_data = df.select_dtypes(
    include=np.number
)

correlation_matrix = numeric_data.corr()

print("\n========== CORRELATION MATRIX ==========")

print(correlation_matrix)


plt.figure(figsize=(10, 7))

sns.heatmap(
    correlation_matrix,
    annot=True,
    cmap="coolwarm",
    fmt=".2f"
)

plt.title("Correlation Heatmap")

plt.tight_layout()

plt.savefig(
    "visualizations/correlation_heatmap.png",
    dpi=300
)

plt.show()


# -----------------------------------------
# 18. QUANTITY VS TOTAL SALES
# -----------------------------------------

if "Quantity" in df.columns and "Total Amount" in df.columns:

    plt.figure(figsize=(10, 6))

    sns.scatterplot(
        data=df,
        x="Quantity",
        y="Total Amount"
    )

    plt.title(
        "Relationship Between Quantity and Total Sales"
    )

    plt.xlabel("Quantity")

    plt.ylabel("Total Amount")

    plt.tight_layout()

    plt.savefig(
        "visualizations/quantity_vs_sales.png",
        dpi=300
    )

    plt.show()


# -----------------------------------------
# 19. TOP TRANSACTIONS
# -----------------------------------------

if "Total Amount" in df.columns:

    top_transactions = df.sort_values(
        by="Total Amount",
        ascending=False
    ).head(10)

    print("\n========== TOP 10 TRANSACTIONS ==========")

    print(top_transactions)


# -----------------------------------------
# 20. FINAL DATASET
# -----------------------------------------

print("\n========== FINAL DATASET ==========")

print("Rows after cleaning:", len(df))

print("Columns:", len(df.columns))

print("\nAnalysis completed successfully!")

print(
    "\nGraphs have been saved inside the "
    "'visualizations' folder."
)