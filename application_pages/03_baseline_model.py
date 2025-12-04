import streamlit as st
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report
import matplotlib.pyplot as plt
import seaborn as sns

@st.cache_resource
def train_model(X_train, y_train, sample_weight=None):
    model = LogisticRegression(solver='liblinear', random_state=42)
    model.fit(X_train, y_train, sample_weight=sample_weight)
    return model

@st.cache_data(ttl="2h")
def evaluate_model(model, X_test, y_test, name="Model"):
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, zero_division=0)
    recall = recall_score(y_test, y_pred, zero_division=0)
    f1 = f1_score(y_test, y_pred, zero_division=0)
    conf_matrix = confusion_matrix(y_test, y_pred)
    report = classification_report(y_test, y_pred, output_dict=True, zero_division=0)
    return accuracy, precision, recall, f1, conf_matrix, y_pred, report

def main():
    st.header("🤖 Baseline Model")

    st.markdown("""
    ### 1. Baseline Model Training (Logistic Regression)

    Our first step is to train a **Baseline Model** to predict credit loan approval. For this, we'll use **Logistic Regression**, a powerful yet interpretable statistical model widely used in classification tasks. It's an excellent starting point for understanding predictive modeling before diving into more complex AI.

    <div style="background-color:#e6f7ff; padding: 10px; border-radius: 5px;">
    <p>💡 <b>What is Logistic Regression?</b></p>
    <p>Logistic Regression models the probability that a given input belongs to a particular class using the logistic function:</p>
    $$ P(\hat{Y}=1 | X) = \frac{1}{1 + e^{-(\beta_0 + \beta_1X_1 + \dots + \beta_nX_n)}} $$
    <p>where $P(\hat{Y}=1 | X)$ is the probability of the positive class (loan approved), $X$ represents the input features, and $\beta$ are the model coefficients learned during training. These coefficients indicate the strength and direction of each feature's influence on the probability of approval.</p>
    </div>

    We will train our Logistic Regression model on the preprocessed training data.
    """)

    if not st.session_state.get('data_loaded', False):
        st.warning("Please load and preprocess data in the 'Data Management' section first. 💡")
        return

    if st.button("Train Baseline Model 📈"):
        with st.spinner("Training Logistic Regression model..."):
            st.session_state.baseline_model = train_model(st.session_state.X_train_df, st.session_state.y_train)
            st.success("Baseline Logistic Regression Model Trained Successfully! ✅")

            # Evaluate the model immediately after training
            (st.session_state.baseline_accuracy, st.session_state.baseline_precision,
             st.session_state.baseline_recall, st.session_state.baseline_f1,
             st.session_state.baseline_conf_matrix, st.session_state.baseline_predictions,
             st.session_state.baseline_report) = evaluate_model(
                 st.session_state.baseline_model, st.session_state.X_test_df, st.session_state.y_test, "Baseline Model")
            st.success("Baseline Model Evaluated! 🎉")

    if st.session_state.baseline_model is not None:
        st.markdown("""
        ### 2. Baseline Model Evaluation

        After training our model, it's crucial to evaluate its performance. We use several standard metrics to understand how well our model predicts loan approvals and denials:

        *   **Accuracy:** The proportion of correctly predicted instances out of the total instances. $$ \text{Accuracy} = \frac{\text{True Positives} + \text{True Negatives}}{\text{Total Instances}} $$
        *   **Precision:** The proportion of true positive predictions among all positive predictions. It tells us how many of the approved loans were actually good. $$ \text{Precision} = \frac{\text{True Positives}}{\text{True Positives} + \text{False Positives}} $$
        *   **Recall (Sensitivity):** The proportion of true positive predictions among all actual positive instances. It tells us how many of the truly good loans our model identified. $$ \text{Recall} = \frac{\text{True Positives}}{\text{True Positives} + \text{False Negatives}} $$
        *   **F1-Score:** The harmonic mean of precision and recall, providing a balanced measure. $$ \text{F1-Score} = 2 \cdot \frac{\text{Precision} \cdot \text{Recall}}{\text{Precision} + \text{Recall}} $$
        *   **Confusion Matrix:** A table that summarizes the performance of a classification algorithm. It shows the number of true positives, true negatives, false positives, and false negatives.
        *   **Classification Report:** Provides a detailed breakdown of precision, recall, and F1-score for each class (Approved/Denied).

        """)

        st.subheader("Model Performance Metrics")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(label="Accuracy", value=f"{st.session_state.baseline_accuracy:.2f}")
        with col2:
            st.metric(label="Precision", value=f"{st.session_state.baseline_precision:.2f}")
        with col3:
            st.metric(label="Recall", value=f"{st.session_state.baseline_recall:.2f}")
        with col4:
            st.metric(label="F1-Score", value=f"{st.session_state.baseline_f1:.2f}")

        st.markdown("""
        💡 The baseline Logistic Regression model achieved an accuracy of approximately **_""")
        st.write(f"**{st.session_state.baseline_accuracy:.2f}**.")

        st.subheader("Confusion Matrix")
        cm_df = pd.DataFrame(st.session_state.baseline_conf_matrix,
                             index=['Actual Denied', 'Actual Approved'],
                             columns=['Predicted Denied', 'Predicted Approved'])
        st.dataframe(cm_df)

        st.subheader("Classification Report")
        report_df = pd.DataFrame(st.session_state.baseline_report).transpose()
        st.dataframe(report_df)
    else:
        st.info("Click 'Train Baseline Model' to train and evaluate your first AI credit decision model. This will provide a foundational understanding of its predictive capabilities. 🚀")

if __name__ == '__main__':
    main()
