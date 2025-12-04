id: 6931e3d8ca38c557e5169691_documentation
summary: AI Design and deployment lab 5 - Clone Documentation
feedback link: https://docs.google.com/forms/d/e/1FAIpQLSfWkOK-in_bMMoHSZfcIvAeO58PAH9wrDqcxnJABHaxiDqhSA/viewform?usp=sf_link
environments: Web
status: Published
# Building Interactive Data Applications with Streamlit

## Introduction to Interactive Streamlit Applications
Duration: 0:05:00

Welcome to this codelab, where you will learn how to build interactive data applications using Streamlit! This codelab focuses on understanding and extending a typical Streamlit application designed for interactive data analysis and visualization.

Streamlit is an open-source Python library that makes it incredibly easy to create beautiful, custom web applications for machine learning and data science. In a few lines of code, you can build powerful data tools, dashboards, and interactive prototypes without needing front-end development experience.

This application serves as a prime example of Streamlit's capabilities, demonstrating how to:
*   **Rapidly Prototype**: Quickly turn Python scripts into shareable web apps.
*   **Engage Users**: Create interactive elements like file uploaders, sliders, and select boxes.
*   **Visualize Data**: Generate dynamic plots and tables directly within the web interface.
*   **Explain Complex Concepts**: Present data analysis and even machine learning model insights in an intuitive way.

The core concept behind Streamlit is to treat your Python script as the web application itself. As your script runs from top to bottom, Streamlit re-executes it whenever an input widget changes, automatically updating the UI. This "dataflow" model simplifies development significantly.

### Application's Importance and Concepts
This application is crucial for anyone looking to build quick data exploration tools, demonstrate ML models, or create internal dashboards without delving into complex web frameworks. It showcases:
*   **Reactive Programming**: How Streamlit's rerun mechanism simplifies UI updates.
*   **Component-Based UI**: Using pre-built widgets like `st.sidebar`, `st.file_uploader`, `st.selectbox`, `st.dataframe`, and `st.pyplot`.
*   **Data Handling with Pandas**: Integrating common data science libraries for robust data manipulation.
*   **Dynamic Visualization**: Using `matplotlib` or `seaborn` to create plots that respond to user input.

<aside class="positive">
<b>Key Takeaway:</b> Streamlit empowers data scientists and ML engineers to build powerful web applications purely in Python, bridging the gap between data analysis and interactive user interfaces.
</aside>

### Application Architecture Overview

The application follows a simple client-server architecture. The Streamlit server runs on your machine (or a cloud instance) and renders the Python script into a web page. Users interact with this web page through their browser.

```mermaid
graph TD
    A[User Browser] -- HTTP Requests --> B[Streamlit Server]
    B -- Renders & Executes --> C[Python Script (app.py)]
    C -- Uses Libraries --> D[Pandas, Matplotlib, Scikit-learn, etc.]
    D -- Processes Data --> C
    C -- Generates UI & Data --> B
    B -- HTTP Responses --> A
```

**Workflow:**
1.  The user opens the application in their web browser.
2.  The browser sends requests to the Streamlit server.
3.  The Streamlit server executes the `app.py` script.
4.  The script uses libraries like Pandas for data manipulation, and Matplotlib/Seaborn for visualization.
5.  Based on user interactions (e.g., file upload, slider change), Streamlit re-executes the script, updating the application state and UI.
6.  The server sends the updated UI back to the user's browser.

## Setting Up Your Development Environment
Duration: 0:03:00

Before we dive into the application code, let's ensure your development environment is properly set up.

### Prerequisites

*   Python 3.8+
*   A code editor (e.g., VS Code, PyCharm)
*   Command-line interface (CLI) access

### 1. Install Python

If you don't have Python installed, download it from [python.org](https://www.python.org/downloads/). Make sure to add Python to your system's PATH during installation.

### 2. Create a Virtual Environment

It's a best practice to use virtual environments to manage dependencies for your projects.

Open your terminal or command prompt and navigate to your desired project directory. Then run:

```console
mkdir streamlit_codelab
cd streamlit_codelab
python -m venv venv
```

This creates a new virtual environment named `venv` in your project directory.

### 3. Activate the Virtual Environment

Activate the virtual environment:

*   **On macOS/Linux:**
    ```console
    source venv/bin/activate
    ```
