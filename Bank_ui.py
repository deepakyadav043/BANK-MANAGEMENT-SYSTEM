import json
import random
import string
from pathlib import Path
import streamlit as st

# ─── PAGE CONFIG ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="NeoBank",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── GLOBAL CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

/* ── Reset & base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background: #080c14 !important;
    color: #e8eaf0 !important;
    font-family: 'DM Sans', sans-serif !important;
}

[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(ellipse 80% 60% at 10% 0%, #0d2240 0%, transparent 60%),
        radial-gradient(ellipse 60% 50% at 90% 100%, #091a30 0%, transparent 55%),
        #080c14 !important;
}

[data-testid="stHeader"], [data-testid="stToolbar"] { display: none !important; }
[data-testid="stSidebar"] { display: none !important; }
.block-container { padding: 2rem 3rem !important; max-width: 1100px !important; }

/* ── Typography ── */
h1, h2, h3 { font-family: 'Syne', sans-serif !important; }

/* ── Hero header ── */
.hero {
    text-align: center;
    padding: 3rem 0 2rem;
    position: relative;
}
.hero-badge {
    display: inline-block;
    background: rgba(0,180,255,0.08);
    border: 1px solid rgba(0,180,255,0.25);
    color: #00b4ff;
    font-size: 0.72rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    padding: 0.3rem 1rem;
    border-radius: 99px;
    margin-bottom: 1.2rem;
    font-family: 'DM Sans', sans-serif;
}
.hero h1 {
    font-size: clamp(2.4rem, 5vw, 3.8rem) !important;
    font-weight: 800 !important;
    line-height: 1.1 !important;
    background: linear-gradient(135deg, #ffffff 30%, #00b4ff 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.6rem !important;
}
.hero p {
    color: #7a8499;
    font-size: 1rem;
    max-width: 420px;
    margin: 0 auto;
}

/* ── Nav pills ── */
div[data-testid="stHorizontalBlock"] button {
    background: transparent !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    color: #7a8499 !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.88rem !important;
    padding: 0.55rem 1rem !important;
    transition: all 0.2s !important;
    width: 100% !important;
}
div[data-testid="stHorizontalBlock"] button:hover {
    border-color: rgba(0,180,255,0.4) !important;
    color: #00b4ff !important;
    background: rgba(0,180,255,0.06) !important;
}

/* ── Cards ── */
.card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 20px;
    padding: 2rem;
    backdrop-filter: blur(12px);
    margin-bottom: 1.2rem;
}
.card-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.15rem;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 0.3rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.card-sub {
    font-size: 0.82rem;
    color: #4a5568;
    margin-bottom: 1.5rem;
}

