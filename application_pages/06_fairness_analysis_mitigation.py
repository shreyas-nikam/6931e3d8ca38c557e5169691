import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Import sklearn components (needed for train_model and evaluate_model)
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report

# Import AIF360 for fairness
from aif360.datasets import StandardDataset
from aif360.metrics import BinaryLabelDatasetMetric, ClassificationMetric
from aif360.algorithms.preprocessing import Reweighing
from aif360.algorithms.postprocessing import CalibratedEqOddsPostprocessing

sns.set_style("whitegrid")
plt.rcParams.update({'font.size': 10})

# Re-define train_model and evaluate_model for this page's scope, 
# leveraging Streamlit's caching mechanisms.
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

@st.cache_data(ttl="2h")
def calculate_fairness_metrics(model, X_test, y_test, protected_attribute_names, privileged_groups, unprivileged_groups, model_name="Model"):
    # Ensure 'Gender' column is correctly identified or passed through for AIF360.
    # X_test_df should have 'Gender' as a numerical (0/1) passthrough column.
    aif_test_df_for_aif = X_test.copy()
    aif_test_df_for_aif['LoanApproved'] = y_test.values # Add target for StandardDataset

    # Convert protected attribute to categorical if not already, for StandardDataset to interpret groups correctly
    # If 'Gender' is 0 or 1, and treated as numerical by sklearn preprocessor, aif360 might treat it as continuous.
    # For aif360's StandardDataset to correctly identify groups with e.g., privileged_classes=[[1]],
    # the corresponding column in the dataframe should be treated as categorical or have explicit integer values.
    # Since our 'Gender' is 0/1 integer and passed through, this should work directly.

    aif_test_ds = StandardDataset(
        aif_test_df_for_aif,
        label_name='LoanApproved',
        favorable_classes=[1], # Loan Approved is the favorable outcome
        protected_attribute_names=protected_attribute_names, # e.g., ['Gender']
        privileged_classes=[[1]] # 1 for male (privileged)
    )

    y_pred = model.predict(X_test)
    dataset_pred = aif_test_ds.copy()
    dataset_pred.labels = y_pred

    metric = ClassificationMetric(
        aif_test_ds,
        dataset_pred,
        unprivileged_groups=unprivileged_groups, # [{'Gender': 0}]
        privileged_groups=privileged_groups    # [{'Gender': 1}]
    )

    spd = metric.statistical_parity_difference()
    eod = metric.equal_opportunity_difference()
    tpr_priv = metric.true_positive_rate(privileged=True)
    tpr_unpriv = metric.true_positive_rate(privileged=False)
    pos_outcome_priv = metric.selection_rate(privileged=True) # P(Y_hat=1 | A=a_1)
    pos_outcome_unpriv = metric.selection_rate(privileged=False) # P(Y_hat=1 | A=a_0)

    fig, ax = plt.subplots(figsize=(8, 5))
    metrics_data = {
        'Metric': ['SPD', 'EOD'],
        'Value': [spd, eod]
    }
    metrics_df = pd.DataFrame(metrics_data)
    sns.barplot(x='Metric', y='Value', data=metrics_df, palette='viridis', ax=ax)
    ax.axhline(0, color='grey', linestyle='--', linewidth=0.8)
    ax.set_title(f'{model_name} Fairness Metrics')
    ax.set_ylabel('Metric Value')
    ax.set_ylim(-0.5, 0.5) # Consistent y-axis for comparison
    fig.tight_layout()
    
    return spd, eod, tpr_priv, tpr_unpriv, pos_outcome_priv, pos_outcome_unpriv, fig