*   **On Windows:**
    ```console
    venv\Scripts\activate
    ```

You should see `(venv)` preceding your prompt, indicating that the virtual environment is active.

### 4. Install Dependencies

Now, install Streamlit and other common data science libraries that a typical application like this might use.

```console
pip install streamlit pandas matplotlib seaborn scikit-learn
```

<aside class="positive">
<b>Tip:</b> Always activate your virtual environment before installing dependencies or running your application to ensure project isolation and avoid conflicts.
</aside>

## Understanding the Streamlit Application Structure
Duration: 0:10:00

In this step, we'll examine the fundamental structure of a Streamlit application. A typical application is contained within a single Python file, commonly named `app.py` (or `main.py`).

Let's assume our example application, `app.py`, has the following logical flow:

```python
# app.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans # Example ML component

#  1. Set Page Configuration 
st.set_page_config(
    page_title="Interactive Data Explorer",
    page_icon="📊",
    layout="wide"
)

#  2. Sidebar for Controls 
st.sidebar.title("Configuration")

#  3. Main Content Area 
st.title("📊 Interactive Data Analysis & Visualization")
st.write("Upload your CSV file to get started with interactive data exploration.")

#  4. File Uploader 
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("File uploaded successfully!")

    #  5. Data Preview and Basic Statistics 
    st.subheader("Raw Data Preview")
    st.dataframe(df.head())

    st.subheader("Descriptive Statistics")
    st.write(df.describe())

    #  6. Data Preprocessing Options (Sidebar) 
    st.sidebar.subheader("Preprocessing")
    if st.sidebar.checkbox("Show Missing Values"):
        st.subheader("Missing Values")
        st.write(df.isnull().sum())
    
    # Example: Handle missing values
    impute_option = st.sidebar.radio(
        "Handle Missing Numerical Values:",
        ("Do nothing", "Mean Imputation", "Median Imputation")
    )

    if impute_option == "Mean Imputation":
        for col in df.select_dtypes(include=['number']).columns:
            df[col].fillna(df[col].mean(), inplace=True)
        st.sidebar.info("Mean imputation applied.")
    elif impute_option == "Median Imputation":
        for col in df.select_dtypes(include=['number']).columns:
            df[col].fillna(df[col].median(), inplace=True)
        st.sidebar.info("Median imputation applied.")
    
    #  7. Interactive Visualization Options (Sidebar & Main) 
    st.sidebar.subheader("Visualization Settings")
    
    numerical_cols = df.select_dtypes(include=['number']).columns.tolist()
    if numerical_cols:
        x_axis = st.sidebar.selectbox("Select X-axis for plot", numerical_cols)
        y_axis = st.sidebar.selectbox("Select Y-axis for plot", numerical_cols, index=min(1, len(numerical_cols)-1))
        plot_type = st.sidebar.selectbox("Select Plot Type", ["Histogram", "Scatter Plot"])

        st.subheader(f"{plot_type} of {x_axis} vs {y_axis}")
        fig, ax = plt.subplots()

        if plot_type == "Histogram":
            sns.histplot(df[x_axis], kde=True, ax=ax)
            ax.set_title(f"Histogram of {x_axis}")
            ax.set_xlabel(x_axis)
            ax.set_ylabel("Frequency")
        elif plot_type == "Scatter Plot":
            sns.scatterplot(x=df[x_axis], y=df[y_axis], ax=ax)
            ax.set_title(f"Scatter Plot of {x_axis} vs {y_axis}")
            ax.set_xlabel(x_axis)
            ax.set_ylabel(y_axis)
        
        st.pyplot(fig)
    else:
        st.warning("No numerical columns found for visualization.")

    #  8. (Optional) Machine Learning Section 
    st.sidebar.subheader("Machine Learning")
    if numerical_cols and st.sidebar.checkbox("Perform K-Means Clustering"):
        num_clusters = st.sidebar.slider("Number of Clusters (K)", 2, 10, 3)
        
        st.subheader(f"K-Means Clustering with K={num_clusters}")
        
        # Select only numerical features for clustering
        X = df[numerical_cols].dropna() # Drop NaNs for clustering
        
        if not X.empty:
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
            
            kmeans = KMeans(n_clusters=num_clusters, random_state=42, n_init=10)
            clusters = kmeans.fit_predict(X_scaled)
            df_clustered = df.loc[X.index].copy() # Align with original DataFrame's index
            df_clustered['Cluster'] = clusters
            
            st.dataframe(df_clustered[['Cluster'] + numerical_cols].head())

            # Visualize clusters (example with 2 selected features)
            if len(numerical_cols) >= 2:
                st.subheader("Cluster Visualization")
                fig_cluster, ax_cluster = plt.subplots()
                sns.scatterplot(
                    x=df_clustered[x_axis],
                    y=df_clustered[y_axis],
                    hue=df_clustered['Cluster'],
                    palette='viridis',
                    ax=ax_cluster
                )
                ax_cluster.set_title(f"Clusters based on {x_axis} and {y_axis}")
                ax_cluster.set_xlabel(x_axis)
                ax_cluster.set_ylabel(y_axis)
                st.pyplot(fig_cluster)
            else:
                st.warning("Need at least two numerical columns to visualize clusters.")
        else:
            st.warning("No data available for clustering after dropping missing values.")

else:
    st.info("Please upload a CSV file to proceed.")

```

