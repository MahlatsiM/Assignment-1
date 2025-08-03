import streamlit as st
import openai
import pyttsx3

# Set your OpenAI API key
openai_api_key = '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'

# Function to speak locally with pyttsx3
def speak_offline(text):
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 200)
        engine.setProperty('volume', 0.9)
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        st.warning(f"pyttsx3 Error: {e}")

# Function to get OpenAI response
def get_openai_response(prompt):
    try:
        client = openai.OpenAI(api_key=openai_api_key)
        response = client.chat.completions.create(
            model="gpt-4.1-nano-2025-04-14",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"OpenAI Error: {e}")
        return None

# Streamlit UI
st.set_page_config(page_title="CV & Job Fit Assistant", layout="wide")
st.title("📄 CV vs Job Description AI Assistant")

# Inputs
with st.expander("✏️ Paste CV Text Here"):
    user_cv = st.text_area("Paste your entire CV below:", height=300)

with st.expander("🧾 Paste Job Description Here"):
    job_desc = st.text_area("Paste the job description below:", height=300)

if st.button("🔍 Analyze Fit"):
    if not user_cv or not job_desc:
        st.warning("Please paste both your CV and the Job Description.")
    else:
        # Step 1: Comparison Prompt
        comparison_prompt = f"""
        Compare this CV with the Job Description. Identify:
        - Skills that match
        - Skills that are missing
        - Recommendations for improvement
        - Courses/tools/experience to fill gaps

        CV:
        {user_cv}

        Job Description:
        {job_desc}
        """

        with st.spinner("Analyzing the CV and job description..."):
            comparison_result = get_openai_response(comparison_prompt)

        if comparison_result:
            # Step 2: Voice Summary of Comparison
            summary_prompt = f"""
            Summarize this CV comparison in 60 seconds:
            - Highlight key matches
            - Highlight skill gaps
            - Add 1 recommendation

            Analysis:
            {comparison_result}
            """
            summary_text = get_openai_response(summary_prompt)

            if summary_text:
                st.subheader("🔊 CV Fit Summary")
                st.write(summary_text)

                # Speak locally with pyttsx3
                st.info("🔈 Playing voice summary using your device speaker...")
                speak_offline(summary_text)

            # Step 3: Full Comparison Text
            st.subheader("📌 Full CV vs Job Fit Analysis")
            st.write(comparison_result)

            # Step 4: Roadmap Prompt
            roadmap_prompt = f"""
            Based on the skill gaps in this CV vs Job Description analysis, create a 30-day roadmap.
            Focus on:
            - What to learn
            - Which tools to practice
            - How to gain experience (e.g. side projects, courses)
            - Structure by week

            CV:
            {user_cv}

            Job Description:
            {job_desc}
            """

            with st.spinner("📚 Building your career development roadmap..."):
                roadmap_result = get_openai_response(roadmap_prompt)

            if roadmap_result:
                # Step 5: Summary Voice Prompt
                summary_roadmap_prompt = f"""
                Summarize this roadmap into a motivating voice script. Focus on:
                - Key actions
                - Time frame
                - Encouraging closing sentence

                Roadmap:
                {roadmap_result}
                """
                roadmap_summary = get_openai_response(summary_roadmap_prompt)

                if roadmap_summary:
                    st.subheader("🎧 Roadmap Summary")
                    st.write(roadmap_summary)

                    # Speak the roadmap summary
                    st.info("🔈 Playing roadmap summary using your device speaker...")
                    speak_offline(roadmap_summary)

                # Step 6: Full Roadmap Text
                st.subheader("📚 Full Roadmap")
                st.write(roadmap_result)
