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

# Function to extract video ID from YouTube link
def get_video_id(youtube_url):
    if "watch?v=" in youtube_url:
        return youtube_url.split("watch?v=")[1].split("&")[0]
    elif "youtu.be" in youtube_url:
        return youtube_url.split("=")[-1]
    elif "youtube.com/embed/" in youtube_url:
        return youtube_url.split("/embed/")[1].split("?")[0]
    else:
        st.error("Invalid YouTube URL format.")
        return None

# Function to extract transcript details from YouTube
def extract_transcript_details(vid_id):
    try:
        # Attempt to fetch the transcript in supported languages
        transcript_text = YouTubeTranscriptApi.get_transcript(vid_id, languages=['en'])
        
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
    video_id = get_video_id(youtube_link)  # Extract video ID

    if video_id:
        st.write(f"Extracted Video ID: {video_id}")  # Display extracted video ID for debugging

        # Get the transcript of the video
        transcript_text = extract_transcript_details(video_id)

        if transcript_text:
            # Generate the notes using the transcript and Google Gemini API
            summary = generate_gemini_content(transcript_text, prompt)
            # Display the summary (detailed notes) in the Streamlit app
            st.markdown("## Detailed Notes:")
            st.write(summary)
