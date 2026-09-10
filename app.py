import streamlit as st
import streamlit.components.v1 as components
import re
import json
import os
import pandas as pd
from openai import OpenAI
from io import BytesIO
from statement_banks import BANKS, SUBJECTS, PRONOUNS

st.set_page_config(page_title="Student Profile Generator", page_icon="📝", layout="wide")

AI_MODEL = "gpt-5.6-luna"
STORAGE_KEY = "student_profile_generator_v15"

# -----------------------------------------------------------------------------
# Browser-local persistence
# -----------------------------------------------------------------------------
_COMPONENT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "browser_storage_component")

@st.cache_resource(show_spinner=False)
def get_browser_storage_component():
    # Register the local component only once per Streamlit process.
    # This prevents Streamlit's component registry from raising a duplicate
    # registration error during script reruns.
    return components.declare_component(
        "browser_storage_v15", path=_COMPONENT_DIR
    )

_browser_storage = get_browser_storage_component()

def storage_load():
    return _browser_storage(action="load", storage_key=STORAGE_KEY, default="")

def storage_save(payload):
    return _browser_storage(
        action="save", storage_key=STORAGE_KEY, data=json.dumps(payload, ensure_ascii=False), default="saved"
    )

def storage_clear():
    return _browser_storage(action="clear", storage_key=STORAGE_KEY, default="cleared")


# -----------------------------------------------------------------------------
# Existing profile/AI logic
# -----------------------------------------------------------------------------
def get_openai_client():
    try:
        api_key = st.secrets.get("OPENAI_API_KEY")
    except Exception:
        api_key = None
    return OpenAI(api_key=api_key) if api_key else None


def ai_edit_profile(profile, subject, name, gender, mode="adjust", max_attempts=5):
    client = get_openai_client()
    if client is None:
        return None, None, "no_api_key"

    first_name = str(name).strip().split()[0] if str(name).strip() else "Student"
    anonymized = re.sub(rf"\b{re.escape(first_name)}\b", "STUDENT", str(profile), flags=re.I)
    p = PRONOUNS.get(str(gender).strip().lower(), PRONOUNS["male"])
    pronouns = f"Use {p['subj']}/{p['obj']}/{p['poss']} correctly after the first sentence."

    task = (
        "Improve grammar, flow, coherence and professional school-report wording while preserving the teacher's meaning and observations."
        if mode == "refine"
        else "Adjust the profile to the required character range while preserving the teacher's meaning and observations."
    )

    last_error = ""
    for attempt in range(max_attempts):
        target = "Aim for 375–385 characters." if attempt == 0 else "MUST be 366–390 characters inclusive; aim for about 378 characters."
        instructions = f"""You are an editor for a school end-term student profile.
{task}
Subject: {subject}.
{pronouns}
The first sentence MUST begin with the word STUDENT. Use STUDENT only in the first sentence; never repeat the student's name in later sentences.
Preserve all important teacher-selected strengths, areas for improvement, recommendations and subject-specific observations.
Do not invent facts, marks, achievements, weaknesses, topics or behaviour.
Do not add bullet points, headings or quotation marks.
Return ONLY the final profile.
The final profile MUST be between 366 and 390 characters inclusive, counting spaces and punctuation.
{target}"""
        try:
            response = client.responses.create(
                model=AI_MODEL,
                instructions=instructions,
                input=anonymized,
                reasoning={"effort": "low"},
                max_output_tokens=2000,
                store=False,
            )
            candidate = (getattr(response, "output_text", None) or "").strip()
            if not candidate:
                chunks = []
                for item in (getattr(response, "output", None) or []):
                    for content in (getattr(item, "content", None) or []):
                        text = getattr(content, "text", None)
                        if text:
                            chunks.append(text)
                candidate = "".join(chunks).strip()
            candidate = candidate.strip().strip("`").strip()
            candidate = re.sub(r"\bSTUDENT\b", first_name, candidate)
            n = len(candidate)
            if 366 <= n <= 390 and candidate.startswith(first_name):
                return candidate, n, "ai"
            last_error = f"AI returned {n} characters. The API responded, but the returned text did not meet the required length."
        except Exception as e:
            last_error = str(e)
    return None, None, last_error or "AI could not produce a valid profile."


