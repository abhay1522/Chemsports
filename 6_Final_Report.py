import plotly.express as px
import streamlit as st
from utils import setup, load_df, footer

setup("Final Project Report", "🏆")
df = load_df()
st.markdown("""<div class="card"><b>Aim:</b> analyse the chemistry of a car (fuels, fluids, polymers,
emissions) and a driver's glovebox (common drugs) using RDKit descriptors.<br>
<b>Method:</b> SMILES → RDKit → MW, LogP, TPSA, HBD, HBA, rotatable bonds, rings → Lipinski rule → plots.</div>""",
            unsafe_allow_html=True)
a, b, c = st.columns(3)
a.metric("Heaviest", df.loc[df.MW.idxmax(), "Name"], f"{df.MW.max()} g/mol")
b.metric("Most lipophilic", df.loc[df.LogP.idxmax(), "Name"], f"LogP {df.LogP.max()}")
c.metric("Most polar (TPSA)", df.loc[df.TPSA.idxmax(), "Name"], f"{df.TPSA.max()} Å²")
st.plotly_chart(px.bar(df.groupby("Group").MW.mean().round(1).reset_index(), x="Group", y="MW",
                       color="Group", template="plotly_dark", title="Average MW by group"),
                use_container_width=True)
st.write(f"Drug-like (Rule of Five): **{(df.Drug_like == 'Yes').sum()} / {len(df)}** compounds.")
st.download_button("⬇️ Full data (CSV)", df.to_csv(index=False).encode(), "chem_garage_report.csv")
st.subheader("Conclusion")
st.markdown("- Branched/aromatic hydrocarbons are lipophilic and fuel-like.\n- Polar fluids (urea, glycol) have low LogP and high TPSA.\n"
            "- Almost all common drugs here obey Lipinski's rule, which supports oral use.")
footer()
