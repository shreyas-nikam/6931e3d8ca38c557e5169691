id: 6931e3d8ca38c557e5169691_documentation
summary: AI Design and deployment lab 5 - Clone Documentation
feedback link: https://docs.google.com/forms/d/e/1FAIpQLSfWkOK-in_bMMoHSZfcIvAeO58PAH9wrDqcxnJABHaxiDqhSA/viewform?usp=sf_link
environments: Web
status: Published
# Interactive Data Science Dashboard with Streamlit

## Introduction to the Interactive Data Science Dashboard
Duration: 0:05

Welcome to this codelab, where you will explore and understand the architecture and functionalities of an Interactive Data Science Dashboard built with Streamlit. This application empowers users to perform exploratory data analysis (EDA) and even build machine learning models with an intuitive, no-code/low-code interface.

In today's data-driven world, the ability to quickly visualize data, understand its underlying patterns, and prototype machine learning solutions is crucial. Traditional methods often require deep programming knowledge, creating a barrier for domain experts and non-technical users. This Streamlit application addresses this challenge by providing an interactive web interface that simplifies complex data science workflows.

<aside class="positive">
<b>Streamlit</b> is an open-source Python library that makes it incredibly easy to create custom web apps for machine learning and data science. You can turn data scripts into shareable web apps in minutes, all in pure Python.
</aside>

### Why is this application important?

*   **Democratization of Data Science:** It makes powerful data analysis and machine learning tools accessible to a broader audience, including business analysts, researchers, and students, without needing extensive coding skills.
*   **Rapid Prototyping:** Data scientists and developers can quickly prototype ideas, visualize datasets, and test different ML models, accelerating the development lifecycle.
*   **Interactive Exploration:** Users can dynamically interact with their data, filter, visualize, and configure model parameters, leading to deeper insights.
*   **Educational Tool:** It serves as an excellent example for understanding the basics of data processing, visualization, and machine learning concepts in a practical, hands-on manner.

### Key Concepts Explained in this Codelab:

*   **Streamlit Fundamentals:** Setting up pages, using widgets (sliders, select boxes, file uploader), managing session state.
*   **Data Handling with Pandas:** Reading CSVs, displaying dataframes, generating summary statistics, checking for missing values.
*   **Data Visualization with Matplotlib & Seaborn:** Creating histograms, scatter plots, and box plots dynamically.
*   **Machine Learning Workflow (Conceptual):** Understanding data preprocessing (missing value imputation, categorical encoding), feature selection, model training, and evaluation.

### Application Architecture Overview

The application follows a client-server model typical for Streamlit apps. The user interacts with the web interface (client), which sends requests to the Streamlit Python backend (server). The backend processes data using libraries like Pandas, generates visualizations with Matplotlib/Seaborn, and conceptually handles ML model building, then sends updates back to the client.

Here's a high-level architectural diagram:

```mermaid
graph TD
    A[User Browser] --> B(Streamlit Web UI);
    B --> C{Streamlit Server - Python Application};
    C --> D[Data Processing - Pandas];
    C --> E[Data Visualization - Matplotlib/Seaborn];
    C --> F[ML Model Building - Scikit-learn (Conceptual)];
    D --> C;
    E --> C;
    F --> C;
    C --> B;
```

*   **User Browser:** The client-side interface where users interact with the Streamlit application.
*   **Streamlit Web UI:** Rendered by Streamlit, it provides the interactive widgets and displays.
*   **Streamlit Server - Python Application:** The core Python script running the Streamlit app. It handles all backend logic.
*   **Data Processing (Pandas):** Manages data loading, manipulation, and summary statistics.
*   **Data Visualization (Matplotlib/Seaborn):** Generates plots based on user selections.
*   **ML Model Building (Scikit-learn - Conceptual):** Placeholder for future implementation of actual ML pipelines.

## Setting Up Your Development Environment
Duration: 0:05

To run this Streamlit application, you'll need a Python environment configured with the necessary libraries.

### Prerequisites

*   Python 3.7+ installed on your system.
*   `pip`, Python's package installer.

### 1. Create a Virtual Environment (Recommended)

It's a good practice to use a virtual environment to manage dependencies for your projects.

```console
python -m venv streamlit_env
source streamlit_env/bin/activate  # On Linux/macOS
streamlit_env\Scripts\activate   # On Windows
```

### 2. Install Required Libraries

Once your virtual environment is active, install Streamlit and other data science libraries:

```console
pip install streamlit pandas numpy matplotlib seaborn scikit-learn
```

### 3. Save the Application Code

Create a file named `app.py` (or any other `.py` file) and paste the entire Streamlit application code into it.

