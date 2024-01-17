import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
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
    lengths=['Brief - around 150 words', 'Moderate - around 350 words', 'Substantial - around 500 words', 'Extensive - over 800 words']    
    story_tone=['Adventurous','Comedy','Educative','Fictional','Mystery','Non-Fictional','Romantic']
    essay_tone=['Argumentative','Expository','Descriptive','Informative','Narrative','Persuasive']
    if(req_type=="Story"):
        opt1 = st.selectbox('Choose the preferred length for the Story',lengths)
        
    if(req_type=="Story"):
         opt2 = st.selectbox('Choose the tone of Story',story_tone)
         
    if(req_type=="Essay"):
        opt1 = st.selectbox(
        'Choose the preferred length for the Essay',lengths)
        
    if(req_type=="Essay"):
         opt2 = st.selectbox(
        'Choose the tone of Essay',essay_tone)
         
    default_lang="English"
    languages = ["Arabic","Bengali","English","French","German","Hindi","Indonesian","Italian","Japanese","Korean","Mandarin Chinese","Portuguese","Russian","Spanish","Swahili"]
    lang= st.selectbox('Choose the language',languages, index=languages.index(default_lang) if default_lang in languages else 0)     
    
    st.markdown("[Connect with me on Linkedin](https://www.linkedin.com/in/sgvkamlakar/)")
    st.makrdown("[Source code](https://github.com/Sgvkamalakar/Genre-Genius)")
    st.markdown("[Github](https://github.com/sgvkamalakar)")

if 'Story' in option:
    icon='📖'
else:
    icon='📝' 
       
st.title(option+icon)    

def generate(prompt,ip,lang):
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        if ip.strip()!='':
            response = model.generate_content(prompt)
            st.success("Genre Genius nailed it 🎉")
            st.success(f"Your {req_type} is ready !😄✨")
            st.write(response.text)
    
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



 
if(req_type=="Story" or req_type=="Essay"):
    with st.form("myform"):
        ip=st.text_input(f"Mention topic of the {req_type} *")
        additional=st.text_input(f"Mention some description about the {req_type} (optional)")
            
        submitted = st.form_submit_button("Submit")
        prompt = f"""Write a {req_type} on the topic - {ip} with a {opt1} tone in {lang} language and mention the title for {req_type}. Here are some additional points regarding this -  {additional}. Structure your {req_type} with a clear introduction, actions and characters that support your story lines, and a strong climax and mention the sections. Ensure your writing is clear, concise, and engaging. Pay attention to tone given above , grammar, spelling, and punctuation with suitable emojis. Give me {req_type} {option} long """
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
