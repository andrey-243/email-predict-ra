import streamlit as st
import pandas as pd
import unicodedata
import re

st.set_page_config(
    page_title="Email Predictor — RealAdvisors",
    page_icon="📧",
    layout="centered",
)

# ── Data ──────────────────────────────────────────────────────────────────────

@st.cache_data
def load_data():
    df = pd.read_csv(
        "02_top3_motifs_par_network.csv",
        sep=";",
        dtype=str,
    )
    # coerce probability columns to float
    for col in df.columns:
        if "proba_pct" in col:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0.0)
    return df

# ── Name normalisation ────────────────────────────────────────────────────────

def normalize(text: str) -> str:
    """Lowercase, remove accents, replace apostrophes with hyphen, strip other non-alphanum chars."""
    # remove accents
    nfkd = unicodedata.normalize("NFD", text)
    no_accent = "".join(c for c in nfkd if unicodedata.category(c) != "Mn")
    # lowercase
    s = no_accent.lower()
    # apostrophe → hyphen
    s = s.replace("'", "-").replace("'", "-")
    # keep only a-z 0-9 and hyphen
    s = re.sub(r"[^a-z0-9-]", "", s)
    # collapse multiple hyphens
    s = re.sub(r"-+", "-", s).strip("-")
    return s

# ── Email local-part generation ───────────────────────────────────────────────

MOTIF_LABELS = {
    "prenom_point_nom":  "prénom.nom",
    "initiale_plus_nom": "initiale + nom",
    "prenom_nom_concat": "prénom+nom collés",
    "prenom_seul":       "prénom seul",
    "nom_seul":          "nom seul",
    "adresse_generique": "contact@ / info@",
    "autre":             "alias / perso (imprévisible)",
}

def generate_local(motif: str, prenom: str, nom: str) -> list[str]:
    """Return a list of candidate local parts for a given motif."""
    p = normalize(prenom)
    n = normalize(nom)
    if motif == "prenom_point_nom":
        return [f"{p}.{n}"] if p and n else []
    if motif == "initiale_plus_nom":
        return [f"{p[0]}.{n}"] if p and n else []
    if motif == "prenom_nom_concat":
        return [f"{p}{n}"] if p and n else []
    if motif == "prenom_seul":
        return [p] if p else []
    if motif == "nom_seul":
        return [n] if n else []
    if motif == "adresse_generique":
        return ["contact", "info"]
    return []  # "autre" — unpredictable

# ── Which inputs are needed for a given set of motifs ─────────────────────────

def needs_inputs(motifs: list[str]) -> tuple[bool, bool]:
    """Return (needs_prenom, needs_nom)."""
    needs_p = any(m in {"prenom_point_nom", "initiale_plus_nom", "prenom_nom_concat", "prenom_seul"} for m in motifs)
    needs_n = any(m in {"prenom_point_nom", "initiale_plus_nom", "prenom_nom_concat", "nom_seul"} for m in motifs)
    return needs_p, needs_n

# ── UI ────────────────────────────────────────────────────────────────────────

st.title("📧 Email Predictor par Réseau")
st.caption("Génère les adresses email les plus probables d'un agent selon son réseau.")

df = load_data()
networks = df["network"].tolist()

col1, col2 = st.columns([2, 1])
with col1:
    selected_network = st.selectbox("Réseau immobilier", networks)
with col2:
    st.metric("Emails analysés", f"{int(df.loc[df['network'] == selected_network, 'nb_emails_classes'].values[0]):,}".replace(",", " "))

row = df[df["network"] == selected_network].iloc[0]

# Parse motifs and domains
motifs_data = []
for i in [1, 2, 3]:
    cle = row.get(f"estimation_{i}_cle", "")
    lib = row.get(f"estimation_{i}_motif", "")
    proba = float(row.get(f"estimation_{i}_proba_pct", 0.0) or 0.0)
    if pd.notna(cle) and cle and proba > 0:
        motifs_data.append({"cle": cle, "libelle": lib, "proba": proba})

