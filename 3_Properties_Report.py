import streamlit as st
from utils import setup, load_df, mol_image, footer

setup("Molecular Properties Report", "📊")
df = load_df()
c1, c2, c3 = st.columns(3)
kinds = c1.multiselect("Type", ["Molecule", "Drug"], default=["Molecule", "Drug"])
groups = c2.multiselect("Group", sorted(df.Group.unique()), default=sorted(df.Group.unique()))
q = c3.text_input("Search name")
f = df[df.Type.isin(kinds) & df.Group.isin(groups)]
if q:
    f = f[f.Name.str.contains(q, case=False)]
st.dataframe(f.drop(columns=["Role"]), use_container_width=True, height=380)
st.download_button("⬇️ Download CSV", f.to_csv(index=False).encode(), "properties.csv", "text/csv")

st.subheader("Single molecule report")
if len(f):
    n = st.selectbox("Molecule", f.Name.tolist())
    r = f[f.Name == n].iloc[0]
    a, b = st.columns([1, 2])
    a.image(mol_image(r.SMILES), use_container_width=True)
    with b:
        st.markdown(f"**{r.Name}** ({r.Formula}) · {r.Role}")
        cols = st.columns(4)
        for i, k in enumerate(["MW", "LogP", "TPSA", "HBD", "HBA", "RotB", "Rings", "HeavyAtoms"]):
            cols[i % 4].metric(k, r[k])
        st.write(f"Lipinski violations: **{r.Lipinski_Violations}** → drug-like: **{r.Drug_like}**")
footer()
