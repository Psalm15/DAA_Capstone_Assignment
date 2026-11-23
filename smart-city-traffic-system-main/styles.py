"""Frontend styling (CSS + animations) for the Smart City Traffic System dashboard."""

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --bg: #0b1020;
    --panel: #121a33;
    --panel-2: #172042;
    --border: rgba(148, 163, 255, 0.16);
    --cyan: #22d3ee;
    --violet: #8b5cf6;
    --amber: #fbbf24;
    --green: #34d399;
    --text: #e6ecff;
    --muted: #94a3c7;
}

html, body, [class*="css"], .stApp { font-family: 'Inter', sans-serif; }

/* ---------- animated background ---------- */
.stApp {
    background:
        radial-gradient(900px 500px at 10% -10%, rgba(139, 92, 246, 0.20), transparent 60%),
        radial-gradient(800px 500px at 100% 0%, rgba(34, 211, 238, 0.16), transparent 60%),
        var(--bg);
    background-attachment: fixed;
}
header[data-testid="stHeader"] { background: transparent; }
#MainMenu, footer { visibility: hidden; }

/* ---------- keyframes ---------- */
@keyframes fadeUp   { from { opacity: 0; transform: translateY(18px); } to { opacity: 1; transform: none; } }
@keyframes fadeIn   { from { opacity: 0; } to { opacity: 1; } }
@keyframes slideIn  { from { opacity: 0; transform: translateX(-16px); } to { opacity: 1; transform: none; } }
@keyframes gradientShift { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }
@keyframes pulse    { 0% { box-shadow: 0 0 0 0 rgba(52, 211, 153, .65); } 70% { box-shadow: 0 0 0 10px rgba(52, 211, 153, 0); } 100% { box-shadow: 0 0 0 0 rgba(52, 211, 153, 0); } }
@keyframes drive    { from { left: -60px; } to { left: 100%; } }
@keyframes shimmer  { from { background-position: -200% 0; } to { background-position: 200% 0; } }

/* ---------- page content ---------- */
.block-container { padding-top: 2rem; max-width: 1250px; animation: fadeIn .5s ease both; }
.block-container > div > div > div > div { animation: fadeUp .55s ease both; }
.block-container > div > div > div > div:nth-child(2) { animation-delay: .06s; }
.block-container > div > div > div > div:nth-child(3) { animation-delay: .12s; }
.block-container > div > div > div > div:nth-child(4) { animation-delay: .18s; }
.block-container > div > div > div > div:nth-child(5) { animation-delay: .24s; }

/* ---------- hero ---------- */
.hero {
    position: relative; overflow: hidden;
    padding: 1.6rem 1.8rem 1.9rem; margin-bottom: 1.2rem;
    border-radius: 20px; border: 1px solid var(--border);
    background: linear-gradient(135deg, rgba(34,211,238,.10), rgba(139,92,246,.12));
    backdrop-filter: blur(6px);
}
.hero h1 {
    margin: 0; font-size: 2.1rem; font-weight: 800; letter-spacing: -0.02em;
    background: linear-gradient(90deg, var(--cyan), var(--violet), var(--cyan));
    background-size: 200% auto; -webkit-background-clip: text; background-clip: text;
    -webkit-text-fill-color: transparent; animation: gradientShift 6s ease infinite;
}
.hero p { margin: .35rem 0 0; color: var(--muted); font-size: 1rem; }
.hero .badge {
    display: inline-flex; align-items: center; gap: .45rem; margin-bottom: .6rem;
    padding: .22rem .7rem; border-radius: 999px; font-size: .75rem; font-weight: 600;
    color: var(--green); background: rgba(52, 211, 153, .10); border: 1px solid rgba(52, 211, 153, .35);
}
.hero .dot { width: 8px; height: 8px; border-radius: 50%; background: var(--green); animation: pulse 1.8s infinite; }
/* road + moving car strip */
.road { position: absolute; left: 0; right: 0; bottom: 0; height: 5px; background: rgba(148,163,255,.14); }
.road::before { content: ""; position: absolute; inset: 2px 0; background: repeating-linear-gradient(90deg, rgba(251,191,36,.7) 0 18px, transparent 18px 38px); opacity: .5; }
.car { position: absolute; bottom: 0; width: 46px; height: 5px; border-radius: 4px;
       background: linear-gradient(90deg, transparent, var(--cyan)); box-shadow: 0 0 14px var(--cyan);
       animation: drive 4.5s linear infinite; }
.car.c2 { animation-duration: 6.5s; animation-delay: 1.2s; background: linear-gradient(90deg, transparent, var(--amber)); box-shadow: 0 0 14px var(--amber); }

/* ---------- headings ---------- */
h2, h3 { letter-spacing: -0.01em; }
[data-testid="stHeadingWithActionElements"] h2 { font-weight: 700; }
.section-title { font-weight: 700; font-size: 1.05rem; margin: 1.1rem 0 .4rem; color: var(--text); display: flex; align-items: center; gap: .5rem; }
.section-title::before { content: ""; width: 4px; height: 1.1em; border-radius: 3px; background: linear-gradient(var(--cyan), var(--violet)); }

/* ---------- sidebar ---------- */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0e1530 0%, #0b1020 100%);
    border-right: 1px solid var(--border);
}
.brand { display: flex; align-items: center; gap: .7rem; margin: .4rem 0 1rem; animation: slideIn .6s ease both; }
.brand .logo { width: 42px; height: 42px; border-radius: 12px; display: grid; place-items: center; font-size: 1.4rem;
               background: linear-gradient(135deg, var(--cyan), var(--violet)); box-shadow: 0 6px 20px rgba(34,211,238,.3); }