### Key Components Explained:

1.  **`st.set_page_config()`**:
    *   This function allows you to configure global settings for your Streamlit app, such as the page title, icon, and layout (e.g., `wide` for more screen real estate). It should be the first Streamlit command in your script.

2.  **`st.sidebar`**:
    *   Any Streamlit command prefixed with `st.sidebar.` will render its elements in a collapsible sidebar on the left side of the application. This is ideal for controls, filters, or settings that don't need to be in the main content area.

3.  **Main Content Area (`st.title`, `st.write`, etc.)**:
    *   Commands without the `st.sidebar.` prefix render in the main content area of the application.
    *   `st.title("...")`: Displays a large, prominent title.
    *   `st.write("...")`: A versatile function to write text, dataframes, plots, and more.
    *   `st.subheader("...")`: Displays a smaller subtitle.

4.  **`st.file_uploader("...", type="csv")`**:
    *   Provides a widget for users to upload files. The `type` argument restricts allowed file types. When a file is uploaded, this function returns a file-like object.

5.  **`pd.read_csv(uploaded_file)`**:
    *   After a file is uploaded, `uploaded_file` can be directly passed to Pandas functions like `read_csv` to load the data into a DataFrame.

6.  **`st.dataframe(df.head())`**:
    *   Displays an interactive table of a Pandas DataFrame. Users can sort columns and scroll through the data.
    *   `df.describe()`: A standard Pandas method to generate descriptive statistics.

7.  **`st.checkbox("...")`, `st.radio("...")`**:
    *   **`st.checkbox`**: A simple boolean toggle. Returns `True` if checked, `False` otherwise.
    *   **`st.radio`**: Allows users to select one option from a list.

8.  **`st.selectbox("...", options)`**:
    *   A dropdown menu for selecting a single item from a list. This is very useful for choosing columns for analysis or visualization.

9.  **`matplotlib.pyplot` and `seaborn`**:
    *   Standard Python libraries for creating plots. Streamlit integrates seamlessly with them.
    *   `fig, ax = plt.subplots()`: Creates a new Matplotlib figure and an axes object.
    *   `sns.histplot()`, `sns.scatterplot()`: Examples of using Seaborn for different plot types.

10. **`st.pyplot(fig)`**:
    *   Displays a Matplotlib figure within the Streamlit application. Make sure to pass the figure object, not just `plt`.

11. **Machine Learning Integration (e.g., `KMeans`, `StandardScaler`)**:
    *   Streamlit doesn't directly provide ML models, but you can seamlessly integrate any Python ML library (like Scikit-learn, TensorFlow, PyTorch).
    *   User inputs (e.g., `st.slider`) can dynamically control ML model parameters.
    *   Model outputs (predictions, clusters) can be displayed using `st.dataframe` or visualized with `st.pyplot`.

This structured approach allows you to build complex applications by breaking them down into manageable, interactive components.

## Running the Streamlit Application
Duration: 0:02:00

Now that we understand the structure, let's run the application and see it in action.

### 1. Save the Code

Save the code from the previous step into a file named `app.py` in your `streamlit_codelab` directory.

### 2. Run the Application

With your virtual environment activated, navigate to the `streamlit_codelab` directory in your terminal and run:

```console
streamlit run app.py
```

Streamlit will launch a local server and open the application in your default web browser. You'll typically see output like this:

