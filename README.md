
# Student Profile Generator — 11 Subjects

A non-AI Streamlit application for generating end-term student profiles.

## Subjects
Physics, Biology, Chemistry, Mathematics, English Language, English Literature,
Computer Science, History and Civics, Geography, Physical Education, Economics.

## Teacher workflow
1. Upload an Excel class list containing `Name` and `Gender`.
2. Select the subject.
3. For each student, tick the statements that apply.
4. Click **Generate Profile**.
5. The app builds a deterministic profile using the built-in statement bank.
6. The profile must be between 366 and 390 characters inclusive.
7. Click **Save & Next Child**.
8. Download the completed Excel file at the end.

No API key or AI service is used.

## GitHub / Streamlit Community Cloud
Upload `app.py`, `statement_banks.py`, and `requirements.txt` to your GitHub repository.
Then deploy `app.py` on Streamlit Community Cloud.

## Class list format
The uploaded Excel file needs these columns:
- Name
- Gender

Other columns are ignored.