.brand b { display: block; font-size: 1.02rem; line-height: 1.1; }
.brand span { font-size: .75rem; color: var(--muted); }
[data-testid="stSidebar"] .stRadio > label { display: none; }
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] { gap: .35rem; }
[data-testid="stSidebar"] .stRadio label[data-baseweb="radio"] {
    padding: .6rem .8rem; border-radius: 12px; border: 1px solid transparent;
    transition: all .25s ease; width: 100%; animation: slideIn .5s ease both;
}
[data-testid="stSidebar"] .stRadio label[data-baseweb="radio"]:hover {
    background: rgba(34,211,238,.08); border-color: var(--border); transform: translateX(5px);
}
[data-testid="stSidebar"] .stRadio label[data-baseweb="radio"]:has(input:checked) {
    background: linear-gradient(90deg, rgba(34,211,238,.18), rgba(139,92,246,.14));
    border-color: rgba(34,211,238,.45);
}
[data-testid="stSidebar"] .stRadio label[data-baseweb="radio"] > div:first-child { display: none; }

/* ---------- stat cards ---------- */
.stat-row { display: grid; grid-template-columns: 1fr 1fr; gap: .6rem; margin-top: .8rem; }
.stat { padding: .8rem .9rem; border-radius: 14px; background: var(--panel); border: 1px solid var(--border);
        transition: transform .25s ease, border-color .25s ease; animation: fadeUp .6s ease both; }
.stat:hover { transform: translateY(-3px); border-color: rgba(34,211,238,.5); }
.stat .v { font-size: 1.6rem; font-weight: 800; color: var(--cyan); line-height: 1; }
.stat .l { font-size: .72rem; color: var(--muted); text-transform: uppercase; letter-spacing: .06em; margin-top: .25rem; }

/* ---------- buttons ---------- */
.stButton > button {
    border-radius: 12px; border: 1px solid rgba(34,211,238,.45); font-weight: 600; padding: .55rem 1.2rem;
    color: #06121f; background: linear-gradient(90deg, var(--cyan), #67e8f9);
    transition: transform .2s ease, box-shadow .2s ease, filter .2s ease;
}
.stButton > button:hover { transform: translateY(-2px) scale(1.02); box-shadow: 0 10px 26px rgba(34,211,238,.35); filter: brightness(1.05); color: #06121f; border-color: transparent; }
.stButton > button:active { transform: translateY(0) scale(.98); }
.stButton > button p { font-weight: 700; }

/* ---------- inputs ---------- */
[data-baseweb="select"] > div, .stTextInput input, .stNumberInput input {
    border-radius: 12px !important; background: var(--panel) !important; border: 1px solid var(--border) !important;
    transition: border-color .2s ease, box-shadow .2s ease;
}
[data-baseweb="select"] > div:hover, .stTextInput input:focus, .stNumberInput input:focus {
    border-color: var(--cyan) !important; box-shadow: 0 0 0 3px rgba(34,211,238,.15) !important;
}

/* ---------- panels / media ---------- */
[data-testid="stImage"], [data-testid="stPyplot"], .stPlotlyChart, [data-testid="stDataFrame"], [data-testid="stTable"], [data-testid="stJson"] {
    border-radius: 16px; overflow: hidden;
}
[data-testid="stPyplot"] img, [data-testid="stImage"] img {
    border-radius: 16px; border: 1px solid var(--border); box-shadow: 0 12px 40px rgba(0,0,0,.35);
    transition: transform .35s ease, box-shadow .35s ease; animation: fadeUp .6s ease both;
}
[data-testid="stPyplot"] img:hover { transform: scale(1.015); box-shadow: 0 18px 50px rgba(34,211,238,.18); }
[data-testid="stAlert"] { border-radius: 14px; animation: fadeUp .45s ease both; border: 1px solid var(--border); }
[data-testid="stTable"] table { border-collapse: separate; border-spacing: 0; }
[data-testid="stTable"] th { background: var(--panel-2); }
[data-testid="stTable"] tr { transition: background .2s ease; }
[data-testid="stTable"] tr:hover td { background: rgba(34,211,238,.06); }

/* ---------- result chips ---------- */
.chip-row { display: flex; flex-wrap: wrap; gap: .4rem; margin: .3rem 0 .8rem; }
.chip { padding: .28rem .7rem; border-radius: 999px; background: var(--panel-2); border: 1px solid var(--border);
        font-weight: 600; font-size: .85rem; animation: fadeUp .5s ease both; transition: transform .2s ease, border-color .2s ease; }
.chip:hover { transform: translateY(-2px); border-color: var(--cyan); }
.chip.hot { border-color: rgba(251,191,36,.55); color: var(--amber); }
.chip.ok  { border-color: rgba(52,211,153,.55); color: var(--green); }
.chip.arrow { background: transparent; border: none; color: var(--muted); padding: .28rem .1rem; }
.kv { color: var(--muted); font-size: .9rem; margin: .15rem 0; }
.kv b { color: var(--text); }
.cost-card { display: inline-block; padding: .6rem 1.1rem; border-radius: 14px; margin: .2rem .5rem .6rem 0;
             background: linear-gradient(135deg, rgba(34,211,238,.14), rgba(139,92,246,.14)); border: 1px solid var(--border);
             animation: fadeUp .5s ease both; }
.cost-card .v { font-size: 1.5rem; font-weight: 800; color: var(--cyan); }
.cost-card .l { font-size: .72rem; text-transform: uppercase; letter-spacing: .06em; color: var(--muted); }

::-webkit-scrollbar { width: 10px; height: 10px; }
::-webkit-scrollbar-thumb { background: rgba(148,163,255,.25); border-radius: 8px; }
@media (prefers-reduced-motion: reduce) { * { animation: none !important; transition: none !important; } }
</style>
"""
