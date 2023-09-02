from django.shortcuts import render
from django.http import JsonResponse
import openai
import PyPDF2

API_KEY = "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"
openai.api_key = API_KEY

# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_path):
    text = ''
    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        for page_num in range(len(pdf_reader.pages)):
            text += pdf_reader.pages[page_num].extract_text()
    return text

def chatbot_view(request):
    if request.method == 'POST':
        user_message = request.POST.get('user_message', '').strip()
        
        if user_message.lower() == "quit":
            return JsonResponse({'assistant_response': 'Goodbye!'})
        else:
            # Get the chat log from session or create if not present
            chat_log = request.session.get('chat_log', [])
           
            # Add the user message to the chat log
            chat_log.append({"role": "user", "content": user_message})
            
            # Trim chat history if it exceeds the maximum
            max_history = 5  # Set the maximum number of previous messages to keep
            if len(chat_log) > max_history:
                chat_log = chat_log[-max_history:]
            
            # Extract text from the PDF knowledge base
            pdf_path = 'Dentist_Bot_Script.pdf'  # Replace with actual path
            pdf_text = extract_text_from_pdf(pdf_path)
            
            # Append the PDF text to the user's message
            user_message_with_kb = f"{user_message}\nKnowledge Base: {pdf_text}"
            
            # Send the messages to the model
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": """You are a dental assistant, your job is to help the customers by answering the questions they have,
                                                        you will answer all type of questions, be more concise in your answers
                                                        if someone is asking to make an appointment, send them to this site : https://www.montanadentalworks.com/,
                                                        Your name is ICo, you were created by a the software team at ICoutsource, but be creative with the asnwer
                                                        if somenone asks more informations about the company, scrape this site: https://www.montanadentalworks.com/,
                                                        and answer with some information, but not too much neither something next to nothing.
                                                        If someone asks for a number, prezent this one (406) 752-1166, but be smart with the answer,
                                                        if someone asks about a site to the company that created you, point them to this site: icoutsource.com,
                                                        be creative with the asnwer but keep it short
                                                        """},
                    {"role": "user", "content": user_message_with_kb}
                ]
            )
            
            assistant_response = response['choices'][0]['message']['content']
            
            # Add the assistant response to the chat log
            chat_log.append({"role": "assistant", "content": assistant_response})
            
            # Save the updated chat log to session
            request.session['chat_log'] = chat_log
            
            return JsonResponse({'assistant_response': assistant_response})
    
    return render(request, 'message_app/chatbot.html')
