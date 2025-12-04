import streamlit as st
import pandas as pd
import numpy as np
import urllib.request
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from io import StringIO # Added for df.info()

@st.cache_data(ttl="2h")
def load_and_explore_data(file_path):
    """
    Loads the German Credit Data.
    """
    data = pd.read_csv(file_path)
    return data

@st.cache_data(ttl="2h")
def preprocess_data(data):
    df_processed = data.copy()
    # Renaming columns for better readability and consistency
    df_processed = df_processed.rename(columns={
        'Status_of_existing_checking_account': 'CheckingAccountStatus',
        'Duration_of_Credit_month': 'CreditDurationMonths',
        'Credit_history': 'CreditHistory',
        'Purpose': 'LoanPurpose',
        'Credit_Amount': 'CreditAmount',
        'Savings_account_bonds': 'SavingsAccountBonds',
        'Present_employment_since': 'EmploymentDuration',
        'Installation_Rate_in_Percentage_of_Disposable_Income': 'InstallmentRate',
        'Personal_Status_and_Sex': 'PersonalStatusSex',
        'Other_debtors_guarantors': 'OtherDebtorsGuarantors',
        'Present_Residence_since': 'ResidenceDuration',
        'Property': 'PropertyType',
        'Age_in_years': 'Age',
        'Other_installment_plans': 'OtherInstallmentPlans',
        'Housing': 'HousingType',
        'Number_of_Credits_at_this_Bank': 'NumExistingCredits',
        'Job': 'JobType',
        'Number_of_people_being_liable_to_provide_maintenance_for': 'NumDependents',
        'Telephone': 'HasTelephone',
        'foreign_worker': 'ForeignWorker',
        'Class': 'LoanApproved' # Target variable: 1 for approved, 2 for denied
    })

    # Map target variable: 1 (Good) -> 1 (Approved), 2 (Bad) -> 0 (Denied)
    df_processed['LoanApproved'] = df_processed['LoanApproved'].map({1: 1, 2: 0})

    # Create 'Gender' from 'PersonalStatusSex'
    # Assuming the mapping from the notebook:
    # A91 : 'male   : divorced/separated' -> male (1)
    # A92 : 'female : divorced/separated/married' -> female (0)
    # A93 : 'male   : single' -> male (1)
    # A94 : 'male   : married/widowed' -> male (1)
    # A95 : 'female : single' -> female (0)
    df_processed['Gender'] = df_processed['PersonalStatusSex'].apply(
        lambda x: 1 if x in ['A91', 'A93', 'A94'] else 0
    ) # 1 for male (privileged), 0 for female (unprivileged)

    # Create 'AgeGroup'
    bins = [18, 25, 35, 45, 55, 65, 100]
    labels = ['18-24', '25-34', '35-44', '45-54', '55-64', '65+']
    df_processed['AgeGroup'] = pd.cut(df_processed['Age'], bins=bins, labels=labels, right=False)
    df_processed['AgeGroup'] = df_processed['AgeGroup'].astype(str) # Convert to string for OHE

    # Drop original 'PersonalStatusSex' column
    df_processed = df_processed.drop(columns=['PersonalStatusSex'])

    # Separate features (X) and target (y)
    X = df_processed.drop('LoanApproved', axis=1)
    y = df_processed['LoanApproved']

    # Identify categorical and numerical features for preprocessing
    # Gender is numerical (0/1) but we want to pass it through, not scale it.
    categorical_features = X.select_dtypes(include='object').columns.tolist()
    numerical_features = X.select_dtypes(include=['int64', 'float64']).columns.tolist()

    # Remove 'Gender' from numerical features list if it's there, as it will be passthrough
    if 'Gender' in numerical_features:
        numerical_features.remove('Gender')
    
    passthrough_features = ['Gender'] # Ensure Gender is explicitly passed through

    # Create preprocessing pipelines for numerical and categorical features
    numerical_transformer = StandardScaler()
    categorical_transformer = OneHotEncoder(handle_unknown='ignore')

    # Create a column transformer to apply different transformations to different columns
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numerical_transformer, numerical_features),
            ('cat', categorical_transformer, categorical_features),
            ('passthrough', 'passthrough', passthrough_features)
        ],
        remainder='drop' # Drop any columns not specified
    )
    
    return X, y, preprocessor, categorical_features, numerical_features, df_processed.columns.tolist() # original_cols_with_target

