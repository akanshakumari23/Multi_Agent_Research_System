import streamlit as st
import time
from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ResearchMind · AI Research Agent",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Inter:wght@300;400;500&family=JetBrains+Mono:wght@300;400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; }

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    color: #c8d0e8;
}

.stApp {
    background: #080810;
    min-height: 100vh;
    position: relative;
    overflow-x: hidden;
}

/* Ambient background orbs */
.stApp::before {
    content: '';
    position: fixed;
    top: -20%;
    left: -10%;
    width: 60vw;
    height: 60vw;
    background: radial-gradient(circle, rgba(108,99,255,0.12) 0%, transparent 65%);
    border-radius: 50%;
    pointer-events: none;
    z-index: 0;
    animation: orbFloat 18s ease-in-out infinite;
}
.stApp::after {
    content: '';
    position: fixed;
    bottom: -15%;
    right: -5%;
    width: 50vw;
    height: 50vw;
    background: radial-gradient(circle, rgba(255,82,140,0.08) 0%, transparent 65%);
    border-radius: 50%;
    pointer-events: none;
    z-index: 0;
    animation: orbFloat2 22s ease-in-out infinite;
}
@keyframes orbFloat {
    0%, 100% { transform: translate(0, 0) scale(1); }
    33% { transform: translate(3%, 5%) scale(1.05); }
    66% { transform: translate(-2%, 3%) scale(0.97); }
}
@keyframes orbFloat2 {
    0%, 100% { transform: translate(0, 0) scale(1); }
    50% { transform: translate(-4%, -3%) scale(1.08); }
}

/* Grid overlay */
.grid-overlay {
    position: fixed;
    inset: 0;
    background-image:
        linear-gradient(rgba(108,99,255,0.04) 1px, transparent 1px),
        linear-gradient(90deg, rgba(108,99,255,0.04) 1px, transparent 1px);
    background-size: 60px 60px;
    pointer-events: none;
    z-index: 0;
}

/* Hide streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding: 0 2.5rem 1rem;
    max-width: 1280px;
    position: relative;
    z-index: 1;
}

/* Hero */
.hero-wrap {
    min-height: 38vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 5rem 1rem 3rem;
    position: relative;
}

.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    background: rgba(108,99,255,0.12);
    border: 1px solid rgba(108,99,255,0.3);
    border-radius: 100px;
    padding: 0.35rem 1rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    font-weight: 500;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #6C63FF;
    margin-bottom: 2rem;
}
.hero-badge::before {
    content: '';
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #6C63FF;
    box-shadow: 0 0 8px #6C63FF;
    animation: pulse 2s ease-in-out infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.5; transform: scale(0.7); }
}

