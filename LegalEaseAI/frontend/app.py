import os
from pathlib import Path

import requests
import streamlit as st
from dotenv import load_dotenv

from utils.formatters import (
    format_docx,
    format_pdf,
    format_html_preview
)

from utils.sanitizer import sanitize_text


BASE_DIR = Path(
    __file__
).resolve().parents[1]


load_dotenv(
    BASE_DIR / ".env"
)


API_URL = os.getenv(
    "FRONTEND_API_URL",
    "http://127.0.0.1:8000"
).rstrip("/")


LOGO_PATH = (
    BASE_DIR
    / "assets"
    / "legal_ease_logo.png"
)


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="LegalEase",
    page_icon="⚖️",
    layout="wide"
)


# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown(
    """
<style>

.main-title {
    text-align: center;
    font-size: 42px;
    font-weight: 700;
}

.subtitle {
    text-align: center;
    color: #9ca3af;
    font-size: 18px;
}

.document-card {
    background: #111827;
    border: 1px solid #374151;
    border-radius: 15px;
    padding: 30px;
    line-height: 1.7;
    max-height: 650px;
    overflow-y: auto;
}

.document-card h2 {
    color: white;
}

.document-card h3 {
    color: #e5e7eb;
}

.document-card p {
    color: #f3f4f6;
}

.document-card .bullet {
    color: #f3f4f6;
    margin: 8px 0;
}

.warning-box {
    background: #422006;
    border: 1px solid #92400e;
    border-radius: 10px;
    padding: 15px;
}

</style>
""",
    unsafe_allow_html=True
)


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "generated_text" not in st.session_state:

    st.session_state.generated_text = ""


if "editing" not in st.session_state:

    st.session_state.editing = False


if "model" not in st.session_state:

    st.session_state.model = ""


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    if LOGO_PATH.exists():

        st.image(
            str(LOGO_PATH),
            width=180
        )

    st.title("LegalEase")

    st.caption(
        "AI-Assisted Legal Document Generator"
    )

    st.divider()

    st.markdown(
        """
### Features

- AI legal document drafting
- Structured legal clauses
- Editable document
- TXT export
- DOCX export
- PDF export
- FastAPI backend
- Gemini AI integration
"""
    )

    st.divider()

    st.warning(
        "LegalEase generates drafts. "
        "Always review the final document "
        "with a qualified legal professional."
    )


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown(
    '<div class="main-title">⚖️ LegalEase</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'AI Legal Document Generator'
    '</div>',
    unsafe_allow_html=True
)

st.write("")


# --------------------------------------------------
# INPUT FORM
# --------------------------------------------------

with st.form("legal_document_form"):

    st.subheader(
        "Document Information"
    )

    col1, col2 = st.columns(2)

    with col1:

        document_type = st.text_input(
            "Document Type",
            placeholder=(
                "Example: Freelance Work Contract"
            )
        )

    with col2:

        dates = st.text_input(
            "Effective Date",
            placeholder=(
                "Example: April 15, 2026"
            )
        )

    parties = st.text_area(
        "Parties Involved",
        placeholder=(
            "Example:\n"
            "Jane Doe (Service Provider)\n"
            "TechNova Inc. (Client)"
        ),
        height=130
    )

    terms = st.text_area(
        "Terms & Conditions",
        placeholder=(
            "Payment within 30 days of invoice; "
            "Confidentiality must be maintained; "
            "Provider must deliver work by deadline; "
            "Either party may terminate with 15 days notice"
        ),
        height=180
    )

    st.caption(
        "Tip: Separate individual clauses using semicolons (;)."
    )

    generate = st.form_submit_button(
        "🚀 Generate Document",
        use_container_width=True,
        type="primary"
    )


# --------------------------------------------------
# GENERATE
# --------------------------------------------------

