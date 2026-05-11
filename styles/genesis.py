# styles/genesis.py

import streamlit as st


def inject_genesis_style():
    st.markdown(
        """
        <style>
        @import url('https://api.fontshare.com/v2/css?f[]=general-sans@600,700&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=JetBrains+Mono:wght@400;500&display=swap');

        :root {
            --primary: #6366F1;
            --primary-hover: #4F46E5;
            --background: #FAFAFA;
            --surface: #FFFFFF;
            --text-primary: #0A0A0A;
            --text-secondary: #6B6B6B;
            --border: #E8E8EC;
            --success: #10B981;
            --warning: #F59E0B;
            --error: #EF4444;
        }

        .stApp {
            background: var(--background);
            color: var(--text-primary);
            font-family: 'DM Sans', sans-serif;
        }

        .block-container {
            max-width: 1280px;
            padding-top: 48px;
            padding-left: 24px;
            padding-right: 24px;
        }

        h1, h2, h3 {
            font-family: 'General Sans', sans-serif;
            letter-spacing: -0.035em;
            color: var(--text-primary);
        }

        h1 {
            font-size: 56px !important;
            line-height: 1.05 !important;
            font-weight: 700 !important;
        }

        .stButton button {
            background: var(--primary);
            color: white;
            border: 1px solid var(--primary);
            border-radius: 6px;
            min-height: 38px;
            padding: 10px 16px;
            font-weight: 500;
            transition: all 200ms ease;
        }

        .stButton button:hover {
            background: var(--primary-hover);
            border-color: var(--primary-hover);
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(99, 102, 241, 0.35);
        }

        [data-testid="stChatMessage"] {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 16px;
            margin-bottom: 12px;
        }

        [data-testid="stDataFrame"] {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 12px;
            overflow: hidden;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
