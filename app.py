
import streamlit as st
import re
import pandas as pd
from openai import OpenAI
from io import BytesIO
from statement_banks import BANKS, SUBJECTS, PRONOUNS

st.set_page_config(page_title="Student Profile Generator", page_icon="📝", layout="wide")

AI_MODEL = "gpt-5.6-luna"

def get_openai_client():
    try:
        api_key = st.secrets.get("OPENAI_API_KEY")
    except Exception:
        api_key = None
    return OpenAI(api_key=api_key) if api_key else None

def ai_edit_profile(profile, subject, name, gender, mode="adjust", max_attempts=5):
    """Use AI to adjust/refine any profile into 366–390 characters.

    The student's real first name is anonymised before the API call.
    mode="adjust" focuses on length; mode="refine" also improves flow/grammar.
    """
    client = get_openai_client()
    if client is None:
        return None, None, "no_api_key"

    first_name = str(name).strip().split()[0] if str(name).strip() else "Student"
    # Replace only the exact first-name word, case-insensitively.
    anonymized = re.sub(rf"\b{re.escape(first_name)}\b", "STUDENT", str(profile), flags=re.I)
    p = PRONOUNS.get(str(gender).strip().lower(), PRONOUNS["male"])
    pronouns = f"Use {p['subj']}/{p['obj']}/{p['poss']} correctly after the first sentence."

    if mode == "refine":
        task = "Improve grammar, flow, coherence and professional school-report wording while preserving the teacher's meaning and observations."
    else:
        task = "Adjust the profile to the required character range while preserving the teacher's meaning and observations."

    last_error = ""
    for attempt in range(max_attempts):
        target = "Aim for 375–385 characters." if attempt == 0 else "The previous attempt missed the limit. MUST be 366–390 characters inclusive; aim for about 378 characters."
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
            # Robust fallback for SDK/API responses where output_text is empty.
            if not candidate:
                chunks = []
                for item in (getattr(response, "output", None) or []):
                    for content in (getattr(item, "content", None) or []):
                        text = getattr(content, "text", None)
                        if text:
                            chunks.append(text)
                candidate = "".join(chunks).strip()
            candidate = candidate.strip().strip('`').strip()
            candidate = re.sub(r"\bSTUDENT\b", first_name, candidate)
            n = len(candidate)
            if 366 <= n <= 390 and candidate.startswith(first_name):
                return candidate, n, "ai"
            last_error = f"AI returned {n} characters. The API responded, but the returned text did not meet the required length."
        except Exception as e:
            last_error = str(e)
    return None, None, last_error or "AI could not produce a valid profile."


def genderize(text, gender):
    """Convert the bank's gendered wording to the student's gender.

    The source bank contains a mixture of He/She and his/her wording.
    This normalises those forms before the statement is displayed/generated.
    """
    g = str(gender).strip().lower()
    p = PRONOUNS.get(g, PRONOUNS["male"])
    s = text

    # Mixed forms used in the Physics source document.
    s = re.sub(r"\bhis\s*/\s*her\b", p["poss"], s, flags=re.I)
    s = re.sub(r"\bhe\s*/\s*she\b", p["subj"], s, flags=re.I)
    s = re.sub(r"\bhim\s*/\s*her\b", p["obj"], s, flags=re.I)
    s = re.sub(r"\bhis/her\b", p["poss"], s, flags=re.I)

    # Context-sensitive object pronoun before the general possessive rule.
    if p["obj"] == "him":
        s = re.sub(r"\bbenefit her\b", "benefit him", s, flags=re.I)

    # Whole-word replacements. Order matters.
    s = re.sub(r"\bHe\b|\bShe\b", p["subj"], s)
    s = re.sub(r"\bHis\b|\bHer\b", p["poss"].capitalize(), s)
    s = re.sub(r"\bhe\b|\bshe\b", p["subj"].lower(), s)
    s = re.sub(r"\bhis\b|\bher\b", p["poss"], s)
    s = re.sub(r"\bhim\b", p["obj"], s)
    return s

