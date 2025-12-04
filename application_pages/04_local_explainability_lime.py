import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import lime
import lime.lime_tabular

@st.cache_data(ttl="2h")
def generate_lime_explanation(model, X_train_df, X_test_df, feature_names, instance_idx):
    explainer = lime.lime_tabular.LimeTabularExplainer(
        training_data=X_train_df.values,
        feature_names=feature_names,
        class_names=['Denied', 'Approved'],
        mode='classification',
        random_state=42
    )
    instance = X_test_df.iloc[instance_idx]
    explanation = explainer.explain_instance(
        data_row=instance.values,
        predict_fn=model.predict_proba,
        num_features=10,
        num_samples=5000
    )
    prediction = model.predict(instance.to_frame().T)[0]
    proba = model.predict_proba(instance.to_frame().T)[0]

    fig = explanation.as_pyplot_figure()
    plt.title(f'LIME Explanation for Test Instance {instance_idx}')
    plt.tight_layout()
    return fig, explanation, prediction, proba

def main():
    st.header("🔍 Local Explainability (LIME)")

    st.markdown("""
    ### 1. Local Explainability with LIME

    Welcome to the realm of **Local Explainability**! While a model's overall performance metrics are crucial, understanding *why* a specific prediction was made for an individual applicant is paramount in high-stakes domains like credit lending. This is where **LIME** (Local Interpretable Model-agnostic Explanations) shines. LIME helps us understand the predictions of any black-box machine learning model by approximating it locally with an interpretable model.

    <div style="background-color:#e6f7ff; padding: 10px; border-radius: 5px;">
    <p>💡 <b>How LIME Works:</b></p>
    <p>LIME generates a local, interpretable approximation of the black-box model's behavior around a specific instance. It does this by:</p>
    <ol>
        <li>Perturbing the input instance to create new, slightly modified samples.</li>
        <li>Getting predictions from the black-box model for these perturbed samples.</li>
        <li>Weighting the perturbed samples by their proximity to the original instance.</li>
        <li>Training a simple, interpretable model (e.g., linear model) on these weighted samples and their predictions.</li>
    </ol>
    <p>The weighted loss function minimized by LIME is:</p>
    $$ L(f, g, \pi_x) = \sum_{z \in Z} \pi_x(z) (f(z) - g(z))^2 $$
    <p>where $f$ is the black-box model, $g$ is the interpretable model, $Z$ is the set of perturbed samples, and $\pi_x(z)$ is the proximity measure of $z$ to the instance $x$ being explained.</p>
    </div>

    In this section, you can select any test instance and generate a LIME explanation to see which features contributed positively or negatively to the model's prediction for that specific individual.
    """)

    if not st.session_state.get('data_loaded', False):
        st.warning("Please load and preprocess data in the 'Data Management' section first. 💡")
        return
    if st.session_state.get('baseline_model') is None:
        st.warning("Please train the Baseline Model in the 'Baseline Model' section first. 🤖")
        return

    X_test_df_len = len(st.session_state.X_test_df)
    if X_test_df_len == 0:
        st.warning("Test data is empty. Cannot generate LIME explanation.")
        return

    # Ensure the options list is not empty before creating selectbox
    test_instance_options = list(range(X_test_df_len))
    if not test_instance_options:
        st.warning("No test instances available to select for LIME explanation.")
        return

    selected_instance_idx = st.selectbox(
        "Select a Test Instance Index for Explanation",
        options=test_instance_options,
        index=0 # Default to the first instance
    )

    if st.button("Generate LIME Explanation ⚡"):
        with st.spinner(f"Generating LIME explanation for instance {selected_instance_idx}..."):
            lime_fig, _, prediction, proba = generate_lime_explanation(
                st.session_state.baseline_model,
                st.session_state.X_train_df,
                st.session_state.X_test_df,
                st.session_state.all_feature_names,
                selected_instance_idx
            )

            st.subheader(f"LIME Explanation for Instance {selected_instance_idx}")
            st.write(f"**Model's Prediction:** {'Approved' if prediction == 1 else 'Denied'}")
            st.write(f"**Probability of Approval:** {proba[1]:.2f}")
            st.pyplot(lime_fig)
            plt.close(lime_fig) # Close the figure to prevent display issues in Streamlit

            st.markdown("""
            💡 **What's happening here?**

            The LIME plot above shows the top features influencing the model's decision for the selected individual. 
            *   **Green bars** indicate features that pushed the prediction towards **Approved (1)**.
            *   **Red bars** indicate features that pushed the prediction towards **Denied (0)**.
            *   The length of the bar represents the strength of the influence.

            By examining these local explanations, you can understand how different attributes of a credit applicant (e.g., CreditAmount, CreditHistory, Age) contributed to their specific loan approval or denial, making the black-box model's decision transparent on an individual level.
            """)
    else:
        st.info("Select an instance and click 'Generate LIME Explanation' to understand individual loan decisions. 🧐")

if __name__ == '__main__':
    main()