```console
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.1.XX:8501

```

### 3. Interact with the App

*   **Upload a CSV:** The app starts by prompting you to upload a CSV file. You can use any public dataset (e.g., Iris, Titanic, or a simple CSV you create yourself).
    <button>
      [Download Sample CSV (Iris)](https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv)
    </button>
*   **Explore Data:** After uploading, observe the raw data preview and descriptive statistics.
*   **Use Sidebar Controls:**
    *   Click the "Show Missing Values" checkbox.
    *   Select different "Handle Missing Numerical Values" options.
    *   Change the X-axis, Y-axis, and Plot Type for visualizations.
    *   Toggle "Perform K-Means Clustering" and adjust the "Number of Clusters (K)" slider.
*   **Observe Reactivity:** Notice how the application reloads and updates its content dynamically as you interact with the widgets.

<aside class="negative">
If you encounter any errors, check your terminal for traceback messages. Common issues include missing libraries (ensure `pip install` was successful) or syntax errors in `app.py`.
</aside>

## Data Upload and Initial Exploration
Duration: 0:08:00

The first key functionality of our application is allowing users to upload their own data and get an immediate overview. This step focuses on how Streamlit handles file uploads and displays initial data insights.

### 1. File Uploader (`st.file_uploader`)

The `st.file_uploader` widget is crucial for applications that process user-provided data.

```python
# app.py snippet
# ...
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Code to process the file goes here
    df = pd.read_csv(uploaded_file)
    st.success("File uploaded successfully!")
    # ... rest of the app logic
else:
    st.info("Please upload a CSV file to proceed.")
```

*   **`st.file_uploader("Choose a CSV file", type="csv")`**: This line creates the upload button.
    *   The first argument is the label displayed to the user.
    *   `type="csv"` restricts the uploaded files to CSV format. You can specify multiple types, e.g., `type=["csv", "xlsx", "json"]`.
*   **`if uploaded_file is not None:`**: This condition is essential. `st.file_uploader` returns `None` if no file has been uploaded yet. Once a file is uploaded, it returns a `UploadedFile` object.
*   **`pd.read_csv(uploaded_file)`**: The `UploadedFile` object is directly compatible with Pandas functions like `pd.read_csv`, making it straightforward to load data.

### 2. Displaying Raw Data (`st.dataframe`)

After the data is loaded, it's good practice to show a preview to the user.

```python
# app.py snippet
# ...
    st.subheader("Raw Data Preview")
    st.dataframe(df.head())
```

*   **`st.dataframe(df.head())`**: This displays the first few rows of the DataFrame in an interactive table. Users can sort columns and scroll horizontally if the DataFrame is wide.
    *   You can also use `st.table(df)` for a static table, which is useful for smaller datasets where interactivity is not required.

### 3. Displaying Descriptive Statistics (`df.describe()`)

Providing basic statistical summaries gives users a quick understanding of their data's distribution and characteristics.

```python
# app.py snippet
# ...
    st.subheader("Descriptive Statistics")
    st.write(df.describe())
```

*   **`df.describe()`**: This Pandas method generates a summary of numerical columns, including count, mean, standard deviation, min, max, and quartiles.
*   **`st.write(df.describe())`**: `st.write()` is a versatile function that can display almost anything, including DataFrames, strings, numbers, and plots. When passed a DataFrame, it renders it as a static table.

<aside class="positive">
<b>Best Practice:</b> Always provide immediate feedback to the user after a significant action, like a file upload. `st.success()` or `st.info()` are great for this.
</aside>

### Exercise: Extend Initial Exploration

Modify `app.py` to also display the shape of the DataFrame (number of rows and columns) and the data types of each column using `df.shape` and `df.dtypes`.

```python
# Inside the if uploaded_file is not None: block

# ... existing code for st.dataframe(df.head()) and st.write(df.describe()) ...

    st.subheader("Data Info")
    st.write(f"DataFrame Shape: {df.shape[0]} rows, {df.shape[1]} columns")
    st.write("Column Data Types:")
    st.write(df.dtypes)
```

Run the app again (`streamlit run app.py`), upload your CSV, and observe the new information.

## Data Preprocessing and Cleaning
Duration: 0:12:00

Real-world datasets often require preprocessing steps like handling missing values or feature scaling. This section covers how to provide interactive controls for these operations.

