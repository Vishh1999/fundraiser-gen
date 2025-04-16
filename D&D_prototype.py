from google.cloud import bigquery
from google.oauth2 import service_account
from openai import OpenAI
import os

# === Config ===
GOOGLE_FORM_LINK = "https://docs.google.com/forms/d/1Eowu2gF7Xo1ZKv9Pt26vBJJZCGe1h_pi7SNEIG6eH68/viewform?edit_requested=true"
SERVICE_ACCOUNT_PATH = "credentials.json"
PROJECT_ID = "accessible-intelligence-456411"
QUERY = "SELECT * FROM accessible-intelligence-456411.fundraising_form.responses"
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# === Setup BigQuery ===
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_PATH,
    scopes=[
        "https://www.googleapis.com/auth/cloud-platform",
        "https://www.googleapis.com/auth/drive"
    ]
)
_client = bigquery.Client(credentials=credentials, project=PROJECT_ID)
query_job = _client.query(QUERY)
result = query_job.result().to_dataframe().to_dict(orient='records')[-1]

# def responses(name, answer):
#     my_dict={}
#     answer=answer.loc[answer['What_is_your_name_']==name,:]
#     for column in answer:
#         for value in answer[column]:
#             my_dict[column]=value
#     return my_dict
#
# responses(input("Enter fundraiser's name: "), result)

# === Modified Text Prompt Function ===
def generate_text_prompt(data: dict) -> str:
    return f"""
You are a professional fundraising campaign writer with deep experience in crafting 
highly effective campaign descriptions.
Your task is to generate a compelling, emotionally engaging, and action-driven fundraising 
campaign description between 300–500 words.
Base your response on both the user inputs and proven patterns from successful campaigns. 
The campaign should be optimised for sharing via email and social media.

📌 Campaign Title: Fundraiser for {data['What_is_the_name_of_the_charity_or_friend_']}
🎯 Goal Amount: £{data['How_much_would_you_like_to_raise_']}
💬 Tone: Hopeful
🧠 Keywords: {data['What_are_your_reasons_for_raising_funds_']}, {data['How_will_the_funds_be_distributed_']}, 
{data['How_did_you_come_to_know_about_this_charity_or_friend_']}
📖 Background: {data['How_did_you_come_to_know_about_this_charity_or_friend_']}
🙌 Call to Action Style: Direct appeal

---
Context: {data['What_are_your_reasons_for_raising_funds_']}
Objectives: Raise £{data['How_much_would_you_like_to_raise_']} for {data['What_is_the_name_of_the_charity_or_friend_']} 
({data['Who_are_you_raising_money_for_']}).
Style: Clear and compassionate
Tone: Hopeful
Audience: Public donors and well-wishers

---

💡 Prompt Design Guidelines (learned from analysis of 500K+ campaigns):

Start with a short, emotionally powerful hook (ideal 80–140 characters)  
Clearly explain the problem and why it's urgent  
Describe how the funds will make a tangible impact  
Use specific, real-world imagery or stories (if available)  
Include social-proof-style encouragement (e.g., “Join 200+ supporters”)  
End with a direct, emotionally strong call to action  
Avoid jargon; write in a warm, conversational tone  
Use emotionally resonant verbs: support, build, create, protect, uplift  
If “Polish Mode” is enabled, emulate the tone of Kickstarter Staff Picks:
   - Clear structure
   - Professional grammar
   - Empowering tone

---

🎯 Output Requirements:

Must be a 300–500 word campaign description  
Include campaign name as the title  
Focus on readability, shareability, and human connection  
Text only — do not mention AI or the generation process  
The output should feel like it was written by a passionate fundraiser who knows the cause well
"""
# === GPT-4 Text Generator ===
def generate_campaign_text(prompt):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a professional fundraising copywriter."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    return response.choices[0].message.content

# === DALL·E 3 Image Prompt Builder ===
def generate_image_prompt(campaign_text: str, tone="hopeful", style="emotive", keywords=None) -> str:
    keywords_str = ", ".join(keywords) if keywords else ""
    return f"""
Context: This is a fundraising campaign visual.
Objective: Create an image that visually represents the emotional and thematic core of the following text.
Style: {style}
Tone: {tone}
Keywords: {keywords_str}
Audience: General public on social media and print platforms
Response: Generate a visual prompt description based on the following campaign text:

\"{campaign_text[:500]}...\"

The image should be emotionally impactful, metaphorically rich, and visually supportive of a fundraising cause.
"""

# === DALL·E 3 Image Generator ===
def generate_image_with_openai(prompt):
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1
    )
    image_url = response.data[0].url
    print(image_url)
    return image_url

# === Main Pipeline ===
def run_agents_pipeline(data: dict):
    text_prompt = generate_text_prompt(data)
    campaign_text = generate_campaign_text(text_prompt)

    print("\n=== Campaign Description ===\n")
    print(campaign_text)

    # Output to a text file
    with open("campaign_description.txt", "w", encoding="utf-8") as file:
        file.write(campaign_text)

    keywords = [
        data['What_are_your_reasons_for_raising_funds_'][0],
        data['How_will_the_funds_be_distributed_'][0],
        data['How_did_you_come_to_know_about_this_charity_or_friend_'][0]
    ]
    image_prompt = generate_image_prompt(campaign_text, tone="hopeful", style="compassionate", keywords=keywords)
    image_url = generate_image_with_openai(image_prompt)

    return campaign_text, image_prompt, image_url

campaign_description, visual_prompt, image_url = run_agents_pipeline(result)
