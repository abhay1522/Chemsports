import plotly.express as px
import streamlit as st
from utils import setup, load_df, NUM, footer

setup("Structure–Property Analysis", "📈")
df = load_df()
c1, c2, c3 = st.columns(3)
x = c1.selectbox("X axis", NUM, index=0)
y = c2.selectbox("Y axis", NUM, index=1)
color = c3.selectbox("Colour by", ["Group", "Type", "Drug_like"])
fig = px.scatter(df, x=x, y=y, color=color, size="HeavyAtoms", hover_name="Name",
                 template="plotly_dark", color_discrete_sequence=px.colors.qualitative.Bold)
st.plotly_chart(fig, use_container_width=True)
corr = df[x].corr(df[y])
st.markdown(f'<div class="card">Correlation of <b>{x}</b> and <b>{y}</b>: <b>{corr:.2f}</b> — '
            f'{"strong" if abs(corr) > .7 else "moderate" if abs(corr) > .4 else "weak"} relationship.</div>',
            unsafe_allow_html=True)
a, b = st.columns(2)
a.plotly_chart(px.imshow(df[NUM].corr().round(2), text_auto=True, template="plotly_dark",
                         color_continuous_scale="RdYlBu_r", title="Correlation heatmap"), use_container_width=True)
b.plotly_chart(px.box(df, x="Group", y=y, color="Group", template="plotly_dark",
                      title=f"{y} by group"), use_container_width=True)
footer()
