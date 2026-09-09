
import streamlit as st
import re
import pandas as pd
from io import BytesIO
from statement_banks import BANKS, SUBJECTS, PRONOUNS

st.set_page_config(page_title="Student Profile Generator", page_icon="📝", layout="wide")


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

def prepare(statement, name, gender):
    # Use only the student's first name throughout the interface and profile.
    first_name = str(name).strip().split()[0] if str(name).strip() else "Student"

    s = genderize(statement, gender)
    s = s.replace("----", first_name).replace("------", first_name)
    s = s.replace("{name}", first_name)

    # Convert source statements into complete, student-specific sentences.
    # This keeps the original wording as much as possible while avoiding
    # abrupt fragments in the checkbox list and generated profile.
    s = re.sub(r"^He\s+", first_name + " ", s)
    s = re.sub(r"^She\s+", first_name + " ", s)
    s = re.sub(r"^His\s+", first_name + "'s ", s)
    s = re.sub(r"^Her\s+", first_name + "'s ", s)

    # Common fragments from the supplied Physics bank and the built-in banks.
    fragment_prefixes = (
        "has ", "needs ", "can ", "is ", "shows ", "demonstrates ",
        "displays ", "recalls ", "requires ", "puts ", "makes ",
        "uses ", "comprehends ", "shirks ", "tends ", "must ",
        "should ", "solving ", "a regular ", "with the focus ",
        "analysis ", "diagram is ", "the concepts ", "also ",
        "the laws ", "maps ", "economic diagrams ", "chemical structures "
    )
    lower = s.lower()
    if lower.startswith(fragment_prefixes):
        s = first_name + " " + s[0].lower() + s[1:]

    # Statements beginning with a gerund are made complete where needed.
    if s.startswith("Solving ") and "would benefit " in s:
        s = s.replace("would benefit her.", f"would benefit {first_name}.")
        s = s.replace("would benefit him.", f"would benefit {first_name}.")
    if s.startswith("A regular ") and "will help him" in s:
        s = s.replace("will help him", f"will help {first_name}")
    if s.startswith("A regular ") and "will help her" in s:
        s = s.replace("will help her", f"will help {first_name}")

    return s.strip()

def clean_join(parts):
    out = []
    for s in parts:
        s = s.strip()
        if not s:
            continue
        if out:
            # Avoid accidental double punctuation.
            if out[-1][-1] in ".!?":
                out.append(s[0].upper() + s[1:] if s else s)
            else:
                out.append(s)
        else:
            out.append(s)
    return " ".join(out)

def generate_profile(selected, all_statements, name, gender):
    """Deterministically build a 366–390 character profile.

    Selected statements are always preferred. If they are too short, the
    application adds the best-fitting approved bank statements. It searches
    combinations rather than padding with invented text.
    """
    selected_items = []
    for cat, statements in selected.items():
        for idx in statements:
            raw = all_statements[cat][idx]
            selected_items.append((cat, idx, prepare(raw, name, gender)))

    # De-duplicate exact text while retaining category information.
    seen = set()
    selected_items = [x for x in selected_items
                      if not (x[2] in seen or seen.add(x[2]))]

    # If the teacher's choices are already too long, do not silently alter them.
    selected_text = clean_join([x[2] for x in selected_items])
    if len(selected_text) > 390:
        return None, len(selected_text), "too_long"

    # Prefer the teacher's selected statements, then add approved statements
    # from unselected categories/statements until the profile fits.
    candidates = []
    selected_keys = {(c, i) for c, i, _ in selected_items}
    for cat, statements in all_statements.items():
        for idx, raw in enumerate(statements):
            if (cat, idx) in selected_keys:
                continue
            candidates.append((cat, idx, prepare(raw, name, gender)))

    # Score additions: prioritize categories not already represented, then
    # favor shorter additions so the 366–390 window is easier to hit.
    represented = {c for c, _, _ in selected_items}
    candidates.sort(key=lambda x: (x[0] in represented, len(x[2])))

    best = None
    # Exact search is feasible because each category has a modest bank.
    # First try subsets up to 4 additions; then a bounded greedy fallback.
    from itertools import combinations
    max_r = min(4, len(candidates))
    for r in range(0, max_r + 1):
        for combo in combinations(candidates, r):
            parts = [x[2] for x in selected_items] + [x[2] for x in combo]
            text = clean_join(parts)
            n = len(text)
            if 366 <= n <= 390:
                # Prefer fewer additions and more category diversity.
                cats = [x[0] for x in combo]
                score = (r, len(set(cats)), abs(378 - n))
                if best is None or score < best[0]:
                    best = (score, text)
        if best is not None:
            break

    if best:
        return best[1], len(best[1]), "ok"

    # Greedy fallback, useful for very short selections.
    text = selected_text
    remaining = candidates[:]
    while remaining and len(text) < 366:
        feasible = []
        for c in remaining:
            candidate_text = clean_join([text, c[2]])
            if len(candidate_text) <= 390:
                feasible.append((abs(378-len(candidate_text)), c, candidate_text))
        if not feasible:
            break
        _, chosen, text = min(feasible, key=lambda x: x[0])
        remaining.remove(chosen)

    if 366 <= len(text) <= 390:
        return text, len(text), "ok"
    return text, len(text), "too_short"

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
    cols = ["Serial No.", "Name", "Gender", "Subject", "Profile", "Characters"]
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
st.caption("Non-AI • No API key • Built-in subject-specific statements • Every final profile: 366–390 characters")

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
                label = prepare(statement, name, gender)
                if st.checkbox(label, key=f"{subject}_{i}_{cat}_{idx}"):
                    picks.append(idx)
            selections[cat] = picks

    if st.button("Generate Profile", type="primary", use_container_width=True):
        profile, count, status = generate_profile(selections, bank, name, gender)
        st.session_state.generated = (profile, count, status, selections)
        st.session_state[f"profile_output_{i}_{subject}"] = profile or ""
        if status == "ok":
            st.success(f"Profile generated: {count} characters.")
        elif status == "too_long":
            st.error(f"Selected statements are {count} characters. Deselect one or more statements to bring the profile to 390 characters or less.")
        else:
            st.warning(f"The selected statements total {count} characters. The app could not reach 366 characters using the available approved statements. Select a few more statements.")

    if st.session_state.generated:
        profile, count, status, selections = st.session_state.generated
        st.markdown("#### Generated profile")
        st.session_state[f"profile_output_{i}_{subject}"] = profile or ""
        st.text_area(
            "Profile",
            value=st.session_state[f"profile_output_{i}_{subject}"],
            height=170,
            key=f"profile_box_{i}_{subject}",
            disabled=True
        )
        st.write(f"**Character count: {count}** (required: 366–390)")
        if status == "ok":
            st.success("✓ Length requirement satisfied.")
            if st.button("Save & Next Child →", type="primary", use_container_width=True):
                st.session_state.profiles[i] = {
                    "Name": name, "Gender": gender, "Subject": subject,
                    "Profile": profile, "Characters": count
                }
                if i + 1 < len(df):
                    st.session_state.student_index += 1
                    st.session_state.generated = None
                    st.rerun()
                else:
                    st.session_state.stage = "finish"
                    st.session_state.generated = None
                    st.rerun()

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
                "Characters": p["Characters"]
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
        for key in ["students", "profiles", "generated"]:
            st.session_state[key] = None if key == "students" else {}
        st.session_state.stage = "upload"
        st.session_state.student_index = 0
        st.rerun()

st.divider()
st.caption("Profiles are generated deterministically from the built-in subject statement banks. No student data is sent to an AI service.")
