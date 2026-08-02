import streamlit as st
from agents.synthesis_agent import SynthesisAgent

# ---------------------------------------------------
# Page Configuration
# ---------------------------------------------------
st.set_page_config(
    page_title="Dengue Surveillance AI",
    page_icon="🦟",
    layout="wide"
)

# ---------------------------------------------------
# Title
# ---------------------------------------------------
st.title("🦟 Dengue Surveillance Decision-Support System")
st.write(
    "Sri Lanka district-level dengue risk assessment powered by Agentic AI."
)
st.divider()

# ---------------------------------------------------
# User Inputs
# ---------------------------------------------------
district = st.selectbox(
    "Select District",
    [
        "Colombo",
        "Gampaha",
        "Kalutara",
        "Jaffna"
    ]
)

query = st.text_area(
    "Query / Focus Area",
    value=f"Generate a dengue risk assessment for {district}.",
    height=120
)

# ---------------------------------------------------
# Generate Report
# ---------------------------------------------------
if st.button("Generate Report", use_container_width=True):
    with st.spinner("Analyzing weather, epidemiological data and guidelines..."):
        try:
            agent = SynthesisAgent()
            report = agent.generate_report(
                district=district,
                query=query
            )
            st.success("Report generated successfully!")
            st.subheader("📄 Dengue Risk Assessment Report")
            st.markdown(report)
        except Exception as e:
            st.error(f"Error generating report: {str(e)}")