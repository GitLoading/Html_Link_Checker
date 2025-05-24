{\rtf1\ansi\ansicpg1252\cocoartf2822
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import streamlit as st\
from bs4 import BeautifulSoup\
import requests\
\
st.title("Broken Link Checker for HTML Emails")\
\
uploaded_file = st.file_uploader("Upload an HTML file", type="html")\
\
if uploaded_file:\
    html_content = uploaded_file.read()\
    soup = BeautifulSoup(html_content, "html.parser")\
    links = soup.find_all("a")\
\
    st.write(f"Found \{len(links)\} links. Checking...")\
\
    for link in links:\
        href = link.get("href")\
\
        # Check for missing or placeholder links\
        if not href or href.strip() == "" or href in ("#", "javascript:void(0)"):\
            st.warning(f"Empty or placeholder link found: \{href\}")\
            continue\
\
        if not href.startswith(("http://", "https://")):\
            st.warning(f"Ignored non-http link: \{href\}")\
            continue\
\
        try:\
            response = requests.head(href, allow_redirects=True, timeout=5)\
            if response.status_code >= 400:\
                st.error(f"Broken: \{href\} (Status: \{response.status_code\})")\
            else:\
                st.success(f"OK: \{href\}")\
        except Exception as e:\
            st.warning(f"Error checking \{href\}: \{str(e)\}")\
}