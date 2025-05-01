import string
import random
import secrets
import re
import os
import bcrypt
import africastalking
import streamlit as st 
import google.generativeai as genai


from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))

africastalking.initialize(
    username='EMID',
    api_key = os.getenv("AT_API_KEY")
)

sms = africastalking.SMS
airtime = africastalking.Airtime
voice = africastalking.Voice

def send_sms(phone_number, otp_sms):
    # amount = "10"
    # currency_code = "KES"

    recipients = [f"+254{str(phone_number)}"]

    # airtime_rec = "+254" + str(phone_number)

    print(recipients)
    print(phone_number)

    # Set your message
    message = f"{otp_sms}";

    # Set your shortCode or senderId
    sender = 20880

    try:
        # responses = airtime.send(phone_number=airtime_rec, amount=amount, currency_code=currency_code)
        response = sms.send(message, recipients, sender)

        print(response)

        # print(responses)

    except Exception as e:
        print(f'Houston, we have a problem: {e}')

    st.toast(f"OTP Sent Successfully")


def welcome_message(first_name, phone_number):

    recipients = [f"+254{str(phone_number)}"]

    print(recipients)
    print(phone_number)

    # Set your message
    message = f"Hi {first_name}, welcome to ExposHer! We're excited to have you join our sisterhood of innovators, leaders, and changemakers. \n#WomenWhoLead";

    # Set your shortCode or senderId
    sender = 20880

    try:
        response = sms.send(message, recipients, sender)

        print(response)

    except Exception as e:
        print(f'Houston, we have a problem: {e}')

    st.toast(f"Account Created Successfully")



def make_call(phone_number):    
  
  # Set your Africa's Talking phone number in international format
    callFrom = "+254730731123"
  
  # Set the numbers you want to call to in a comma-separated list
    callTo   = [f"+254{str(phone_number)}"]
    
    try:
  # Make the call
        result = voice.call(callFrom, callTo)
        # print (result)
        return result
    except Exception as e:
        # print ("Encountered an error while making the call:%s" %str(e))
        return f"Encountered an error while making the call:%s" %str(e)



def generate_otp(length=6):
    characters = string.ascii_uppercase + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))



def check_and_encrypt_password(password: str, confirm_password: str):
    
    if password != confirm_password:
        return st.error("Error: Passwords do not match!")

    if len(password) < 8:
        return st.error(f"Error: Password must be at least 8 characters long!")
    
    if not re.search(r"[A-Z]", password):
        return st.error(f"Error: Password must contain at least one uppercase letter!")
    
    if not re.search(r"\d", password):
        return st.error(f"Error: Password must contain at least one number!")
    
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return st.error(f"Error: Password must contain at least one special character!")

    # Encrypt password using bcrypt
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    return st.text_input(label='Encrypted password', value=hashed_password.decode(), type='password')



def sheroes_context(prompt):

    model = genai.GenerativeModel("gemini-1.5-flash", 

        system_instruction = f"""
        
            You are a professional researcher generating rich, organized, and educational content about influential women around the world.

            Given the following female-led subsector: **{prompt}**, randomly select **one well-known or impactful woman** who has made a difference in this area globally.

            Return the output in **Markdown format** and strictly follow this structure:

            ---

            ### 🧾 Overview
            - ##### Name of the iconic woman
            - Introduce the selected woman (2–3 lines).
            - State her connection to the **{prompt}** and why she stands out.

            ### 🧠 Key Achievements
            - List 3–5 major accomplishments using bullet points.
            - Include notable years, awards, and pivotal actions.

            ### 📌 Notable Contributions
            - Write a brief paragraph on her specific work and how it advanced the subsector.
            - Use **bold** and *italics* to highlight significant themes or phrases.

            ### 🌍 Global Impact or Legacy
            - Describe how her influence shaped global perspectives, policies, or communities.

            ### 🔍 Quick Facts
            - Birthplace:  
            - Birth/Death (if applicable):  
            - Known For:  
            - Awards/Nominations:  
            - Affiliated Movements/Organizations:  

            ### 💡 Did You Know?
            - Provide a surprising, quirky, or inspiring fun fact about her life or work.

            ---

            🔄 The woman must be **randomly selected** from the given subsector and should reflect **diversity across countries and industries**.  
            🎯 Avoid generic or overly long content. Focus on structure, clarity, and relevance.

            """

            )


    response = model.generate_content(
        prompt,
        generation_config = genai.GenerationConfig(
        max_output_tokens=1000,
        temperature=0.1, 
      )
    
    )


    
    return response.text