def prepare(statement, name, gender, first_sentence=True):
    first_name = str(name).strip().split()[0] if str(name).strip() else 'Student'
    p = PRONOUNS.get(str(gender).strip().lower(), PRONOUNS['male'])
    s = str(statement).strip()
    s = s.replace('----', first_name).replace('------', first_name).replace('{name}', first_name)

    # Replace whole words only. Never replace the substring "he" inside words
    # such as "The" or "these".
    s = re.sub(r'\bHe\b', p['subj'], s)
    s = re.sub(r'\bShe\b', p['subj'], s)
    s = re.sub(r'\bhe\b', p['subj'].lower(), s)
    s = re.sub(r'\bshe\b', p['subj'].lower(), s)
    s = re.sub(r'\bHim\b', p['obj'].capitalize(), s)
    s = re.sub(r'\bhim\b', p['obj'], s)
    s = re.sub(r'\bHer\b', p['poss'].capitalize(), s)
    s = re.sub(r'\bher\b', p['poss'], s)
    s = re.sub(r'\bHis\b', p['poss'].capitalize(), s)
    s = re.sub(r'\bhis\b', p['poss'], s)
    s = re.sub(r'\bhis\s*/\s*her\b', p['poss'], s, flags=re.I)

    if first_sentence:
        # First sentence begins with the child's first name.
        if re.match(r'^(He|She)\b', s):
            s = re.sub(r'^(He|She)\b', first_name, s, count=1)
        elif re.match(r'^(His|Her)\b', s):
            rest = re.sub(r'^(His|Her)\b\s*', '', s, count=1)
            s = first_name + "'s " + rest
        elif re.match(r'^(has|needs|can|is|shows|demonstrates|displays|recalls|requires|puts|makes|uses|comprehends|shirks|tends|must|should|solving|a regular|with the focus|analysis|diagram is|also|the laws|maps|economic diagrams|chemical structures)\b', s, re.I):
            s = first_name + ' ' + s[0].lower() + s[1:]
    else:
        # Subsequent sentences use He/She rather than repeating the name.
        if re.match(r'^(has|needs|can|is|shows|demonstrates|displays|recalls|requires|puts|makes|uses|comprehends|shirks|tends|must|should)\b', s, re.I):
            s = p['subj'] + ' ' + s[0].lower() + s[1:]
        elif s.startswith(('Solving ', 'A regular ')):
            s = s.replace('would benefit her.', f"would benefit {p['obj']}.")
            s = s.replace('would benefit him.', f"would benefit {p['obj']}.")
            s = s.replace('will help him', f"will help {p['obj']}")
            s = s.replace('will help her', f"will help {p['obj']}")
        elif re.match(r'^Analysis\b', s):
            s = p['subj'] + "'s " + s[0].lower() + s[1:]
        elif re.match(r'^Diagram\b', s):
            s = p['subj'] + "'s " + s[0].lower() + s[1:]
    return s.strip()

def clean_join(parts):
    """Join profile sentences cleanly without changing their wording."""
    return " ".join(str(p).strip() for p in parts if str(p).strip())

def render_items(items, name, gender):
    rendered = []
    for pos, item in enumerate(items):
        rendered.append(prepare(item[2], name, gender, first_sentence=(pos == 0)))
    return rendered

def generate_profile(selected, all_statements, name, gender):
    """Create the teacher-selected draft without enforcing the length.

    The teacher sees exactly what was selected first. AI adjustment/refinement
    is a separate, explicit action.
    """
    items=[]
    seen=set()
    for cat, indices in selected.items():
        for idx in indices:
            raw=all_statements[cat][idx]
            if raw not in seen:
                items.append((cat, idx, raw))
                seen.add(raw)
    text=clean_join(render_items(items, name, gender))
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
        widths = {"A":12, "B":24, "C":14, "D":24, "E":100, "F":12}
        for col, width in widths.items():
            ws.column_dimensions[col].width = width
    return bio.getvalue()

st.title("📝 Student Profile Generator")
st.caption("Built-in statement banks • AI used only when a selected profile exceeds 390 characters • Every final profile: 366–390 characters")

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
if "generated" not in st.session_state:
    st.session_state.generated = None
if "profile_draft" not in st.session_state:
    st.session_state.profile_draft = ""

st.sidebar.header("Profile settings")
use_ai = st.sidebar.checkbox(
    "Use AI if profile exceeds 390 characters",
    value=True,
    help="AI is used only when the deterministic profile is over 390 characters. The student's first name is anonymised before the API call."
)

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
                st.session_state.stage = "subject"
                st.rerun()
        except Exception as e:
            st.error(str(e))

elif st.session_state.stage == "subject":
    st.subheader("2. Select subject")
    st.session_state.subject = st.selectbox(
        "Subject", SUBJECTS, index=SUBJECTS.index(st.session_state.subject)
    )
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
            st.session_state.stage = "profile"
            st.rerun()