def genderize(text, gender):
    g = str(gender).strip().lower()
    p = PRONOUNS.get(g, PRONOUNS["male"])
    s = text
    s = re.sub(r"\bhis\s*/\s*her\b", p["poss"], s, flags=re.I)
    s = re.sub(r"\bhe\s*/\s*she\b", p["subj"], s, flags=re.I)
    s = re.sub(r"\bhim\s*/\s*her\b", p["obj"], s, flags=re.I)
    s = re.sub(r"\bhis/her\b", p["poss"], s, flags=re.I)
    if p["obj"] == "him":
        s = re.sub(r"\bbenefit her\b", "benefit him", s, flags=re.I)
    s = re.sub(r"\bHe\b|\bShe\b", p["subj"], s)
    s = re.sub(r"\bHis\b|\bHer\b", p["poss"].capitalize(), s)
    s = re.sub(r"\bhe\b|\bshe\b", p["subj"].lower(), s)
    s = re.sub(r"\bhis\b|\bher\b", p["poss"], s)
    s = re.sub(r"\bhim\b", p["obj"], s)
    return s


def prepare(statement, name, gender, first_sentence=True):
    first_name = str(name).strip().split()[0] if str(name).strip() else "Student"
    p = PRONOUNS.get(str(gender).strip().lower(), PRONOUNS["male"])
    s = str(statement).strip()
    s = s.replace("----", first_name).replace("------", first_name).replace("{name}", first_name)
    s = re.sub(r"\bHe\b", p["subj"], s)
    s = re.sub(r"\bShe\b", p["subj"], s)
    s = re.sub(r"\bhe\b", p["subj"].lower(), s)
    s = re.sub(r"\bshe\b", p["subj"].lower(), s)
    s = re.sub(r"\bHim\b", p["obj"].capitalize(), s)
    s = re.sub(r"\bhim\b", p["obj"], s)
    s = re.sub(r"\bHer\b", p["poss"].capitalize(), s)
    s = re.sub(r"\bher\b", p["poss"], s)
    s = re.sub(r"\bHis\b", p["poss"].capitalize(), s)
    s = re.sub(r"\bhis\b", p["poss"], s)
    s = re.sub(r"\bhis\s*/\s*her\b", p["poss"], s, flags=re.I)

    if first_sentence:
        if re.match(r"^(He|She)\b", s):
            s = re.sub(r"^(He|She)\b", first_name, s, count=1)
        elif re.match(r"^(His|Her)\b", s):
            rest = re.sub(r"^(His|Her)\b\s*", "", s, count=1)
            s = first_name + "'s " + rest
        elif re.match(r"^(has|needs|can|is|shows|demonstrates|displays|recalls|requires|puts|makes|uses|comprehends|shirks|tends|must|should|solving|a regular|with the focus|analysis|diagram is|also|the laws|maps|economic diagrams|chemical structures)\b", s, re.I):
            s = first_name + " " + s[0].lower() + s[1:]
    else:
        if re.match(r"^(has|needs|can|is|shows|demonstrates|displays|recalls|requires|puts|makes|uses|comprehends|shirks|tends|must|should)\b", s, re.I):
            s = p["subj"] + " " + s[0].lower() + s[1:]
        elif s.startswith(("Solving ", "A regular ")):
            s = s.replace("would benefit her.", f"would benefit {p['obj']}.")
            s = s.replace("would benefit him.", f"would benefit {p['obj']}.")
            s = s.replace("will help him", f"will help {p['obj']}")
            s = s.replace("will help her", f"will help {p['obj']}")
        elif re.match(r"^Analysis\b", s):
            s = p["subj"] + "'s " + s[0].lower() + s[1:]
        elif re.match(r"^Diagram\b", s):
            s = p["subj"] + "'s " + s[0].lower() + s[1:]
    return s.strip()


def clean_join(parts):
    return " ".join(str(p).strip() for p in parts if str(p).strip())