### 1. Showing Missing Values (`st.checkbox`)

Letting users inspect missing values is a crucial first step in data cleaning.

```python
# app.py snippet (inside the if uploaded_file is not None: block)
# ...
    st.sidebar.subheader("Preprocessing")
    if st.sidebar.checkbox("Show Missing Values"):
        st.subheader("Missing Values")
        st.write(df.isnull().sum())
```

*   **`st.sidebar.checkbox("Show Missing Values")`**: This creates a checkbox in the sidebar. When checked, the condition becomes `True`, and the code inside the `if` block executes, displaying the sum of null values for each column using `df.isnull().sum()`.

### 2. Handling Missing Numerical Values (`st.radio`)

Providing options for imputation allows users to decide how to deal with numerical missing data.

```python
# app.py snippet
# ...
    impute_option = st.sidebar.radio(
        "Handle Missing Numerical Values:",
        ("Do nothing", "Mean Imputation", "Median Imputation")
    )

    if impute_option == "Mean Imputation":
        for col in df.select_dtypes(include=['number']).columns:
            df[col].fillna(df[col].mean(), inplace=True)
        st.sidebar.info("Mean imputation applied.")
    elif impute_option == "Median Imputation":
        for col in df.select_dtypes(include=['number']).columns:
            df[col].fillna(df[col].median(), inplace=True)
        st.sidebar.info("Median imputation applied.")
```

*   **`st.sidebar.radio("...", ("Do nothing", "Mean Imputation", "Median Imputation"))`**: This widget creates radio buttons. The user can select one of the provided options. The selected option's string value is stored in `impute_option`.
*   **Conditional Logic**: Based on the `impute_option`, the code applies either mean or median imputation to all numerical columns in the DataFrame using Pandas' `fillna()` method.
*   **`st.sidebar.info("...")`**: Displays an informative message in the sidebar, confirming the action taken.

<aside class="negative">
<b>Warning:</b> Modifying the DataFrame `df` in place (e.g., `df.fillna(..., inplace=True)`) means subsequent operations will use the modified data. Be mindful of the order of operations and potential side effects if you need the original data later. For complex workflows, consider creating copies of the DataFrame (`df.copy()`).
</aside>

### 3. Flowchart for Preprocessing

Here's a simple flowchart illustrating the preprocessing flow:

```mermaid
graph TD
    A[Start Preprocessing] --> B{Show Missing Values?};
    B -- Yes --> C[Display df.isnull().sum()];
    B -- No --> D[Select Imputation Option];
    C --> D;
    D --> E{Option Selected};
    E -- Mean Imputation --> F[Apply Mean Imputation];
    E -- Median Imputation --> G[Apply Median Imputation];
    E -- Do nothing --> H[No Imputation];
    F --> I[End Preprocessing];
    G --> I;
    H --> I;
```

This visual representation helps understand how user choices drive different preprocessing paths within the application.

## Interactive Data Visualization
Duration: 0:15:00

Visualization is key to understanding data. Streamlit makes it easy to create dynamic plots that respond to user selections. This section demonstrates how to build interactive charts using `matplotlib` and `seaborn`.

### 1. Selecting Columns for Visualization (`st.selectbox`)

Users need to choose which features they want to plot. `st.selectbox` is perfect for this.

```python
# app.py snippet (inside the if uploaded_file is not None: block)
# ...
    st.sidebar.subheader("Visualization Settings")
    
    numerical_cols = df.select_dtypes(include=['number']).columns.tolist()
    if numerical_cols:
        x_axis = st.sidebar.selectbox("Select X-axis for plot", numerical_cols)
        y_axis = st.sidebar.selectbox("Select Y-axis for plot", numerical_cols, index=min(1, len(numerical_cols)-1))
        plot_type = st.sidebar.selectbox("Select Plot Type", ["Histogram", "Scatter Plot"])

        # ... plot generation code below ...
    else:
        st.warning("No numerical columns found for visualization.")
```

*   **`numerical_cols = df.select_dtypes(include=['number']).columns.tolist()`**: We first identify all numerical columns. This ensures that the user can only select appropriate columns for these types of plots.
*   **`st.sidebar.selectbox("Select X-axis for plot", numerical_cols)`**: Creates a dropdown in the sidebar allowing the user to pick an X-axis column from the list of `numerical_cols`.
*   **`index=min(1, len(numerical_cols)-1)`**: This sets the default selected item for the Y-axis. It tries to select the second column if available, otherwise the first.
*   **`plot_type = st.sidebar.selectbox("Select Plot Type", ["Histogram", "Scatter Plot"])`**: Allows the user to choose between different visualization types.