```python
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set page config
st.set_page_config(page_title="Data Science Dashboard", page_icon="📊", layout="wide")

# Custom CSS for styling
st.markdown("""
<style>
.main-header {
    font-size: 3em;
    color: #4CAF50;
    text-align: center;
    margin-bottom: 30px;
}
.subheader {
    font-size: 2em;
    color: #2196F3;
    margin-top: 20px;
    margin-bottom: 15px;
}
.stRadio > label {
    font-size: 1.2em;
    font-weight: bold;
}
.sidebar .sidebar-content {
    background-color: #f0f2f6;
}
.stButton>button {
    background-color: #4CAF50;
    color: white;
    padding: 10px 20px;
    border-radius: 5px;
    border: none;
}
</style>
""", unsafe_allow_html=True)

# Initialize session state for data
if 'df' not in st.session_state:
    st.session_state['df'] = None

# Sidebar Navigation
st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Data Explorer", "ML Model Builder"])

if page == "Home":
    st.markdown("<h1 class='main-header'>Welcome to the Interactive Data Science Dashboard</h1>", unsafe_allow_html=True)
    st.write("""
    This interactive dashboard is designed to provide a comprehensive, no-code/low-code platform for data exploration,
    visualization, and machine learning model building. Whether you're a data scientist, analyst, or researcher,
    this tool aims to simplify your workflow and help you gain insights faster.
    """)

    st.image("https://www.streamlit.io/images/brand/streamlit-logo-secondary-colormark-light.png", width=300) # Placeholder for a relevant image

    st.markdown("<h2 class='subheader'>Key Features</h2>", unsafe_allow_html=True)
    st.write("""
    *   **Data Explorer:** Upload your CSV files, view raw data, get summary statistics, check for missing values, and create various interactive visualizations (histograms, scatter plots, box plots).
    *   **ML Model Builder:** (Conceptual) Prepare your data for machine learning, select features, choose from different model types, and train models (functionality to be fully implemented).
    """)

    st.markdown("<h2 class='subheader'>How It Works</h2>", unsafe_allow_html=True)
    st.write("""
    1.  **Upload:** Start by uploading your dataset in the 'Data Explorer' section.
    2.  **Explore:** Dive deep into your data with interactive tables and statistical summaries.
    3.  **Visualize:** Generate beautiful charts to uncover patterns and relationships.
    4.  **Build (Conceptual):** Navigate to the 'ML Model Builder' to preprocess data and train machine learning models.
    5.  **Analyze:** (Future) Evaluate model performance and interpret results.
    """)
    
    st.info("This dashboard leverages the power of Streamlit for interactive UI, Pandas for data manipulation, and Matplotlib/Seaborn for stunning visualizations.")


elif page == "Data Explorer":
    st.markdown("<h1 class='main-header'>Data Explorer</h1>", unsafe_allow_html=True)
    st.write("Upload your CSV file here to start exploring your data.")

    uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.session_state['df'] = df
        st.success("File uploaded successfully!")

        st.markdown("<h2 class='subheader'>Raw Data</h2>", unsafe_allow_html=True)
        st.dataframe(df)

        st.markdown("<h2 class='subheader'>Summary Statistics</h2>", unsafe_allow_html=True)
        st.write(df.describe())

        st.markdown("<h2 class='subheader'>Missing Values</h2>", unsafe_allow_html=True)
        st.write(df.isnull().sum())

        st.markdown("<h2 class='subheader'>Data Visualization</h2>", unsafe_allow_html=True)
        
        # Select chart type
        chart_type = st.selectbox("Select Chart Type", ["Histogram", "Scatter Plot", "Box Plot"])

        plt.figure(figsize=(10, 6)) # Create a new figure for each plot

        if chart_type == "Histogram":
            column = st.selectbox("Select Column for Histogram", df.columns)
            if df[column].dtype in ['int64', 'float64']:
                bins = st.slider("Number of Bins", min_value=5, max_value=50, value=20)
                plt.hist(df[column], bins=bins, edgecolor='black')
                plt.title(f'Histogram of {column}')
                plt.xlabel(column)
                plt.ylabel('Frequency')
                st.pyplot(plt)
            else:
                st.warning("Please select a numerical column for a Histogram.")
        
        elif chart_type == "Scatter Plot":
            x_column = st.selectbox("Select X-axis Column", df.columns)
            y_column = st.selectbox("Select Y-axis Column", df.columns)
            color_column = st.selectbox("Select Color Column (optional)", [None] + list(df.columns))

            if x_column and y_column:
                if color_column:
                    sns.scatterplot(x=df[x_column], y=df[y_column], hue=df[color_column])
                else:
                    sns.scatterplot(x=df[x_column], y=df[y_column])
                plt.title(f'Scatter Plot of {x_column} vs {y_column}')
                plt.xlabel(x_column)
                plt.ylabel(y_column)
                st.pyplot(plt)
            else:
                st.warning("Please select both X and Y axis columns.")

        elif chart_type == "Box Plot":
            column = st.selectbox("Select Column for Box Plot", df.columns)
            if df[column].dtype in ['int64', 'float64']:
                sns.boxplot(y=df[column])
                plt.title(f'Box Plot of {column}')
                plt.ylabel(column)
                st.pyplot(plt)
            else:
                st.warning("Please select a numerical column for a Box Plot.")
        plt.clf() # Clear the current figure to prevent plots from stacking

    else:
        st.info("Please upload a CSV file to proceed with data exploration.")


elif page == "ML Model Builder":
    st.markdown("<h1 class='main-header'>ML Model Builder</h1>", unsafe_allow_html=True)
    st.write("Prepare your data and build machine learning models.")

    if st.session_state['df'] is not None:
        df = st.session_state['df']
        st.dataframe(df.head())

        st.markdown("<h2 class='subheader'>Data Preprocessing</h2>", unsafe_allow_html=True)
        
        # Missing Value Imputation
        st.subheader("Handle Missing Values")
        missing_strategy = st.selectbox("Select Strategy", ["None", "Drop Rows", "Mean Imputation", "Median Imputation", "Mode Imputation"])
        if missing_strategy != "None":
            st.info(f"Selected strategy: {missing_strategy}. (Implementation for processing is pending.)")

        # Categorical Encoding
        st.subheader("Encode Categorical Features")
        encoding_strategy = st.selectbox("Select Encoding Method", ["None", "One-Hot Encoding", "Label Encoding"])
        if encoding_strategy != "None":
            st.info(f"Selected strategy: {encoding_strategy}. (Implementation for processing is pending.)")
            
        st.markdown("<h2 class='subheader'>Feature Selection</h2>", unsafe_allow_html=True)
        all_columns = df.columns.tolist()
        
        # Select features (X)
        features = st.multiselect("Select Features (X)", all_columns, default=all_columns)
        
        # Select target variable (y)
        target = st.selectbox("Select Target Variable (y)", all_columns)

        if not features:
            st.warning("Please select at least one feature.")
        elif not target:
            st.warning("Please select a target variable.")
        elif target in features:
            st.warning("Target variable cannot be among features. Please adjust your selection.")
        else:
            st.markdown("<h2 class='subheader'>Model Training</h2>", unsafe_allow_html=True)
            model_type = st.selectbox("Select Model Type", ["Linear Regression", "Logistic Regression", "Decision Tree Classifier", "Random Forest Classifier"])
            
            st.subheader("Train/Test Split Configuration")
            test_size = st.slider("Test Set Size", min_value=0.1, max_value=0.5, value=0.3, step=0.05)
            random_state = st.number_input("Random State", value=42, min_value=0)

            if st.button("Train Model"):
                st.info(f"Training {model_type} with features: {features}, target: {target}, test size: {test_size}, random state: {random_state}. (Actual training logic is pending.)")
                st.success("Model training initiated! (Results will appear here upon implementation.)")
                
                # Placeholder for model training and evaluation
                # from sklearn.model_selection import train_test_split
                # from sklearn.linear_model import LinearRegression, LogisticRegression
                # from sklearn.tree import DecisionTreeClassifier
                # from sklearn.ensemble import RandomForestClassifier
                # from sklearn.metrics import mean_squared_error, accuracy_score
                
                # try:
                #     X = df[features]
                #     y = df[target]

                #     # Basic handling of non-numeric data for simplicity in placeholder
                #     for col in X.columns:
                #         if X[col].dtype == 'object':
                #             X[col] = pd.factorize(X[col])[0]
                #     if y.dtype == 'object':
                #         y = pd.factorize(y)[0]

                #     X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)

                #     model = None
                #     if model_type == "Linear Regression":
                #         model = LinearRegression()
                #     elif model_type == "Logistic Regression":
                #         model = LogisticRegression(random_state=random_state)
                #     elif model_type == "Decision Tree Classifier":
                #         model = DecisionTreeClassifier(random_state=random_state)
                #     elif model_type == "Random Forest Classifier":
                #         model = RandomForestClassifier(random_state=random_state)

                #     if model:
                #         model.fit(X_train, y_train)
                #         y_pred = model.predict(X_test)

                #         st.markdown("<h3 class='subheader'>Model Evaluation</h3>", unsafe_allow_html=True)
                #         if model_type in ["Linear Regression"]:
                #             mse = mean_squared_error(y_test, y_pred)
                #             st.write(f"Mean Squared Error: {mse:.2f}")
                #         else: # Classification models
                #             accuracy = accuracy_score(y_test, y_pred)
                #             st.write(f"Accuracy: {accuracy:.2f}")
                #     else:
                #         st.error("Model type not recognized or implemented.")
                # except Exception as e:
                #     st.error(f"An error occurred during model training: {e}. Please ensure data is numeric or processed.")

    else:
        st.warning("Please upload a CSV file in the 'Data Explorer' section first to build models.")

```

