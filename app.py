from dotenv import load_dotenv

load_dotenv() #will load all environment variables from our .env

import streamlit as st
import os 
from PIL import Image
import google.generativeai as genai 

genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))
model=genai.GenerativeModel('gemini-pro-vision')

#Function for gemini pro
def get_gemini_response(input,image,prompt):
    response = model.generate_content([input,image[0],prompt])
    return response.text

#Function for converting image to bytes
def input_image_details(uploaded_file):
    if uploaded_file is not None:
        #Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type, #getting the mime type of the uploaded image
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("File was not uploaded")

#Streamlit setup
st.set_page_config(page_title= "📄Cross-Language Invoice Scanner")

st.header("Cross-Language Invoice Scanner")
user_input = st.text_input("Ask your question here: ", key = "user_input")
uploaded_file = st.file_uploader("Provide an image for the invoice", type=["jpg","jpeg","png"])
image=""

if uploaded_file is not None:
    image=Image.open(uploaded_file)
    st.image(image, caption = "Uploaded Image", use_column_width = True)

submit = st.button("Submit Question")

input_prompt="""
You are an expert in understanding invoices. User will upload images of the invoices 
and you will answer questions about the invoices
"""

#If submit is clicked
if submit:
    image_data = input_image_details(uploaded_file)
    response = get_gemini_response(input_prompt,image_data,user_input)
    st.subheader("Answer to your question:")
    st.write(response)


