AI-Powered Fundraising Campaign Generator
=========================================

A multi-agent AI system that turns Google Form responses into persuasive fundraising campaign descriptions and poster-style images. Built using GPT-4o and DALL·E 3, it helps users generate emotionally resonant donation pages with just a few inputs.

What It Does
------------

This project:
- Collects form data from Google BigQuery (connected to a Google Form)
- Generates a fundraising campaign description using GPT-4o (or GPT-3.5-turbo)
- Creates a matching poster-style image using DALL·E 3
- Outputs the campaign description and a shareable image URL

Note: The Google Form link used to collect responses is defined as a variable in the code.

Powered By
----------

- GPT-4o — for writing campaign descriptions
- DALL·E 3 — for AI image generation
- Google BigQuery — for accessing form responses
- Python 3.10+

Project Structure
-----------------

- ├── D&D_prototype.py       # Main pipeline script
- ├── credentials.json       # Google Cloud service account key (NOT tracked in Git)
- ├── README.txt             # This file

Requirements
------------

Install the required Python packages:

    pip install openai pandas google-cloud-bigquery

API Keys & Credentials
----------------------

OpenAI API Key:

- Get your key from: https://platform.openai.com/account/api-keys
- Export it in your terminal or set in code:

      export OPENAI_API_KEY="your-api-key"

Google Cloud BigQuery:

1. Create a service account with BigQuery access
2. Download the JSON credentials
3. Save it as `credentials.json` in the project directory
4. Ensure access to the BigQuery dataset linked to your Google Form

How to Clone and Run the Project
--------------------------------

Follow these steps to set up and run the AI-powered fundraising generator:

1. Clone the repository:

    git clone https://github.com/Vishh1999/fundraiser-gen.git
    cd fundraiser-gen

2. Install the dependencies:

    pip install openai pandas google-cloud-bigquery

3. Set your OpenAI API key:

    export OPENAI_API_KEY="your-api-key"

4. Place your BigQuery credentials file in the root directory and name it:

    credentials.json

5. Run the script:

    python D&D_prototype.py

What It Will Do:
----------------

- Pull the latest Google Form response from BigQuery
- Generate a campaign description using GPT-4o
- Generate a matching poster-style image using DALL·E 3
- Print:
  - The campaign text
  - The image prompt
  - The DALL·E-generated image URL

Sample Use Case
---------------

Someone submits a Google Form to raise funds for a friend undergoing treatment. This tool:
- Generates a heartfelt 400–500 word campaign message
- Creates a visual poster prompt
- Returns a shareable image URL ready for social media or donation platforms

Example Output
--------------

Campaign Title:
"Help James Thompson Fight Lymphoma"

Generated Campaign Description:
A message describing James' diagnosis, medical challenges, and a call to support.

Image Prompt:
"Hopeful poster showing a man surrounded by supportive hands, warm tones, medical themes subtly illustrated."

Total Output:
Campaign text + Image prompt + Poster image URL

Future Additions
----------------

- Web UI (Streamlit)
- CSV/PDF export
- Batch generation of multiple campaigns
- Token usage and cost summary

Contributing
------------

Pull requests and suggestions welcome!

License
-------

MIT License

Acknowledgements
----------------

Thanks to:
- OpenAI
- Google Cloud
- Everyone using tech to make a difference