### 2. Generating Plots (`matplotlib` & `seaborn`)

Once column and plot types are selected, we generate the actual charts.

```python
# app.py snippet (continued from above)
# ...
        st.subheader(f"{plot_type} of {x_axis} vs {y_axis}")
        fig, ax = plt.subplots() # Create a Matplotlib figure and axes

        if plot_type == "Histogram":
            sns.histplot(df[x_axis], kde=True, ax=ax)
            ax.set_title(f"Histogram of {x_axis}")
            ax.set_xlabel(x_axis)
            ax.set_ylabel("Frequency")
        elif plot_type == "Scatter Plot":
            sns.scatterplot(x=df[x_axis], y=df[y_axis], ax=ax)
            ax.set_title(f"Scatter Plot of {x_axis} vs {y_axis}")
            ax.set_xlabel(x_axis)
            ax.set_ylabel(y_axis)
        
        st.pyplot(fig) # Display the Matplotlib figure
```

*   **`fig, ax = plt.subplots()`**: It's crucial to explicitly create a Matplotlib figure and axes object. Streamlit will capture and display whatever is on the *current* Matplotlib figure.
*   **`sns.histplot(...)` / `sns.scatterplot(...)`**: These Seaborn functions are used to draw the plots. We pass the DataFrame columns (`df[x_axis]`, `df[y_axis]`) and the `ax=ax` argument to ensure the plot is drawn on our specific axes.
*   **`ax.set_title()`, `ax.set_xlabel()`, `ax.set_ylabel()`**: Standard Matplotlib methods to customize plot titles and labels.
*   **`st.pyplot(fig)`**: This is the Streamlit command that takes the generated `fig` object and renders it as an image in the web application.

<aside class="positive">
<b>Tip:</b> Always call `plt.subplots()` to ensure Streamlit correctly displays a new plot each time the script reruns. If you don't explicitly create a figure, Matplotlib might reuse an old figure, leading to unexpected results.
</aside>

### Exercise: Add a Box Plot Option

Extend the `plot_type` selection to include a "Box Plot" option. A box plot is useful for visualizing the distribution of a single numerical variable.

1.  Modify the `plot_type` `st.selectbox` to include `"Box Plot"`.
2.  Add an `elif` condition to handle the `"Box Plot"` choice. For a box plot, you typically only need one numerical variable (e.g., `x_axis`).

```python
# app.py snippet (modify existing code)
# ...
        plot_type = st.sidebar.selectbox("Select Plot Type", ["Histogram", "Scatter Plot", "Box Plot"])

        st.subheader(f"{plot_type} of {x_axis}" + (f" vs {y_axis}" if plot_type == "Scatter Plot" else ""))
        fig, ax = plt.subplots()

        if plot_type == "Histogram":
            sns.histplot(df[x_axis], kde=True, ax=ax)
            ax.set_title(f"Histogram of {x_axis}")
            ax.set_xlabel(x_axis)
            ax.set_ylabel("Frequency")
        elif plot_type == "Scatter Plot":
            sns.scatterplot(x=df[x_axis], y=df[y_axis], ax=ax)
            ax.set_title(f"Scatter Plot of {x_axis} vs {y_axis}")
            ax.set_xlabel(x_axis)
            ax.set_ylabel(y_axis)
        elif plot_type == "Box Plot": # New condition
            sns.boxplot(y=df[x_axis], ax=ax) # Box plot typically uses one variable on an axis
            ax.set_title(f"Box Plot of {x_axis}")
            ax.set_ylabel(x_axis)
        
        st.pyplot(fig)
# ...
```

Run the app again, upload your data, and try out the new "Box Plot" option.

## Integrating a Machine Learning Model (K-Means Clustering)
Duration: 0:15:00

Streamlit is not just for data exploration; it's also excellent for demonstrating machine learning models. This section shows how to integrate a simple K-Means clustering algorithm, allowing users to interactively explore clusters in their data.

### 1. Enabling Clustering (`st.checkbox` and `st.slider`)