### 4. Run the Application

Open your terminal, navigate to the directory where you saved `app.py`, and run:

```console
streamlit run app.py
```

This command will open the application in your default web browser (usually `http://localhost:8501`).

## Understanding the Application Structure
Duration: 0:10

The Streamlit application is organized into several key parts, demonstrating best practices for building multi-page dashboards.

### 1. Page Configuration

The `st.set_page_config` function is called at the very beginning to configure the Streamlit page's appearance.

```python
st.set_page_config(page_title="Data Science Dashboard", page_icon="📊", layout="wide")
```

*   `page_title`: Sets the title that appears in the browser tab.
*   `page_icon`: Sets the favicon for the page.
*   `layout="wide"`: Makes the application use the full width of the browser, which is ideal for data-heavy applications.

### 2. Custom CSS Styling

The application uses `st.markdown` with `unsafe_allow_html=True` to inject custom CSS. This allows for branding and enhancing the visual appeal beyond Streamlit's default styling.

```python
st.markdown("""
<style>
.main-header { /* ... styles ... */ }
.subheader { /* ... styles ... */ }
/* ... more styles ... */
</style>
""", unsafe_allow_html=True)
```

This technique is powerful for customizing fonts, colors, spacing, and component appearances.

### 3. Session State Management

`st.session_state` is crucial for maintaining data across reruns and different pages of the Streamlit application. Since Streamlit reruns the script from top to bottom on every user interaction, `st.session_state` provides a way to persist variables.

