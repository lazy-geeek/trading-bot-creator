from openai import OpenAI

from decouple import config

client = OpenAI(
    api_key=config("summary_api_key"),
    base_url=config("summary_llm")
)

def summarize_transcript(transcript):
    #Send transcript to openai and revceive summary
    
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
       
        
summarize_transcript("Meine Idee")
    
    
    