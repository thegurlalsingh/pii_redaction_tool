import os
import tempfile
import streamlit as st
from detectors.docx_handler import docx_handler

st.set_page_config(page_title="PII Redactor", page_icon="🔒")
st.title("DOCX PII Redaction")
st.write("Upload a .docx file, redact PII, and download the redacted file.")

uploaded = st.file_uploader("Upload DOCX", type=["docx"])

if uploaded is not None:
    st.success(f"Uploaded: {uploaded.name}")

    if st.button("Redact Document"):
        with st.spinner("Redacting"):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as in_file:
                in_file.write(uploaded.read())
                input_path = in_file.name

            with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as out_file:
                output_path = out_file.name

            handler = docx_handler(input_path=input_path, output_path=output_path)
            handler.process_and_save()

        st.success("Redaction complete!")

        with open(output_path, "rb") as f:
            st.download_button(
                label="Download Redacted DOCX",
                data=f.read(),
                file_name=f"redacted_{uploaded.name}",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )

        try:
            os.remove(input_path)
            os.remove(output_path)
        except Exception:
            pass