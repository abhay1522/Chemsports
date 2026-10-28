import json
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from rdkit import Chem
from rdkit.Chem import AllChem, Descriptors, Crippen, rdMolDescriptors, Lipinski, rdDepictor

AUTHOR = "Abhay Raj"
DEPT = "B.Tech CSE (AI/ML) · Section C · SRM Institute of Science and Technology, Tiruchirappalli"
NUM = ["MW", "LogP", "TPSA", "HBD", "HBA", "RotB", "Rings", "AromRings", "HeavyAtoms"]

# (name, SMILES, group, role in the "garage")
MOLECULES = [
    ("Methane", "C", "Fuel", "CNG main component"),
    ("Methanol", "CO", "Fuel", "Racing / alternative fuel"),
    ("Ethanol", "CCO", "Fuel", "E10/E20 petrol blend"),
    ("Propane", "CCC", "Fuel", "LPG autogas"),
    ("Butane", "CCCC", "Fuel", "LPG autogas"),
    ("Hexane", "CCCCCC", "Fuel", "Light petrol fraction"),
    ("n-Heptane", "CCCCCCC", "Fuel", "Octane rating = 0 reference"),
    ("Isooctane", "CC(C)CC(C)(C)C", "Fuel", "Octane rating = 100 reference"),
    ("MTBE", "COC(C)(C)C", "Additive", "Anti-knock octane booster"),
    ("Benzene", "c1ccccc1", "Aromatic", "Petrol component, toxic"),
    ("Toluene", "Cc1ccccc1", "Aromatic", "Octane booster"),
    ("p-Xylene", "Cc1ccc(C)cc1", "Aromatic", "Petrol / PET plastic feedstock"),
    ("Naphthalene", "c1ccc2ccccc2c1", "Aromatic", "Diesel/coal-tar fraction"),
    ("Acetylene", "C#C", "Fuel", "Oxy-acetylene welding in garages"),
    ("Ethylene", "C=C", "Monomer", "Polyethylene: fuel tank, bumpers"),
    ("Propylene", "CC=C", "Monomer", "Polypropylene: dashboard, bumpers"),
    ("1,3-Butadiene", "C=CC=C", "Monomer", "Synthetic rubber tyres"),
    ("Isoprene", "C=CC(C)=C", "Monomer", "Natural/synthetic rubber unit"),
    ("Styrene", "C=Cc1ccccc1", "Monomer", "Tyre rubber (SBR), ABS parts"),
    ("Vinyl chloride", "C=CCl", "Monomer", "PVC wiring insulation"),
    ("Tetrafluoroethylene", "FC(F)=C(F)F", "Monomer", "Teflon seals and gaskets"),
    ("Ethylene glycol", "OCCO", "Fluid", "Radiator coolant / antifreeze"),
    ("Glycerol", "OCC(O)CO", "Fluid", "Biodiesel by-product"),
    ("Urea", "NC(N)=O", "Fluid", "AdBlue diesel emission fluid"),
    ("Ammonia", "N", "Fluid", "Reduces NOx in SCR exhaust systems"),
    ("Sulfuric acid", "OS(=O)(=O)O", "Fluid", "Lead-acid battery electrolyte"),
    ("Carbon dioxide", "O=C=O", "Emission", "Complete combustion product"),
    ("Carbon monoxide", "[C-]#[O+]", "Emission", "Incomplete combustion, toxic"),
    ("Nitrogen dioxide", "[O-][N+]=O", "Emission", "Diesel exhaust NOx"),
    ("Water", "O", "Emission", "Combustion product, steam"),
]