```python
if 'df' not in st.session_state:
    st.session_state['df'] = None
```

Here, `st.session_state['df']` is initialized to `None` if it doesn't already exist. This variable will store the DataFrame uploaded by the user, making it accessible across the "Data Explorer" and "ML Model Builder" pages.

<aside class="positive">
Using <b>st.session_state</b> is fundamental for building complex Streamlit applications where data needs to be shared or maintained across different user interactions or pages.
</aside>

### 4. Sidebar Navigation

The application uses a sidebar for navigation, allowing users to switch between different functionalities.

```python
st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Data Explorer", "ML Model Builder"])
```

*   `st.sidebar.header`: Adds a header to the sidebar.
*   `st.sidebar.radio`: Creates a set of radio buttons in the sidebar. The selected option is stored in the `page` variable, which then dictates which section of the application is rendered.

### 5. Conditional Rendering based on Navigation

The core of the multi-page structure relies on `if/elif` statements that check the value of the `page` variable.

```python
if page == "Home":
    # ... Home page content ...
elif page == "Data Explorer":
    # ... Data Explorer content ...
elif page == "ML Model Builder":
    # ... ML Model Builder content ...
```

This structure ensures that only the content relevant to the currently selected page is displayed, creating a smooth user experience.

### Application Flowchart

Here's a flowchart visualizing the application's overall navigation and data flow:

```mermaid
graph TD
    A[Start Application] --> B{Set Page Config & CSS};
    B --> C{Initialize Session State (df)};
    C --> D[Render Sidebar Navigation];
    D --> E{User Selects Page?};
    E -- Home --> F[Display Home Page Content];
    E -- Data Explorer --> G[Display Data Explorer Page];
    E -- ML Model Builder --> H[Display ML Model Builder Page];

    G --> G1{Upload File?};
    G1 -- Yes --> G2[Read CSV into DataFrame];
    G2 --> G3[Store DataFrame in st.session_state['df']];
    G3 --> G4[Display Raw Data, Summary, Missing Values];
    G4 --> G5[Render Visualization Widgets];
    G5 --> G6[Generate & Display Plots];

    H --> H1{Is df in session state?};
    H1 -- Yes --> H2[Display Data Head];
    H2 --> H3[Render Preprocessing Widgets];
    H3 --> H4[Render Feature Selection Widgets];
    H4 --> H5[Render Model Training Widgets];
    H5 -- Train Model Clicked --> H6[Conceptual Model Training & Evaluation];
    H1 -- No --> H7[Display Warning to Upload Data];
```

## The Home Page - Overview
Duration: 0:05

The "Home" page serves as an introduction to the application, providing users with an understanding of its purpose, features, and how to get started.

When `page == "Home"`, the following content is displayed:

### 1. Main Title and Introduction

A prominent title welcomes users, followed by a concise description of the dashboard's capabilities.

```python
st.markdown("<h1 class='main-header'>Welcome to the Interactive Data Science Dashboard</h1>", unsafe_allow_html=True)
st.write("""
This interactive dashboard is designed to provide a comprehensive, no-code/low-code platform for data exploration,
visualization, and machine learning model building. ...
""")
```
The `main-header` class is defined in the custom CSS to give the title a distinct look.

