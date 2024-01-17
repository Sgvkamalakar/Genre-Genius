import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import googletrans
from googletrans import Translator
import os
load_dotenv()

api_key=os.getenv("API_KEY")
# print(API_KEY)
st.set_page_config(page_title='Genre Genius', page_icon = 'favicon.png', initial_sidebar_state = 'auto')
# Sidebar code
with st.sidebar:
    # Here we take Gemini API as a Input from user
    # api_key = st.text_input("API Key *", type="password")
    # st.markdown("[Get Your API Key](https://makersuite.google.com/app/apikey)")

    # Select the type of Text Generation
    option = st.selectbox(
    'Choose the genre for text generation',
    ('Story Generation','Essay Generation'))
    if(option=="Story Generation"):
        req_type='Story'
    else:
        req_type='Essay'
    if(option=="Story Generation"):
        optioneg1 = st.selectbox(
        'Choose the preferred length for the Story',
        ('small -  approx 150 words', 'medium -  approx 350 words', 'long -  approx 500 words','extensive -  more than 800 words'))
        
    if(option=="Story Generation"):
         optioneg2 = st.selectbox(
        'Choose the tone of Story',
        ('Adventurous','Comedy','Educative','Fictional','Mystery','Non-Fictional','Romantic'))
         
    if(option=="Essay Generation"):
        optioneg1 = st.selectbox(
        'Choose the preferred length for the Essay',
        ('small -  approx 150 words', 'medium -  approx 350 words', 'long -  approx 500 words','extensive -  more than 800 words'))
        
    
    if(option=="Essay Generation"):
         optioneg2 = st.selectbox(
        'Choose the tone of Essay',
        ('Argumentative','Expository','Descriptive','Informative','Narrative','Persuasive'))
         
    default_lang="English"
    languages = ["Arabic","Bengali","English","French","German","Hindi","Indonesian","Japanese","Mandarin Chinese","Portuguese","Russian","Spanish","Swahili","Telugu","Urdu"]
    lang= st.selectbox('Choose the language',languages, index=languages.index(default_lang) if default_lang in languages else 0)     

    
    st.markdown("[Linkedin](https://www.linkedin.com/in/sgvkamlakar/)")
    st.markdown("[Github](https://github.com/sgvkamalakar)")

if 'Story' in option:
    icon='📖'
else:
    icon='📝' 
       
st.title(option+icon)    

def translate_text(text, target_lang_code):
    translator = Translator()
    translated_text = translator.translate(text, dest=target_lang_code)
    return translated_text


def generate(prompt,ip,lang):
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        language_codes = {"Arabic": "ar","Bengali": "bn","English": "en","French": "fr","German": "de","Hindi": "hi","Indonesian": "id","Japanese": "ja",
        "Mandarin Chinese": "zh-CN","Portuguese": "pt","Russian": "ru","Spanish": "es","Swahili": "sw","Telugu": "te","Urdu": "ur"}
        target_lang_code=language_codes[lang] 
        if ip.strip()!='':
            response = model.generate_content(prompt)
            if target_lang_code!='en':            
                translated_text=translate_text(response.text,target_lang_code)
                st.write(translated_text.text)
            else:
                st.success(response.text)
                # st.write()
        else:
            st.info("Don't forget to mention the topic! 😐")

            
    except Exception as e:
        error_msg=str(e)
        if "API_KEY_INVALID" in error_msg:
            st.error("Oops!🤨 It seems like the provided API Key is invalid")
            st.info("Please enter a valid API Key. 😉")

        elif "response.parts" in error_msg:
            st.error("⚠️ There was an issue processing your request due to a quick accessor problem.🫠")
            st.error("This might 🤔 be related to the Gemini, not 🥴 returning any candidates.")
            st.error("🔍 Check the response.prompt_feedback to see if the prompt was blocked.😶‍🌫️")
            
        elif "504 Deadline Exceeded" in error_msg:
            st.error("😵 We're experiencing high traffic at the moment🚦")
            st.info("Please try again after some time. 🕰️")       
        else:
            st.error("💀 There was an issue processing your request 😪")
            st.error(f"The reason 👉🏻 {error_msg}☠️")



 
if(option=="Story Generation" or option=="Essay Generation"):
    with st.form("myform"):
        ip=st.text_input(f"Mention topic of the {req_type} *")
        additional=st.text_input(f"Mention some description about the {req_type} (optional)")
            
        submitted = st.form_submit_button("Submit")
        prompt = f"""Write a {req_type} on the topic - {ip} with a {optioneg1} tone and mention the title for {req_type}. Here are some additional points regarding this -  {additional}. Structure your {req_type} with a clear introduction, actions and characters that support your story lines, and a strong climax and mention the sections. Ensure your writing is clear, concise, and engaging. Pay attention to tone given above , grammar, spelling, and punctuation with suitable emojis. Give me {req_type} {option} long """
        # if not api_key:
        #     st.info('Enter your API key 👀')
        if submitted:
            response=generate(prompt,ip,lang)

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

footer="""<style>
a:link , a:visited{
color: blue;
background-color: transparent;
}

a:hover,  a:active {
color: white;
background-color: transparent;
text-decoration: underline;
}

.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
background-color: #0e1117;
color: white;
text-align: center;
}
</style>
<div class="footer">
    <p>Developed with ❤ by <a href="https://www.linkedin.com/in/sgvkamalakar" target="_blank">Kamalakar</a></p>
</div>

"""
st.markdown(footer,unsafe_allow_html=True)