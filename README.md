# IronHeart

**IronHeart is a Python-based voice assistant designed to simplify your daily tasks through voice commands. It utilizes advanced technologies for speech recognition, text-to-speech, and AI-driven responses to enhance user interaction.**


**Features**

**Voice Commands**: Control various actions like opening websites, searching YouTube, and asking questions.

**Speech Recognition**: Converts spoken language into text using Google Speech Recognition.

**Text-to-Speech**: Provides spoken feedback and responses using the pyttsx3 library.

**YouTube Search**: Searches and plays videos from YouTube.

**AI Responses**: Generates and summarizes responses using the Google Gemini API and Hugging Face transformers.

# Installation

**Clone the Repository:**

git clone https://github.com/memonriyaz/IronHeart.git

cd IronHeart
<hr>
**Set Up a Virtual Environment**:

python -m venv env

source env/bin/activate  # On Windows use: env\Scripts\activate

**Install Dependencies:**

pip install -r requirements.txt

**Set Up API Keys**

Replace the placeholder API keys in main.py with your own Google API keys:

gemini_api_key = 'YOUR_GOOGLE_GEMINI_API_KEY'

api_key_youtube = 'YOUR_YOUTUBE_API_KEY'

# Usage

**Run the Assistant**

Start the voice assistant:

python main.py

**Give Commands**

To open a website: "Open example.com"

To play a YouTube video: "Play [video name] on YouTube"

To ask a question: "[your question]"

The assistant will respond accordingly and perform the requested actions.
