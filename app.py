"""
AI-Powered E-Commerce Business Analyzer
Main Streamlit Application
─────────────────────────────────────────
Run with:  streamlit run app.py
"""

import time
import streamlit as st
import plotly.graph_objects as go
from problem_detector import ProblemDetector
from strategy_engine import StrategyEngine
from explainer import Explainer, generate_explanation
from pdf_generator import PDFGenerator, generate_pdf

# ════════════════════════════════════════════════════════════════════
#  PAGE CONFIG  (must be first Streamlit call)
# ════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title = "AI Business Analyzer",
    page_icon  = "🤖",
    layout     = "wide",
    initial_sidebar_state = "collapsed",
)

# ════════════════════════════════════════════════════════════════════
#  GLOBAL CSS
# ════════════════════════════════════════════════════════════════════
def inject_css():
    theme = st.session_state.get("theme", "gradient")
    bg = "linear-gradient(135deg, #1f170f 0%, #6a5c4f 35%, #b9ad9f 65%, #767779 85%, #30281d 100%)" if theme == "gradient" else "#1f170f"
    st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* ── Reset & Base ── */
* {{ font-family: 'Inter', sans-serif !important; box-sizing: border-box; }}

.stApp {{
    background: {bg} !important;
    min-height: 100vh;
}}

/* Hide default chrome */
#MainMenu, footer, header {{ visibility: hidden; }}
.block-container {{ padding-top: 2rem !important; max-width: 900px !important; }}

