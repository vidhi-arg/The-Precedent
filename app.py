import streamlit as st
import requests

API_URL = "http://localhost:8000/analyze"

st.set_page_config(page_title="Village Legal AI", layout="centered")
st.title("Village Legal Assistant")
st.markdown("Get legal advice based on your country's constitution and case law.")

with st.form("legal_form"):
    country = st.selectbox("Country", ["India", "USA", "Canada", "UK"])
    issue = st.text_area("Describe the issue in detail (e.g. boundary, noise, land access)")
    submitted = st.form_submit_button("Get Legal Analysis")

if submitted:
    if not issue.strip():
        st.error("Issue description is required.")
    else:
        with st.spinner("Analyzing..."):
            try:
                response = requests.post(API_URL, json={
                    "country": country,
                    "issue_description": issue
                })

                if response.status_code != 200:
                    st.error(response.json().get("detail", "Server error"))
                else:
                    data = response.json()

                    st.subheader("Relevant Constitutional Article")
                    st.code(data["article"])

                    st.subheader("Key Past Court Cases")
                    for case in data["cases"]:
                        st.markdown(f"- **{case['name']}** ({case['year']})")

                    st.subheader("Escalation Paths")
                    for step in data["escalation_paths"]:
                        st.markdown(f"- {step}")

                    st.subheader("People Involved")
                    for role, person in data["people_involved"].items():
                        st.markdown(f"- **{role.title()}**: {person}")

                    st.subheader("Suggested Legal Actions")
                    for action in data["suggested_actions"]:
                        st.markdown(f"- {action}")
            except Exception as e:
                st.error(f"Something went wrong: {e}")