DRUGS = [
    ("Paracetamol", "CC(=O)Nc1ccc(O)cc1", "Drug", "Fever / pain (PCM tablet)"),
    ("Caffeine", "Cn1cnc2c1c(=O)n(C)c(=O)n2C", "Drug", "Driver alertness"),
    ("Aspirin", "CC(=O)Oc1ccccc1C(=O)O", "Drug", "Pain, blood thinner"),
    ("Ibuprofen", "CC(C)Cc1ccc(cc1)C(C)C(=O)O", "Drug", "Pain, inflammation"),
    ("Naproxen", "COc1ccc2cc(ccc2c1)C(C)C(=O)O", "Drug", "Long-lasting pain relief"),
    ("Diclofenac", "OC(=O)Cc1ccccc1Nc1c(Cl)cccc1Cl", "Drug", "Muscle / joint pain"),
    ("Diphenhydramine", "CN(C)CCOC(c1ccccc1)c1ccccc1", "Drug", "Allergy, travel sickness"),
    ("Cetirizine", "OC(=O)COCCN1CCN(CC1)C(c1ccccc1)c1ccc(Cl)cc1", "Drug", "Allergy (dust, pollen)"),
    ("Loratadine", "CCOC(=O)N1CCC(=C2c3ccc(Cl)cc3CCc3cccnc23)CC1", "Drug", "Non-drowsy allergy"),
    ("Omeprazole", "COc1ccc2[nH]c(nc2c1)S(=O)Cc1ncc(C)c(OC)c1C", "Drug", "Acidity / reflux"),
    ("Metformin", "CN(C)C(=N)N=C(N)N", "Drug", "Type-2 diabetes"),
    ("Amoxicillin", "CC1(C)SC2C(NC(=O)C(N)c3ccc(O)cc3)C(=O)N2C1C(=O)O", "Drug", "Antibiotic"),
    ("Salbutamol", "CC(C)(C)NCC(O)c1ccc(O)c(CO)c1", "Drug", "Asthma inhaler"),
    ("Ondansetron", "Cc1nccn1CC1CCc2c(C1=O)c1ccccc1n2C", "Drug", "Nausea / vomiting"),
    ("Propranolol", "CC(C)NCC(O)COc1cccc2ccccc12", "Drug", "Blood pressure"),
]


@st.cache_data
def load_df():
    rows = []
    for kind, items in (("Molecule", MOLECULES), ("Drug", DRUGS)):
        for name, smi, grp, role in items:
            m = Chem.MolFromSmiles(smi)
            mw, lp = Descriptors.MolWt(m), Crippen.MolLogP(m)
            hbd, hba = Lipinski.NumHDonors(m), Lipinski.NumHAcceptors(m)
            viol = int(mw > 500) + int(lp > 5) + int(hbd > 5) + int(hba > 10)
            rows.append(dict(
                Name=name, Type=kind, Group=grp, Role=role, SMILES=smi,
                Formula=rdMolDescriptors.CalcMolFormula(m),
                MW=round(mw, 2), LogP=round(lp, 2),
                TPSA=round(rdMolDescriptors.CalcTPSA(m), 1), HBD=hbd, HBA=hba,
                RotB=rdMolDescriptors.CalcNumRotatableBonds(m),
                Rings=rdMolDescriptors.CalcNumRings(m),
                AromRings=rdMolDescriptors.CalcNumAromaticRings(m),
                HeavyAtoms=m.GetNumHeavyAtoms(),
                Lipinski_Violations=viol, Drug_like="Yes" if viol <= 1 else "No"))
    return pd.DataFrame(rows)


COL = {"O": "#ff4d4d", "N": "#4d8dff", "S": "#ffd23f", "Cl": "#3ddc84", "F": "#7fffd4"}


def mol_svg(smiles, w=420, h=320):
    """Pure-Python 2D drawing (no rdkit.Chem.Draw, so no system libraries needed)."""
    m = Chem.MolFromSmiles(smiles)
    rdDepictor.Compute2DCoords(m)
    c = m.GetConformer()
    pts = [(c.GetAtomPosition(i).x, -c.GetAtomPosition(i).y) for i in range(m.GetNumAtoms())]
    minx, maxx = min(p[0] for p in pts), max(p[0] for p in pts)
    miny, maxy = min(p[1] for p in pts), max(p[1] for p in pts)
    span = max(maxx - minx, maxy - miny, 1e-6)
    k = min(70, (min(w, h) - 90) / span)
    ox, oy = (w - k * (maxx - minx)) / 2, (h - k * (maxy - miny)) / 2
    P = [((x - minx) * k + ox, (y - miny) * k + oy) for x, y in pts]
    lab = {}
    for a in m.GetAtoms():
        if a.GetSymbol() != "C" or a.GetDegree() == 0:
            n = a.GetTotalNumHs()
            lab[a.GetIdx()] = a.GetSymbol() + ("H" if n == 1 else f"H{n}" if n > 1 else "")
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%">',
           f'<rect width="{w}" height="{h}" rx="12" fill="#16161a"/>']
    for b in m.GetBonds():
        i, j = b.GetBeginAtomIdx(), b.GetEndAtomIdx()
        (x1, y1), (x2, y2) = P[i], P[j]
        dx, dy = x2 - x1, y2 - y1
        L = (dx * dx + dy * dy) ** .5 or 1
        ux, uy, nx, ny = dx / L, dy / L, -dy / L, dx / L
        if i in lab: x1, y1 = x1 + ux * 13, y1 + uy * 13
        if j in lab: x2, y2 = x2 - ux * 13, y2 - uy * 13
        order = b.GetBondTypeAsDouble()
        offs = {1.0: [0], 2.0: [-3.5, 3.5], 3.0: [-5, 0, 5], 1.5: [0, 5]}.get(order, [0])
        for n, o in enumerate(offs):
            dash = ' stroke-dasharray="5 4"' if order == 1.5 and n == 1 else ""
            out.append(f'<line x1="{x1+nx*o:.1f}" y1="{y1+ny*o:.1f}" x2="{x2+nx*o:.1f}" y2="{y2+ny*o:.1f}" '
                       f'stroke="#e6e6e6" stroke-width="2.2" stroke-linecap="round"{dash}/>')
    for i, t in lab.items():
        x, y = P[i]
        col = COL.get(m.GetAtomWithIdx(i).GetSymbol(), "#ffb400")
        out.append(f'<text x="{x:.1f}" y="{y+6:.1f}" text-anchor="middle" font-size="18" '
                   f'font-weight="700" font-family="Arial" fill="{col}">{t}</text>')
    out.append("</svg>")
    return "".join(out)