### 2. Placeholder Image

A placeholder image is included to visually enhance the home page. In a real application, this could be a custom logo or an illustrative graphic.

```python
st.image("https://www.streamlit.io/images/brand/streamlit-logo-secondary-colormark-light.png", width=300) # Placeholder for a relevant image
```

### 3. Key Features Section

This section outlines the primary functionalities offered by the dashboard, namely "Data Explorer" and "ML Model Builder."

```python
st.markdown("<h2 class='subheader'>Key Features</h2>", unsafe_allow_html=True)
st.write("""
*   **Data Explorer:** Upload your CSV files, view raw data, get summary statistics, ...
*   **ML Model Builder:** (Conceptual) Prepare your data for machine learning, select features, ...
""")
```
The `subheader` class provides consistent styling for section headings.

### 4. How It Works Section

A step-by-step guide helps users understand the typical workflow within the application. This ensures users can quickly grasp how to navigate and utilize the dashboard.

```python
st.markdown("<h2 class='subheader'>How It Works</h2>", unsafe_allow_html=True)
st.write("""
1.  **Upload:** Start by uploading your dataset in the 'Data Explorer' section.
2.  **Explore:** Dive deep into your data with interactive tables and statistical summaries.
3.  **Visualize:** Generate beautiful charts to uncover patterns and relationships.
4.  **Build (Conceptual):** Navigate to the 'ML Model Builder' to preprocess data and train machine learning models.
5.  **Analyze:** (Future) Evaluate model performance and interpret results.
""")
```

### 5. Informative Note

A small `st.info` box highlights the underlying technologies used, giving users context about the technical stack.

```python
st.info("This dashboard leverages the power of Streamlit for interactive UI, Pandas for data manipulation, and Matplotlib/Seaborn for stunning visualizations.")
```

This page serves as an excellent starting point, providing proper context before users dive into the application's core functionalities.

## Data Explorer - Uploading and Viewing Data
Duration: 0:15

The "Data Explorer" is the first main functional section of the application. It allows users to upload their datasets and get an immediate overview of their data.

When `page == "Data Explorer"`, the application focuses on data input and initial inspection.

### 1. File Upload

The `st.file_uploader` widget is used to allow users to upload their CSV files.

```python
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
```

*   `"Upload your CSV file"`: The label displayed to the user.
*   `type=["csv"]`: Restricts the file upload to CSV files only.

### 2. Reading and Storing Data

If a file is successfully uploaded, it's read into a Pandas DataFrame, and then stored in `st.session_state` for persistence.

```python
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.session_state['df'] = df
    st.success("File uploaded successfully!")
```

*   `pd.read_csv(uploaded_file)`: Reads the content of the uploaded file directly into a Pandas DataFrame.
*   `st.session_state['df'] = df`: Stores the DataFrame in the session state, making it available for other parts of the application without re-uploading.
*   `st.success("File uploaded successfully!")`: Provides positive feedback to the user.

<aside class="negative">
It's crucial to handle scenarios where `uploaded_file` is `None`. The application correctly places all subsequent data exploration logic inside the `if uploaded_file is not None:` block, ensuring that operations on `df` only happen when data is available.
</aside>

### 3. Displaying Raw Data

The `st.dataframe` widget is used to display the entire DataFrame in an interactive table format. Users can sort columns and scroll through the data.

```python
st.markdown("<h2 class='subheader'>Raw Data</h2>", unsafe_allow_html=True)
st.dataframe(df)
```

### 4. Generating Summary Statistics

`df.describe()` is a powerful Pandas function that generates descriptive statistics of the DataFrame's numerical columns.

```python
st.markdown("<h2 class='subheader'>Summary Statistics</h2>", unsafe_allow_html=True)
st.write(df.describe())
```

This output includes count, mean, standard deviation, min/max values, and quartiles, providing a quick statistical overview of the dataset.

### 5. Identifying Missing Values

Understanding missing data is a critical first step in data preprocessing. `df.isnull().sum()` helps identify the number of missing values per column.

```python
st.markdown("<h2 class='subheader'>Missing Values</h2>", unsafe_allow_html=True)
st.write(df.isnull().sum())
```

This output clearly shows which columns have missing entries and how many, guiding subsequent data cleaning steps.

## Data Explorer - Interactive Visualizations
Duration: 0:20

After uploading and inspecting the data, the "Data Explorer" page provides tools for interactive data visualization using Matplotlib and Seaborn. This section allows users to generate common chart types with customizable parameters.

### 1. Chart Type Selection

A `st.selectbox` widget allows the user to choose the type of visualization they want to create.

```python
chart_type = st.selectbox("Select Chart Type", ["Histogram", "Scatter Plot", "Box Plot"])
```

### 2. Plotting Environment Setup

