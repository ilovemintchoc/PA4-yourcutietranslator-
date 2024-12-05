import streamlit as st
import pandas as pd
import openai
import json

#sidebar API key
with st.sidebar:
    st.title(':tulip: OpenAI :rainbow[_yourcutietraslator_]')
    user_api_key = st.text_input('Enter OpenAI API key:', type='password')
    client = openai.OpenAI(api_key=user_api_key)
    if not client:
        st.warning('Please enter your API key!', icon='⚠️')
    else:
        st.success('Ready to help!', icon='☺️')
        
st.title("What could :rainbow[yourcutietranslator] do?🧚🏻‍♀️")
st.markdown("""She is your professional translator and writer who specializes in English, Thai, Korea and Japanese. She can translate English words to ***Thai***, ***Korea*** ***and*** ***Japanese***. 
            Don't hesitate to call for her help! ><""")

st.divider()

#prompt for text input
prompt = """ Act as a translator who is professional in English, Thai, Korea and Japanese. You will receive an English word,
and your job is to label a parts of speech of that word and translate that word to Thai, Korea, and Japanese. 
Also always provide the user 5 synonyms of that word in each languages(English,Thai,Korea,Japanese) in the same row.
Always provide the pronunciation of each word.
If you receive an English word that is no synonym, you can provide the user only the traslated word in Thai, Korea,and Japanese.
List the traslated word in a JSON array. 
The list should include the following 5 fields:
- ENG word: the English word that you recieved from the user and its parts of speech
- ENG synonyms: 5 synonyms in English of the English word in one row and audio how to pronouce each word
- THAI word: a Thai word that translated from the English word
- THAI synonyms: 5 synonyms in Thai of the Thai word that translated from the English word in one row and audio how to pronouce each word
- KOREA word: a Korea word that translated from the English word
- KOREA synonyms: 5 synonyms in Korea of the Korea word that translated from the English word in one row and audio how to pronouce each word
- JPN word: a Japanese word that translated from the English word
- JPN synonyms: 5 synonyms in Japanese of the Japanese word that translated from the English word in one row and audio how to pronouce each word
"""
#text input
st.title("Learn more from one word!")
user_input = st.text_input("Type an English word", 'Sad')


if st.button('Submit'):
    messages_so_far = [
        {"role": "system", "content": prompt},
        {'role': 'user', 'content': user_input},
    ]
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.9,
        messages=messages_so_far
    )
    st.markdown('**AI response:**')
    vocabs_dictionary = response.choices[0].message.content

    vd = json.loads(vocabs_dictionary)
    vd = {k: [v] for k, v in vd.items()}
    print (vd)
    vocab_df = pd.DataFrame.from_dict(vd)
    st.table(vocab_df)

st.divider()


#prompt for creating input
for_file_prompt = """ Act as a writer who is professional in English, Thai, Korea and Japanese. 
You will receive a text from the user in this pattern: "Create a [Genres of story] story".
Your job is to create the short story in 4 languages(English,Thai,Korea,Japanese).
Output should be:
A Title of the story in english
English: a story in English
Thai: The same story in Thai
Korea: Tha same story in Korea
Japanese: The same story in Japanese
Do not forget that the story must have only 200 words and using specific word.
Always use the specific word and other relating word. Highlight 20 words that are used frequently.
Seperate the output to 2 parts:
1.Story 
2.Table of vocabulary containing the list below. 
List all 20 words in a Pandas dataframe.
The dataframe should include the following 5 columns:
- ENG word: the English word that you recieved from the user and its parts of speech
- ENG synonyms: 5 synonyms in English of the English word in one row and audio how to pronouce each word
- THAI word: a Thai word that translated from the English word
- THAI synonyms: 5 synonyms in Thai of the Thai word that translated from the English word in one row and audio how to pronouce each word
- KOREA word: a Korea word that translated from the English word
- KOREA synonyms: 5 synonyms in Korea of the Korea word that translated from the English word in one row and audio how to pronouce each word
- JPN word: a Japanese word that translated from the English word
- JPN synonyms: 5 synonyms in Japanese of the Japanese word that translated from the English word in one row and audio how to pronouce each word
Do not forget to return it as table
"""

#creating input
st.title("Let's be more creative.📝")
story_user_input = st.text_input(
    "Create your own story in 4 languages. By using this pattern: Create a [Genres of story] story about [specific word] in 4 languages",
    "Create a fantasy story about sun in 4 languages"
)

if st.button('Create'):
    messages_so_far = [
        {"role": "system", "content": for_file_prompt},
        {"role": "user", "content": story_user_input},
    ]
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.9,
        messages=messages_so_far
    )

    # Display AI response
    st.markdown('**AI response:**')
    story = response.choices[0].message.content
    st.write(story)  # Display the story
  
   