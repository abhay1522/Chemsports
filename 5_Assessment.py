import random
import streamlit as st
from utils import setup, load_df, footer

setup("Assessment", "📝")
df = load_df()


def make_quiz():
    qs = []
    for i in range(8):
        t = i % 4
        if t in (0, 1):
            col = "MW" if t == 0 else "LogP"
            while True:
                a, b = df.sample(2).iloc
                if a[col] != b[col]:
                    break
            ans = a.Name if a[col] > b[col] else b.Name
            qs.append((f"Which has the higher {col}: {a.Name} or {b.Name}?", [a.Name, b.Name], ans))
        elif t == 2:
            r = df.sample(1).iloc[0]
            qs.append((f"Does {r.Name} pass Lipinski's Rule of Five (≤1 violation)?", ["Yes", "No"], r.Drug_like))
        else:
            rows = df.drop_duplicates("Formula").sample(4)
            r = rows.iloc[0]
            opts = rows.Formula.tolist(); random.shuffle(opts)
            qs.append((f"What is the molecular formula of {r.Name}?", opts, r.Formula))
    return qs


if "quiz" not in st.session_state:
    st.session_state.quiz, st.session_state.qid = make_quiz(), 0
if st.button("🔄 New quiz"):
    st.session_state.quiz = make_quiz(); st.session_state.qid += 1
    st.rerun()
score, answers = 0, []
for i, (q, opts, ans) in enumerate(st.session_state.quiz):
    answers.append(st.radio(f"Q{i+1}. {q}", opts, index=None, key=f"q{st.session_state.qid}_{i}"))
if st.button("Submit"):
    for (q, opts, ans), a in zip(st.session_state.quiz, answers):
        score += a == ans
        (st.success if a == ans else st.error)(f"{q} → {ans}")
    st.metric("Score", f"{score} / {len(answers)}")
footer()