/* ── Progress Bar ── */
.prog-wrap {{
    background: rgba(255,255,255,0.07);
    border-radius: 50px; height: 6px;
    margin: 0.5rem 0 1rem;
}}
.prog-bar {{
    background: linear-gradient(90deg,#6366f1,#8b5cf6,#a78bfa);
    height: 6px; border-radius: 50px;
    transition: width .5s ease;
}}
.step-label {{
    text-align: center;
    color: rgba(255,255,255,0.45);
    font-size: 0.82rem;
    margin-bottom: 0.4rem;
    letter-spacing: .04em;
}}
.step-dots {{ display:flex; justify-content:center; gap:10px; margin-bottom:1.8rem; }}
.dot {{ width:10px; height:10px; border-radius:50%; background:rgba(255,255,255,.18); }}
.dot.active {{ background:#6366f1; box-shadow:0 0 8px #6366f1; }}
.dot.done   {{ background:#10b981; }}

/* ── Cards ── */
.glass {{
    background: rgba(239,234,223,0.15);
    backdrop-filter: blur(18px);
    border: 1px solid rgba(220,210,191,0.4);
    border-radius: 20px;
    padding: 2rem;
    margin-bottom: 1.4rem;
}}
.card-title {{
    font-size: 1.25rem; font-weight: 700;
    color: white; margin-bottom: .4rem;
    display: flex; align-items: center; gap: .5rem;
}}
.card-sub {{
    color: rgba(255,255,255,.5);
    font-size: .88rem; margin-bottom: 1.2rem;
}}

/* ── Hero ── */
.hero-title {{
    font-size: 2.9rem; font-weight: 800; text-align: center;
    background: linear-gradient(135deg,#38bdf8,#a78bfa,#f472b6);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    margin-bottom: .3rem;
}}
.hero-sub {{
    text-align: center; color: rgba(225,225,255,.75);
    font-size: 1.05rem; margin-bottom: 2.5rem; line-height: 1.6;
}}

/* ── Inputs ── */
.stNumberInput > div > div > input,
.stTextInput > div > div > input {{
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(255,255,255,0.14) !important;
    border-radius: 12px !important; color: white !important;
}}
.stSelectbox > div > div {{
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(255,255,255,0.14) !important;
    border-radius: 12px !important; color: white !important;
}}
label, .stNumberInput label, .stTextInput label, .stSelectbox label {{
    color: rgba(255,255,255,.75) !important;
    font-size: .88rem !important; font-weight: 500 !important;
}}

/* ── Buttons ── */
.stButton > button {{
    background: linear-gradient(135deg,#f97316,#ec4899) !important;
    color: white !important; border: none !important;
    border-radius: 14px !important;
    padding: .8rem 1.9rem !important;
    font-size: 1rem !important; font-weight: 700 !important;
    width: 100% !important; transition: all .25s ease !important;
}}
.stButton > button:hover {{
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(236,72,153,.45) !important;
}}

/* ── Banners ── */
.banner-ok  {{ background:rgba(16,185,129,.12); border:1px solid rgba(16,185,129,.35);
               border-radius:10px; padding:.75rem 1.2rem; color:#10b981; margin-bottom:.8rem; }}
.banner-warn{{ background:rgba(245,158,11,.12); border:1px solid rgba(245,158,11,.35);
               border-radius:10px; padding:.75rem 1.2rem; color:#f59e0b; margin-bottom:.8rem; }}
.banner-err {{ background:rgba(239,68,68,.12); border:1px solid rgba(239,68,68,.35);
               border-radius:10px; padding:.75rem 1.2rem; color:#ef4444; margin-bottom:.8rem; }}

/* ── Review metric tiles ── */
.metric-tile {{
    background:rgba(255,255,255,0.05);
    border:1px solid rgba(255,255,255,0.1);
    border-radius:14px; padding:1rem;
    text-align:center; margin-bottom:.8rem;
}}
.metric-tile .val {{
    font-size:1.45rem; font-weight:700; color:#a78bfa;
}}
.metric-tile .lbl {{
    font-size:.78rem; color:rgba(255,255,255,.45); margin-top:.2rem;
}}

/* ── Results: section header ── */
.r-section {{
    font-size:1.65rem; font-weight:700; color:white;
    margin:1.6rem 0 .6rem; letter-spacing:-.01em;
}}

/* ── Problem card ── */
.prob-card {{
    border-radius:14px; padding:1.3rem 1.4rem; margin-bottom:.9rem;
    border: 1.5px solid rgba(239,68,68,.4);
    background: rgba(239,68,68,.07);
}}
.prob-card.med {{
    border-color: rgba(245,158,11,.4);
    background: rgba(245,158,11,.07);
}}
.conf-bar-bg {{ background:rgba(255,255,255,.1); border-radius:50px; height:5px; margin-top:.7rem; }}
.conf-bar    {{ height:5px; border-radius:50px;
               background:linear-gradient(90deg,#ef4444,#f59e0b); }}

/* ── Explanation box ── */
.expl-box {{
    background: rgba(99,102,241,.07);
    border-left: 4px solid #6366f1;
    border-radius: 0 14px 14px 0;
    padding: 1.4rem 1.5rem;
    color: rgba(255,255,255,.88);
    font-size: 1rem; line-height: 1.75;
    margin: .8rem 0;
}}

/* ── Health score ── */
.health-wrap {{
    text-align:center;
    background:rgba(255,255,255,.04);
    border:1px solid rgba(255,255,255,.09);
    border-radius:20px; padding:2rem;
    margin-bottom:1.2rem;
}}

/* ── Toggle Button ── */
#toggle {{
    position: fixed !important;
    bottom: 20px !important;
    left: 20px !important;
    z-index: 1000 !important;
    background: rgba(255,255,255,0.1) !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
    color: white !important;
    border-radius: 8px !important;
    padding: 0.5rem 1rem !important;
    font-size: 0.9rem !important;
    cursor: pointer !important;
}}
</style>
""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════
#  SESSION STATE INIT
# ════════════════════════════════════════════════════════════════════
def init_state():
    defaults = {
        "step":          1,
        "form":          {},
        "results":       None,
        "theme":         "gradient",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


# ════════════════════════════════════════════════════════════════════
#  WIZARD HEADER  (progress bar + step dots)
# ════════════════════════════════════════════════════════════════════
STEP_LABELS = ["Business Info", "Traffic & Sales", "Finance & Stock", "Review & Analyze"]

def wizard_header(step: int, total: int = 4):
    pct = int(step / total * 100)
    label = STEP_LABELS[step - 1]

    dots_html = '<div class="step-dots">'
    for i in range(1, total + 1):
        cls = "done" if i < step else ("active" if i == step else "")
        dots_html += f'<div class="dot {cls}"></div>'
    dots_html += "</div>"

    st.markdown(f"""
<div class="step-label">Step {step} of {total} — {label}</div>
<div class="prog-wrap"><div class="prog-bar" style="width:{pct}%"></div></div>
{dots_html}
""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════
#  STEP 1 — Business Basics
# ════════════════════════════════════════════════════════════════════
def step_1():
    wizard_header(1)
    f = st.session_state.form

    st.markdown("""
<div class="glass">
  <div class="card-title">🏢 Tell us about your business</div>
  <div class="card-sub">Start with the basics — just a few quick details.</div>
</div>""", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("🏷️ Business Name",
                             value=f.get("name", ""),
                             placeholder="e.g. FashionHub Store")
        btype = st.selectbox("📦 Category",
            ["Fashion & Apparel","Electronics","Home & Living",
             "Beauty & Personal Care","Food & Grocery","Sports & Outdoors",
             "Books & Media","Health & Wellness","Other"])
    with col2:
        age = st.selectbox("📅 How long running?",
            ["< 6 months","6 months – 1 year","1–2 years","2–5 years","5+ years"])
        team = st.selectbox("👥 Team Size",
            ["Solo (just me)","2–5 people","6–20 people","20+ people"])

    target = st.number_input("🎯 Monthly Revenue Target (₹/$)",
                              min_value=0, value=int(f.get("target", 100_000)),
                              step=10_000)

    _, mid, _ = st.columns([1, 2, 1])
    with mid:
        if st.button("Continue →", key="n1"):
            if not name.strip():
                st.markdown('<div class="banner-err">⚠️ Please enter a business name.</div>',
                            unsafe_allow_html=True)
            else:
                st.session_state.form.update(
                    name=name, btype=btype, age=age, team=team, target=target)
                st.session_state.step = 2
                st.rerun()


# ════════════════════════════════════════════════════════════════════
#  STEP 2 — Traffic & Conversion
# ════════════════════════════════════════════════════════════════════
def step_2():
    wizard_header(2)
    f = st.session_state.form

    st.markdown("""
<div class="glass">
  <div class="card-title">📊 Traffic & Conversion</div>
  <div class="card-sub">These numbers reveal how well you attract and convert visitors.</div>
</div>""", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        sales = st.number_input("💰 Monthly Sales Revenue (₹/$)",
                                min_value=0, value=int(f.get("monthly_sales", 50_000)), step=5_000)
        traffic = st.number_input("🌐 Monthly Website Visitors",
                                  min_value=0, value=int(f.get("website_traffic", 5_000)), step=500)
    with col2:
        conv = st.number_input("🎯 Conversion Rate (%)",
                               min_value=0.0, max_value=100.0,
                               value=float(f.get("conversion_rate", 1.5)),
                               step=0.1, format="%.1f",
                               help="% of visitors who buy. Industry avg: 2–3%")
        aov = st.number_input("🛒 Avg Order Value (₹/$)",
                              min_value=0, value=int(f.get("avg_order_value", 1_500)), step=100)

    # Quick live hint
    if conv < 1.0:
        st.markdown('<div class="banner-err">🔴 Conversion below 1% — well below average (2–3%). High priority!</div>',
                    unsafe_allow_html=True)
    elif conv >= 3.0:
        st.markdown('<div class="banner-ok">✅ Great conversion rate! Above industry average.</div>',
                    unsafe_allow_html=True)
    elif conv < 2.0:
        st.markdown('<div class="banner-warn">🟡 Conversion below 2% — room for improvement.</div>',
                    unsafe_allow_html=True)

    _, mid, _ = st.columns([1, 2, 1])
    with mid:
        c1, c2 = st.columns(2)
        with c1:
            if st.button("← Back", key="b2"):
                st.session_state.step = 1; st.rerun()
        with c2:
            if st.button("Continue →", key="n2"):
                st.session_state.form.update(
                    monthly_sales=sales, website_traffic=traffic,
                    conversion_rate=conv, avg_order_value=aov)
                st.session_state.step = 3; st.rerun()


# ════════════════════════════════════════════════════════════════════
#  STEP 3 — Finance & Inventory
# ════════════════════════════════════════════════════════════════════
def step_3():
    wizard_header(3)
    f = st.session_state.form

    st.markdown("""
<div class="glass">
  <div class="card-title">💼 Finance & Inventory</div>
  <div class="card-sub">Let's understand your costs, marketing efficiency, and stock levels.</div>
</div>""", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        mkt = st.number_input("📣 Monthly Marketing Spend (₹/$)",
                              min_value=0, value=int(f.get("marketing_spend", 15_000)), step=1_000,
                              help="Ads, influencers, promotions, etc.")
        ret = st.number_input("🔄 Customer Retention Rate (%)",
                              min_value=0.0, max_value=100.0,
                              value=float(f.get("retention_rate", 25.0)),
                              step=1.0, format="%.1f",
                              help="% of customers who come back. Good = 40%+")
    with col2:
        inv = st.number_input("📦 Inventory Level (units in stock)",
                              min_value=0, value=int(f.get("inventory_level", 500)), step=50)
        ops = st.number_input("🏗️ Monthly Operating Cost (₹/$)",
                              min_value=0, value=int(f.get("operating_cost", 20_000)), step=1_000,
                              help="Rent, salaries, packaging, shipping, etc.")

    # Live ROI indicator
    sales = f.get("monthly_sales", 0)
    if mkt > 0 and sales > 0:
        roi = sales / mkt
        col = "#10b981" if roi >= 3 else "#f59e0b" if roi >= 1.5 else "#ef4444"
        st.markdown(f"""
<div style="background:rgba(255,255,255,.04);border-radius:10px;
            padding:.8rem 1.2rem;margin-bottom:.8rem;">
  <span style="color:rgba(255,255,255,.5);font-size:.9rem;">Current Marketing ROI: </span>
  <span style="color:{col};font-weight:700;font-size:1.25rem;">{roi:.1f}x</span>
  <span style="color:rgba(255,255,255,.35);font-size:.8rem;"> (Target ≥ 3x)</span>
</div>""", unsafe_allow_html=True)

    _, mid, _ = st.columns([1, 2, 1])
    with mid:
        c1, c2 = st.columns(2)
        with c1:
            if st.button("← Back", key="b3"):
                st.session_state.step = 2; st.rerun()
        with c2:
            if st.button("Continue →", key="n3"):
                st.session_state.form.update(
                    marketing_spend=mkt, retention_rate=ret,
                    inventory_level=inv, operating_cost=ops)
                st.session_state.step = 4; st.rerun()


# ════════════════════════════════════════════════════════════════════
#  STEP 4 — Review & Analyse
# ════════════════════════════════════════════════════════════════════
def step_4():
    wizard_header(4)
    f = st.session_state.form

    st.markdown("""
<div class="glass">
  <div class="card-title">🔍 Review Your Data</div>
  <div class="card-sub">Confirm your numbers below, then hit Analyze to get your AI report.</div>
</div>""", unsafe_allow_html=True)

    tiles = [
        ("💰 Monthly Sales",      f"₹{f.get('monthly_sales',0):,}"),
        ("🌐 Website Traffic",    f"{f.get('website_traffic',0):,} visitors"),
        ("🎯 Conversion Rate",    f"{f.get('conversion_rate',0)}%"),
        ("📣 Marketing Spend",    f"₹{f.get('marketing_spend',0):,}"),
        ("🔄 Retention Rate",     f"{f.get('retention_rate',0)}%"),
        ("📦 Inventory",          f"{f.get('inventory_level',0):,} units"),
        ("🏗️ Operating Cost",     f"₹{f.get('operating_cost',0):,}"),
        ("🎯 Revenue Target",     f"₹{f.get('target',0):,}"),
    ]

    cols = st.columns(4)
    for i, (lbl, val) in enumerate(tiles):
        with cols[i % 4]:
            st.markdown(f"""
<div class="metric-tile">
  <div class="val">{val}</div>
  <div class="lbl">{lbl}</div>
</div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    _, mid, _ = st.columns([1, 2, 1])
    with mid:
        c1, c2 = st.columns(2)
        with c1:
            if st.button("← Back", key="b4"):
                st.session_state.step = 3; st.rerun()
        with c2:
            if st.button("🧠 Analyze My Business", key="analyze"):
                _run_analysis()


# ════════════════════════════════════════════════════════════════════
#  ANALYSIS ENGINE
# ════════════════════════════════════════════════════════════════════
def _run_analysis():
    f = st.session_state.form

    # Map form keys to detector-expected keys
    data = {
        "business_name":   f.get("name", "My Business"),
        "business_type":   f.get("btype", "E-Commerce"),
        "monthly_sales":   f.get("monthly_sales", 0),
        "website_traffic": f.get("website_traffic", 0),
        "conversion_rate": f.get("conversion_rate", 0),
        "avg_order_value": f.get("avg_order_value", 0),
        "marketing_spend": f.get("marketing_spend", 0),
        "retention_rate":  f.get("retention_rate", 0),
        "inventory_level": f.get("inventory_level", 0),
        "operating_cost":  f.get("operating_cost", 0),
        "monthly_target":  f.get("target", 0),
    }

    bar = st.progress(0)

    bar.progress(10, "🔍 Processing your data...")
    time.sleep(0.4)

    bar.progress(30, "🧠 Detecting business problems...")
    detector = ProblemDetector()
    problems, derived = detector.detect(data)
    time.sleep(0.4)

    bar.progress(55, "📋 Building strategy recommendations...")
    engine = StrategyEngine()
    strategies = engine.get_strategies(problems)
    time.sleep(0.4)

    bar.progress(80, "✍️ Generating AI explanation...")
    explanation = generate_explanation(data, problems, strategies)
    time.sleep(0.3)

    bar.progress(100, "✅ Analysis complete!")
    time.sleep(0.3)

    st.session_state.results = {
        "data":        data,
        "problems":    problems,
        "strategies":  strategies,
        "explanation": explanation,
        "metrics":     derived,
    }
    st.rerun()


# ════════════════════════════════════════════════════════════════════
#  HEALTH SCORE
# ════════════════════════════════════════════════════════════════════
def _health_score(problems: list) -> tuple[int, str, str]:
    score = 100 - sum(20 if p["severity"] == "High" else 10 for p in problems)
    score = max(10, score)
    if score >= 70:
        return score, "Healthy", "#10b981"
    elif score >= 40:
        return score, "Needs Attention", "#f59e0b"
    else:
        return score, "Critical — Immediate Action Needed", "#ef4444"


# ════════════════════════════════════════════════════════════════════
#  RESULTS DASHBOARD
# ════════════════════════════════════════════════════════════════════
def show_results():
    res         = st.session_state.results
    data        = res["data"]
    problems    = res["problems"]
    strategies  = res["strategies"]
    explanation = res["explanation"]
    derived     = res["metrics"]
    biz         = data["business_name"]

    # ── Hero ────────────────────────────────────────────────────────
    st.markdown(f"""
<div style="text-align:center;margin-bottom:1.5rem;">
  <h1 style="color:white;font-size:2.4rem;font-weight:800;margin-bottom:.2rem;">
      📊 Business Analysis Report
  </h1>
  <p style="color:rgba(255,255,255,.5);font-size:1rem;">
      {biz} · {data['business_type']} · Generated just now
  </p>
</div>""", unsafe_allow_html=True)

    # ── Health Score ─────────────────────────────────────────────────
    score, label, col = _health_score(problems)
    _, mid, _ = st.columns([1, 2, 1])
    with mid:
        st.markdown(f"""
<div class="health-wrap">
  <div style="font-size:.85rem;color:rgba(255,255,255,.45);margin-bottom:.3rem;">
      Overall Business Health Score
  </div>
  <div style="font-size:4.5rem;font-weight:800;color:{col};line-height:1;">
      {score}<span style="font-size:2rem;">/100</span>
  </div>
  <div style="font-size:1rem;color:{col};font-weight:600;margin-top:.3rem;">{label}</div>
  <div style="font-size:.82rem;color:rgba(255,255,255,.35);margin-top:.4rem;">
      {len(problems)} problem(s) detected
  </div>
</div>""", unsafe_allow_html=True)

    st.markdown('<hr style="border-color:rgba(255,255,255,.08);margin:1.5rem 0;">', unsafe_allow_html=True)

    # ── Problems ─────────────────────────────────────────────────────
    st.markdown('<div class="r-section">❗ Problems Identified</div>', unsafe_allow_html=True)

    if not problems:
        st.markdown('<div class="banner-ok">✅ No major problems! Your metrics look healthy.</div>',
                    unsafe_allow_html=True)
    else:
        for p in problems:
            css = "prob-card" if p["severity"] == "High" else "prob-card med"
            sev_col = "#ef4444" if p["severity"] == "High" else "#f59e0b"
            st.markdown(f"""
<div class="{css}">
  <div style="display:flex;justify-content:space-between;align-items:flex-start;">
    <div>
      <span style="font-size:1.3rem;">{p['icon']}</span>
      <span style="color:white;font-size:1.05rem;font-weight:700;margin-left:.4rem;">
        {p['problem']}
      </span>
      <span style="background:rgba(255,255,255,.1);color:rgba(255,255,255,.65);
                   font-size:.72rem;padding:.15rem .55rem;border-radius:20px;margin-left:.5rem;">
        {p['severity']} Severity
      </span>
    </div>
    <div style="text-align:right;flex-shrink:0;">
      <span style="color:rgba(255,255,255,.4);font-size:.75rem;">Confidence</span>
      <div style="color:white;font-size:1.3rem;font-weight:700;">{p['confidence']}%</div>
    </div>
  </div>
  <div style="margin-top:.7rem;font-size:.88rem;color:rgba(255,255,255,.6);">
    {p.get('detail','')}
  </div>
  <div style="display:flex;gap:1.5rem;margin-top:.7rem;font-size:.82rem;">
    <span style="color:rgba(255,255,255,.4);">
      Your value: <b style="color:white;">{p['your_value']}</b>
    </span>
    <span style="color:rgba(255,255,255,.4);">
      Benchmark: <b style="color:#a78bfa;">{p['benchmark']}</b>
    </span>
  </div>
  <div class="conf-bar-bg">
    <div class="conf-bar" style="width:{p['confidence']}%;"></div>
  </div>
</div>""", unsafe_allow_html=True)

    st.markdown('<hr style="border-color:rgba(255,255,255,.08);margin:1.5rem 0;">', unsafe_allow_html=True)

    # ── Strategies ───────────────────────────────────────────────────
    st.markdown('<div class="r-section">✅ Recommended Strategies</div>', unsafe_allow_html=True)

    for strat in strategies:
        s = strat["strategies"]
        with st.expander(f"{strat['icon']}  {strat['problem']} — Action Plan", expanded=False):
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("**⚡ Quick Wins (this week)**")
                for item in s.get("short_term", []):
                    st.markdown(f"- {item}")
            with c2:
                st.markdown("**🎯 Long-Term Strategy (1–3 months)**")
                for item in s.get("long_term", []):
                    st.markdown(f"- {item}")
            st.markdown("---")
            kpi_col, tool_col, impact_col = st.columns(3)
            with kpi_col:
                st.markdown(f"📌 **KPI Goal**\n\n{s.get('kpi','—')}")
            with tool_col:
                st.markdown(f"🛠️ **Tools**\n\n{', '.join(s.get('tools',[]))}")
            with impact_col:
                st.markdown(f"📈 **Impact**\n\n{s.get('expected_impact','—')}")

    st.markdown('<hr style="border-color:rgba(255,255,255,.08);margin:1.5rem 0;">', unsafe_allow_html=True)

    # ── AI Explanation ───────────────────────────────────────────────
    st.markdown('<div class="r-section">🧠 AI Analysis</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="expl-box">{explanation}</div>', unsafe_allow_html=True)

    st.markdown('<hr style="border-color:rgba(255,255,255,.08);margin:1.5rem 0;">', unsafe_allow_html=True)

    # ── Charts ───────────────────────────────────────────────────────
    st.markdown('<div class="r-section">📈 Visual Analysis</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)

    with c1:
        # Radar chart — normalised 0-100
        conv_s = min(100, (data["conversion_rate"] / 3.5) * 100)
        roi_s  = min(100, (derived["marketing_roi"] / 4.0) * 100)
        ret_s  = min(100, (data["retention_rate"] / 60.0) * 100)
        inv_s  = min(100, (derived["inventory_turnover"] / 12.0) * 100)
        tgt    = max(data.get("monthly_target", 1), 1)
        sal_s  = min(100, (data["monthly_sales"] / tgt) * 100)

        cats   = ["Conversion", "Mkt ROI", "Retention", "Inventory", "Sales"]
        vals   = [conv_s, roi_s, ret_s, inv_s, sal_s]
        bench  = [75]*5

        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=vals + [vals[0]], theta=cats + [cats[0]],
            fill="toself", fillcolor="rgba(99,102,241,.18)",
            line=dict(color="#6366f1", width=2), name="Your Business"))
        fig.add_trace(go.Scatterpolar(
            r=bench + [bench[0]], theta=cats + [cats[0]],
            fill="toself", fillcolor="rgba(16,185,129,.05)",
            line=dict(color="rgba(16,185,129,.4)", width=1, dash="dash"),
            name="Benchmark"))
        fig.update_layout(
            polar=dict(bgcolor="rgba(0,0,0,0)",
                       radialaxis=dict(visible=True, range=[0,100],
                                       gridcolor="rgba(255,255,255,.1)",
                                       tickfont=dict(color="rgba(255,255,255,.3)")),
                       angularaxis=dict(tickfont=dict(color="rgba(255,255,255,.7)"),
                                        gridcolor="rgba(255,255,255,.1)")),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white"),
            title=dict(text="Business Health Radar", font=dict(color="white", size=14)),
            showlegend=True, legend=dict(font=dict(color="white")),
            margin=dict(t=50, b=20, l=20, r=20),
        )
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        if problems:
            names = [p["problem"][:28] + "…" if len(p["problem"]) > 28 else p["problem"]
                     for p in problems]
            confs  = [p["confidence"] for p in problems]
            bar_colors = ["#ef4444" if p["severity"]=="High" else "#f59e0b" for p in problems]

            fig2 = go.Figure(go.Bar(
                x=confs, y=names, orientation="h",
                marker=dict(color=bar_colors),
                text=[f"{c}%" for c in confs],
                textposition="outside", textfont=dict(color="white")))
            fig2.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="white"),
                title=dict(text="Confidence by Problem", font=dict(color="white", size=14)),
                xaxis=dict(title="Confidence %", gridcolor="rgba(255,255,255,.1)",
                           tickfont=dict(color="rgba(255,255,255,.45)"), range=[0,110]),
                yaxis=dict(gridcolor="rgba(255,255,255,.08)",
                           tickfont=dict(color="rgba(255,255,255,.7)")),
                margin=dict(t=50, b=40, l=20, r=20),
            )
            st.plotly_chart(fig2, use_container_width=True)

    st.markdown('<hr style="border-color:rgba(255,255,255,.08);margin:1.5rem 0;">', unsafe_allow_html=True)

    # ── Download PDF ─────────────────────────────────────────────────
    st.markdown('<div class="r-section">📥 Download Report</div>', unsafe_allow_html=True)

    _, mid, _ = st.columns([1, 2, 1])
    with mid:
        if st.button("📄 Generate PDF Report"):
            with st.spinner("Building your PDF…"):
                pdf_bytes = generate_pdf(res)
            filename = f"{biz.replace(' ','_')}_analysis.pdf"
            st.download_button(
                label="⬇️ Click Here to Download PDF",
                data=pdf_bytes,
                file_name=filename,
                mime="application/pdf",
            )

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("🔄 Analyse Another Business"):
            st.session_state.step    = 1
            st.session_state.form    = {}
            st.session_state.results = None
            st.rerun()


# ════════════════════════════════════════════════════════════════════
#  MAIN
# ════════════════════════════════════════════════════════════════════
def main():
    init_state()
    inject_css()

    # Show hero only on the first step
    if st.session_state.step == 1 and not st.session_state.results:
        st.markdown("""
<div class="hero-title">🤖 AI Business Analyzer</div>
<div class="hero-sub">
  Get an AI-powered deep-dive into your e-commerce business.<br>
  Identify problems, get proven strategies, and download a complete report.
</div>""", unsafe_allow_html=True)

    if st.session_state.results:
        show_results()
    elif st.session_state.step == 1:
        step_1()
    elif st.session_state.step == 2:
        step_2()
    elif st.session_state.step == 3:
        step_3()
    elif st.session_state.step == 4:
        step_4()

    # Toggle button at bottom left
    if st.button("Toggle Background", key="toggle"):
        st.session_state.theme = "solid" if st.session_state.theme == "gradient" else "gradient"
        st.rerun()


if __name__ == "__main__":
    main()
