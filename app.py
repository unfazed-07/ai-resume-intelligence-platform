import streamlit as st
import os
from utils.email_sender import send_automation_email
try:
    from dotenv import load_dotenv
except ImportError:
    import subprocess
    import sys

    subprocess.check_call([sys.executable, "-m", "pip", "install", "python-dotenv"])
    from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from utils.pdf_parser import extract_text_with_azure, extract_multiple_resumes
from utils.applicant_analysis import analyze_applicant_resume, get_score_color, generate_suggested_skills, get_score_label
from utils.recruiter_analysis import analyze_candidate, rank_candidates, generate_hiring_summary, get_recommendation_badge
from prompts.applicant_prompts import ROLE_SKILL_EXPECTATIONS
from prompts.recruiter_prompts import ROLE_DEFAULT_TECH_STACK

# ─────────────────────────────────────────────
# Page Configuration
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Resume X",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# Custom CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
    .main-title {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.2rem;
    }
    .subtitle {
        text-align: center;
        color: #888;
        font-size: 1rem;
        margin-bottom: 2rem;
    }
    .mode-card {
        border: 2px solid #e0e0e0;
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        cursor: pointer;
        transition: all 0.2s ease;
    }
    .score-box {
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .section-header {
        font-size: 1.2rem;
        font-weight: 700;
        margin: 1.5rem 0 0.5rem 0;
        padding-bottom: 0.3rem;
        border-bottom: 2px solid #667eea;
    }
    .tag {
        display: inline-block;
        background: #f0f0f0;
        border-radius: 20px;
        padding: 0.2rem 0.8rem;
        margin: 0.2rem;
        font-size: 0.85rem;
    }
    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

ROLES = list(ROLE_SKILL_EXPECTATIONS.keys())
EXPERIENCE_LEVELS = ["Fresher", "Mid-Level", "Senior-Level"]


# ─────────────────────────────────────────────
# Helper: Score Display
# ─────────────────────────────────────────────
def render_score_metric(label: str, score: int):
    color = get_score_color(score)
    label_text = get_score_label(score)
    st.metric(label=label, value=f"{score}/100", delta=label_text)


# ─────────────────────────────────────────────
# Applicant Mode UI
# ─────────────────────────────────────────────
def render_applicant_mode():
    st.markdown("### 👤 AI-Powered Resume Analysis")
    
    # Input row
    col1, col2 = st.columns([3, 2])
    with col1:
        role = st.text_input("🎯 Target Role", value="AI Engineer", key="role_input")
    with col2:
        experience = st.selectbox("📊 Experience Level", EXPERIENCE_LEVELS, key="exp_input")

    # AI Skill Generation Logic
    if "ai_skills" not in st.session_state:
        st.session_state.ai_skills = []

    if st.button("✨ Generate Skills with AI"):
        with st.spinner(f"AI is researching skills for {role}..."):
            from utils.applicant_analysis import generate_suggested_skills
            st.session_state.ai_skills = generate_suggested_skills(role, experience)

    # Required Skills Text Area
    st.markdown("**🔧 Required Skills for Analysis** *(AI-generated below, edit if needed)*")
    
    # Join list into newline-separated string for the text area
    current_skills_text = "\n".join(st.session_state.ai_skills)
    
    skills_input = st.text_area(
        "Skills List",
        value=current_skills_text,
        height=200,
        help="These are the keywords the AI will look for in your resume."
    )
    
    # Convert back to list for analysis
    final_skills = [s.strip() for s in skills_input.split("\n") if s.strip()]

    # File Upload & Analysis Logic
    uploaded_file = st.file_uploader("📄 Upload Resume (PDF)", type=["pdf"])

    if uploaded_file and st.button("🚀 Run Analysis", use_container_width=True, type="primary"):
        with st.spinner("Analyzing..."):
            # Extraction logic...
            file_bytes = uploaded_file.read()
            from utils.pdf_parser import extract_text_with_azure
            resume_text = extract_text_with_azure(file_bytes, uploaded_file.name)
            
            # Pass final_skills (the AI generated ones) to the analyzer
            from utils.applicant_analysis import analyze_applicant_resume
            result = analyze_applicant_resume(resume_text, role, experience, required_skills=final_skills)
            render_applicant_results(result, role, experience)

            
def render_applicant_results(result: dict, role: str, experience: str):
    st.markdown("---")
    st.markdown(f"## 📊 Analysis Results — {experience} {role}")

    # ── Score Cards ──
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🏆 Overall Score", f"{result.get('overall_score', 0)}/100",
                  get_score_label(result.get('overall_score', 0)))
    with col2:
        st.metric("🤖 ATS Score", f"{result.get('ats_score', 0)}/100",
                  get_score_label(result.get('ats_score', 0)))
    with col3:
        st.metric("💻 Technical Score", f"{result.get('technical_score', 0)}/100",
                  get_score_label(result.get('technical_score', 0)))
    with col4:
        st.metric("📅 Experience Score", f"{result.get('experience_score', 0)}/100",
                  get_score_label(result.get('experience_score', 0)))

    # ── Summary ──
    st.markdown('<div class="section-header">📝 Summary</div>', unsafe_allow_html=True)
    st.info(result.get("summary", "No summary available."))

    # ── Strengths & Weaknesses ──
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-header">✅ Strengths</div>', unsafe_allow_html=True)
        for s in result.get("strengths", []):
            st.markdown(f"- {s}")

    with col2:
        st.markdown('<div class="section-header">⚠️ Weaknesses</div>', unsafe_allow_html=True)
        for w in result.get("weaknesses", []):
            st.markdown(f"- {w}")

    # ── Missing Skills ──
    missing = result.get("missing_skills", [])
    if missing:
        st.markdown('<div class="section-header">🔴 Missing Skills</div>', unsafe_allow_html=True)
        tags_html = "".join(f'<span class="tag">❌ {s}</span>' for s in missing)
        st.markdown(tags_html, unsafe_allow_html=True)

    # ── Keyword Suggestions ──
    keywords = result.get("keyword_suggestions", [])
    if keywords:
        st.markdown('<div class="section-header">🔑 ATS Keyword Suggestions</div>', unsafe_allow_html=True)
        tags_html = "".join(f'<span class="tag">+ {k}</span>' for k in keywords)
        st.markdown(tags_html, unsafe_allow_html=True)

    # ── Detailed Feedback ──
    st.markdown('<div class="section-header">📋 Detailed Feedback</div>', unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["🛠️ Projects", "📐 Formatting", "🏆 Achievements"])
    with tab1:
        st.write(result.get("project_feedback", "N/A"))
    with tab2:
        st.write(result.get("formatting_feedback", "N/A"))
    with tab3:
        st.write(result.get("achievement_feedback", "N/A"))

    # ── Top Suggestions ──
    suggestions = result.get("top_suggestions", [])
    if suggestions:
        st.markdown('<div class="section-header">💡 Top Action Items</div>', unsafe_allow_html=True)
        for i, suggestion in enumerate(suggestions, 1):
            st.markdown(f"**{i}.** {suggestion}")