if generate:

    missing_fields = []

    if not document_type.strip():

        missing_fields.append(
            "Document Type"
        )

    if not parties.strip():

        missing_fields.append(
            "Parties"
        )

    if not terms.strip():

        missing_fields.append(
            "Terms & Conditions"
        )

    if not dates.strip():

        missing_fields.append(
            "Effective Date"
        )

    if missing_fields:

        st.error(
            "Please complete: "
            + ", ".join(
                missing_fields
            )
        )

    else:

        payload = {

            "document_type":
                document_type,

            "parties":
                parties,

            "terms":
                terms,

            "dates":
                dates
        }

        with st.spinner(
            "Gemini is generating your legal document..."
        ):

            try:

                response = requests.post(
                    f"{API_URL}/generate",
                    json=payload,
                    timeout=180
                )

                if response.status_code == 200:

                    result = response.json()

                    st.session_state.generated_text = (
                        sanitize_text(
                            result["document"]
                        )
                    )

                    st.session_state.model = (
                        result.get(
                            "model",
                            "Gemini"
                        )
                    )

                    st.session_state.editing = False

                    st.success(
                        "Document generated successfully!"
                    )

                else:

                    try:

                        error_detail = (
                            response.json()
                            .get(
                                "detail",
                                response.text
                            )
                        )

                    except Exception:

                        error_detail = response.text

                    st.error(
                        f"Backend Error "
                        f"{response.status_code}: "
                        f"{error_detail}"
                    )

            except requests.exceptions.ConnectionError:

                st.error(
                    "Cannot connect to the FastAPI backend.\n\n"
                    "Make sure the backend is running on:\n"
                    f"{API_URL}"
                )

            except requests.exceptions.Timeout:

                st.error(
                    "The request timed out. "
                    "Please try again."
                )

            except Exception as error:

                st.error(
                    f"Unexpected error: {error}"
                )


# --------------------------------------------------
# GENERATED DOCUMENT
# --------------------------------------------------

if st.session_state.generated_text:

    st.divider()

    st.header(
        "📄 Generated Document"
    )

    st.caption(
        f"Model: {st.session_state.model}"
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "✏️ Edit Document",
            use_container_width=True
        ):

            st.session_state.editing = (
                not st.session_state.editing
            )

    with col2:

        if st.button(
            "🗑️ Clear Document",
            use_container_width=True
        ):

            st.session_state.generated_text = ""

            st.session_state.editing = False

            st.rerun()


    # --------------------------------------------------
    # EDITOR
    # --------------------------------------------------

    if st.session_state.editing:

        edited_text = st.text_area(
            "Edit Document",
            value=st.session_state.generated_text,
            height=600
        )

        st.session_state.generated_text = (
            edited_text
        )

        st.info(
            "Your edits are kept in the current session."
        )


    # --------------------------------------------------
    # PREVIEW
    # --------------------------------------------------

    preview = format_html_preview(
        st.session_state.generated_text
    )

    st.markdown(
        f"""
        <div class="document-card">
            {preview}
        </div>
        """,
        unsafe_allow_html=True
    )


    # --------------------------------------------------
    # DOWNLOAD
    # --------------------------------------------------

    st.subheader(
        "⬇️ Download Document"
    )

    download_col1, download_col2, download_col3 = (
        st.columns(3)
    )


    safe_name = "".join(
        character
        if character.isalnum()
        or character in "_-"
        else "_"
        for character in document_type
    ).lower()

    if not safe_name:

        safe_name = "legal_document"


    # TXT

    txt_data = (
        st.session_state.generated_text
        .encode("utf-8")
    )


    # DOCX

    docx_data = format_docx(
        text=st.session_state.generated_text,
        document_type=document_type,
        parties=parties,
        dates=dates,
        terms=terms,
        logo_path=(
            str(LOGO_PATH)
            if LOGO_PATH.exists()
            else None
        )
    )


    # PDF

    pdf_data = format_pdf(
        text=st.session_state.generated_text,
        document_type=document_type,
        parties=parties,
        dates=dates,
        terms=terms,
        logo_path=(
            str(LOGO_PATH)
            if LOGO_PATH.exists()
            else None
        )
    )


    with download_col1:

        st.download_button(
            label="📄 Download TXT",
            data=txt_data,
            file_name=f"{safe_name}.txt",
            mime="text/plain",
            use_container_width=True
        )


    with download_col2:

        st.download_button(
            label="📝 Download DOCX",
            data=docx_data,
            file_name=f"{safe_name}.docx",
            mime=(
                "application/vnd.openxmlformats-officedocument."
                "wordprocessingml.document"
            ),
            use_container_width=True
        )


    with download_col3:

        st.download_button(
            label="📕 Download PDF",
            data=pdf_data,
            file_name=f"{safe_name}.pdf",
            mime="application/pdf",
            use_container_width=True
        )


    # --------------------------------------------------
    # LEGAL NOTICE
    # --------------------------------------------------

    st.markdown(
        """
        <div class="warning-box">

        <strong>Legal Notice</strong>

        <br><br>

        This document was generated with AI and is intended
        only as a drafting aid. It may contain errors,
        omissions, or jurisdiction-specific issues.

        Please verify all information and have the final
        document reviewed by a qualified legal professional
        before signing, filing, or relying upon it.

        </div>
        """,
        unsafe_allow_html=True
    )