def show_2d(smiles):
    st.markdown(mol_svg(smiles), unsafe_allow_html=True)


def viewer3d(smiles, style="stick", height=420):
    m = Chem.AddHs(Chem.MolFromSmiles(smiles))
    ok = AllChem.EmbedMolecule(m, randomSeed=7)
    if ok != 0:
        ok = AllChem.EmbedMolecule(m, useRandomCoords=True, randomSeed=7)
    if ok != 0:
        st.warning("3D coordinates could not be generated for this molecule.")
        return
    try:
        AllChem.MMFFOptimizeMolecule(m)
    except Exception:
        pass
    styles = {"stick": "{stick:{}}", "ball & stick": "{stick:{radius:0.15},sphere:{scale:0.3}}",
              "sphere": "{sphere:{}}", "line": "{line:{}}"}
    html = f"""<div id="v" style="width:100%;height:{height}px;position:relative"></div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/3Dmol/2.0.4/3Dmol-min.js"></script>
<script>let v=$3Dmol.createViewer("v",{{backgroundColor:"#0b0b0d"}});
v.addModel({json.dumps(Chem.MolToMolBlock(m))},"mol");v.setStyle({{}},{styles[style]});
v.zoomTo();v.spin(true);v.render();</script>"""
    components.html(html, height=height)


CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@600;800&family=Inter:wght@400;600&display=swap');
html, body, [class*="css"] {font-family:'Inter',sans-serif;}
h1,h2,h3 {font-family:'Orbitron',sans-serif; letter-spacing:.04em;}
.stApp {background: repeating-linear-gradient(45deg,#0b0b0d 0 6px,#101013 6px 12px);}
.flag {height:18px;border-radius:4px;margin-bottom:14px;
 background:repeating-conic-gradient(#f2f2f2 0 25%,#0b0b0d 0 50%) 0 0/18px 18px;}
.hero {border-left:8px solid #ff1e2d;background:linear-gradient(90deg,#1c1c22,#0b0b0d);
 padding:26px 30px;border-radius:12px;margin-bottom:18px;}
.hero h1 {margin:0;color:#ff1e2d;} .hero p {color:#ffb400;margin:6px 0 0;font-size:1.05rem;}
.card {background:#16161a;border:1px solid #2a2a31;border-top:3px solid #ffb400;
 padding:16px 18px;border-radius:10px;margin-bottom:12px;}
.card b {color:#ffb400;}
.foot {text-align:center;color:#8a8f98;padding:18px 0 4px;border-top:1px solid #2a2a31;margin-top:30px;}
.foot b {color:#ff1e2d;}
[data-testid="stMetricValue"] {color:#ffb400;font-family:'Orbitron',sans-serif;}
</style>
"""


def setup(title, icon="🏎️"):
    st.set_page_config(page_title=f"{title} · Chem Garage", page_icon=icon, layout="wide")
    st.markdown(CSS, unsafe_allow_html=True)
    st.markdown('<div class="flag"></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="hero"><h1>{icon} {title}</h1>'
                f'<p>Chem Garage · Cheminformatics Virtual Laboratory</p></div>',
                unsafe_allow_html=True)


def footer():
    st.markdown(f'<div class="foot">Developed by <b>{AUTHOR}</b><br>{DEPT}</div>',
                unsafe_allow_html=True)