def generate_profile(selected, all_statements, name, gender):
    items = []
    seen = set()
    for cat, indices in selected.items():
        for idx in indices:
            raw = all_statements[cat][idx]
            if raw not in seen:
                items.append((cat, idx, raw))
                seen.add(raw)
    rendered = [prepare(x[2], name, gender, first_sentence=(pos == 0)) for pos, x in enumerate(items)]
    text = clean_join(rendered)
    return text, len(text), "draft"


def read_class_list(uploaded):
    df = pd.read_excel(uploaded)
    df.columns = [str(c).strip() for c in df.columns]
    required = {"Name", "Gender"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError("Missing required column(s): " + ", ".join(sorted(missing)))
    df = df[["Name", "Gender"]].copy()
    df = df.dropna(subset=["Name"]).reset_index(drop=True)
    df["Name"] = df["Name"].astype(str).str.strip()
    df["Gender"] = df["Gender"].fillna("Male").astype(str).str.strip()
    return df


def make_output(rows):
    out = pd.DataFrame(rows)
    cols = ["Serial No.", "Name", "Gender", "Subject", "Profile", "Characters", "AI Edited"]
    return out[cols]


def excel_bytes(df):
    bio = BytesIO()
    with pd.ExcelWriter(bio, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Profiles")
        ws = writer.book["Profiles"]
        ws.freeze_panes = "A2"
        ws.auto_filter.ref = ws.dimensions
        widths = {"A": 12, "B": 24, "C": 14, "D": 24, "E": 100, "F": 12, "G": 12}
        for col, width in widths.items():
            ws.column_dimensions[col].width = width
    return bio.getvalue()


# -----------------------------------------------------------------------------
# Persistence helpers
# -----------------------------------------------------------------------------
def blank_workspace():
    return {"original": "", "ai": "", "selections": {}}


def serializable_state():
    df = st.session_state.students
    students = None if df is None else df.to_dict(orient="records")
    return {
        "version": 15,
        "students": students,
        "subject": st.session_state.subject,
        "current_index": int(st.session_state.student_index),
        "profiles": {str(k): v for k, v in st.session_state.profiles.items()},
        "workspaces": {str(k): v for k, v in st.session_state.workspaces.items()},
    }


def restore_state(raw):
    try:
        data = json.loads(raw)
        if not isinstance(data, dict) or data.get("version") != 15:
            return False
        students = data.get("students")
        if not students:
            return False
        df = pd.DataFrame(students)
        if not {"Name", "Gender"}.issubset(df.columns):
            return False
        st.session_state.students = df[["Name", "Gender"]].copy()
        st.session_state.subject = data.get("subject", SUBJECTS[0]) if data.get("subject") in SUBJECTS else SUBJECTS[0]
        max_i = len(df) - 1
        st.session_state.student_index = max(0, min(int(data.get("current_index", 0)), max_i))
        st.session_state.profiles = {int(k): v for k, v in (data.get("profiles") or {}).items()}
        st.session_state.workspaces = {int(k): v for k, v in (data.get("workspaces") or {}).items()}
        for i in range(len(df)):
            st.session_state.workspaces.setdefault(i, blank_workspace())
        st.session_state.stage = "profile"
        return True
    except Exception:
        return False


def request_save():
    st.session_state.pending_storage_save = True


def sync_current_workspace():
    """Capture current widget values before navigating to another child."""
    if st.session_state.stage != "profile" or st.session_state.students is None:
        return
    i = st.session_state.student_index
    subject = st.session_state.subject
    ws = st.session_state.workspaces.setdefault(i, blank_workspace())
    bank = BANKS[subject]
    sel = {}
    for cat, statements in bank.items():
        sel[cat] = []
        for idx in range(len(statements)):
            key = f"{subject}_{i}_{cat}_{idx}"
            if st.session_state.get(key, False):
                sel[cat].append(idx)
    ws["selections"] = sel
    original_key = f"original_profile_editor_{i}_{subject}"
    if original_key in st.session_state:
        ws["original"] = st.session_state[original_key]
    ai_key_prefix = f"ai_profile_editor_{i}_{subject}"
    for key, value in st.session_state.items():
        if key.startswith(ai_key_prefix):
            ws["ai"] = value
            break


def load_workspace(i):
    ws = st.session_state.workspaces.get(i, blank_workspace())
    st.session_state.profile_draft = ws.get("original", "")
    st.session_state.ai_profile = ws.get("ai", "")
    st.session_state.generated = bool(ws.get("original", "") or ws.get("ai", "") or any(ws.get("selections", {}).values()))
    st.session_state.draft_version += 1
    st.session_state.ai_profile_version += 1


# -----------------------------------------------------------------------------
# Session state and browser restore
# -----------------------------------------------------------------------------
if "hydrated" not in st.session_state:
    st.session_state.hydrated = False
if not st.session_state.hydrated:
    stored = storage_load()
    if isinstance(stored, str) and stored.startswith("__ERROR__"):
        st.session_state.hydrated = True
    elif isinstance(stored, str) and stored:
        if restore_state(stored):
            st.session_state.restored_from_browser = True
        st.session_state.hydrated = True
    elif stored == "":
        st.session_state.hydrated = True

if "stage" not in st.session_state:
    st.session_state.stage = "upload"
if "students" not in st.session_state:
    st.session_state.students = None
if "student_index" not in st.session_state:
    st.session_state.student_index = 0
if "subject" not in st.session_state:
    st.session_state.subject = SUBJECTS[0]
if "profiles" not in st.session_state:
    st.session_state.profiles = {}
if "workspaces" not in st.session_state:
    st.session_state.workspaces = {}
if "generated" not in st.session_state:
    st.session_state.generated = None
if "profile_draft" not in st.session_state:
    st.session_state.profile_draft = ""
if "draft_version" not in st.session_state:
    st.session_state.draft_version = 0
if "ai_profile" not in st.session_state:
    st.session_state.ai_profile = ""
if "ai_profile_version" not in st.session_state:
    st.session_state.ai_profile_version = 0
if "pending_storage_save" not in st.session_state:
    st.session_state.pending_storage_save = False
if "restored_from_browser" not in st.session_state:
    st.session_state.restored_from_browser = False

# -----------------------------------------------------------------------------
# Header/sidebar
# -----------------------------------------------------------------------------
st.title("📝 Student Profile Generator")
st.caption("Built-in statement banks • AI is used only when you explicitly click Adjust or Refine • Every final profile: 366–390 characters")

st.sidebar.header("Children")

if st.session_state.students is not None and st.session_state.stage in ("profile", "finish"):
    df_sidebar = st.session_state.students
    completed = len(st.session_state.profiles)
    st.sidebar.caption(f"{completed} of {len(df_sidebar)} profiles saved")
    for idx, row in df_sidebar.iterrows():
        mark = "✓" if idx in st.session_state.profiles else "○"
        label = f"{mark} {idx + 1}. {row['Name']}"
        if st.sidebar.button(label, key=f"nav_child_{idx}", use_container_width=True):
            if idx != st.session_state.student_index:
                sync_current_workspace()
                st.session_state.student_index = int(idx)
                load_workspace(int(idx))
                request_save()
                st.session_state.stage = "profile"
                st.rerun()
    st.sidebar.divider()
    st.sidebar.write(f"**Subject:** {st.session_state.subject}")
    if st.sidebar.button("🆕 Start a new class / subject", use_container_width=True):
        storage_clear()
        for key in ["students", "profiles", "workspaces", "generated", "profile_draft", "ai_profile"]:
            st.session_state[key] = None if key == "students" else ({} if key in ["profiles", "workspaces"] else ("" if key in ["profile_draft", "ai_profile"] else None))
        st.session_state.stage = "upload"
        st.session_state.student_index = 0
        st.session_state.subject = SUBJECTS[0]
        st.session_state.pending_storage_save = False
        st.session_state.restored_from_browser = False
        st.rerun()
else:
    st.sidebar.info("Upload a class list to begin. Your class and saved progress will be remembered in this browser.")

if st.session_state.restored_from_browser:
    st.info("↩️ Your previous class and saved progress were restored from this browser. You can continue with any child.")
    st.session_state.restored_from_browser = False

# -----------------------------------------------------------------------------
# Pages
# -----------------------------------------------------------------------------
if st.session_state.stage == "upload":
    st.subheader("1. Upload class list")
    st.write("Upload an Excel file containing at least two columns: **Name** and **Gender**.")
    uploaded = st.file_uploader("Class list (.xlsx)", type=["xlsx"])
    if uploaded:
        try:
            df = read_class_list(uploaded)
            st.success(f"{len(df)} students loaded.")
            st.dataframe(df, use_container_width=True, hide_index=True)
            if st.button("Next →", type="primary"):
                st.session_state.students = df
                st.session_state.profiles = {}
                st.session_state.workspaces = {i: blank_workspace() for i in range(len(df))}
                st.session_state.student_index = 0
                st.session_state.generated = None
                st.session_state.profile_draft = ""
                st.session_state.ai_profile = ""
                st.session_state.stage = "subject"
                request_save()
                st.rerun()
        except Exception as e:
            st.error(str(e))

elif st.session_state.stage == "subject":
    st.subheader("2. Select subject")
    st.session_state.subject = st.selectbox("Subject", SUBJECTS, index=SUBJECTS.index(st.session_state.subject))
    st.info("The statement bank for the selected subject is built into the application.")
    c1, c2 = st.columns([1, 5])
    with c1:
        if st.button("← Back"):
            st.session_state.stage = "upload"
            st.rerun()
    with c2:
        if st.button("Start profiles →", type="primary"):
            st.session_state.student_index = 0
            st.session_state.generated = None
            st.session_state.profile_draft = ""
            st.session_state.ai_profile = ""
            st.session_state.workspaces = {i: blank_workspace() for i in range(len(st.session_state.students))}
            st.session_state.stage = "profile"
            request_save()
            st.rerun()

elif st.session_state.stage == "profile":
    df = st.session_state.students
    subject = st.session_state.subject
    i = st.session_state.student_index
    row = df.iloc[i]
    name, gender = row["Name"], row["Gender"]
    bank = BANKS[subject]
    ws = st.session_state.workspaces.setdefault(i, blank_workspace())

    st.subheader(f"3. Create profile — {i + 1} of {len(df)}")
    st.markdown(f"### {name}")
    st.write(f"**Gender:** {gender}  |  **Subject:** {subject}")

    if i in st.session_state.profiles:
        st.success("✓ A final profile has already been saved for this student. You may edit it and save again.")

    selections = {}
    saved_sel = ws.get("selections", {})
    for cat, statements in bank.items():
        with st.expander(cat, expanded=True):
            picks = []
            for idx, statement in enumerate(statements):
                label = prepare(statement, name, gender, first_sentence=False)
                default_checked = idx in saved_sel.get(cat, [])
                key = f"{subject}_{i}_{cat}_{idx}"
                if key not in st.session_state:
                    st.session_state[key] = default_checked
                if st.checkbox(label, key=key):
                    picks.append(idx)
            selections[cat] = picks
    ws["selections"] = selections

    if st.button("Generate Profile", type="primary", use_container_width=True):
        profile, count, status = generate_profile(selections, bank, name, gender)
        st.session_state.profile_draft = profile
        st.session_state.ai_profile = ""
        ws["original"] = profile
        ws["ai"] = ""
        ws["selections"] = selections
        st.session_state.draft_version += 1
        st.session_state.ai_profile_version += 1
        st.session_state.generated = True
        request_save()
        st.rerun()

    if st.session_state.generated:
        st.markdown("#### Original profile")
        original_key = f"original_profile_editor_{i}_{subject}"
        if original_key not in st.session_state:
            st.session_state[original_key] = ws.get("original", st.session_state.profile_draft)
        original_draft = st.text_area("Original profile (editable)", height=190, key=original_key)
        st.session_state.profile_draft = original_draft
        ws["original"] = original_draft
        original_count = len(original_draft)
        ai_exists = bool(st.session_state.get("ai_profile", ""))
        st.write(f"**Character count: {original_count}** (required: 366–390)  |  **AI editing used:** {'Yes' if ai_exists else 'No'}")

        c1, c2 = st.columns(2)
        with c1:
            if st.button("✂️ Adjust to 366–390 characters", use_container_width=True):
                with st.spinner("AI is adjusting the profile to 366–390 characters…"):
                    ai_profile, ai_count, ai_status = ai_edit_profile(original_draft, subject, name, gender, mode="adjust")
                if ai_status == "ai":
                    st.session_state.ai_profile = ai_profile
                    ws["ai"] = ai_profile
                    st.session_state.ai_profile_version += 1
                    request_save()
                    st.rerun()
                elif ai_status == "no_api_key":
                    st.error("AI is not configured. Add OPENAI_API_KEY in Streamlit Secrets.")
                else:
                    st.error(f"AI could not produce a valid 366–390 character profile. {ai_status}")
        with c2:
            if st.button("✨ Refine with AI", use_container_width=True):
                refine_source = st.session_state.get("ai_profile", "") or original_draft
                with st.spinner("AI is refining the profile…"):
                    ai_profile, ai_count, ai_status = ai_edit_profile(refine_source, subject, name, gender, mode="refine")
                if ai_status == "ai":
                    st.session_state.ai_profile = ai_profile
                    ws["ai"] = ai_profile
                    st.session_state.ai_profile_version += 1
                    request_save()
                    st.rerun()
                elif ai_status == "no_api_key":
                    st.error("AI is not configured. Add OPENAI_API_KEY in Streamlit Secrets.")
                else:
                    st.error(f"AI could not produce a valid 366–390 character profile. {ai_status}")

        ai_profile = st.session_state.get("ai_profile", "")
        if ai_profile:
            st.markdown("#### AI-adjusted / refined profile")
            ai_key = f"ai_profile_editor_{i}_{subject}_{st.session_state.ai_profile_version}"
            if ai_key not in st.session_state:
                st.session_state[ai_key] = ai_profile
            edited_ai_profile = st.text_area("AI version (editable)", height=190, key=ai_key)
            st.session_state.ai_profile = edited_ai_profile
            ws["ai"] = edited_ai_profile
            ai_count_current = len(edited_ai_profile)
            st.write(f"**Character count: {ai_count_current}** (required: 366–390)  |  **AI editing used:** Yes")
            if 366 <= ai_count_current <= 390:
                st.success("✓ AI version meets the 366–390 character requirement and can be saved.")
            elif ai_count_current > 390:
                st.warning("The AI version is over 390 characters. You can edit it manually or click Adjust again.")
            else:
                st.warning("The AI version is below 366 characters. You can edit it manually or click Adjust again.")

        final_profile = st.session_state.get("ai_profile", "") or original_draft
        final_count = len(final_profile)
        if 366 <= final_count <= 390:
            st.success("✓ Length requirement satisfied. You can save this profile or refine it with AI.")
            if st.button("Save Profile", type="primary", use_container_width=True):
                st.session_state.profiles[i] = {
                    "Name": name, "Gender": gender, "Subject": subject,
                    "Profile": final_profile, "Characters": final_count,
                    "AI Edited": "Yes" if bool(st.session_state.get("ai_profile", "")) else "No"
                }
                ws["original"] = original_draft
                ws["ai"] = st.session_state.get("ai_profile", "")
                ws["selections"] = selections
                request_save()
                st.success("Profile saved. You can now choose any child from the left navigation.")
        else:
            if final_count > 390:
                st.warning("The profile selected for saving is over 390 characters. Click **Adjust to 366–390 characters** or edit the profile.")
            elif final_count > 0:
                st.warning("The profile selected for saving is below 366 characters. Click **Adjust to 366–390 characters** or edit the profile.")
            else:
                st.warning("No profile text is present. Select statements and click Generate Profile first.")

elif st.session_state.stage == "finish":
    st.session_state.stage = "profile"
    st.rerun()

# Save browser state after all normal UI logic has updated it.
if st.session_state.pending_storage_save:
    payload = serializable_state()
    result = storage_save(payload)
    st.session_state.pending_storage_save = False

st.divider()
st.caption("Profiles are stored locally in this browser for resume purposes. They are not written to GitHub. AI is optional and is used only when you explicitly ask it to adjust or refine a profile.")
