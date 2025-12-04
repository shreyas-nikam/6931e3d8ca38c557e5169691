import streamlit as st

def main():
    st.title("🎯 AI Credit Decision Explainer - Interactive Lab")

    st.markdown("""
    ## 📖 Scenario: Navigating the AI Frontier in Credit Lending

    Welcome, trailblazer! In the fast-paced world of financial services, Artificial Intelligence (AI) is transforming how credit decisions are made. While AI offers immense potential for efficiency and accuracy, it also brings forth critical questions about transparency, fairness, and accountability. As a **Risk Manager, Executive Stakeholder**, or **Financial Data Engineer**, your mission is to not just use AI, but to truly understand and master it.

    This interactive lab is your sandbox for exploring the inner workings of an AI-driven credit lending model. We'll embark on a journey through a simulated credit application process, using the renowned **UCI German Credit Dataset**.

    ### Your Journey Ahead:

    *   **🔍 Demystifying Decisions:** Ever wondered *why* an AI approves or denies a loan? We'll use cutting-edge **eXplainable AI (XAI)** techniques like **LIME** (Local Interpretable Model-agnostic Explanations) and **SHAP** (SHapley Additive exPlanations) to peer into the model's "brain." You'll see which factors influence individual decisions and understand the overall drivers of credit approval across a portfolio.

    *   **⚖️ Unmasking Bias:** AI, while powerful, can sometimes inherit and even amplify biases present in historical data. We'll confront the critical issue of **algorithmic fairness**, identifying and quantifying potential biases in our credit decisions using industry-standard metrics like **Statistical Parity Difference (SPD)** and **Equal Opportunity Difference (EOD)**.

    *   **🛠️ Forging Fairer Futures:** The journey doesn't stop at identifying bias. You'll actively apply and evaluate **bias mitigation techniques**, specifically **Reweighting** (a preprocessing method) and **Threshold Adjustment** (a postprocessing method). Witness how these strategies impact both model performance and fairness, and learn to navigate the delicate trade-offs.

    *   **🚀 Building Trust in AI:** Ultimately, this lab is about empowering you to build, deploy, and trust AI systems responsibly. By the end of this experience, you'll have a practical understanding of how to make AI models transparent, accountable, and fair, fostering greater confidence in their deployment in critical financial applications.

    Get ready to roll up your sleeves and dive into the exciting world of Responsible AI! Let's make some transparent and fair credit decisions! 💡
    """)

    st.info("Navigate through the sections using the sidebar to begin your exploration!")

if __name__ == '__main__':
    main()