.hero-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: clamp(3.2rem, 7vw, 6rem);
    font-weight: 700;
    line-height: 0.95;
    letter-spacing: -0.04em;
    color: #eef0fa;
    margin-bottom: 1.4rem;
}
.hero-title .accent { color: #6C63FF; }
.hero-title .dim { opacity: 0.35; }

.hero-sub {
    font-size: 1rem;
    font-weight: 300;
    color: #6a7290;
    max-width: 500px;
    line-height: 1.75;
    margin: 0 auto;
}

/* Decorative rule */
.rule {
    width: 100%;
    height: 1px;
    background: linear-gradient(90deg, transparent 0%, rgba(108,99,255,0.25) 30%, rgba(108,99,255,0.25) 70%, transparent 100%);
    margin: 2.5rem 0;
    position: relative;
}
.rule::before {
    content: '✦';
    position: absolute;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
    color: #6C63FF;
    font-size: 0.6rem;
    background: #080810;
    padding: 0 0.5rem;
    opacity: 0.6;
}

/* Input zone */
.input-zone {
    background: rgba(14,14,28,0.8);
    border: 1px solid rgba(108,99,255,0.2);
    border-radius: 20px;
    padding: 2.2rem 2.5rem 2rem;
    backdrop-filter: blur(20px);
    box-shadow:
        0 0 0 1px rgba(108,99,255,0.05) inset,
        0 40px 80px rgba(0,0,0,0.5),
        0 0 60px rgba(108,99,255,0.06);
    transition: border-color 0.3s, box-shadow 0.3s;
    margin-bottom: 1rem;
}
.input-zone:hover {
    border-color: rgba(108,99,255,0.35);
    box-shadow:
        0 0 0 1px rgba(108,99,255,0.08) inset,
        0 40px 80px rgba(0,0,0,0.5),
        0 0 80px rgba(108,99,255,0.1);
}

/* Text input overrides */
.stTextInput > div > div > input {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(108,99,255,0.18) !important;
    border-radius: 12px !important;
    color: #eef0fa !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 1.05rem !important;
    font-weight: 300 !important;
    padding: 0.85rem 1.2rem !important;
    transition: all 0.25s !important;
    caret-color: #6C63FF !important;
}
.stTextInput > div > div > input::placeholder {
    color: rgba(106,114,144,0.6) !important;
}
.stTextInput > div > div > input:focus {
    border-color: #6C63FF !important;
    box-shadow: 0 0 0 3px rgba(108,99,255,0.15), 0 0 20px rgba(108,99,255,0.1) !important;
    background: rgba(108,99,255,0.06) !important;
}
.stTextInput > label {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.68rem !important;
    font-weight: 400 !important;
    letter-spacing: 0.18em !important;
    text-transform: uppercase !important;
    color: #6C63FF !important;
    margin-bottom: 0.6rem !important;
}

/* CTA button */
.stButton > button {
    background: linear-gradient(135deg, #6C63FF 0%, #8B5CF6 50%, #A855F7 100%) !important;
    color: #fff !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.02em !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.8rem 2.2rem !important;
    width: 100% !important;
    cursor: pointer !important;
    transition: all 0.2s !important;
    box-shadow: 0 6px 30px rgba(108,99,255,0.4), 0 2px 8px rgba(0,0,0,0.3) !important;
    position: relative !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 12px 40px rgba(108,99,255,0.5), 0 4px 12px rgba(0,0,0,0.3) !important;
}
.stButton > button:active {
    transform: translateY(0) !important;
    box-shadow: 0 4px 16px rgba(108,99,255,0.35) !important;
}

/* Chip pills */
.chips-row {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    flex-wrap: wrap;
    margin-top: 1rem;
}
.chip-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.15em;
    color: #3a3f5c;
    text-transform: uppercase;
}
.chip {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 8px;
    padding: 0.28rem 0.8rem;
    font-size: 0.73rem;
    color: #5a6280;
    font-family: 'Inter', sans-serif;
    cursor: default;
}

/* Section title */
.section-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 0.78rem;
    font-weight: 500;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #3a3f5c;
    margin-bottom: 1.2rem;
    display: flex;
    align-items: center;
    gap: 0.7rem;
}
.section-title::after {
    content: '';
    flex: 1;
    height: 1px;
    background: rgba(255,255,255,0.05);
}

/* Pipeline */
.pipeline-wrap { display: flex; flex-direction: column; gap: 0; }

.pipeline-step {
    display: flex;
    gap: 1.2rem;
    align-items: flex-start;
    position: relative;
}

.pipeline-step:not(:last-child) .step-connector {
    position: absolute;
    left: 17px;
    top: 50px;
    width: 2px;
    height: calc(100% - 10px);
    background: rgba(255,255,255,0.05);
    z-index: 0;
}
.pipeline-step.done:not(:last-child) .step-connector {
    background: linear-gradient(to bottom, rgba(108,99,255,0.6), rgba(108,99,255,0.1));
}