Users should have control over whether to run the clustering and with how many clusters.

```python
# app.py snippet (inside the if uploaded_file is not None: block)
# ...
    st.sidebar.subheader("Machine Learning")
    if numerical_cols and st.sidebar.checkbox("Perform K-Means Clustering"):
        num_clusters = st.sidebar.slider("Number of Clusters (K)", 2, 10, 3)
        
        # ... clustering logic below ...
```

*   **`st.sidebar.checkbox("Perform K-Means Clustering")`**: A checkbox to toggle the clustering functionality. It's conditionally enabled only if `numerical_cols` are present.
*   **`st.sidebar.slider("Number of Clusters (K)", 2, 10, 3)`**: A slider widget that allows the user to select an integer value within a range (2 to 10 in this case), with a default value of 3. This directly controls the `k` parameter for K-Means.

### 2. Performing K-Means Clustering

The core ML logic involves scaling the data and applying the K-Means algorithm.

```python
# app.py snippet (continued from above)
# ...
        st.subheader(f"K-Means Clustering with K={num_clusters}")
        
        # Select only numerical features for clustering and drop any remaining NaNs
        X = df[numerical_cols].dropna() 
        
        if not X.empty:
            # Scale the data before clustering
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
            
            # Apply K-Means
            kmeans = KMeans(n_clusters=num_clusters, random_state=42, n_init=10)
            clusters = kmeans.fit_predict(X_scaled)
            
            # Add cluster labels back to a copy of the original DataFrame
            df_clustered = df.loc[X.index].copy() 
            df_clustered['Cluster'] = clusters
            
            st.dataframe(df_clustered[['Cluster'] + numerical_cols].head())

            # ... cluster visualization below ...
        else:
            st.warning("No data available for clustering after dropping missing values.")
```

*   **`X = df[numerical_cols].dropna()`**: It's crucial to select only numerical features for K-Means and handle any remaining missing values (here, by dropping rows with NaNs) as K-Means cannot handle them.
*   **`scaler = StandardScaler()` & `X_scaled = scaler.fit_transform(X)`**: Standard scaling is performed on the data. This is a common preprocessing step for many ML algorithms, especially distance-based ones like K-Means, to ensure all features contribute equally.
*   **`kmeans = KMeans(n_clusters=num_clusters, random_state=42, n_init=10)`**: Initializes the K-Means model with the user-selected number of clusters. `random_state` ensures reproducibility. `n_init` explicitly sets the number of times the k-means algorithm is run with different centroid seeds.
*   **`clusters = kmeans.fit_predict(X_scaled)`**: Fits the K-Means model to the scaled data and predicts the cluster for each data point.
*   **`df_clustered = df.loc[X.index].copy()` & `df_clustered['Cluster'] = clusters`**: The cluster labels are added as a new column to a DataFrame that is aligned with the data used for clustering.

### 3. Visualizing Clusters

Displaying the clusters visually helps users interpret the results.

```python
# app.py snippet (continued from above)
# ...
            # Visualize clusters (example with 2 selected features)
            if len(numerical_cols) >= 2:
                st.subheader("Cluster Visualization")
                fig_cluster, ax_cluster = plt.subplots()
                sns.scatterplot(
                    x=df_clustered[x_axis],
                    y=df_clustered[y_axis],
                    hue=df_clustered['Cluster'], # Color points by cluster
                    palette='viridis',
                    ax=ax_cluster
                )
                ax_cluster.set_title(f"Clusters based on {x_axis} and {y_axis}")
                ax_cluster.set_xlabel(x_axis)
                ax_cluster.set_ylabel(y_axis)
                st.pyplot(fig_cluster)
            else:
                st.warning("Need at least two numerical columns to visualize clusters.")
# ...
```

*   **`sns.scatterplot(..., hue=df_clustered['Cluster'], palette='viridis', ax=ax_cluster)`**: A scatter plot is used to visualize the clusters. The `hue` argument is crucial here; it tells Seaborn to color the points based on their `Cluster` label, making the clusters visually distinct. `palette='viridis'` provides a colormap.

<aside class="positive">
<b>Tip:</b> For more complex ML models, you could consider caching (`@st.cache_data` or `@st.cache_resource`) the model loading or training steps to improve performance, especially if they are computationally expensive and inputs don't change frequently.
</aside>

