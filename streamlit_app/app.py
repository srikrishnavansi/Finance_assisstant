import streamlit as st
import base64
import pandas as pd
import plotly.express as px
from audio_recorder_streamlit import audio_recorder
from utils import process_text_query, process_voice_query
from audio_utils import ensure_wav_format

# --- Sidebar for API Keys ---
st.sidebar.header("🔑 Enter API Keys to Start")
if "GEMINI_API_KEY" not in st.session_state:
    st.session_state["GEMINI_API_KEY"] = ""
if "ELEVENLABS_API_KEY" not in st.session_state:
    st.session_state["ELEVENLABS_API_KEY"] = ""
if "ELEVENLABS_VOICE_ID" not in st.session_state:
    st.session_state["ELEVENLABS_VOICE_ID"] = "tnSpp4vdxKPjI9w0GnoV"

gemini_key = st.sidebar.text_input("Gemini API Key", type="password", value=st.session_state["GEMINI_API_KEY"])
elevenlabs_key = st.sidebar.text_input("ElevenLabs API Key", type="password", value=st.session_state["ELEVENLABS_API_KEY"])
voice_id = st.sidebar.text_input("ElevenLabs Voice ID", value=st.session_state["ELEVENLABS_VOICE_ID"])

if st.sidebar.button("Submit Keys"):
    st.session_state["GEMINI_API_KEY"] = gemini_key.strip()
    st.session_state["ELEVENLABS_API_KEY"] = elevenlabs_key.strip()
    st.session_state["ELEVENLABS_VOICE_ID"] = voice_id.strip()
    st.rerun()

if st.session_state["GEMINI_API_KEY"] and st.session_state["ELEVENLABS_API_KEY"]:
    # --- Session State Initialization ---
    for key, value in {
        "audio_bytes": None,
        "processing": False,
        "response_text": "",
        "response_audio": None,
        "data_insights": None,
        "plan": [],
        "recording_complete": False
    }.items():
        if key not in st.session_state:
            st.session_state[key] = value

    st.title("📈 Alpha Analyst — AI Financial Assistant")
    st.caption("Your Voice-Activated, Data-Driven Market Intelligence Platform")

    voice_tab, text_tab = st.tabs(["🎙️ Voice Query", "⌨️ Text Query"])

    with voice_tab:
        st.header("Ask your question by voice")
        st.markdown(
            "Click the <span style='color:#1e88e5;font-weight:bold;'>microphone</span> to record. "
            "Your AI answer will be spoken back automatically.",
            unsafe_allow_html=True
        )

        audio_bytes = audio_recorder(
            text="Tap to record",
            recording_color="#1e88e5",
            neutral_color="#1565c0",
            icon_name="microphone",
            icon_size="3x"
        )

        min_audio_length = 2000  # bytes, adjust as needed
        if audio_bytes and len(audio_bytes) > min_audio_length and not st.session_state.recording_complete:
            st.session_state.audio_bytes = audio_bytes
            st.session_state.recording_complete = True
            st.success("Recording complete! Listen to your recording below.")
            st.markdown("### 🎵 Your Recording")
            st.audio(audio_bytes, format="audio/wav")
        elif not audio_bytes or (audio_bytes and len(audio_bytes) <= min_audio_length):
            st.session_state.recording_complete = False

        if st.session_state.audio_bytes and not st.session_state.processing:
            if st.button("Analyze", key="analyze_voice"):
                st.session_state.processing = True
                with st.spinner("Analyzing your voice query..."):
                    processed_audio = ensure_wav_format(st.session_state.audio_bytes)
                    result = process_voice_query(
                        processed_audio,
                        st.session_state["GEMINI_API_KEY"],
                        st.session_state["ELEVENLABS_API_KEY"],
                        st.session_state["ELEVENLABS_VOICE_ID"]
                    )
                    st.session_state.response_text = result["text"]
                    st.session_state.response_audio = result["audio_bytes"]
                    st.session_state.data_insights = result.get("data", {})
                    st.session_state.plan = result.get("plan", [])
                st.session_state.processing = False
                st.session_state.audio_bytes = None
                st.session_state.recording_complete = False
                st.rerun()

    with text_tab:
        st.header("Ask your question by text")
        query = st.text_area("Type your financial question here:", height=80)
        if st.button("Analyze", key="analyze_text") and query:
            st.session_state.processing = True
            with st.spinner("Analyzing your text query..."):
                result = process_text_query(
                    query,
                    st.session_state["GEMINI_API_KEY"],
                    st.session_state["ELEVENLABS_API_KEY"],
                    st.session_state["ELEVENLABS_VOICE_ID"]
                )
                st.session_state.response_text = result["text"]
                st.session_state.response_audio = result["audio_bytes"]
                st.session_state.data_insights = result.get("data", {})
                st.session_state.plan = result.get("plan", [])
            st.session_state.processing = False
            st.rerun()

    if st.session_state.response_text:
        st.markdown("---")
        st.subheader("AI Analysis Report")
        st.markdown(
            f'<div style="line-height: 1.6; font-size: 17px; color: #fff;">{st.session_state.response_text}</div>',
            unsafe_allow_html=True
        )

        if st.session_state.response_audio:
            audio_base64 = base64.b64encode(st.session_state.response_audio).decode()
            audio_html = f"""
            <audio id="ai-audio" src="data:audio/mp3;base64,{audio_base64}" autoplay controls style="width:100%; outline:none; border-radius:8px; background:#181c24;">
            Your browser does not support the audio element.
            </audio>
            <script>
            var audio = document.getElementById('ai-audio');
            if (audio) {{
                audio.play();
            }}
            </script>
            """
            st.markdown(audio_html, unsafe_allow_html=True)

    if st.session_state.data_insights:
        st.markdown("---")
        st.subheader("📊 Interactive Data Insights")
        data_shown = False
        if "market_data" in st.session_state.data_insights:
            df = pd.DataFrame(st.session_state.data_insights["market_data"])
            if not df.empty and "date" in df and "price" in df:
                fig = px.line(df, x="date", y="price", title="Market Performance Trend", template="plotly_dark")
                st.plotly_chart(fig, use_container_width=True)
                data_shown = True
        if "sector_performance" in st.session_state.data_insights:
            sector_data = pd.DataFrame(st.session_state.data_insights["sector_performance"])
            if not sector_data.empty and "sector" in sector_data and "performance" in sector_data:
                fig = px.bar(sector_data, x="sector", y="performance", title="Sector Performance", template="plotly_dark")
                st.plotly_chart(fig, use_container_width=True)
                data_shown = True
        if "news_sentiment" in st.session_state.data_insights:
            sentiment_data = pd.DataFrame(st.session_state.data_insights["news_sentiment"])
            if not sentiment_data.empty and "sentiment" in sentiment_data and "count" in sentiment_data:
                fig = px.pie(sentiment_data, names="sentiment", values="count", title="News Sentiment", template="plotly_dark")
                st.plotly_chart(fig, use_container_width=True)
                data_shown = True
        if not data_shown:
            st.info("No chartable data available for this query.")

else:
    st.warning("Please enter both Gemini and ElevenLabs API keys in the sidebar to use the app.")