Before plotting, a new Matplotlib figure is created, and `plt.clf()` is used at the end to clear the figure, preventing plots from stacking up on reruns.

```python
plt.figure(figsize=(10, 6)) # Create a new figure for each plot
# ... plotting logic ...
st.pyplot(plt)
plt.clf() # Clear the current figure to prevent plots from stacking
```

`st.pyplot(plt)` is the Streamlit function used to render a Matplotlib plot in the application.

### 3. Histogram

Histograms are used to visualize the distribution of a single numerical variable.

```python
if chart_type == "Histogram":
    column = st.selectbox("Select Column for Histogram", df.columns)
    if df[column].dtype in ['int64', 'float64']: # Ensure numerical column
        bins = st.slider("Number of Bins", min_value=5, max_value=50, value=20)
        plt.hist(df[column], bins=bins, edgecolor='black')
        plt.title(f'Histogram of {column}')
        plt.xlabel(column)
        plt.ylabel('Frequency')
        st.pyplot(plt)
    else:
        st.warning("Please select a numerical column for a Histogram.")
```

*   `st.selectbox`: Allows selecting a column for the histogram.
*   `st.slider`: Provides an interactive slider to control the number of bins, dynamically changing the granularity of the histogram.
*   `plt.hist()`: The Matplotlib function to create the histogram.

### 4. Scatter Plot

Scatter plots are ideal for visualizing the relationship between two numerical variables. An optional third variable can be used for coloring points.

```python
elif chart_type == "Scatter Plot":
    x_column = st.selectbox("Select X-axis Column", df.columns)
    y_column = st.selectbox("Select Y-axis Column", df.columns)
    color_column = st.selectbox("Select Color Column (optional)", [None] + list(df.columns))

    if x_column and y_column:
        if color_column:
            sns.scatterplot(x=df[x_column], y=df[y_column], hue=df[color_column])
        else:
            sns.scatterplot(x=df[x_column], y=df[y_column])
        plt.title(f'Scatter Plot of {x_column} vs {y_column}')
        plt.xlabel(x_column)
        plt.ylabel(y_column)
        st.pyplot(plt)
    else:
        st.warning("Please select both X and Y axis columns.")
```

*   `st.selectbox`: Used to select X-axis, Y-axis, and an optional color encoding column.
*   `sns.scatterplot()`: The Seaborn function for creating scatter plots, offering enhanced aesthetics and easy handling of hue mapping.

### 5. Box Plot

