import streamlit as st
from utils import setup, footer

setup("Theory", "📘")
topics = {
 "SMILES notation": "A text code for a structure. `CCO` = ethanol, `c1ccccc1` = benzene (lowercase = aromatic ring). It is how the app stores every molecule.",
 "Molecular weight (MW)": "Sum of atomic masses (g/mol). Like a car's kerb weight: heavier molecules are usually less volatile (diesel > petrol > LPG).",
 "LogP (lipophilicity)": "How much a molecule prefers oil over water. High LogP = fuel-like (benzene, isooctane); low = water-soluble (urea, glycol). Crippen method in RDKit.",
 "TPSA": "Topological Polar Surface Area (Å²): surface of N and O atoms. Low TPSA means better membrane absorption for drugs.",
 "H-bond donors / acceptors": "HBD = N-H/O-H groups, HBA = N/O atoms. They control solubility and boiling point (ethylene glycol boils at 197 °C because of H-bonds).",
 "Rotatable bonds": "Flexible single bonds. More = more floppy; more than 10 hurts oral drug absorption.",
 "Lipinski Rule of Five": "A drug is likely orally active if: MW ≤ 500, LogP ≤ 5, HBD ≤ 5, HBA ≤ 10 (at most one violation allowed). Think of it as the 'emission test' for drugs.",
 "Octane rating analogy": "Isooctane (branched) resists knocking = 100; n-heptane (straight chain) knocks = 0. Shape of the molecule changes behaviour even with the same carbon count.",
}
for t, d in topics.items():
    with st.expander(t, expanded=(t == "SMILES notation")):
        st.markdown(d)
st.info("Tip: open **Molecular Visualization** and compare isooctane and n-heptane in 3D.")
footer()