# ─────────────────────────────────────────────
# Recruiter Mode UI
# ─────────────────────────────────────────────
def render_recruiter_mode():
    st.markdown("### 🏢 Recruiter — Candidate Evaluation")
    st.markdown("Upload multiple resumes for AI-powered candidate ranking and hiring insights.")

    # ── Job Setup ──
    col1, col2 = st.columns([3, 2])
    with col1:
        # Changed to text_input to allow custom roles
        role = st.text_input("🎯 Hiring Role", value="AI Engineer", key="rec_role_input")
    with col2:
        experience = st.selectbox("📊 Experience Level", EXPERIENCE_LEVELS, key="rec_exp_input")

    # ── State Management ──
    # Initialize session state keys to ensure UI persists after button clicks
    if "recruiter_ai_skills" not in st.session_state:
        st.session_state.recruiter_ai_skills = []
    if "ranked_results" not in st.session_state:
        st.session_state.ranked_results = None
    if "hiring_summary" not in st.session_state:
        st.session_state.hiring_summary = None

    # AI Skill Generation
    if st.button("✨ Generate Tech Stack with AI", key="rec_gen_btn"):
        with st.spinner(f"AI is researching the ideal stack for {role}..."):
            # Reusing the logic from the applicant side
            st.session_state.recruiter_ai_skills = generate_suggested_skills(role, experience)

    # ── Editable Tech Stack ──
    st.markdown("**✏️ Required Tech Stack** *(AI-generated, edit as needed)*")

    current_rec_skills = "\n".join(st.session_state.recruiter_ai_skills)

    custom_input = st.text_area(
        "Required Skills",
        value=current_rec_skills,
        height=150,
        label_visibility="collapsed",
        help="These keywords will be used to rank all uploaded resumes."
    )
    # Convert input to list for the analysis engine
    required_skills = [s.strip() for s in custom_input.split("\n") if s.strip()]

    # ── File Upload ──
    uploaded_files = st.file_uploader(
        "📂 Upload Candidate Resumes (PDF) — Multiple Allowed",
        type=["pdf"],
        accept_multiple_files=True,
        help="Upload one or more candidate resumes for batch analysis."
    )

    if uploaded_files:
        st.success(f"✅ {len(uploaded_files)} resume(s) uploaded")

        if st.button("🚀 Analyze All Candidates", use_container_width=True, type="primary"):
            with st.spinner("🔍 Extracting and analyzing candidates..."):
                # Use existing parser logic
                resume_texts = extract_multiple_resumes(uploaded_files)

                all_results = []
                progress = st.progress(0, text="Analyzing candidates...")
                total = len(resume_texts)

                for i, (filename, text) in enumerate(resume_texts.items()):
                    progress.progress((i + 1) / total, text=f"Analyzing {filename}...")
                    if not text or "[ERROR]" in text:
                        continue
                    try:
                        # Analyze using required_skills
                        result = analyze_candidate(text, role, experience, required_skills)
                        result["_filename"] = filename
                        all_results.append(result)
                    except Exception as e:
                        st.warning(f"⚠️ Analysis failed for {filename}: {e}")

                progress.empty()

                if all_results:
                    # Save results to session state to prevent disappearance on rerun
                    st.session_state.ranked_results = rank_candidates(all_results, role, experience)
                    try:
                        st.session_state.hiring_summary = generate_hiring_summary(
                            st.session_state.ranked_results, role, experience
                        )
                    except Exception as e:
                        st.session_state.hiring_summary = {}
                        st.warning(f"Could not generate summary: {e}")
                else:
                    st.error("No candidates could be analyzed.")

    # ── Persistent Rendering ──
    # Check session state to render results even after outreach buttons trigger a rerun
    if st.session_state.ranked_results is not None:
        render_recruiter_results(
            st.session_state.ranked_results,
            st.session_state.hiring_summary,
            role,
            experience
        )
        