elif st.session_state.stage == "profile":
    df = st.session_state.students
    subject = st.session_state.subject
    i = st.session_state.student_index
    row = df.iloc[i]
    name, gender = row["Name"], row["Gender"]
    bank = BANKS[subject]

    st.subheader(f"3. Create profile — {i+1} of {len(df)}")
    st.markdown(f"### {name}")
    st.write(f"**Gender:** {gender}  |  **Subject:** {subject}")

    saved = st.session_state.profiles.get(i)
    if saved:
        st.success("A profile has already been saved for this student. You may edit the selections and regenerate it.")

    selections = {}
    for cat, statements in bank.items():
        with st.expander(cat, expanded=True):
            picks = []
            for idx, statement in enumerate(statements):
                # Show pronouns in the checkbox list rather than repeating the student's name.
                label = prepare(statement, name, gender, first_sentence=False)
                if st.checkbox(label, key=f"{subject}_{i}_{cat}_{idx}"):
                    picks.append(idx)
            selections[cat] = picks

    if st.button("Generate Profile", type="primary", use_container_width=True):
        profile, count, status = generate_profile(selections, bank, name, gender)
        st.session_state.profile_draft = profile
        st.session_state.generated = (profile, count, status, selections, False)

    if st.session_state.generated:
        profile, count, status, selections, ai_used = st.session_state.generated
        st.markdown("#### Generated profile")

        # Editable draft: the teacher can make manual changes before asking AI
        # to refine the wording.
        draft = st.text_area(
            "Profile",
            value=st.session_state.profile_draft,
            height=190,
            key=f"profile_editor_{i}_{subject}"
        )
        st.session_state.profile_draft = draft
        current_count = len(draft)
        st.write(f"**Character count: {current_count}** (required: 366–390)  |  **AI editing used:** {'Yes' if ai_used else 'No'}")

        c1, c2 = st.columns(2)
        with c1:
            if st.button("✂️ Adjust to 366–390 characters", use_container_width=True):
                with st.spinner("AI is adjusting the profile to 366–390 characters…"):
                    ai_profile, ai_count, ai_status = ai_edit_profile(draft, subject, name, gender, mode="adjust")
                if ai_status == "ai":
                    st.session_state.profile_draft = ai_profile
                    st.session_state.generated = (ai_profile, ai_count, "ok", selections, True)
                    st.rerun()
                elif ai_status == "no_api_key":
                    st.error("AI is not configured. Add OPENAI_API_KEY in Streamlit Secrets.")
                else:
                    st.error(f"AI could not produce a valid 366–390 character profile. {ai_status}")
        with c2:
            if st.button("✨ Refine with AI", use_container_width=True):
                with st.spinner("AI is refining the profile…"):
                    ai_profile, ai_count, ai_status = ai_edit_profile(draft, subject, name, gender, mode="refine")
                if ai_status == "ai":
                    st.session_state.profile_draft = ai_profile
                    st.session_state.generated = (ai_profile, ai_count, "ok", selections, True)
                    st.rerun()
                elif ai_status == "no_api_key":
                    st.error("AI is not configured. Add OPENAI_API_KEY in Streamlit Secrets.")
                else:
                    st.error(f"AI could not produce a valid 366–390 character profile. {ai_status}")

        if 366 <= current_count <= 390:
            st.success("✓ Length requirement satisfied. You can save this profile or refine it with AI.")
            if st.button("Save & Next Child →", type="primary", use_container_width=True):
                st.session_state.profiles[i] = {
                    "Name": name, "Gender": gender, "Subject": subject,
                    "Profile": draft, "Characters": current_count,
                    "AI Edited": "Yes" if ai_used else "No"
                }
                if i + 1 < len(df):
                    st.session_state.student_index += 1
                    st.session_state.generated = None
                    st.session_state.profile_draft = ""
                    st.rerun()
                else:
                    st.session_state.stage = "finish"
                    st.session_state.generated = None
                    st.session_state.profile_draft = ""
                    st.rerun()
        else:
            if current_count > 390:
                st.warning("This profile is over 390 characters. Click **Adjust to 366–390 characters** to have AI shorten it.")
            elif current_count > 0:
                st.warning("This profile is below 366 characters. Click **Adjust to 366–390 characters** to have AI adjust it to the required range.")
            else:
                st.warning("No profile text is present. Select statements and click Generate Profile first.")

elif st.session_state.stage == "finish":
    st.subheader("4. Profiles complete")
    rows = []
    for i, row in st.session_state.students.iterrows():
        if i in st.session_state.profiles:
            p = st.session_state.profiles[i]
            rows.append({
                "Serial No.": i + 1,
                "Name": p["Name"],
                "Gender": p["Gender"],
                "Subject": p["Subject"],
                "Profile": p["Profile"],
                "Characters": p["Characters"],
                "AI Edited": p.get("AI Edited", "No")
            })
    result = make_output(rows)
    st.success(f"{len(result)} profile(s) completed.")
    st.dataframe(result, use_container_width=True, hide_index=True)
    st.download_button(
        "⬇️ Download Profiles Excel",
        data=excel_bytes(result),
        file_name=f"{st.session_state.subject.replace(' ', '_')}_Student_Profiles.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        type="primary",
        use_container_width=True
    )
    if st.button("Start a new class / subject"):
        for key in ["students", "profiles", "generated", "profile_draft"]:
            st.session_state[key] = None if key == "students" else {}
        st.session_state.stage = "upload"
        st.session_state.student_index = 0
        st.rerun()

st.divider()
st.caption("Profiles are generated from built-in statement banks. AI is optional and is used only when you explicitly ask it to adjust or refine a profile.")
