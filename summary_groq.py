from ftp_mgt import get_texts_from_folder, save_text_to_file
from groq import Groq, GroqError
from decouple import config
import time
from openai_instructions import summary_system_content, summary_user_content
from tqdm import tqdm

foldername = "transcripts"

client = Groq(api_key=config("groq_api_key"))


def summarize_transcripts(model):

    texts = get_texts_from_folder(foldername=foldername)

    for text in tqdm(texts, desc="Summarizing transcripts", total=len(texts)):
        response = None
        transcript = text["text"]
        tqdm.write("*****************************************************")
        tqdm.write(text["name"])
        # Send transcript to openai compatible llm and revceive summary

        # TODO Compress the tokens

        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": summary_system_content},
                    {
                        "role": "user",
                        "content": summary_user_content.format(transcript=transcript),
                    },
                ],
            )

        except GroqError as e:
            tqdm.write(f"OpenAI API error: {e}")

        except Exception as e:
            tqdm.write(f"Error: {e}")
            continue

        message = response.choices[0].message.content

        tqdm.write(message)
        tqdm.write("\n*****************************************************")

        if not message.lower() in ["none", "tradingview"]:
            save_text_to_file(message, text["name"], model)

        time.sleep(30)
