import streamlit as st
from utils import setup, load_df, mol_image, viewer3d, footer

setup("Molecular Visualization", "🧬")
df = load_df()
with st.sidebar:
    kind = st.radio("Type", ["All", "Molecule", "Drug"])
    pool = df if kind == "All" else df[df.Type == kind]
    group = st.selectbox("Group", ["All"] + sorted(pool.Group.unique()))
    if group != "All":
        pool = pool[pool.Group == group]
    name = st.selectbox("Choose molecule", pool.Name.tolist())
    style = st.radio("3D style", ["ball & stick", "stick", "sphere", "line"])
row = df[df.Name == name].iloc[0]
a, b = st.columns(2)
with a:
    st.subheader("2D structure")
    st.image(mol_image(row.SMILES), use_container_width=True)
with b:
    st.subheader("3D (drag to rotate)")
    viewer3d(row.SMILES, style)
st.markdown(f'<div class="card"><b>{row.Name}</b> · {row.Formula} · {row.Group}<br>'
            f'Garage role: {row.Role}<br>SMILES: <code>{row.SMILES}</code></div>', unsafe_allow_html=True)
m1, m2, m3, m4 = st.columns(4)
m1.metric("MW (g/mol)", row.MW); m2.metric("LogP", row.LogP)
m3.metric("TPSA (Å²)", row.TPSA); m4.metric("Drug-like", row.Drug_like)
footer()
