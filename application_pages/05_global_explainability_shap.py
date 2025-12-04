import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import shap
import seaborn as sns # For general plotting style

@st.cache_data(ttl="2h")
def generate_shap_summary(model, X_train_df, X_test_df, feature_names):
    # For LinearExplainer, background is often a subset of the training data
    # or the entire training data mean/median.
    # Using a sample from X_train_df as background for performance.
    background = shap.sample(X_train_df, 100) # Sample 100 instances for background
    
    # For LogisticRegression (linear model), LinearExplainer is appropriate.
    explainer = shap.LinearExplainer(model, background)
    
    # Calculate SHAP values for the test set
    shap_values = explainer.shap_values(X_test_df)

    # Create a figure object explicitly for Streamlit
    fig, ax = plt.subplots(figsize=(10, 6))
    shap.summary_plot(shap_values, X_test_df, feature_names=feature_names, show=False, ax=ax, plot_type="bar") # Changed to plot_type="bar" for better readability of global importance
    ax.set_title('SHAP Global Feature Importance (Loan Approved)')
    fig.tight_layout()
    return fig, shap_values

@st.cache_data(ttl="2h")
def generate_shap_dependence_plot(shap_values, X_data, feature_name, feature_names_list, interaction_feature=None):
    fig, ax = plt.subplots(figsize=(10, 6)) # Create a figure object explicitly for Streamlit
    shap.dependence_plot(
        ind=feature_name,
        shap_values=shap_values,
        features=X_data,
        feature_names=feature_names_list,
        interaction_index=interaction_feature,
        show=False,
        ax=ax # Pass the axes object
    )
    ax.set_title(f'SHAP Dependence Plot: {feature_name}' + (f' with {interaction_feature}' if interaction_feature else ''))
    fig.tight_layout()
    return fig

def main():
    st.header("🌍 Global Explainability (SHAP)")

    st.markdown("""
    ### 1. Global Explainability with SHAP

    Moving beyond individual predictions, **Global Explainability** helps us understand the overall behavior of our AI model. **SHAP** (SHapley Additive exPlanations) is a game-theory based approach that provides a unified framework to explain any model's predictions by assigning each feature an importance value for a particular prediction. It connects optimal credit allocation with local explanations using Shapley values.

    <div style="background-color:#e6f7ff; padding: 10px; border-radius: 5px;">
    <p>💡 <b>How SHAP Values Work:</b></p>
    <p>SHAP values quantify the contribution of each feature to the prediction for a given instance, relative to a baseline prediction (e.g., the average prediction). The SHAP value $\phi_j$ for a feature $j$ is calculated as:</p>
    $$ \phi_j = \sum_{S \subseteq N \setminus \{j\}} \frac{|S|!(|N| - |S| - 1)!}{|N|!} [f_x(S \cup \{j\}) - f_x(S)] $$
    <p>where $N$ is the set of all features, $S$ is a subset of features, and $f_x(S)$ is the model's prediction with features in $S$ present. This formula ensures that feature contributions are distributed fairly and consistently across all features.</p>
    </div>

    In this section, you'll generate a SHAP summary plot to see the most important features globally, and then dive deeper with SHAP dependence plots.
    """)

    if not st.session_state.get('data_loaded', False):
        st.warning("Please load and preprocess data in the 'Data Management' section first. 💡")
        return
    if st.session_state.get('baseline_model') is None:
        st.warning("Please train the Baseline Model in the 'Baseline Model' section first. 🤖")
        return

    st.subheader("SHAP Summary Plot: Global Feature Importance")
    st.markdown("""
    The **SHAP Summary Plot** provides a concise overview of the most impactful features across the entire dataset. Each point on the plot represents a Shapley value for a feature and an instance. The color indicates the feature value (e.g., red for high, blue for low), and the position on the x-axis indicates the impact on the model output (prediction). A vertical stack of points represents the density of instances at that impact level.
    """)

    if st.button("Generate SHAP Summary Plot 📊"):
        with st.spinner("Generating SHAP summary plot..."):
            shap_summary_fig, shap_values_baseline = generate_shap_summary(
                st.session_state.baseline_model,
                st.session_state.X_train_df,
                st.session_state.X_test_df,
                st.session_state.all_feature_names
            )
            st.session_state.shap_values_baseline = shap_values_baseline # Store for dependence plots
            st.pyplot(shap_summary_fig)
            plt.close(shap_summary_fig)
            st.success("SHAP Summary Plot Generated! ✅")
    else:
        st.info("Click 'Generate SHAP Summary Plot' to visualize the overall importance of features in our credit decision model. 📈")


    st.markdown("""
    ### 2. SHAP Dependence Plots

    **SHAP Dependence Plots** illustrate how the value of a single feature affects the prediction of the model. They show how SHAP values for a feature change as the feature itself changes, providing insights into non-linear relationships and interactions.

    By selecting an **Interaction Feature**, you can also explore how the primary feature's impact is modulated by the values of another feature, revealing complex interactions within the model.
    """)

    if st.session_state.get('shap_values_baseline') is not None:
        # Ensure all_feature_names is available and not empty
        if not st.session_state.get('all_feature_names') or len(st.session_state.all_feature_names) == 0:
            st.warning("Feature names not available. Please ensure data is loaded and preprocessed.")
            return

        all_feature_names_list = st.session_state.all_feature_names

        # Handle case where all_feature_names_list might be empty or contain only a few items
        if not all_feature_names_list:
            st.warning("No features available for SHAP Dependence Plot.")
            return
        
        # Default index for selectbox, ensure it's within bounds
        default_primary_feature_index = 0
        if 'CreditAmount' in all_feature_names_list:
            default_primary_feature_index = all_feature_names_list.index('CreditAmount')
        elif len(all_feature_names_list) > 0:
            default_primary_feature_index = 0
        else:
            st.warning("No features available for SHAP Dependence Plot.")
            return


        primary_feature = st.selectbox(
            "Select Primary Feature for Dependence Plot",
            options=all_feature_names_list,
            index=default_primary_feature_index
        )

        interaction_feature_options = ['None'] + [f for f in all_feature_names_list if f != primary_feature]
        interaction_feature_selected = st.selectbox(
            "Select Interaction Feature (Optional)",
            options=interaction_feature_options,
            index=0 # Default to 'None'
        )
        interaction_feature = None if interaction_feature_selected == 'None' else interaction_feature_selected

        if st.button("Generate SHAP Dependence Plot 📈"):
            with st.spinner(f"Generating SHAP dependence plot for {primary_feature}" + (f" with interaction {interaction_feature}" if interaction_feature else "") + "..."):
                shap_dep_fig = generate_shap_dependence_plot(
                    st.session_state.shap_values_baseline,
                    st.session_state.X_test_df,
                    primary_feature,
                    all_feature_names_list,
                    interaction_feature
                )
                st.pyplot(shap_dep_fig)
                plt.close(shap_dep_fig)
                st.success(f"SHAP Dependence Plot for {primary_feature} Generated! ✅")
        else:
            st.info("Select a primary feature (and optionally an interaction feature) and click 'Generate SHAP Dependence Plot' to explore feature relationships. 🔬")
    else:
        st.info("Please generate the SHAP Summary Plot first to enable dependence plots. 👆")

if __name__ == '__main__':
    main()
