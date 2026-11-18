"""streamlit_app.py — main UI"""

import json, time, os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
from prompt_builder import SYSTEM_PROMPT, build_user_message
from validator import validate_response, SymptomSummary
from pydantic import ValidationError

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Colour scheme for each triage level — icon, background colour, text colour
TRIAGE_COLOURS = {
    "low":      ("🟢", "#d4edda", "#155724"),
    "moderate": ("🟡", "#fff3cd", "#856404"),
    "high":     ("🔴", "#f8d7da", "#721c24"),
}
MAX_RETRIES = 3
def call_api(symptom_text: str) -> SymptomSummary:
    """Call GPT-4o with automatic retry on failure."""
    user_msg = build_user_message(symptom_text)

    for attempt in range(MAX_RETRIES):
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_msg},
                ],
                temperature=0.2,
            )
            raw = json.loads(response.choices[0].message.content)
            return validate_response(raw)

        except ValidationError as e:
            if attempt == MAX_RETRIES - 1:
                raise
            time.sleep(2 ** attempt)

        except Exception as e:
            if attempt == MAX_RETRIES - 1:
                raise
            time.sleep(2 ** attempt)




# Configure the webpage
st.set_page_config(
    page_title="Medical Symptom Summarizer",
    page_icon="🏥",
    layout="wide"
)

st.title("🏥 Medical Symptom Summarizer")

# Important disclaimer — always shown at the top
st.warning(
    "⚠️ **Disclaimer:** This tool does not provide medical advice or diagnosis. "
    "All outputs require clinical judgment by a qualified professional."
)

# Two-column layout: input on left, output on right
col_input, col_output = st.columns([1, 1], gap="large")

with col_input:
    st.subheader("Patient Symptom Description")

    symptom_text = st.text_area(
        label="Paste or type the patient's description",
        height=250,
        placeholder="e.g. I've had a severe headache for 2 days, pain is 8/10...",
    )

    submitted = st.button(
        "🔍 Summarise",
        type="primary",
        use_container_width=True
    )

    # Keep a session history of the last 5 summaries
    if "history" not in st.session_state:
        st.session_state.history = []

    if st.session_state.history:
        st.markdown("---")
        st.caption("Recent summaries (this session)")

        for item in reversed(st.session_state.history[-5:]):
            st.caption(
                f"• {item['chief_complaint']} — "
                f"**{item['triage_level'].upper()}**"
            )


with col_output:
    st.subheader("Structured Summary")

    if submitted:
        if not symptom_text.strip():
            st.error("Please enter a symptom description.")

        elif len(symptom_text.strip().split()) < 5:
            st.warning("Description is very short. Please provide more detail.")

        else:
            with st.spinner("Analysing symptoms..."):
                try:
                    result = call_api(symptom_text)

                    # Render triage badge with colour
                    icon, bg, fg = TRIAGE_COLOURS[result.triage_level]

                    st.markdown(
                        f"""<div style='background:{bg};color:{fg};padding:12px 18px;
                        border-radius:8px;font-weight:bold;font-size:1.1rem;margin-bottom:16px'>
                        {icon} Triage Level: {result.triage_level.upper()}</div>""",
                        unsafe_allow_html=True,
                    )

                    # Display each field
                    st.markdown(f"**Chief Complaint:** {result.chief_complaint}")
                    st.markdown(f"**Onset:** {result.onset or 'Not mentioned'}")
                    st.markdown(f"**Duration:** {result.duration or 'Not mentioned'}")
                    st.markdown(f"**Severity:** {result.severity or 'Not mentioned'}/10")

                    if result.red_flags:
                        st.markdown("**🚨 Red Flags:**")

                        for flag in result.red_flags:
                            st.markdown(f"- {flag}")
                    else:
                        st.markdown("**Red Flags:** None identified")

                    # JSON export button
                    st.download_button(
                        label="⬇ Export as JSON",
                        data=result.model_dump_json(indent=2),
                        file_name="symptom_summary.json",
                        mime="application/json",
                    )

                    # Add to session history
                    st.session_state.history.append(result.model_dump())

                except ValidationError as e:
                    st.error(f"Output validation failed: {e}")

                except Exception as e:
                    st.error(f"Something went wrong: {e}")
