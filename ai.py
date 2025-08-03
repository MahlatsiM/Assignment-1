import streamlit as st
import openai
import requests
import io

# Set your keys
openai.api_key = 'sk-proj-jZwTb2svhrTxwWrKAv52cIWkSmbQjNbmUCCWYm4aITeH39JypgSs991J-SfC52e_4wDO8ssD_JT3BlbkFJf2rW2jL1uWXS7A4My1r_AGIN9PJ9yfdCHThXoG_rTEP8FuKgGPkV6-NODxxjglcA-0A9SCPigAOPENAI_API_KEY'
elevenlabs_api_key = '380bdb2568b547cb888af8dd0264dc7a'
elevenlabs_voice_id = '2qfp6zPuviqeCOZIE9RZ'

def get_openai_response(prompt):
    try:
        client = openai.OpenAI()
        response = client.chat.completions.create(
            model="gpt-4.1-nano-2025-04-14",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"OpenAI Error: {e}")
        return None

def generate_audio_safe(text):
    try:
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{elevenlabs_voice_id}"
        headers = {
            "xi-api-key": elevenlabs_api_key,
            "Content-Type": "application/json"
        }
        payload = {
            "text": text,
            "voice_settings": {"stability": 0.4, "similarity_boost": 0.75}
        }
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.content
    except Exception as e:
        st.error(f"ElevenLabs Error: {e}")
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
        # Prompt for OpenAI comparison
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
            # Summarize comparison for voice
            summary_prompt = f"""
            Summarize this CV comparison in 60 seconds:
            - Highlight key matches
            - Highlight skill gaps
            - Add 1 recommendation

            Analysis:
            {comparison_result}
            """
            summary_text = get_openai_response(summary_prompt)

            with st.spinner("🎙️ Generating audio summary..."):
                audio_bytes = generate_audio_safe(summary_text)

            if audio_bytes:
                st.success("🔊 Here's your voice summary:")
                st.audio(io.BytesIO(audio_bytes), format='audio/mp3')
            else:
                st.warning("Failed to generate voice summary.")

            # Show full comparison
            st.subheader("📌 Full CV vs Job Fit Analysis")
            st.write(comparison_result)

            # Generate Roadmap
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

            # Summarize roadmap for audio
            summary_roadmap_prompt = f"""
            Summarize this roadmap into a motivating voice script. Focus on:
            - Key actions
            - Time frame
            - Encouraging closing sentence

            Roadmap:
            {roadmap_result}
            """
            roadmap_summary = get_openai_response(summary_roadmap_prompt)

            with st.spinner("🎙️ Generating audio roadmap..."):
                roadmap_audio = generate_audio_safe(roadmap_summary)

            if roadmap_audio:
                st.success("🎧 Here's your spoken roadmap:")
                st.audio(io.BytesIO(roadmap_audio), format='audio/mp3')
            else:
                st.warning("❌ Roadmap audio generation failed.")

            st.subheader("📚 Full Roadmap")
            st.write(roadmap_result)