@st.cache_resource
def apply_reweighing_and_retrain(X_train, y_train, protected_attribute_names, privileged_groups, unprivileged_groups):
    aif_train_df = X_train.copy()
    aif_train_df['LoanApproved'] = y_train.values

    aif_train_ds = StandardDataset(
        aif_train_df,
        label_name='LoanApproved',
        favorable_classes=[1],
        protected_attribute_names=protected_attribute_names,
        privileged_classes=[[1]]
    )

    RW = Reweighing(unprivileged_groups=unprivileged_groups, privileged_groups=privileged_groups)
    aif_train_ds_reweighed = RW.fit_transform(aif_train_ds)
    
    # Reconstruct X_train from aif_train_ds_reweighed, ensuring columns match original X_train
    # The order of features might change in aif_train_ds_reweighed.features if 'Gender' was moved
    # Assuming feature order is preserved or handled by pd.DataFrame(..., columns=X_train.columns)
    X_train_reweighed = pd.DataFrame(aif_train_ds_reweighed.features, columns=X_train.columns, index=X_train.index)
    y_train_reweighed = aif_train_ds_reweighed.labels.ravel()
    sample_weights = aif_train_ds_reweighed.instance_weights
    
    reweighed_model = train_model(X_train_reweighed, y_train_reweighed, sample_weight=sample_weights)
    return reweighed_model

@st.cache_data(ttl="2h")
def apply_threshold_adjustment_and_evaluate(model, X_train, y_train, X_test, y_test, protected_attribute_names, privileged_groups, unprivileged_groups):
    aif_train_df = X_train.copy()
    aif_train_df['LoanApproved'] = y_train.values
    aif_train_ds = StandardDataset(
        aif_train_df,
        label_name='LoanApproved',
        favorable_classes=[1],
        protected_attribute_names=protected_attribute_names,
        privileged_classes=[[1]]
    )

    aif_test_df = X_test.copy()
    aif_test_df['LoanApproved'] = y_test.values
    aif_test_ds = StandardDataset(
        aif_test_df,
        label_name='LoanApproved',
        favorable_classes=[1],
        protected_attribute_names=protected_attribute_names,
        privileged_classes=[[1]]
    )

    y_proba_train = model.predict_proba(X_train)[:, 1]
    y_proba_test = model.predict_proba(X_test)[:, 1]

    dataset_pred_train = aif_train_ds.copy(deepcopy=True)
    dataset_pred_train.scores = y_proba_train.reshape(-1, 1) # Reshape for AIF360 compatibility

    dataset_pred_test = aif_test_ds.copy(deepcopy=True)
    dataset_pred_test.scores = y_proba_test.reshape(-1, 1)

    # Calibrated Equalized Odds Postprocessing
    ceopp = CalibratedEqOddsPostprocessing(
        unprivileged_groups=unprivileged_groups,
        privileged_groups=privileged_groups,
        cost_constraint='weighted', # Use 'weighted' or 'fpr', 'fnr', 'tpr'
        seed=42
    )
    
    # Fit on training data and probabilities
    ceopp = ceopp.fit(aif_train_ds, dataset_pred_train)
    
    # Predict on test data with adjusted thresholds
    dataset_pred_transformed_test = ceopp.predict(dataset_pred_test)
    y_pred_adjusted = dataset_pred_transformed_test.labels.ravel()
    
    # Evaluate adjusted model performance
    adjusted_accuracy = accuracy_score(y_test, y_pred_adjusted)
    adjusted_precision = precision_score(y_test, y_pred_adjusted, zero_division=0)
    adjusted_recall = recall_score(y_test, y_pred_adjusted, zero_division=0)
    adjusted_f1 = f1_score(y_test, y_pred_adjusted, zero_division=0)
    adjusted_conf_matrix = confusion_matrix(y_test, y_pred_adjusted)
    adjusted_report = classification_report(y_test, y_pred_adjusted, output_dict=True, zero_division=0)

    # Calculate fairness metrics for the adjusted model
    adjusted_metrics = ClassificationMetric(
        aif_test_ds,
        dataset_pred_transformed_test,
        unprivileged_groups=unprivileged_groups,
        privileged_groups=privileged_groups
    )
    adjusted_spd = adjusted_metrics.statistical_parity_difference()
    adjusted_eod = adjusted_metrics.equal_opportunity_difference()

    fig, ax = plt.subplots(figsize=(8, 5))
    metrics_data = {
        'Metric': ['SPD', 'EOD'],
        'Value': [adjusted_spd, adjusted_eod]
    }
    metrics_df = pd.DataFrame(metrics_data)
    sns.barplot(x='Metric', y='Value', data=metrics_df, palette='cividis', ax=ax)
    ax.axhline(0, color='grey', linestyle='--', linewidth=0.8)
    ax.set_title(f'Threshold-Adjusted Model Fairness Metrics')
    ax.set_ylabel('Metric Value')
    ax.set_ylim(-0.5, 0.5)
    fig.tight_layout()

    return adjusted_accuracy, adjusted_spd, adjusted_eod, y_pred_adjusted, adjusted_report, fig

