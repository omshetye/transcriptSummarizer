from urllib.parse import urlparse, parse_qs
from youtube_transcript_api import YouTubeTranscriptApi as yta
import spacy

def get_youtube_video_id(url):
    # Parse the URL
    parsed_url = urlparse(url)

    # Check if the domain is youtube.com
    if parsed_url.netloc == 'www.youtube.com' or parsed_url.netloc == 'youtube.com':
        # Extract the video ID from the query parameters
        query_params = parse_qs(parsed_url.query)
        video_id = query_params.get('v', [None])[0]

        return video_id

    # Check if the domain is youtu.be
    elif parsed_url.netloc == 'youtu.be':
        # Extract the video ID from the path
        video_id = parsed_url.path[1:]

        return video_id

    else:
        # URL is not from YouTube
        return None

def get_transcript(video_id):
    # Initialize data variable
    data = None

    # Check if subtitles are available
    try:
        data = yta.get_transcript(video_id)
    except Exception as e:
        if "Subtitles are disabled for this video" in str(e):
            print(f"TranscriptsDisabled: Subtitles are disabled for the video {video_id}! {e}")
            # Handle the situation where subtitles are disabled (e.g., print an error message, exit the program, etc.)
            return None
        else:
            # Handle other exceptions if needed
            print(f"An error occurred: {e}")
            return None

    # Check if data is None before iterating
    if data is not None:
        transcript = ''
        for value in data:
            for key, val in value.items():
                if key == 'text':
                    transcript += val

        return transcript
    else:
        print("No transcript available for the given video.")
        return None

def get_keywords(paragraph):
    # Load the English language model
    nlp = spacy.load("en_core_web_sm")

    # Process the input paragraph
    doc = nlp(paragraph)

    # Extract keywords (nouns and proper nouns)
    keywords = [token.text for token in doc if token.pos_ in ['NOUN', 'PROPN'] and len(token.text) > 4]

    return keywords


# Example usage

video_id = get_youtube_video_id("https://www.youtube.com/watch?v=pQCJmxEOzhs")

transcript_result = get_transcript(video_id)

kw = get_keywords(transcript_result)
print(kw)
