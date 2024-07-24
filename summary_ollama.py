from ftp_mgt import get_texts_from_folder, save_text_to_file
import ollama
from tqdm import tqdm

from decouple import config
import time
from openai_instructions import summary_system_content, summary_user_content

foldername = "transcripts"


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
            response = ollama.chat(
                model=model,
                messages=[
                    {"role": "system", "content": summary_system_content},
                    {
                        "role": "user",
                        "content": summary_user_content.format(transcript=transcript),
                    },
                ],
            )

        except ollama.ResponseError as e:
            tqdm.write(f"ollama API error: {e}")

        except Exception as e:
            tqdm.write(f"Error: {e}")
            continue

        message = response["message"]["content"]

        tqdm.write(message)
        tqdm.write("\n*****************************************************")

        save_text_to_file(message, text["name"], model)
