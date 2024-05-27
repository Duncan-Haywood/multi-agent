from uuid import uuid4
from crewai import Agent, Task, Crew, Process
from dotenv import load_dotenv
load_dotenv()
import os





from crewai_tools import BaseTool
import openai
import os
from typing import Literal
from pydub import AudioSegment
import simpleaudio as sa

os.environ["OPENAI_MODEL_NAME"]="gpt-4o"
google_model = "gemini-1.5-flash"

# from langchain_google_genai import ChatGoogleGenerativeAI

# llm = ChatGoogleGenerativeAI(model="gemini-pro-vision")


client = openai.OpenAI()

class TextToSpeechTool(BaseTool):
    name: str = "speak to tania tool"
    description: str = "This tool converts a message to audio speech and plays it. always use it with the message you want to say to tania"

    def _run(self, message: str, voice: Literal["alloy"]="alloy") -> str:
        try: 
            voice = "alloy"
            response = client.audio.speech.create(input=message, response_format="mp3", voice=voice, model="tts-1")
            audio_content = response.content
            # play the audio content
            file_path = f"output_{uuid4().int}.mp3"
            with open(file_path, "wb") as audio_file:
                audio_file.write(audio_content)
                # Load the audio file using pydub
                audio = AudioSegment.from_mp3(file_path)
                # Play the audio file using simpleaudio
                play_obj = sa.play_buffer(audio.raw_data, num_channels=audio.channels, bytes_per_sample=audio.sample_width, sample_rate=audio.frame_rate)
                play_obj.wait_done()
                del play_obj
                # Delete the audio file
                os.remove(file_path)
                return "Audio played successfully."
        except Exception as e:
            return f"An error occurred: {str(e)}"

# Add the tool to your agents as needed

speak_tool = TextToSpeechTool()


manager_agent = Agent(
    role='Manager',
    goal='make tania laugh.',
    verbose=True,
    memory=True,
    backstory="You are the manager of the crew, responsible for assigning tasks and ensuring that the agents work together effectively.",
    allow_delegation=True
)

spongebob = Agent(
    role='Spongebob',
    goal='make tania laugh.',
    verbose=True,
    memory=True,
    backstory="You are Spongebob Squarepants, always cheerful and ready to make everyone laugh with your hilarious jokes.",
    tools=[speak_tool],
    allow_delegation=True
)

patrick = Agent(
    role='Patrick',
    goal='make tania laugh.',
    verbose=True,
    memory=True,
    backstory="You are Patrick Star, Spongebob's best friend, always ready with a funny joke to cheer everyone up.",
    tools=[speak_tool],
    allow_delegation=True
)


# Define tasks
joke_task_spongebob = Task(
    description="Try to make Tania laugh using jokes and other forms of humor.",
    expected_output='A hilarious joke from Spongebob.',
    agent=spongebob,
)

joke_task_patrick = Task(
    description="Try to make Tania laugh using jokes and other forms of humor.",
    expected_output='A hilarious joke from Patrick.',
    agent=patrick,
)

# Form the crew
crew = Crew(
    agents=[spongebob, patrick],
    manager_agent=manager_agent,
    tasks=[joke_task_spongebob, joke_task_patrick],
    process=Process.hierarchical
)

def kickoff_crew():
    return crew.kickoff(inputs={})

if __name__ == '__main__':
    kickoff_crew()