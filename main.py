import streamlit as st
from bs4 import BeautifulSoup
import requests

st.title("Broken Link Checker for HTML Emails")

uploaded_file = st.file_uploader("Upload an EML file", type="eml")

if uploaded_file:
    html_content = uploaded_file.read()
    soup = BeautifulSoup(html_content, "html.parser")
    links = soup.find_all("a")

    st.write(f"Found {len(links)} links. Checking...")

    for link in links:
        href = link.get("href")
        html_snippet = str(link)  # capture full <a> tag for debugging

        # Check for missing or placeholder links
        if not href or href.strip() == "" or href in ("#", "javascript:void(0)"):
            st.warning(f"⚠️ Placeholder or empty link: `{href}`")
            st.code(html_snippet, language="html")
            continue

        if not href.startswith(("http://", "https://")):
            st.warning(f"⚠️ Ignored non-http link: `{href}`")
            st.code(html_snippet, language="html")
            continue

        try:
            response = requests.head(href, allow_redirects=True, timeout=5)
            if response.status_code >= 400:
                st.error(f"❌ Broken link: `{href}` (Status: {response.status_code})")
                st.code(html_snippet, language="html")
            else:
                st.success(f"✅ OK: {href}")
        except Exception as e:
            st.warning(f"⚠️ Error checking `{href}`: {str(e)}")
            st.code(html_snippet, language="html")