def main():
    st.header("📊 Data Management")

    st.markdown("""\
    ### 1. Dataset Loading and Initial Exploration

    We'll be working with the **UCI German Credit Dataset**, a classic benchmark dataset in credit risk modeling. It contains 1000 entries, each representing a person applying for a credit loan, with 20 features and a binary target variable indicating whether the loan was approved ('Good') or denied ('Bad').

    Our objective is to build a model that predicts loan approval and then analyze its behavior for explainability and fairness.

    *   The original target variable `Class` is mapped:
        *   `1` (Good Credit) $\rightarrow$ `1` (Loan Approved)
        *   `2` (Bad Credit) $\rightarrow$ `0` (Loan Denied)

    *   We will identify **protected attributes** such as `Gender` and `AgeGroup` to assess and mitigate potential biases in our AI model. The `Gender` attribute is derived from `Personal_Status_and_Sex`, where males are considered the `privileged` group and females the `unprivileged` group for fairness analysis. Similarly, `AgeGroup` will be created from `Age` to observe its impact.
    """)

    data_file = 'german.data'
    csv_file = 'german_credit.csv'

    # Initialize session state variables if not already present
    if 'data_loaded' not in st.session_state:
        st.session_state.data_loaded = False
        st.session_state.df = None
        st.session_state.X_raw = None
        st.session_state.y = None
        st.session_state.preprocessor = None
        st.session_state.categorical_features = None
        st.session_state.numerical_features = None
        st.session_state.all_feature_names = None
        st.session_state.X_train_df = None
        st.session_state.X_test_df = None
        st.session_state.y_train = None
        st.session_state.y_test = None
        st.session_state.aif360_privileged_groups = None
        st.session_state.aif360_unprivileged_groups = None
        st.session_state.protected_attribute_names = None
        # Initialize other model-related session states for later pages
        st.session_state.baseline_model = None
        st.session_state.baseline_accuracy = None
        st.session_state.baseline_precision = None
        st.session_state.baseline_recall = None
        st.session_state.baseline_f1 = None
        st.session_state.baseline_conf_matrix = None
        st.session_state.baseline_report = None
        st.session_state.baseline_predictions = None
        st.session_state.baseline_spd = None
        st.session_state.baseline_eod = None
        st.session_state.reweighed_model = None
        st.session_state.reweighed_accuracy = None
        st.session_state.reweighed_spd = None
        st.session_state.reweighed_eod = None
        st.session_state.adjusted_accuracy = None
        st.session_state.adjusted_spd = None
        st.session_state.adjusted_eod = None
        st.session_state.shap_values_baseline = None

    if st.button("Load & Preprocess Data 🚀"):
        with st.spinner("Loading and preprocessing data..."):
            # Data Download Logic
            column_names = [
                'Status_of_existing_checking_account', 'Duration_of_Credit_month', 'Credit_history',
                'Purpose', 'Credit_Amount', 'Savings_account_bonds', 'Present_employment_since',
                'Installation_Rate_in_Percentage_of_Disposable_Income', 'Personal_Status_and_Sex',
                'Other_debtors_guarantors', 'Present_Residence_since', 'Property', 'Age_in_years',
                'Other_installment_plans', 'Housing', 'Number_of_Credits_at_this_Bank', 'Job',
                'Number_of_people_being_liable_to_provide_maintenance_for', 'Telephone',
                'foreign_worker', 'Class'
            ]

            if not os.path.exists(csv_file):
                if not os.path.exists(data_file):
                    url = 'https://archive.ics.uci.edu/ml/machine-learning-databases/statlog/german/german.data'
                    st.info(f"Downloading dataset from {url}...")
                    urllib.request.urlretrieve(url, data_file)
                
                st.info("Converting to CSV format...")
                df_temp = pd.read_csv(data_file, sep='\\s+', header=None, names=column_names)
                df_temp.to_csv(csv_file, index=False)
                st.success(f"Dataset saved as {csv_file}")
            else:
                st.info(f"{csv_file} already exists.")

            # Load and preprocess
            df = load_and_explore_data(csv_file)
            st.session_state.df = df

            X_raw, y, preprocessor, categorical_features_from_func, numerical_features_from_func, _ = preprocess_data(df) # _ is original_cols_with_target

            # Splitting data
            X_train_pre, X_test_pre, y_train, y_test = train_test_split(X_raw, y, test_size=0.3, random_state=42, stratify=y)
            
            # Fit preprocessor on training data and transform both train and test
            preprocessor.fit(X_train_pre)
            X_train_transformed = preprocessor.transform(X_train_pre)
            X_test_transformed = preprocessor.transform(X_test_pre)

            # Get feature names after one-hot encoding
            encoded_feature_names = preprocessor.named_transformers_['cat'].get_feature_names_out(categorical_features_from_func)
            
            # The passthrough features from ColumnTransformer are at the end.
            all_feature_names = numerical_features_from_func + list(encoded_feature_names) + ['Gender'] # 'Gender' is the passthrough feature


            st.session_state.X_raw = X_raw
            st.session_state.y = y
            st.session_state.preprocessor = preprocessor
            st.session_state.categorical_features = categorical_features_from_func
            st.session_state.numerical_features = numerical_features_from_func
            st.session_state.all_feature_names = all_feature_names
            st.session_state.X_train_df = pd.DataFrame(X_train_transformed, columns=all_feature_names, index=X_train_pre.index)
            st.session_state.X_test_df = pd.DataFrame(X_test_transformed, columns=all_feature_names, index=X_test_pre.index)
            st.session_state.y_train = y_train
            st.session_state.y_test = y_test

            # Define AIF360 groups. 'Gender' is 1 for male (privileged), 0 for female (unprivileged)
            # This assumes 'Gender' is directly available in X_train_df/X_test_df as a numerical column.
            st.session_state.aif360_privileged_groups = [{'Gender': 1}]
            st.session_state.aif360_unprivileged_groups = [{'Gender': 0}]
            st.session_state.protected_attribute_names = ['Gender'] # For AIF360, use the actual column name

            st.session_state.data_loaded = True
            st.success("Data loaded, preprocessed, and split successfully! 🎉")
            

    if st.session_state.data_loaded:
        st.subheader("Loaded Data Snapshot (First 5 Rows)")
        st.dataframe(st.session_state.df.head())

        st.subheader("Data Information")
        buffer = StringIO()
        st.session_state.df.info(buf=buffer)
        s = buffer.getvalue()
        st.text(s)
        st.write(f"Data Shape: {st.session_state.df.shape}")

        st.markdown("""\
        ### 2. Data Preprocessing for Modeling

        Before feeding the data into our machine learning model, we perform several preprocessing steps:

        *   **Column Renaming:** Renaming columns for clarity and consistency.
        *   **Target Variable Mapping:** `Class` (Good/Bad) is mapped to `LoanApproved` (1/0).
        *   **Protected Attribute Derivation:**
            *   `Gender` is extracted from `Personal_Status_and_Sex` (Male: 1, Female: 0).
            *   `AgeGroup` is created by binning `Age` into categorical groups.
        *   **One-Hot Encoding:** Categorical features (e.g., `LoanPurpose`, `HousingType`, `AgeGroup`) are converted into numerical format using one-hot encoding.
        *   **Standard Scaling:** Numerical features (e.g., `CreditAmount`, `Age`) are scaled to have zero mean and unit variance, which helps in model convergence.
        *   **Train-Test Split:** The dataset is split into training and testing sets to evaluate model performance on unseen data.

        This structured approach ensures that our model receives clean, normalized data, which is crucial for effective and fair AI decision-making. We have stored the processed dataframes and the preprocessor in the session state for subsequent steps.
        """)

        st.subheader("Processed Training Data (First 5 Rows)")
        st.dataframe(st.session_state.X_train_df.head())
        st.subheader("Processed Test Data (First 5 Rows)")
        st.dataframe(st.session_state.X_test_df.head())

        st.info(f"Total Features after Preprocessing: {len(st.session_state.all_feature_names)}")
    else:
        st.warning("Click 'Load & Preprocess Data' to prepare the dataset for modeling. This step downloads and transforms the raw data, making it ready for AI analysis. 💡")

if __name__ == '__main__':
    main()