/* ── Metric tiles ── */
.metric-row { display: flex; gap: 1rem; margin-bottom: 1.2rem; }
.metric-tile {
    flex: 1;
    background: rgba(0,180,255,0.05);
    border: 1px solid rgba(0,180,255,0.15);
    border-radius: 14px;
    padding: 1.2rem 1.4rem;
    position: relative;
    overflow: hidden;
}
.metric-tile::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, transparent, #00b4ff, transparent);
}
.metric-label { font-size: 0.72rem; color: #4a5568; letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 0.3rem; }
.metric-value { font-family: 'Syne', sans-serif; font-size: 1.5rem; font-weight: 700; color: #fff; }
.metric-value.green { color: #00e5a0; }
.metric-value.blue  { color: #00b4ff; }

/* ── Streamlit inputs ── */
[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important;
    color: #e8eaf0 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.92rem !important;
    padding: 0.6rem 0.9rem !important;
    transition: border-color 0.2s !important;
}
[data-testid="stTextInput"] input:focus,
[data-testid="stNumberInput"] input:focus {
    border-color: rgba(0,180,255,0.5) !important;
    box-shadow: 0 0 0 3px rgba(0,180,255,0.08) !important;
}
[data-testid="stTextInput"] label,
[data-testid="stNumberInput"] label {
    color: #7a8499 !important;
    font-size: 0.8rem !important;
    letter-spacing: 0.05em !important;
    text-transform: uppercase !important;
}

/* ── Primary button ── */
[data-testid="stFormSubmitButton"] button,
.stButton > button {
    background: linear-gradient(135deg, #0070f3, #00b4ff) !important;
    border: none !important;
    border-radius: 10px !important;
    color: #fff !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    padding: 0.65rem 1.6rem !important;
    letter-spacing: 0.04em !important;
    transition: opacity 0.2s, transform 0.15s !important;
    width: 100% !important;
}
[data-testid="stFormSubmitButton"] button:hover,
.stButton > button:hover {
    opacity: 0.88 !important;
    transform: translateY(-1px) !important;
}

/* ── Alerts ── */
[data-testid="stAlert"] {
    border-radius: 12px !important;
    border: none !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.88rem !important;
}

/* ── Account info table ── */
.info-table { width: 100%; border-collapse: collapse; }
.info-table tr { border-bottom: 1px solid rgba(255,255,255,0.05); }
.info-table tr:last-child { border-bottom: none; }
.info-table td { padding: 0.7rem 0.5rem; font-size: 0.9rem; }
.info-table td:first-child { color: #4a5568; width: 40%; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.05em; }
.info-table td:last-child { color: #e8eaf0; font-weight: 500; }

/* ── Divider ── */
.divider { border: none; border-top: 1px solid rgba(255,255,255,0.06); margin: 1.5rem 0; }

/* ── Tab menu ── */
.nav-container {
    display: flex;
    gap: 0.5rem;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 14px;
    padding: 0.4rem;
    margin-bottom: 2rem;
}
</style>
""", unsafe_allow_html=True)


# ─── BANK LOGIC ─────────────────────────────────────────────────────────────
DATABASE = "database.json"

def load_data():
    if Path(DATABASE).exists():
        with open(DATABASE) as f:
            return json.loads(f.read())
    return []

def save_data(data):
    with open(DATABASE, "w") as f:
        f.write(json.dumps(data))

def generate_account():
    alpha = random.choices(string.ascii_letters, k=8)
    num   = random.choices(string.digits, k=4)
    acc   = alpha + num
    random.shuffle(acc)
    return "".join(acc)

def find_user(data, accno, pin):
    return [u for u in data if u["AccountNo"] == accno and u["pin"] == pin]


# ─── SESSION STATE ───────────────────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "Create Account"
if "bank_data" not in st.session_state:
    st.session_state.bank_data = load_data()


# ─── HERO ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-badge">✦ Secure Banking Platform</div>
    <h1>NeoBank</h1>
    <p>Modern. Secure. Instant. Your money, always in control.</p>
</div>
""", unsafe_allow_html=True)


# ─── NAVIGATION ─────────────────────────────────────────────────────────────
pages = {
    "➕  Create Account": "Create Account",
    "💰  Deposit":        "Deposit",
    "💸  Withdraw":       "Withdraw",
    "👤  My Account":     "My Account",
    "✏️  Update Details": "Update Details",
    "🗑️  Delete Account": "Delete Account",
}

cols = st.columns(len(pages))
for col, (label, key) in zip(cols, pages.items()):
    if col.button(label, key=f"nav_{key}"):
        st.session_state.page = key

st.markdown("<hr class='divider'>", unsafe_allow_html=True)

page = st.session_state.page
data = st.session_state.bank_data


# ═══════════════════════════════════════════════════════════════════════════
# PAGE: CREATE ACCOUNT
# ═══════════════════════════════════════════════════════════════════════════
if page == "Create Account":
    st.markdown("""
    <div class="card">
        <div class="card-title">➕ Open New Account</div>
        <div class="card-sub">Fill in your details to get started in seconds.</div>
    </div>
    """, unsafe_allow_html=True)

    with st.form("create_form"):
        c1, c2 = st.columns(2)
        name  = c1.text_input("Full Name")
        age   = c2.number_input("Age", min_value=1, max_value=120, step=1, value=18)
        email = st.text_input("Email Address")
        pin   = st.text_input("4-Digit PIN", type="password", max_chars=4)
        submit = st.form_submit_button("🚀 Create Account")

    if submit:
        if not name or not email or not pin:
            st.error("⚠️ Please fill in all fields.")
        elif age < 12:
            st.error("⚠️ You must be at least 12 years old to open an account.")
        elif len(pin) != 4 or not pin.isdigit():
            st.error("⚠️ PIN must be exactly 4 digits.")
        else:
            acc_no = generate_account()
            new_user = {
                "name":      name,
                "age":       int(age),
                "email":     email,
                "AccountNo": acc_no,
                "pin":       pin,
                "balance":   0,
            }
            data.append(new_user)
            save_data(data)
            st.session_state.bank_data = data
            st.success("✅ Account created successfully!")
            st.markdown(f"""
            <div class="metric-row">
                <div class="metric-tile">
                    <div class="metric-label">Account Number</div>
                    <div class="metric-value blue" style="font-size:1.1rem;">{acc_no}</div>
                </div>
                <div class="metric-tile">
                    <div class="metric-label">Welcome</div>
                    <div class="metric-value" style="font-size:1.1rem;">{name}</div>
                </div>
            </div>
            <p style="color:#4a5568;font-size:0.8rem;">🔐 Save your Account Number — you'll need it to log in.</p>
            """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════
# PAGE: DEPOSIT
# ═══════════════════════════════════════════════════════════════════════════
elif page == "Deposit":
    st.markdown("""
    <div class="card">
        <div class="card-title">💰 Deposit Money</div>
        <div class="card-sub">Add funds to your account instantly.</div>
    </div>
    """, unsafe_allow_html=True)

    with st.form("deposit_form"):
        accno  = st.text_input("Account Number")
        pin    = st.text_input("PIN", type="password", max_chars=4)
        amount = st.number_input("Amount (₹)", min_value=1, step=100, value=500)
        submit = st.form_submit_button("💰 Deposit Now")

    if submit:
        if not accno or not pin:
            st.error("⚠️ Please fill in all fields.")
        else:
            user = find_user(data, accno, pin)
            if not user:
                st.error("❌ Account not found. Check your account number and PIN.")
            else:
                user[0]["balance"] += amount
                save_data(data)
                st.session_state.bank_data = data
                st.success(f"✅ ₹{amount:,} deposited successfully!")
                st.markdown(f"""
                <div class="metric-row">
                    <div class="metric-tile">
                        <div class="metric-label">Deposited</div>
                        <div class="metric-value green">+ ₹{amount:,}</div>
                    </div>
                    <div class="metric-tile">
                        <div class="metric-label">New Balance</div>
                        <div class="metric-value blue">₹{user[0]['balance']:,}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════
# PAGE: WITHDRAW
# ═══════════════════════════════════════════════════════════════════════════
elif page == "Withdraw":
    st.markdown("""
    <div class="card">
        <div class="card-title">💸 Withdraw Money</div>
        <div class="card-sub">Transfer funds out of your account securely.</div>
    </div>
    """, unsafe_allow_html=True)

    with st.form("withdraw_form"):
        accno  = st.text_input("Account Number")
        pin    = st.text_input("PIN", type="password", max_chars=4)
        amount = st.number_input("Amount (₹)", min_value=1, step=100, value=500)
        submit = st.form_submit_button("💸 Withdraw Now")

    if submit:
        if not accno or not pin:
            st.error("⚠️ Please fill in all fields.")
        else:
            user = find_user(data, accno, pin)
            if not user:
                st.error("❌ Account not found. Check your account number and PIN.")
            elif amount > user[0]["balance"]:
                st.error(f"❌ Insufficient balance. Available: ₹{user[0]['balance']:,}")
            else:
                user[0]["balance"] -= amount
                save_data(data)
                st.session_state.bank_data = data
                st.success(f"✅ ₹{amount:,} withdrawn successfully!")
                st.markdown(f"""
                <div class="metric-row">
                    <div class="metric-tile">
                        <div class="metric-label">Withdrawn</div>
                        <div class="metric-value" style="color:#ff6b6b;">- ₹{amount:,}</div>
                    </div>
                    <div class="metric-tile">
                        <div class="metric-label">Remaining Balance</div>
                        <div class="metric-value blue">₹{user[0]['balance']:,}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════
# PAGE: MY ACCOUNT
# ═══════════════════════════════════════════════════════════════════════════
elif page == "My Account":
    st.markdown("""
    <div class="card">
        <div class="card-title">👤 Account Details</div>
        <div class="card-sub">View your profile and balance.</div>
    </div>
    """, unsafe_allow_html=True)

    with st.form("details_form"):
        accno  = st.text_input("Account Number")
        pin    = st.text_input("PIN", type="password", max_chars=4)
        submit = st.form_submit_button("🔍 View Account")

    if submit:
        if not accno or not pin:
            st.error("⚠️ Please fill in all fields.")
        else:
            user = find_user(data, accno, pin)
            if not user:
                st.error("❌ Account not found.")
            else:
                u = user[0]
                st.markdown(f"""
                <div class="metric-row">
                    <div class="metric-tile">
                        <div class="metric-label">Total Balance</div>
                        <div class="metric-value green">₹{u['balance']:,}</div>
                    </div>
                    <div class="metric-tile">
                        <div class="metric-label">Account Status</div>
                        <div class="metric-value blue">Active ✦</div>
                    </div>
                </div>
                <div class="card">
                    <table class="info-table">
                        <tr><td>Name</td><td>{u['name']}</td></tr>
                        <tr><td>Age</td><td>{u['age']} years</td></tr>
                        <tr><td>Email</td><td>{u['email']}</td></tr>
                        <tr><td>Account No.</td><td><code style="background:rgba(0,180,255,0.1);padding:2px 8px;border-radius:6px;color:#00b4ff;">{u['AccountNo']}</code></td></tr>
                    </table>
                </div>
                """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════
# PAGE: UPDATE DETAILS
# ═══════════════════════════════════════════════════════════════════════════
elif page == "Update Details":
    st.markdown("""
    <div class="card">
        <div class="card-title">✏️ Update Details</div>
        <div class="card-sub">Leave a field blank to keep it unchanged.</div>
    </div>
    """, unsafe_allow_html=True)

    with st.form("update_form"):
        accno     = st.text_input("Account Number")
        pin       = st.text_input("Current PIN", type="password", max_chars=4)
        st.markdown("<hr class='divider'>", unsafe_allow_html=True)
        new_name  = st.text_input("New Name  (leave blank to keep current)")
        new_email = st.text_input("New Email (leave blank to keep current)")
        new_pin   = st.text_input("New PIN   (leave blank to keep current)", type="password", max_chars=4)
        submit    = st.form_submit_button("💾 Save Changes")

    if submit:
        if not accno or not pin:
            st.error("⚠️ Account number and current PIN are required.")
        else:
            user = find_user(data, accno, pin)
            if not user:
                st.error("❌ Account not found.")
            else:
                u = user[0]
                if new_name:  u["name"]  = new_name
                if new_email: u["email"] = new_email
                if new_pin:
                    if len(new_pin) != 4 or not new_pin.isdigit():
                        st.error("⚠️ New PIN must be exactly 4 digits.")
                        st.stop()
                    u["pin"] = new_pin
                save_data(data)
                st.session_state.bank_data = data
                st.success("✅ Details updated successfully!")


# ═══════════════════════════════════════════════════════════════════════════
# PAGE: DELETE ACCOUNT
# ═══════════════════════════════════════════════════════════════════════════
elif page == "Delete Account":
    st.markdown("""
    <div class="card" style="border-color:rgba(255,80,80,0.2);">
        <div class="card-title" style="color:#ff6b6b;">🗑️ Delete Account</div>
        <div class="card-sub">This action is permanent and cannot be undone.</div>
    </div>
    """, unsafe_allow_html=True)

    with st.form("delete_form"):
        accno  = st.text_input("Account Number")
        pin    = st.text_input("PIN", type="password", max_chars=4)
        confirm = st.checkbox("I understand this action is irreversible")
        submit = st.form_submit_button("🗑️ Delete Account")

    if submit:
        if not accno or not pin:
            st.error("⚠️ Please fill in all fields.")
        elif not confirm:
            st.warning("⚠️ Please confirm you want to delete this account.")
        else:
            user = find_user(data, accno, pin)
            if not user:
                st.error("❌ Account not found.")
            else:
                data.remove(user[0])
                save_data(data)
                st.session_state.bank_data = data
                st.success("✅ Account deleted successfully. Goodbye! 👋")


# ─── FOOTER ─────────────────────────────────────────────────────────────────
st.markdown("""
<br><br>
<div style="text-align:center; color:#1e2535; font-size:0.75rem; font-family:'DM Sans',sans-serif;">
    NeoBank © 2024 &nbsp;·&nbsp; Secure Banking Platform &nbsp;·&nbsp; Built with Streamlit
</div>
""", unsafe_allow_html=True)