import pandas as pd
from io import BytesIO
import streamlit as st
from utils.email_sender import send_automation_email


def render_recruiter_results(ranked: list, summary: dict, role: str, experience: str):
    """
    Renders the recruiter analysis dashboard.
    Features: Outreach Automation, Excel Export, Hiring Summary, and Candidate Profiles.
    """
    st.markdown("---")
    st.markdown(f"## 🏆 Candidate Rankings — {experience} {role}")

    # ── Section 1: Outreach Automation Control Center ──
    st.markdown("### 🚀 Outreach Automation")
    col_t1, col_t2 = st.columns([2, 3])

    with col_t1:
        # Recruiter sets the threshold for automatic qualification
        threshold = st.slider("Minimum Overall Score to Qualify", 0, 100, 80)

    with col_t2:
        custom_message = st.text_area(
            "Custom Email Message",
            value=f"Hi, we were impressed by your profile for the {role} position and would like to discuss the next steps.",
            height=100
        )

    # Filter candidates based on the slider value
    qualified_candidates = [c for c in ranked if c.get("overall_match_score", 0) >= threshold]
    st.info(f"💡 {len(qualified_candidates)} candidates meet your {threshold}% threshold.")

    # Bulk Email Trigger
    if st.button(f"📧 Send Emails to {len(qualified_candidates)} Qualified Candidates", use_container_width=True):
        progress_bar = st.progress(0)
        success_count = 0

        for i, cand in enumerate(qualified_candidates):
            email = cand.get("candidate_email", "No Mail")
            name = cand.get("candidate_name", "Unknown")
            score = cand.get("overall_match_score", 0)

            if email != "No Mail":
                success, msg = send_automation_email(email, name, score, custom_message)
                if success:
                    success_count += 1

            progress_bar.progress((i + 1) / len(qualified_candidates))

        st.success(f"✅ Successfully sent {success_count} emails!")

    # ── Section 2: Excel Export ──
    export_data = []
    for candidate in ranked:
        export_data.append({
            "Candidate Name": candidate.get("candidate_name", "Unknown"),
            "Email": candidate.get("candidate_email", "No Mail"),  # Extracted via Groq
            "Overall Score (%)": candidate.get("overall_match_score", 0),
            "Technical Score (%)": candidate.get("technical_score", 0),
            "Experience Score (%)": candidate.get("experience_score", 0),
            "ATS Score (%)": candidate.get("ats_score", 0),
            "Matched Skills": ", ".join(candidate.get("matched_skills", [])),
            "Missing Skills": ", ".join(candidate.get("missing_skills", [])),
            "Recommendation": candidate.get("hiring_recommendation", "Unknown"),
            "Reasoning": candidate.get("recommendation_reason", "")
        })

    if export_data:
        df = pd.DataFrame(export_data)
        output = BytesIO()
        try:
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Rankings')

            st.download_button(
                label="📥 Download Hiring Report (Excel)",
                data=output.getvalue(),
                file_name=f"Hiring_Report_{role.replace(' ', '_')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
        except Exception as e:
            st.error(f"Excel generation failed: {e}")

    # ── Section 3: Hiring Summary Dashboard ──
    if summary:
        st.markdown('<div class="section-header">📊 Hiring Summary</div>', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.success(f"🥇 Top Candidate: **{summary.get('top_candidate', 'N/A')}**")
        with col2:
            st.info(f"✅ Shortlisted: **{len(summary.get('shortlisted', []))}**")
        with col3:
            st.error(f"❌ Rejected: **{len(summary.get('rejected', []))}**")

        st.markdown(f"**💡 AI Insights:** {summary.get('hiring_insights', '')}")

        gaps = summary.get("common_gaps", [])
        if gaps:
            st.warning(f"**Common Skill Gaps:** {' • '.join(gaps)}")

    # ── Section 4: Candidate Profiles ──
    st.markdown('<div class="section-header">👥 Candidate Profiles</div>', unsafe_allow_html=True)

    for rank, candidate in enumerate(ranked, 1):
        name = candidate.get("candidate_name", f"Candidate {rank}")
        email = candidate.get("candidate_email", "No Mail")
        score = candidate.get("overall_match_score", 0)
        rec = candidate.get("hiring_recommendation", "Unknown")
        filename = candidate.get("_filename", "Unknown")

        emoji, _ = get_recommendation_badge(rec)

        # Highlight qualified candidates with a distinct label
        qual_label = "⭐ QUALIFIED" if score >= threshold else ""

        with st.expander(f"#{rank} {qual_label} | {emoji} {name} | Match: {score}% | 📧 {email}"):
            # Layout for individual email action
            col_info, col_action = st.columns([3, 1])

            with col_info:
                st.caption(f"Source File: {filename}")
                st.write(f"**📧 Contact:** {email}")

            with col_action:
                if email != "No Mail":
                    if st.button(f"📧 Send Invite", key=f"individual_email_{rank}"):
                        success, msg = send_automation_email(email, name, score, custom_message)
                        if success:
                            st.toast(f"Invitation sent to {name}!", icon="✅")
                        else:
                            st.error(f"Failed: {msg}")

            # Metric Grid
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Overall", f"{score}%")
            m2.metric("Technical", f"{candidate.get('technical_score', 0)}%")
            m3.metric("Experience", f"{candidate.get('experience_score', 0)}%")
            m4.metric("ATS", f"{candidate.get('ats_score', 0)}%")

            # Skills & Feedback
            col_left, col_right = st.columns(2)
            with col_left:
                st.markdown("**✅ Matched Skills**")
                matched = candidate.get("matched_skills", [])
                st.markdown("".join(f'<span class="tag">✅ {s}</span>' for s in matched) if matched else "None",
                            unsafe_allow_html=True)

                st.markdown("**❌ Missing Skills**")
                missing = candidate.get("missing_skills", [])
                st.markdown("".join(f'<span class="tag">❌ {s}</span>' for s in missing) if missing else "None",
                            unsafe_allow_html=True)

            with col_right:
                st.markdown("**🎯 Interview Focus**")
                for area in candidate.get("interview_focus_areas", []):
                    st.markdown(f"- {area}")

                st.markdown(f"**🧾 Recommendation:** {candidate.get('recommendation_reason', 'N/A')}")

            # Strengths & Weaknesses
            s_col, w_col = st.columns(2)
            with s_col:
                st.markdown("**💪 Strengths**")
                for s in candidate.get("strengths", []): st.markdown(f"- {s}")
            with w_col:
                st.markdown("**⚠️ Weaknesses**")
                for w in candidate.get("weaknesses", []): st.markdown(f"- {w}")# ─────────────────────────────────────────────

# Sidebar
# ─────────────────────────────────────────────
def render_sidebar():
    with st.sidebar:
        st.markdown("## 🧠 AI Resume Platform")
        st.markdown("---")

        # API Status
        st.markdown("### ⚙️ API Configuration")
        gemini_ok = bool(os.getenv("GEMINI_API_KEY"))
        azure_ok = bool(os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY"))

        st.markdown(f"{'✅' if gemini_ok else '❌'} Gemini API")
        st.markdown(f"{'✅' if azure_ok else '⚠️'} Azure Doc Intelligence")

        if not azure_ok:
            st.caption("Azure not configured — using PyPDF2 fallback for PDF parsing.")

        st.markdown("---")
        st.markdown("### 📌 About")
        st.markdown("""
        An AI-powered resume intelligence platform that helps:
        - **Applicants** get personalized feedback
        - **Recruiters** rank and evaluate candidates
        
        Powered by **Gemini API** + **Azure AI Document Intelligence**
        """)

        st.markdown("---")
        st.caption("Built with Streamlit • Azure • Gemini")


# ─────────────────────────────────────────────
# Main App
# ─────────────────────────────────────────────
def main():
    render_sidebar()

    st.markdown('<div class="main-title">🧠 Resume X</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Azure + Gemini Powered Resume Analysis System</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### Select Your Mode")

    col1, col2 = st.columns(2)
    with col1:
        applicant_clicked = st.button(
            "👤 Applicant Mode\nGet personalized resume feedback",
            use_container_width=True,
            key="applicant_btn"
        )
    with col2:
        recruiter_clicked = st.button(
            "🏢 Recruiter Mode\nRank and evaluate candidates",
            use_container_width=True,
            key="recruiter_btn"
        )

    if "mode" not in st.session_state:
        st.session_state.mode = None

    if applicant_clicked:
        st.session_state.mode = "applicant"
    if recruiter_clicked:
        st.session_state.mode = "recruiter"

    st.markdown("---")

    if st.session_state.mode == "applicant":
        render_applicant_mode()
    elif st.session_state.mode == "recruiter":
        render_recruiter_mode()
    else:
        st.markdown("""
        <div style="text-align:center; padding: 3rem; color: #888;">
            <h3>👆 Choose a mode above to get started</h3>
            <p>Applicant Mode for resume feedback • Recruiter Mode for candidate ranking</p>
        </div>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
