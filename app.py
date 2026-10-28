import streamlit as st
from utils import setup, load_df, footer

setup("Home", "🏁")
df = load_df()
c1, c2, c3, c4 = st.columns(4)
c1.metric("Molecules", int((df.Type == "Molecule").sum()))
c2.metric("Drugs", int((df.Type == "Drug").sum()))
c3.metric("Properties / molecule", 12)
c4.metric("Groups", df.Group.nunique())

st.markdown("""<div class="card"><b>What is this lab?</b><br>
Every molecule in a car (fuels, coolant, rubber, plastics, exhaust gases) and in the driver's
glovebox (common drugs) is analysed with <b>RDKit</b>: 2D/3D structure, molecular properties,
Lipinski drug-likeness, and structure-property relationships.</div>""", unsafe_allow_html=True)

st.subheader("Pit lane (pages)")
pages = [("pages/1_Theory.py", "Theory", "📘"), ("pages/2_Molecular_Visualization.py", "Molecular Visualization", "🧬"),
         ("pages/3_Properties_Report.py", "Molecular Properties Report", "📊"),
         ("pages/4_Structure_Property.py", "Structure–Property Analysis", "📈"),
         ("pages/5_Assessment.py", "Assessment", "📝"), ("pages/6_Final_Report.py", "Final Project Report", "🏆")]
cols = st.columns(3)
for i, (p, label, icon) in enumerate(pages):
    with cols[i % 3]:
        st.page_link(p, label=label, icon=icon, use_container_width=True)
footer()
