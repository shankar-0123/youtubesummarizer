import streamlit as st
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
API_KEY=st.text_input("Enter your api key")
genai.configure(api_key=API_KEY)

prompt="This is the transcript of youtube video. make the complete notes for this video without missing any points. Give output in english only even the transcript is in other language you have to translate and give notes for it in english only"


## getting the transcript data from yt videos
def extract_transcript_details(youtube_video_url):
        vid_id=youtube_video_url
        transcript_text = YouTubeTranscriptApi.get_transcript(vid_id,languages= [
    "af", "ak", "sq", "am", "ar", "hy", "as", "ay", "az", "bn", "eu", "be", "bho", "bs", "bg",
    "my", "ca", "ceb", "zh-Hans", "zh-Hant", "co", "hr", "cs", "da", "dv", "nl", "en", "eo", "et",
    "ee", "fil", "fi", "fr", "gl", "lg", "ka", "de", "el", "gn", "gu", "ht", "ha", "haw", "iw",
    "hi", "hmn", "hu", "is", "ig", "id", "ga", "it", "ja", "jv", "kn", "kk", "km", "rw", "ko",
    "kri", "ku", "ky", "lo", "la", "lv", "ln", "lt", "lb", "mk", "mg", "ms", "ml", "mt", "mi",
    "mr", "mn", "ne", "nso", "no", "ny", "or", "om", "ps", "fa", "pl", "pt", "pa", "qu", "ro",
    "ru", "sm", "sa", "gd", "sr", "sn", "sd", "si", "sk", "sl", "so", "st", "es", "su", "sw",
    "sv", "tg", "ta", "tt", "te", "th", "ti", "ts", "tr", "tk", "uk", "ur", "ug", "uz", "vi",
    "cy", "fy", "xh", "yi", "yo", "zu"
]
)

        transcript = ""
        for i in transcript_text:
            transcript += " " + i["text"]

        return transcript


    
## getting the summary based on Prompt from Google Gemini Pro
def generate_gemini_content(transcript_text,prompt):

    model=genai.GenerativeModel("gemini-pro")
    response=model.generate_content(prompt+transcript_text)
    return response.text

st.title("YouTube Transcript to Detailed Notes Converter")
youtube_link = st.text_input("Enter YouTube Video Link:")

if youtube_link:
    if "watch" in youtube_link:
        video_id = youtube_link.split("?v=")[1].split("&")[0] 
    else  :
        video_id=youtube_link.split("?")[0]
        video_id=video_id[17:]
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)
    transcript_text=extract_transcript_details(video_id)
    if transcript_text:
        summary=generate_gemini_content(transcript_text,prompt)
        st.markdown("## Detailed Notes:")
        st.write(summary)





