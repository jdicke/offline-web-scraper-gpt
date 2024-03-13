

import os
import requests
from dotenv import load_dotenv
from transformers import AutoTokenizer, AutoModelForCausalLM
import streamlit as st
from bs4 import BeautifulSoup

# Load environment variables from .env file
load_dotenv()

# Load any necessary API credentials from environment variables
API_KEY = os.getenv("API_KEY")
# ... load other credentials if needed

# Load the model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("facebook/opt-iml-1.3b")
model = AutoModelForCausalLM.from_pretrained("facebook/opt-iml-1.3b")

# Function to generate a response
def generate_response(prompt, context="", max_tokens=256):
    input_text = f"{context} {prompt}"
    input_ids = tokenizer.encode(input_text, return_tensors="pt")
    output = model.generate(input_ids, max_length=max_tokens, do_sample=True, top_k=50, top_p=0.95, num_return_sequences=1)
    response = tokenizer.decode(output[0], skip_special_tokens=True)
    return response

# Function to scrape content from a URL
def scrape_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    content = soup.get_text()
    return content

# Streamlit app
def main():
    st.title("Local ChatGPT with URL Scraping")

    # Get user input
    prompt = st.text_area("Enter your prompt:", height=200)
    url = st.text_input("Enter a URL (optional):")

    if st.button("Generate Response"):
        if url:
            try:
                scraped_content = scrape_url(url)
                response = generate_response(prompt, context=scraped_content)
            except Exception as e:
                st.error(f"Error scraping URL: {e}")
                response = generate_response(prompt)
        else:
            response = generate_response(prompt)

        st.success(response)

if __name__ == "__main__":
    main()