Box plots are useful for visualizing the distribution of a numerical variable and identifying potential outliers, often grouped by a categorical variable (though here it's for a single column).

```python
elif chart_type == "Box Plot":
    column = st.selectbox("Select Column for Box Plot", df.columns)
    if df[column].dtype in ['int64', 'float64']:
        sns.boxplot(y=df[column])
        plt.title(f'Box Plot of {column}')
        plt.ylabel(column)
        st.pyplot(plt)
    else:
        st.warning("Please select a numerical column for a Box Plot.")
```

*   `st.selectbox`: Allows selecting the numerical column for the box plot.
*   `sns.boxplot()`: The Seaborn function to generate box plots.

These interactive visualization tools provide users with a dynamic way to gain insights from their data without writing any code.

## ML Model Builder - Data Preprocessing
Duration: 0:15

The "ML Model Builder" page is designed to guide users through the crucial initial steps of a machine learning workflow: data preprocessing and feature selection. This page conditionally displays its content only if a dataset has been uploaded in the "Data Explorer."

```python
if st.session_state['df'] is not None:
    df = st.session_state['df']
    st.dataframe(df.head()) # Display the head of the DataFrame for context
    # ... Preprocessing and ML content ...
else:
    st.warning("Please upload a CSV file in the 'Data Explorer' section first to build models.")
```

This ensures a proper workflow, as ML model building inherently requires data.

### 1. Handling Missing Values

Missing data can significantly impact model performance. This section provides options for various imputation strategies.

```python
st.markdown("<h2 class='subheader'>Data Preprocessing</h2>", unsafe_allow_html=True)
st.subheader("Handle Missing Values")
missing_strategy = st.selectbox("Select Strategy", ["None", "Drop Rows", "Mean Imputation", "Median Imputation", "Mode Imputation"])
if missing_strategy != "None":
    st.info(f"Selected strategy: {missing_strategy}. (Implementation for processing is pending.)")
```

*   **Concepts of Missing Value Strategies:**
    *   **None:** No action is taken.
    *   **Drop Rows:** Removes all rows containing any missing values. This can lead to significant data loss if many rows have missing data.
    *   **Mean Imputation:** Replaces missing numerical values with the mean of the column. This is simple but can distort the data's variance.
    *   **Median Imputation:** Replaces missing numerical values with the median of the column. More robust to outliers than mean imputation.
    *   **Mode Imputation:** Replaces missing values (numerical or categorical) with the most frequent value (mode) of the column. Useful for categorical data.

<aside class="negative">
The current application provides the UI elements for selecting these strategies but does not implement the actual data transformation logic. This is an excellent area for further development using libraries like Scikit-learn's `SimpleImputer` or Pandas methods (`dropna`, `fillna`).
</aside>

### 2. Encoding Categorical Features

Machine learning models typically require numerical input. Categorical features (e.g., "color": "red", "blue", "green") must be converted into numerical representations.

```python
st.subheader("Encode Categorical Features")
encoding_strategy = st.selectbox("Select Encoding Method", ["None", "One-Hot Encoding", "Label Encoding"])
if encoding_strategy != "None":
    st.info(f"Selected strategy: {encoding_strategy}. (Implementation for processing is pending.)")
```

*   **Concepts of Categorical Encoding Strategies:**
    *   **None:** No action is taken.
    *   **One-Hot Encoding:** Creates new binary columns for each category in a feature. For example, a "color" column with "red", "blue", "green" would become `color_red`, `color_blue`, `color_green` (each with 0 or 1). This is suitable for nominal (unordered) categorical data.
    *   **Label Encoding:** Assigns a unique integer to each category. For example, "red" becomes 0, "blue" becomes 1, "green" becomes 2. This implies an ordinal relationship that might not exist, making it less suitable for nominal data but good for ordinal (ordered) data.

<aside class="negative">
Similar to missing value handling, the actual implementation for categorical encoding is left for future development. Scikit-learn offers `OneHotEncoder` and `LabelEncoder` for these tasks.
</aside>

These preprocessing steps are fundamental for preparing raw data for machine learning models, ensuring they can effectively learn from the features.

## ML Model Builder - Feature Selection and Model Training
Duration: 0:20

Once the data preprocessing steps are conceptually defined, the next stage in the "ML Model Builder" is to select the features and target variable, and then configure the machine learning model training process.

### 1. Feature Selection

This section allows users to define their independent variables (features, X) and dependent variable (target, y).

```python
st.markdown("<h2 class='subheader'>Feature Selection</h2>", unsafe_allow_html=True)
all_columns = df.columns.tolist()

# Select features (X)
features = st.multiselect("Select Features (X)", all_columns, default=all_columns)

# Select target variable (y)
target = st.selectbox("Select Target Variable (y)", all_columns)

if not features:
    st.warning("Please select at least one feature.")
elif not target:
    st.warning("Please select a target variable.")
elif target in features:
    st.warning("Target variable cannot be among features. Please adjust your selection.")
else:
    # Proceed to model training if selections are valid
    # ... model training logic ...
```

*   `st.multiselect("Select Features (X)", all_columns, default=all_columns)`: Allows users to select multiple columns that will serve as input features for the model. `default=all_columns` pre-selects all columns, which can be convenient for users.
*   `st.selectbox("Select Target Variable (y)", all_columns)`: Allows users to select a single column as the target variable that the model will try to predict.
*   **Validation:** Basic checks ensure that features are selected, a target is selected, and the target is not also included in the features.

### 2. Model Training Configuration

This part enables users to choose a model type and configure the train-test split parameters.

```python
st.markdown("<h2 class='subheader'>Model Training</h2>", unsafe_allow_html=True)
model_type = st.selectbox("Select Model Type", ["Linear Regression", "Logistic Regression", "Decision Tree Classifier", "Random Forest Classifier"])

st.subheader("Train/Test Split Configuration")
test_size = st.slider("Test Set Size", min_value=0.1, max_value=0.5, value=0.3, step=0.05)
random_state = st.number_input("Random State", value=42, min_value=0)

if st.button("Train Model"):
    st.info(f"Training {model_type} with features: {features}, target: {target}, test size: {test_size}, random state: {random_state}. (Actual training logic is pending.)")
    st.success("Model training initiated! (Results will appear here upon implementation.)")
    # Placeholder for actual model training and evaluation
```

*   `st.selectbox("Select Model Type", ...)`: Offers a selection of common regression and classification models.
    *   **Linear Regression:** A statistical method for modeling the relationship between a scalar dependent variable and one or more independent variables by fitting a linear equation to observed data. Suitable for continuous target variables.
    *   **Logistic Regression:** Despite its name, it's a classification algorithm used to estimate the probability of a binary outcome. It can be extended for multi-class classification. Suitable for categorical target variables.
    *   **Decision Tree Classifier:** A non-parametric supervised learning method used for classification and regression. It works by creating a tree-like model of decisions.
    *   **Random Forest Classifier:** An ensemble learning method that operates by constructing a multitude of decision trees at training time and outputting the class that is the mode of the classes (classification) or mean prediction (regression) of the individual trees. Generally robust and accurate.
*   `test_size = st.slider(...)`: Determines the proportion of the dataset to be used for testing the model's performance. A common value is 0.2 or 0.3.
*   `random_state = st.number_input(...)`: Used for reproducibility. Setting a `random_state` ensures that the train-test split and any random processes within the model (like in Random Forest) yield the same results every time the script is run with the same inputs.
*   `st.button("Train Model")`: Triggers the conceptual model training process.

### Conceptual ML Pipeline Flowchart

This diagram illustrates the intended flow of data through the machine learning pipeline within the application:

```mermaid
graph TD
    A[Raw Data (from Data Explorer)] --> B{Data Preprocessing};
    B --> B1[Handle Missing Values];
    B --> B2[Encode Categorical Features];
    B1 --> C;
    B2 --> C;
    C[Cleaned & Transformed Data] --> D{Feature Selection};
    D --> D1[Select Features (X)];
    D --> D2[Select Target (y)];
    D1 --> E;
    D2 --> E;
    E[Features (X) & Target (y)] --> F{Train/Test Split};
    F --> F1[Training Set (X_train, y_train)];
    F --> F2[Test Set (X_test, y_test)];
    F1 --> G[Model Training];
    G --> G1[Selected ML Model];
    G1 --> H[Trained Model];
    F2 --> H;
    H --> I[Model Evaluation (Conceptual)];
    I --> J[Performance Metrics & Results];
```

<aside class="positive">
Implementing the actual model training and evaluation logic (commented out in the provided code) would involve using Scikit-learn. This includes `train_test_split`, model instantiation (e.g., `LinearRegression()`, `RandomForestClassifier()`), `model.fit()`, `model.predict()`, and metrics like `mean_squared_error` or `accuracy_score`.
</aside>

This section lays the groundwork for a powerful, interactive ML model building experience, even though the full backend implementation is a placeholder for demonstration and future expansion.

## Running the Application and Further Enhancements
Duration: 0:05

You've now explored the complete structure and conceptual functionalities of the Streamlit Interactive Data Science Dashboard.

### Running Your Application

To run the application, open your terminal, navigate to the directory where you saved `app.py`, and execute:

```console
streamlit run app.py
```

This will launch the application in your web browser. Try uploading a CSV file (you can find many sample datasets online, e.g., from Kaggle or UCI Machine Learning Repository) and experiment with the data explorer and the ML model builder pages.

### Potential Further Enhancements

The provided application serves as a strong foundation. Here are several ways you can expand its capabilities:

1.  **Implement Data Preprocessing:**
    *   Add actual logic for "Drop Rows", "Mean/Median/Mode Imputation" using `df.dropna()`, `df.fillna()`, `SimpleImputer` from `sklearn.impute`.
    *   Implement "One-Hot Encoding" using `pd.get_dummies()` or `OneHotEncoder` from `sklearn.preprocessing`.
    *   Implement "Label Encoding" using `LabelEncoder` from `sklearn.preprocessing`.
    *   Consider adding data scaling (StandardScaler, MinMaxScaler) for numerical features.

2.  **Complete ML Model Training and Evaluation:**
    *   Uncomment and implement the Scikit-learn code for `train_test_split`, model instantiation, `model.fit()`, and `model.predict()`.
    *   Display relevant evaluation metrics based on the model type (e.g., `accuracy_score`, `precision_score`, `recall_score`, `f1_score` for classification; `mean_squared_error`, `r2_score` for regression).
    *   Visualize model results (e.g., confusion matrix for classification, residual plots for regression).
    *   Add hyperparameter tuning options for models.

3.  **Add More Visualization Types:**
    *   Correlation Heatmaps (`sns.heatmap`).
    *   Pair Plots (`sns.pairplot`).
    *   Count Plots (`sns.countplot`) for categorical distributions.
    *   Interactive plots using libraries like Plotly or Altair for more dynamic exploration.

4.  **Error Handling and Robustness:**
    *   Implement more robust error handling for data types, missing values, and potential issues during model training.
    *   Guide users better when they select incompatible column types for certain visualizations.

5.  **Data Persistence for Models:**
    *   Allow users to save trained models (`joblib` or `pickle`) and load them for making predictions on new data.

6.  **Deployment:**
    *   Learn how to deploy your Streamlit application to platforms like Streamlit Community Cloud, Heroku, or AWS.

### Conclusion

This codelab has walked you through building a powerful and interactive data science dashboard using Streamlit. You've learned how to structure a multi-page application, handle user input, manage session state, perform basic data exploration, create dynamic visualizations, and lay the groundwork for a machine learning pipeline.

By leveraging Streamlit's simplicity and the vast ecosystem of Python data science libraries, you can create compelling and useful tools that democratize access to complex analytical capabilities. We encourage you to continue experimenting and enhancing this application with your own ideas!