.step-ring {
    flex-shrink: 0;
    width: 36px;
    height: 36px;
    border-radius: 50%;
    border: 2px solid rgba(255,255,255,0.07);
    display: flex;
    align-items: center;
    justify-content: center;
    background: #0e0e1c;
    position: relative;
    z-index: 1;
    transition: all 0.4s;
    margin-top: 1.5rem;
}
.step-ring.active {
    border-color: #6C63FF;
    box-shadow: 0 0 0 4px rgba(108,99,255,0.15), 0 0 20px rgba(108,99,255,0.3);
    animation: ringPulse 1.8s ease-in-out infinite;
}
@keyframes ringPulse {
    0%, 100% { box-shadow: 0 0 0 4px rgba(108,99,255,0.15), 0 0 20px rgba(108,99,255,0.3); }
    50% { box-shadow: 0 0 0 8px rgba(108,99,255,0.08), 0 0 35px rgba(108,99,255,0.2); }
}
.step-ring.done {
    border-color: #FFD166;
    background: rgba(255,209,102,0.08);
    box-shadow: 0 0 0 3px rgba(255,209,102,0.1), 0 0 15px rgba(255,209,102,0.2);
}
.step-ring-icon { font-size: 0.85rem; line-height: 1; }

.step-body {
    flex: 1;
    background: rgba(14,14,28,0.6);
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 14px;
    padding: 1.1rem 1.4rem;
    margin-bottom: 0.8rem;
    transition: all 0.3s;
    position: relative;
    overflow: hidden;
}
.step-body::before {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 2px;
    background: rgba(255,255,255,0.04);
    transition: all 0.3s;
}
.step-body.active::before { background: linear-gradient(to bottom, #6C63FF, transparent); }
.step-body.done::before { background: linear-gradient(to bottom, #FFD166, transparent); }
.step-body.active {
    border-color: rgba(108,99,255,0.25);
    background: rgba(108,99,255,0.06);
}
.step-body.done { border-color: rgba(255,209,102,0.12); }

.step-meta {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 0.2rem;
}
.step-name {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 0.88rem;
    font-weight: 600;
    color: #c8d0e8;
}
.step-status-pill {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.6rem;
    font-weight: 500;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    padding: 0.2rem 0.6rem;
    border-radius: 100px;
}
.pill-waiting { color: #3a3f5c; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.05); }
.pill-running { color: #6C63FF; background: rgba(108,99,255,0.12); border: 1px solid rgba(108,99,255,0.25); animation: pillPulse 1.5s ease-in-out infinite; }
.pill-done    { color: #FFD166; background: rgba(255,209,102,0.1); border: 1px solid rgba(255,209,102,0.2); }
@keyframes pillPulse { 0%,100%{opacity:1} 50%{opacity:0.6} }

.step-desc {
    font-size: 0.77rem;
    color: #3a3f5c;
    font-weight: 300;
}
.step-body.active .step-desc { color: #5a6280; }
.step-body.done .step-desc { color: #4a5070; }

/* Spinner */
.stSpinner > div { color: #6C63FF !important; }

/* Results section */
.results-header {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.8rem;
    font-weight: 700;
    color: #eef0fa;
    letter-spacing: -0.02em;
    margin: 3rem 0 0.3rem;
}
.results-sub {
    font-size: 0.85rem;
    color: #3a3f5c;
    margin-bottom: 1.8rem;
}

/* Expanders */
.stExpander {
    background: rgba(14,14,28,0.6) !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
    border-radius: 12px !important;
    overflow: hidden;
    margin-bottom: 0.8rem !important;
}
details summary {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.72rem !important;
    color: #4a5070 !important;
    letter-spacing: 0.1em !important;
    padding: 0.8rem 1rem !important;
}

/* Report card */
.report-card {
    background: rgba(14,14,28,0.85);
    border: 1px solid rgba(108,99,255,0.2);
    border-radius: 18px;
    padding: 2.2rem 2.5rem;
    margin-bottom: 1.2rem;
    box-shadow: 0 0 60px rgba(108,99,255,0.06);
    position: relative;
    overflow: hidden;
}
.report-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, #6C63FF, #A855F7, transparent);
}
.card-eyebrow {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    font-weight: 400;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #6C63FF;
    margin-bottom: 1.4rem;
    padding-bottom: 0.8rem;
    border-bottom: 1px solid rgba(108,99,255,0.12);
}

/* Critic card */
.critic-card {
    background: rgba(14,14,28,0.85);
    border: 1px solid rgba(255,209,102,0.15);
    border-radius: 18px;
    padding: 2.2rem 2.5rem;
    box-shadow: 0 0 60px rgba(255,209,102,0.04);
    position: relative;
    overflow: hidden;
}
.critic-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, #FFD166, #FF9E3C, transparent);
}
.critic-card .card-eyebrow { color: #FFD166; border-bottom-color: rgba(255,209,102,0.12); }

/* Download button */
.stDownloadButton > button {
    background: rgba(108,99,255,0.08) !important;
    color: #9896d8 !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    border: 1px solid rgba(108,99,255,0.2) !important;
    border-radius: 10px !important;
    padding: 0.55rem 1.4rem !important;
    transition: all 0.2s !important;
    width: auto !important;
}
.stDownloadButton > button:hover {
    background: rgba(108,99,255,0.15) !important;
    border-color: rgba(108,99,255,0.4) !important;
    color: #b8b6e8 !important;
    transform: translateY(-1px) !important;
}

/* Footer */
.footer {
    text-align: center;
    padding: 4px 0;
    margin-top: 0;

    font-family: 'JetBrains Mono', monospace;
    font-size: 0.5rem;
    letter-spacing: 0.12em;

    color: #ffffff;
    text-transform: uppercase;
}

[data-testid="column"] { padding: 0 0.5rem; }
</style>
""", unsafe_allow_html=True)


# ── Grid overlay ─────────────────────────────────────────────────────────────
st.markdown('<div class="grid-overlay"></div>', unsafe_allow_html=True)


# ── Helper: pipeline step ────────────────────────────────────────────────────
def step_card(icon, title, desc, state):
    pill_map = {
        "waiting": ("Idle",    "pill-waiting"),
        "running": ("Running", "pill-running"),
        "done":    ("Done",    "pill-done"),
    }
    ring_cls = {"running": "active", "done": "done"}.get(state, "")
    body_cls = {"running": "active", "done": "done"}.get(state, "")
    pill_txt, pill_cls = pill_map.get(state, ("Idle", "pill-waiting"))

    st.markdown(f"""
    <div class="pipeline-step {state}">
        <div class="step-connector"></div>
        <div class="step-ring {ring_cls}">
            <span class="step-ring-icon">{icon}</span>
        </div>
        <div class="step-body {body_cls}">
            <div class="step-meta">
                <span class="step-name">{title}</span>
                <span class="step-status-pill {pill_cls}">{pill_txt}</span>
            </div>
            <div class="step-desc">{desc}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ── Session state ─────────────────────────────────────────────────────────────
for key in ("results", "running", "done"):
    if key not in st.session_state:
        st.session_state[key] = {} if key == "results" else False


# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-wrap">
    <div class="hero-badge">Multi-Agent AI · Research Pipeline</div>
    <h1 class="hero-title">
        Research<span class="accent">Mind</span><br>
        <span class="dim">AI at work.</span>
    </h1>
    <p class="hero-sub">
        Four specialized agents — search, extract, write, and critique —
        collaborate to produce publication-ready research on any topic.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="rule"></div>', unsafe_allow_html=True)


# ── Main layout ───────────────────────────────────────────────────────────────
col_left, col_gap, col_right = st.columns([6, 0.4, 4])

with col_left:
    st.markdown('<div class="input-zone">', unsafe_allow_html=True)
    topic = st.text_input(
        "Research Query",
        placeholder="e.g.  Breakthroughs in quantum error correction 2025",
        key="topic_input",
        label_visibility="visible",
    )
    run_btn = st.button("⚡  Launch Research Pipeline", use_container_width=True)

    st.markdown("""
    <div class="chips-row">
        <span class="chip-label">Try →</span>
        <span class="chip">LLM agents 2025</span>
        <span class="chip">CRISPR gene editing</span>
        <span class="chip">Fusion energy</span>
        <span class="chip">AI hardware trends</span>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


with col_right:
    st.markdown('<div class="section-title" style="margin-top:1.5rem;">Agent Pipeline</div>', unsafe_allow_html=True)

    r = st.session_state.results

    def step_state(step):
        steps = ["search", "reader", "writer", "critic"]
        if step in r:
            return "done"
        if st.session_state.running:
            for k in steps:
                if k not in r:
                    return "running" if k == step else "waiting"
        return "waiting"

    st.markdown('<div class="pipeline-wrap">', unsafe_allow_html=True)
    step_card("🔍", "Search Agent",  "Scans recent web sources for your topic", step_state("search"))
    step_card("📄", "Reader Agent",  "Extracts deep content from top URLs",      step_state("reader"))
    step_card("✍️", "Writer Chain",  "Drafts a structured research report",       step_state("writer"))
    step_card("🧠", "Critic Chain",  "Scores and refines the final output",       step_state("critic"))
    st.markdown('</div>', unsafe_allow_html=True)


# ── Run logic ─────────────────────────────────────────────────────────────────
if run_btn:
    if not topic.strip():
        st.warning("Please enter a research query first.")
    else:
        st.session_state.results = {}
        st.session_state.running = True
        st.session_state.done = False
        st.rerun()

if st.session_state.running and not st.session_state.done:
    results = {}
    topic_val = st.session_state.topic_input

    with st.spinner("Search Agent is scanning the web…"):
        search_agent = build_search_agent()
        sr = search_agent.invoke({
            "messages": [("user", f"Find recent, reliable and detailed information about: {topic_val}")]
        })
        results["search"] = sr["messages"][-1].content
        st.session_state.results = dict(results)

    with st.spinner("Reader Agent is extracting deep content…"):
        reader_agent = build_reader_agent()
        rr = reader_agent.invoke({
            "messages": [("user",
                f"Based on the following search results about '{topic_val}', "
                f"pick the most relevant URL and scrape it for deeper content.\n\n"
                f"Search Results:\n{results['search'][:800]}"
            )]
        })
        results["reader"] = rr["messages"][-1].content
        st.session_state.results = dict(results)

    with st.spinner("Writer is composing the report…"):
        research_combined = (
            f"SEARCH RESULTS:\n{results['search']}\n\n"
            f"DETAILED SCRAPED CONTENT:\n{results['reader']}"
        )
        results["writer"] = writer_chain.invoke({
            "topic": topic_val,
            "research": research_combined
        })
        st.session_state.results = dict(results)

    with st.spinner("Critic is reviewing and scoring…"):
        results["critic"] = critic_chain.invoke({
            "report": results["writer"]
        })
        st.session_state.results = dict(results)

    st.session_state.running = False
    st.session_state.done = True
    st.rerun()


# ── Results display ───────────────────────────────────────────────────────────
r = st.session_state.results

if r:
    st.markdown('<div class="rule"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="results-header">Research Output</div>
    <div class="results-sub">Pipeline complete — all four agents have finished.</div>
    """, unsafe_allow_html=True)

    if "search" in r:
        with st.expander("🔍  Search Agent — raw output", expanded=False):
            st.text(r["search"])

    if "reader" in r:
        with st.expander("📄  Reader Agent — scraped content", expanded=False):
            st.text(r["reader"])

    if "writer" in r:
        st.markdown('<div class="report-card"><div class="card-eyebrow">📝  Final Research Report</div>', unsafe_allow_html=True)
        st.markdown(r["writer"])
        st.markdown('</div>', unsafe_allow_html=True)
        st.download_button(
            label="⬇  Download as Markdown",
            data=r["writer"],
            file_name=f"research_{int(time.time())}.md",
            mime="text/markdown",
        )

    if "critic" in r:
        st.markdown('<div class="critic-card"><div class="card-eyebrow">🧠  Critic Review & Score</div>', unsafe_allow_html=True)
        st.markdown(r["critic"])
        st.markdown('</div>', unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    ResearchMind · Multi-Agent LangChain Pipeline · Built <span class="heart-glow">❤️</span> by <span>Akansha Kumari</span> with Streamlit
</div>
""", unsafe_allow_html=True)