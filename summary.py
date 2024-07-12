from ftp_mgt import get_texts_from_folder
from openai import OpenAI
from decouple import config

foldername = "transcripts"


def summarize_transcripts():

    texts = get_texts_from_folder(foldername=foldername)

    for text in texts:
        print(text["text"])

    # Send transcript to openai compatible llm and revceive summary


"""
    client = OpenAI(
    api_key=config("summary_api_key"),
    base_url=config("summary_llm"))

    
    summary_system_content = config("summary_system_content")
    summary_user_content = config("summary_user_content").format(transcript=transcript)    
    
    chat_completion = client.chat.completions.create(
        json_mode=True,
        model=config("summary_model"),
        messages=[
            {"role": "system", 
            "content": summary_system_content},
            {"role": "user", 
            "content": summary_user_content}
        ]
    
    )    
    print(chat_completion)
       
        

    
    
"""
