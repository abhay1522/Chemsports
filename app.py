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
from pathlib import Path
ICONS = {"theory": "📘", "visual": "🧬", "propert": "📊", "structure": "📈", "assess": "📝", "final": "🏆"}
pdir = Path(__file__).parent / "pages"
files = sorted(pdir.glob("*.py")) if pdir.exists() else []
if not files:
    st.warning("The 'pages' folder was not found in the repository. Upload the 6 files into a folder named 'pages'.")
cols = st.columns(3)
for i, f in enumerate(files):
    label = f.stem.lstrip("0123456789 _-").replace("_", " ")
    icon = next((v for k, v in ICONS.items() if k in label.lower()), "➡️")
    with cols[i % 3]:
        try:
            st.page_link(f"pages/{f.name}", label=label, icon=icon, use_container_width=True)
        except Exception:
            st.write(f"{icon} {label} (use the sidebar)")
footer()