### Exercise: Add Inertia Plot for Elbow Method

The Elbow Method helps determine an optimal number of clusters. Add a feature to plot the inertia for a range of K values.

1.  Add a new checkbox in the sidebar: "Show Elbow Method".
2.  If checked, calculate and plot the inertia for K from 2 to 10 (or a similar range).

```python
# app.py snippet (within the ML section)
# ...
        if numerical_cols and st.sidebar.checkbox("Perform K-Means Clustering"):
            num_clusters = st.sidebar.slider("Number of Clusters (K)", 2, 10, 3)
            # ... existing clustering and visualization code ...

        if numerical_cols and st.sidebar.checkbox("Show Elbow Method"):
            st.subheader("Elbow Method for Optimal K")
            X_elbow = df[numerical_cols].dropna()
            
            if not X_elbow.empty:
                scaler_elbow = StandardScaler()
                X_scaled_elbow = scaler_elbow.fit_transform(X_elbow)
                
                inertias = []
                k_range = range(1, 11) # Test K from 1 to 10
                for k in k_range:
                    kmeans_elbow = KMeans(n_clusters=k, random_state=42, n_init=10)
                    kmeans_elbow.fit(X_scaled_elbow)
                    inertias.append(kmeans_elbow.inertia_)
                
                fig_elbow, ax_elbow = plt.subplots()
                ax_elbow.plot(k_range, inertias, marker='o')
                ax_elbow.set_title("Elbow Method")
                ax_elbow.set_xlabel("Number of Clusters (K)")
                ax_elbow.set_ylabel("Inertia")
                ax_elbow.grid(True)
                st.pyplot(fig_elbow)
            else:
                st.warning("No data for Elbow Method after dropping missing values.")
```

Run the app, upload data, and explore the Elbow Method to see how inertia changes with the number of clusters.

## Conclusion and Next Steps
Duration: 0:03:00

Congratulations! You've successfully navigated through a comprehensive Streamlit codelab, understanding the core functionalities of an interactive data analysis and visualization application.

### What You've Learned

*   **Streamlit Fundamentals**: How to structure a Streamlit application, use various widgets (`st.sidebar`, `st.file_uploader`, `st.selectbox`, `st.slider`, `st.checkbox`, `st.radio`), and display content (`st.title`, `st.write`, `st.dataframe`, `st.pyplot`).
*   **Interactive Data Handling**: How to allow users to upload CSV files, preview data, and perform basic data exploration.
*   **Dynamic Preprocessing**: Implementing interactive controls for data cleaning steps like handling missing values.
*   **Responsive Visualization**: Generating and displaying various plots (`matplotlib`, `seaborn`) that update based on user selections.
*   **Machine Learning Integration**: Incorporating a K-Means clustering model and visualizing its results, demonstrating how Streamlit can front-end complex ML workflows.
*   **Best Practices**: Using virtual environments, structuring code, and providing user feedback.

### Further Enhancements and Next Steps

This application provides a solid foundation. Here are some ideas for how you can extend it:

1.  **More Data Types**: Add support for Excel (`.xlsx`), JSON, or even database connections.
2.  **Advanced Preprocessing**:
    *   One-hot encoding for categorical features.
    *   Outlier detection and handling.
    *   Feature engineering (e.g., creating new features from existing ones).
3.  **Additional Visualizations**:
    *   Pair plots (`seaborn.pairplot`).
    *   Correlation matrices (`sns.heatmap`).
    *   Time-series plots (if applicable to your data).
    *   Interactive plots using libraries like Plotly or Altair (`st.plotly_chart`, `st.altair_chart`).
4.  **More ML Models**:
    *   Implement classification models (e.g., Logistic Regression, Decision Trees) with interactive prediction features.
    *   Regression models.
    *   Allow users to select target variables and features for ML.
5.  **Model Persistence**: Save and load trained ML models using `joblib` or `pickle` to avoid retraining on every run.
6.  **Error Handling**: Implement more robust error handling (e.g., try-except blocks) for file processing or ML operations.
7.  **Deployment**: Learn how to deploy your Streamlit application to:
    *   [Streamlit Cloud](https://streamlit.io/cloud) (the easiest option).
    *   Heroku or Render.
    *   Docker and Kubernetes.

You now have a strong understanding of how to leverage Streamlit for creating powerful and engaging data applications. Keep experimenting and building!
