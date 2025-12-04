import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("whitegrid")
plt.rcParams.update({'font.size': 10})

@st.cache_data(ttl="2h")
def plot_comparative_metrics(baseline_acc, baseline_spd, baseline_eod,
                                 reweighed_acc, reweighed_spd, reweighed_eod,
                                 adjusted_acc, adjusted_spd, adjusted_eod):
    metrics = ['Accuracy', 'SPD', 'EOD']
    baseline_values = [baseline_acc, baseline_spd, baseline_eod]
    reweighed_values = [reweighed_acc, reweighed_spd, reweighed_eod]
    adjusted_values = [adjusted_acc, adjusted_spd, adjusted_eod]

    df_comparison = pd.DataFrame({
        'Metric': metrics * 3,
        'Value': baseline_values + reweighed_values + adjusted_values,
        'Model': ['Baseline'] * 3 + ['Reweighed'] * 3 + ['Threshold-Adjusted'] * 3
    })

    fig, axes = plt.subplots(1, 3, figsize=(18, 6), sharey=False)

    # Accuracy Plot
    sns.barplot(x='Model', y='Value', data=df_comparison[df_comparison['Metric'] == 'Accuracy'], ax=axes[0], palette='pastel')
    axes[0].set_title('Model Accuracy Comparison')
    axes[0].set_ylabel('Accuracy')
    axes[0].set_ylim(0.5, 1.0) # Adjusted for typical accuracy range

    # SPD Plot
    sns.barplot(x='Model', y='Value', data=df_comparison[df_comparison['Metric'] == 'SPD'], ax=axes[1], palette='deep')
    axes[1].axhline(0, color='grey', linestyle='--', linewidth=0.8)
    axes[1].set_title('Statistical Parity Difference (SPD) Comparison')
    axes[1].set_ylabel('SPD Value')
    axes[1].set_ylim(-0.25, 0.25) # Consistent y-axis for fairness metrics

    # EOD Plot
    sns.barplot(x='Model', y='Value', data=df_comparison[df_comparison['Metric'] == 'EOD'], ax=axes[2], palette='dark')
    axes[2].axhline(0, color='grey', linestyle='--', linewidth=0.8)
    axes[2].set_title('Equal Opportunity Difference (EOD) Comparison')
    axes[2].set_ylabel('EOD Value')
    axes[2].set_ylim(-0.25, 0.25) # Consistent y-axis for fairness metrics

    fig.tight_layout()
    return fig

def main():
    st.header("📈 Comparative Analysis")

    st.markdown("""
    ### 1. Comparative Analysis of Mitigation Techniques

    After exploring individual models and bias mitigation strategies, it's crucial to compare their performance and fairness trade-offs. This section provides a comprehensive overview of how the **Baseline Model**, the **Reweighed Model**, and the **Threshold-Adjusted Model** stack up against each other across key metrics.

    This comparative view will help you understand:

    *   How different mitigation techniques impact predictive accuracy.
    *   Their effectiveness in reducing **Statistical Parity Difference (SPD)** and **Equal Opportunity Difference (EOD)**.
    *   The inherent trade-offs between model performance and fairness, guiding you towards more responsible AI deployment decisions.
    """)

    # Check if necessary session states are populated
    required_states = [
        'baseline_accuracy', 'baseline_spd', 'baseline_eod',
        'reweighed_accuracy', 'reweighed_spd', 'reweighed_eod',
        'adjusted_accuracy', 'adjusted_spd', 'adjusted_eod'
    ]
    all_metrics_available = all(st.session_state.get(state) is not None for state in required_states)

    if not all_metrics_available:
        st.warning("Please ensure the Baseline Model is trained and fairness metrics for all models (Baseline, Reweighed, Threshold-Adjusted) are calculated in previous sections before proceeding. 💡")
        return

    if st.button("Generate Comparative Metrics Plot 📊"):
        with st.spinner("Generating comparative plots..."):
            comparative_fig = plot_comparative_metrics(
                st.session_state.baseline_accuracy, st.session_state.baseline_spd, st.session_state.baseline_eod,
                st.session_state.reweighed_accuracy, st.session_state.reweighed_spd, st.session_state.reweighed_eod,
                st.session_state.adjusted_accuracy, st.session_state.adjusted_spd, st.session_state.adjusted_eod
            )
            st.pyplot(comparative_fig)
            plt.close(comparative_fig) # Close the figure to prevent display issues
            st.success("Comparative Analysis Plot Generated! 🎉")
    else:
        st.info("Click 'Generate Comparative Metrics Plot' to visualize the trade-offs between accuracy and fairness across different models. 📈")

if __name__ == '__main__':
    main()