domains_data = []
for i in [1, 2, 3]:
    dom = row.get(f"domaine_{i}", "")
    proba = float(row.get(f"domaine_{i}_proba_pct", 0.0) or 0.0)
    if pd.notna(dom) and dom and proba > 0:
        domains_data.append({"domain": dom, "proba": proba})

# Show pattern summary
with st.expander("📊 Patterns détectés pour ce réseau", expanded=False):
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Format de l'adresse locale**")
        for m in motifs_data:
            bar = int(m["proba"] / 5)
            st.markdown(f"`{m['libelle']}` — **{m['proba']:.1f}%** {'▓' * bar}{'░' * (20 - bar)}")
    with c2:
        st.markdown("**Domaine (@…)**")
        for d in domains_data:
            bar = int(d["proba"] / 5)
            st.markdown(f"`{d['domain']}` — **{d['proba']:.1f}%** {'▓' * bar}{'░' * (20 - bar)}")

# Determine required inputs
motif_keys = [m["cle"] for m in motifs_data]
need_prenom, need_nom = needs_inputs(motif_keys)

st.divider()
st.subheader("Informations de l'agent")

input_col1, input_col2 = st.columns(2)
prenom, nom = "", ""

if need_prenom:
    with input_col1:
        prenom = st.text_input("Prénom", placeholder="ex. Marie")
if need_nom:
    with input_col2:
        nom = st.text_input("Nom", placeholder="ex. Dupont")

if not need_prenom and not need_nom:
    st.info("Ce réseau utilise principalement des alias personnels — la génération automatique n'est pas possible.")

# Generate button
st.divider()
generate = st.button("🔍 Générer les emails", type="primary", use_container_width=True)

if generate:
    if need_prenom and not prenom.strip():
        st.warning("Merci de saisir le prénom.")
        st.stop()
    if need_nom and not nom.strip():
        st.warning("Merci de saisir le nom.")
        st.stop()

    results = []
    unpredictable_proba = 0.0

    for motif in motifs_data:
        cle = motif["cle"]
        m_proba = motif["proba"]

        if cle == "autre":
            unpredictable_proba += m_proba
            continue

        locals_list = generate_local(cle, prenom.strip(), nom.strip())
        if not locals_list:
            continue

        for local in locals_list:
            for dom in domains_data:
                # combined probability: motif_proba * domain_proba / 100
                combined = round(m_proba * dom["proba"] / 100, 1)
                results.append({
                    "Email": f"{local}@{dom['domain']}",
                    "Format": MOTIF_LABELS.get(cle, cle),
                    "Domaine": dom["domain"],
                    "Proba (%)": combined,
                })

    if not results:
        st.warning("Aucun email prédictible pour ce réseau avec ces informations.")
    else:
        results_df = (
            pd.DataFrame(results)
            .sort_values("Proba (%)", ascending=False)
            .drop_duplicates(subset=["Email"])
            .reset_index(drop=True)
        )
        results_df.index = results_df.index + 1

        st.subheader(f"Emails générés pour **{prenom.strip()} {nom.strip()}**")

        # Display with coloured probability
        for _, r in results_df.iterrows():
            pct = r["Proba (%)"]
            if pct >= 50:
                colour = "🟢"
            elif pct >= 15:
                colour = "🟡"
            else:
                colour = "🔴"

            col_a, col_b, col_c = st.columns([4, 2, 1])
            with col_a:
                st.code(r["Email"], language=None)
            with col_b:
                st.markdown(f"*{r['Format']}*")
            with col_c:
                st.markdown(f"{colour} **{pct:.1f}%**")

        if unpredictable_proba > 0:
            st.info(
                f"⚠️ **{unpredictable_proba:.0f}%** des emails de ce réseau sont des alias personnels "
                f"ou adresses non-standard — ils ne peuvent pas être prédits automatiquement."
            )

        # CSV download
        st.download_button(
            label="⬇️ Télécharger en CSV",
            data=results_df.to_csv(index=False, sep=";").encode("utf-8-sig"),
            file_name=f"emails_{normalize(prenom)}_{normalize(nom)}_{selected_network.lower().replace(' ', '_')}.csv",
            mime="text/csv",
        )