def main():
    st.header("⚖️ Fairness Analysis & Mitigation")

    if not st.session_state.get('data_loaded', False):
        st.warning("Please load and preprocess data in the 'Data Management' section first. 💡")
        return
    if st.session_state.get('baseline_model') is None:
        st.warning("Please train the Baseline Model in the 'Baseline Model' section first. 🤖")
        return

    st.markdown("""
    ### 1. Introduction to Fairness Metrics

    Fairness in AI is about ensuring that models do not perpetuate or amplify societal biases present in data. In credit lending, this means ensuring that different demographic groups are treated equitably. We will focus on two key fairness metrics from the AIF360 library:

    <div style="background-color:#fff3e0; padding: 10px; border-radius: 5px;">
    <p>💡 <b>Statistical Parity Difference (SPD):</b></p>
    <p>Measures the difference in the proportion of positive outcomes (e.g., loan approvals) between the unprivileged group ($a_0$) and the privileged group ($a_1$). An SPD of 0 indicates perfect statistical parity.</p>
    $$ SPD = P(\hat{Y}=1|A=a_1) - P(\hat{Y}=1|A=a_0) $$
    <p>Here, $P(\hat{Y}=1|A=a_1)$ is the rate of positive predictions for the privileged group (e.g., males), and $P(\hat{Y}=1|A=a_0)$ is the rate for the unprivileged group (e.g., females).</p>
    </div>

    <div style="background-color:#fff3e0; padding: 10px; border-radius: 5px;">
    <p>💡 <b>Equal Opportunity Difference (EOD):</b></p>
    <p>Measures the difference in the true positive rates (recall for the positive class) between the unprivileged group ($a_0$) and the privileged group ($a_1$), specifically among those who are truly qualified (actual $Y=1$). An EOD of 0 indicates equal opportunity.</p>
    $$ EOD = P(\hat{Y}=1|A=a_1, Y=1) - P(\hat{Y}=1|A=a_0, Y=1) $$
    <p>Here, $P(\hat{Y}=1|A=a_1, Y=1)$ is the true positive rate for the privileged group (males who actually deserved a loan and got it), and $P(\hat{Y}=1|A=a_0, Y=1)$ is the true positive rate for the unprivileged group (females who actually deserved a loan and got it).</p>
    </div>

    <div style="background-color:#e0f7fa; padding: 10px; border-radius: 5px;">
    <p>🛡️ <b>Protected Attributes:</b> These are characteristics that are legally protected from discrimination. In our dataset, we are considering `Gender` (Male as Privileged, Female as Unprivileged) and `AgeGroup` as protected attributes to analyze potential biases.</p>
    </div>
    """)

    st.markdown("""
    ### 2. Calculating Baseline Fairness Metrics

    Let's start by assessing the fairness of our **Baseline Logistic Regression Model** before any mitigation techniques are applied. This will give us a benchmark to understand the extent of any inherent biases.
    """)

    if st.button("Calculate Baseline Fairness Metrics ⚖️"):
        with st.spinner("Calculating fairness metrics for the baseline model..."):
            (st.session_state.baseline_spd,
             st.session_state.baseline_eod,
             baseline_tpr_priv,
             baseline_tpr_unpriv,
             baseline_pos_outcome_priv,
             baseline_pos_outcome_unpriv,
             baseline_fairness_fig) = calculate_fairness_metrics(
                 st.session_state.baseline_model,
                 st.session_state.X_test_df,
                 st.session_state.y_test,
                 st.session_state.protected_attribute_names,
                 st.session_state.aif360_privileged_groups,
                 st.session_state.aif360_unprivileged_groups,
                 model_name="Baseline Model"
             )
            st.success("Baseline fairness metrics calculated! 🎉")

            st.subheader("Baseline Model Fairness Overview")
            col_spd, col_eod = st.columns(2)
            with col_spd:
                st.metric(label="Statistical Parity Difference (SPD)", value=f"{st.session_state.baseline_spd:.3f}")
            with col_eod:
                st.metric(label="Equal Opportunity Difference (EOD)", value=f"{st.session_state.baseline_eod:.3f}")
            
            st.write(f"True Positive Rate (Privileged - Male): {baseline_tpr_priv:.3f}")
            st.write(f"True Positive Rate (Unprivileged - Female): {baseline_tpr_unpriv:.3f}")
            st.write(f"Positive Outcome Rate (Privileged - Male): {baseline_pos_outcome_priv:.3f}")
            st.write(f"Positive Outcome Rate (Unprivileged - Female): {baseline_pos_outcome_unpriv:.3f}")

            st.pyplot(baseline_fairness_fig)
            plt.close(baseline_fairness_fig)

            st.info("A value closer to 0 for SPD and EOD indicates fairer outcomes. Positive values mean the privileged group is favored, while negative values mean the unprivileged group is favored.")
    else:
        st.info("Click 'Calculate Baseline Fairness Metrics' to see the initial fairness assessment of your model. 🎯")


    st.markdown("""
    ### 3. Bias Mitigation Technique: Reweighting

    **Reweighting** is a **preprocessing technique** that aims to mitigate bias by adjusting the weights of individual training examples. It reweighs the examples in each (group, label) combination so that the model training process sees a more balanced representation. This helps ensure that the model pays equal attention to different demographic groups during training, regardless of their initial representation in the dataset.

    <div style="background-color:#e8f5e9; padding: 10px; border-radius: 5px;">
    <p>💡 <b>How Reweighting Works:</b></p>
    <p>Reweighting assigns a new weight $w_i$ to each sample $(x_i, y_i)$ in the training data, typically to balance the representation of protected groups and their outcomes. During model training, these weights are incorporated into the loss function, effectively making the model pay more or less attention to certain samples. For example, in a standard loss function, this would look like:</p>
    $$ \text{Loss}_{reweighted} = \sum_{i=1}^{N} w_i \cdot \text{Loss}(y_i, \hat{y}_i) $$
    <p>where $w_i$ is the reweighting factor for sample $i$, and $\text{Loss}(y_i, \hat{y}_i)$ is the original loss function for true label $y_i$ and predicted label $\hat{y}_i$. The weights are typically derived based on the joint probabilities of protected attributes and labels.</p>
    </div>
    """)

    if st.session_state.get('baseline_model') is not None and st.session_state.get('baseline_spd') is not None:
        if st.button("Apply Reweighting & Retrain Model 🔄"):
            with st.spinner("Applying Reweighting and retraining model..."):
                st.session_state.reweighed_model = apply_reweighing_and_retrain(
                    st.session_state.X_train_df,
                    st.session_state.y_train,
                    st.session_state.protected_attribute_names,
                    st.session_state.aif360_privileged_groups,
                    st.session_state.aif360_unprivileged_groups
                )
                st.success("Reweighed Model Trained Successfully! ✅")

                # Evaluate reweighed model
                (st.session_state.reweighed_accuracy, _, _, _, _, _, _) = evaluate_model(
                    st.session_state.reweighed_model, st.session_state.X_test_df, st.session_state.y_test, "Reweighed Model")

                (st.session_state.reweighed_spd,
                 st.session_state.reweighed_eod,
                 reweighed_tpr_priv,
                 reweighed_tpr_unpriv,
                 reweighed_pos_outcome_priv,
                 reweighed_pos_outcome_unpriv,
                 reweighed_fairness_fig) = calculate_fairness_metrics(
                     st.session_state.reweighed_model,
                     st.session_state.X_test_df,
                     st.session_state.y_test,
                     st.session_state.protected_attribute_names,
                     st.session_state.aif360_privileged_groups,
                     st.session_state.aif360_unprivileged_groups,
                     model_name="Reweighed Model"
                 )
                st.success("Reweighed Model Evaluated for Performance and Fairness! 🎉")

                st.subheader("Reweighed Model Performance and Fairness")
                st.metric(label="Accuracy", value=f"{st.session_state.reweighed_accuracy:.2f}")
                col_spd_rw, col_eod_rw = st.columns(2)
                with col_spd_rw:
                    st.metric(label="Statistical Parity Difference (SPD)", value=f"{st.session_state.reweighed_spd:.3f}")
                with col_eod_rw:
                    st.metric(label="Equal Opportunity Difference (EOD)", value=f"{st.session_state.reweighed_eod:.3f}")
                
                st.write(f"True Positive Rate (Privileged - Male): {reweighed_tpr_priv:.3f}")
                st.write(f"True Positive Rate (Unprivileged - Female): {reweighed_tpr_unpriv:.3f}")
                st.write(f"Positive Outcome Rate (Privileged - Male): {reweighed_pos_outcome_priv:.3f}")
                st.write(f"Positive Outcome Rate (Unprivileged - Female): {reweighed_pos_outcome_unpriv:.3f}")

                st.pyplot(reweighed_fairness_fig)
                plt.close(reweighed_fairness_fig)

                st.markdown("""
                💡 **What's happening here?**

                By reweighting the training data, we've attempted to reduce the bias the model learns. Observe how the SPD and EOD values have changed compared to the baseline model. A move closer to zero indicates improved fairness. However, sometimes there might be a trade-off with overall accuracy. We will compare this in the 'Comparative Analysis' section.
                """)
        else:
            st.info("Click 'Apply Reweighting & Retrain Model' to see how rebalancing training data can impact fairness. ⚖️")
    elif st.session_state.get('baseline_model') is not None:
         st.info("Calculate Baseline Fairness Metrics first to enable Reweighting. 🎯")

    st.markdown("""
    ### 4. Bias Mitigation Technique: Threshold Adjustment

    **Threshold Adjustment** (specifically, using Calibrated Equalized Odds Postprocessing) is a **postprocessing technique** that modifies the classification thresholds for different groups to achieve fairness. Instead of changing the model or the data, it adjusts the decision boundary *after* the model has made its predictions. This method is effective when you want to achieve specific fairness criteria without retraining the underlying model.

    <div style="background-color:#e1f5fe; padding: 10px; border-radius: 5px;">
    <p>💡 <b>How Threshold Adjustment Works:</b></p>
    <p>This technique finds the optimal classification thresholds $T_{a_0}$ and $T_{a_1}$ for the unprivileged ($a_0$) and privileged ($a_1$) groups, respectively. The model still outputs a probability $P(\hat{Y}=1|X)$, but the final prediction $\hat{Y}$ is made by comparing this probability to the group-specific threshold:</p>
    <ul>
        <li>If in unprivileged group ($A=a_0$): predict $\hat{Y}=1$ if $P(\hat{Y}=1|X) > T_{a_0}$</li>
        <li>If in privileged group ($A=a_1$): predict $\hat{Y}=1$ if $P(\hat{Y}=1|X) > T_{a_1}$</li>
    </ul>
    <p>The thresholds are chosen to satisfy a fairness criterion, such as equalized odds (equal true positive and false positive rates across groups).</p>
    </div>
    """)

    if st.session_state.get('baseline_model') is not None and st.session_state.get('baseline_spd') is not None:
        if st.button("Apply Threshold Adjustment & Evaluate ⚡"):
            with st.spinner("Applying Threshold Adjustment and evaluating..."):
                (st.session_state.adjusted_accuracy,
                 st.session_state.adjusted_spd,
                 st.session_state.adjusted_eod,
                 adjusted_predictions,
                 adjusted_report,
                 adjusted_fairness_fig) = apply_threshold_adjustment_and_evaluate(
                     st.session_state.baseline_model,
                     st.session_state.X_train_df,
                     st.session_state.y_train,
                     st.session_state.X_test_df,
                     st.session_state.y_test,
                     st.session_state.protected_attribute_names,
                     st.session_state.aif360_privileged_groups,
                     st.session_state.aif360_unprivileged_groups
                 )
                st.success("Threshold-Adjusted Model Evaluated! 🎉")

                st.subheader("Threshold-Adjusted Model Performance and Fairness")
                st.metric(label="Accuracy", value=f"{st.session_state.adjusted_accuracy:.2f}")
                col_spd_ta, col_eod_ta = st.columns(2)
                with col_spd_ta:
                    st.metric(label="Statistical Parity Difference (SPD)", value=f"{st.session_state.adjusted_spd:.3f}")
                with col_eod_ta:
                    st.metric(label="Equal Opportunity Difference (EOD)", value=f"{st.session_state.adjusted_eod:.3f}")

                # Re-calculating TPRs and Positive Outcome Rates for adjusted model for display consistency
                # This requires an extra call to ClassificationMetric with the adjusted predictions
                adjusted_aif_test_df = st.session_state.X_test_df.copy()
                adjusted_aif_test_df['LoanApproved'] = st.session_state.y_test.values
                adjusted_aif_test_ds = StandardDataset(
                    adjusted_aif_test_df, label_name='LoanApproved', favorable_classes=[1],
                    protected_attribute_names=st.session_state.protected_attribute_names,
                    privileged_classes=[[1]]
                )
                adjusted_dataset_pred = adjusted_aif_test_ds.copy()
                adjusted_dataset_pred.labels = adjusted_predictions
                adjusted_metric_display = ClassificationMetric(
                    adjusted_aif_test_ds, adjusted_dataset_pred,
                    unprivileged_groups=st.session_state.aif360_unprivileged_groups,
                    privileged_groups=st.session_state.aif360_privileged_groups
                )
                adjusted_tpr_priv = adjusted_metric_display.true_positive_rate(privileged=True)
                adjusted_tpr_unpriv = adjusted_metric_display.true_positive_rate(privileged=False)
                adjusted_pos_outcome_priv = adjusted_metric_display.selection_rate(privileged=True)
                adjusted_pos_outcome_unpriv = adjusted_metric_display.selection_rate(privileged=False)

                st.write(f"True Positive Rate (Privileged - Male): {adjusted_tpr_priv:.3f}")
                st.write(f"True Positive Rate (Unprivileged - Female): {adjusted_tpr_unpriv:.3f}")
                st.write(f"Positive Outcome Rate (Privileged - Male): {adjusted_pos_outcome_priv:.3f}")
                st.write(f"Positive Outcome Rate (Unprivileged - Female): {adjusted_pos_outcome_unpriv:.3f}")

                st.pyplot(adjusted_fairness_fig)
                plt.close(adjusted_fairness_fig)

                st.markdown("""
                💡 **What's happening here?**

                By adjusting the classification thresholds for different groups, we aim to achieve fairer outcomes, particularly focusing on Equal Opportunity. Observe how the SPD and EOD values have shifted. This method often allows for fine-tuning fairness without altering the core model, offering a different trade-off landscape than preprocessing techniques.
                """)
        else:
            st.info("Click 'Apply Threshold Adjustment & Evaluate' to explore post-processing bias mitigation. ⚡")
    elif st.session_state.get('baseline_model') is not None:
         st.info("Calculate Baseline Fairness Metrics first to enable Threshold Adjustment. 🎯")

if __name__ == '__main__':
    main()
