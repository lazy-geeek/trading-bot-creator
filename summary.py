from ftp_mgt import get_texts_from_folder
from openai import OpenAI, OpenAIError
from groq import Groq, GroqError
from decouple import config
import time
from openai_instructions import summary_system_content, summary_user_content

foldername = "transcripts"

client = Groq(api_key=config("groq_api_key"))


def summarize_transcripts():

    texts = get_texts_from_folder(foldername=foldername)

    for text in texts:
        response = None
        transcript = text["text"]

        # Send transcript to openai compatible llm and revceive summary

        try:
            response = client.chat.completions.create(
                model=config("summary_model"),
                messages=[
                    {"role": "system", "content": summary_system_content},
                    {
                        "role": "user",
                        "content": summary_user_content.format(transcript=transcript),
                    },
                ],
            )

        except OpenAIError as e:
            print(f"OpenAI API error: {e}")

        except Exception as e:
            print(f"Error: {e}")
            continue

        message = response.choices[0].message.content

        print("*****************************************************")
        print(message)

        time.sleep(10)
