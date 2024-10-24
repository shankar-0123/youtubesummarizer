import streamlit as st
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound, VideoUnavailable

# Input field for API key and YouTube link
API_KEY = st.text_input("Enter your Google API key")
youtube_link = st.text_input("Enter YouTube Video Link:")

# Configure Google Gemini API
if API_KEY:
    genai.configure(api_key=API_KEY)

# Prompt for Google Gemini model
prompt = ("This is the transcript of a YouTube video. "
          "Make the complete notes for this video without missing any points. "
          "Give the output in English only. Even if the transcript is in another language, "
          "you have to translate and give the notes in English.")

# Function to extract transcript details from YouTube
def extract_transcript_details(youtube_video_url):
    try:
        vid_id = youtube_video_url
        # Attempt to fetch the transcript in the supported languages
        transcript_text = YouTubeTranscriptApi.get_transcript(vid_id, languages=[
            "af", "ak", "sq", "am", "ar", "hy", "as", "ay", "az", "bn", "eu", "be", "bho", "bs", "bg",
            "my", "ca", "ceb", "zh-Hans", "zh-Hant", "co", "hr", "cs", "da", "dv", "nl", "en", "eo", "et",
            "ee", "fil", "fi", "fr", "gl", "lg", "ka", "de", "el", "gn", "gu", "ht", "ha", "haw", "iw",
            "hi", "hmn", "hu", "is", "ig", "id", "ga", "it", "ja", "jv", "kn", "kk", "km", "rw", "ko",
            "kri", "ku", "ky", "lo", "la", "lv", "ln", "lt", "lb", "mk", "mg", "ms", "ml", "mt", "mi",
            "mr", "mn", "ne", "nso", "no", "ny", "or", "om", "ps", "fa", "pl", "pt", "pa", "qu", "ro",
            "ru", "sm", "sa", "gd", "sr", "sn", "sd", "si", "sk", "sl", "so", "st", "es", "su", "sw",
            "sv", "tg", "ta", "tt", "te", "th", "ti", "ts", "tr", "tk", "uk", "ur", "ug", "uz", "vi",
            "cy", "fy", "xh", "yi", "yo", "zu"
        ])
        
        # Concatenate transcript segments into a single string
        transcript = ""
        for segment in transcript_text:
            transcript += " " + segment["text"]
        
        return transcript

    except TranscriptsDisabled:
        st.error("Transcripts are disabled for this video.")
        return None
    except NoTranscriptFound:
        st.error("No transcript found for this video.")
        return None
    except VideoUnavailable:
        st.error("This video is unavailable.")
        return None
    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")
        return None

# Function to generate detailed notes using Google Gemini
def generate_gemini_content(transcript_text, prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt + transcript_text)
    return response.text

# Main code execution
if youtube_link and API_KEY:
    if "watch" in youtube_link:
        video_id = youtube_link.split("?v=")[1].split("&")[0]
    else:
        video_id = youtube_link.split("/")[-1]

    # Get the transcript of the video
    transcript_text = extract_transcript_details(video_id)

    if transcript_text:
        # Generate the notes using the transcript and Google Gemini API
        summary = generate_gemini_content(transcript_text, prompt)
        # Display the summary (detailed notes) in the Streamlit app
        st.markdown("## Detailed Notes:")
        st.write(summary)
