import os

# from streamlit.proto.Components_pb2 import ComponentInstance
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'secret.json'
# import io
from google.cloud import texttospeech
import streamlit as st


def synthesize_speech(text, lang='日本語', gender='defalut'):
    gender_type = {
        'defalut': texttospeech.SsmlVoiceGender.SSML_VOICE_GENDER_UNSPECIFIED,
        'male': texttospeech.SsmlVoiceGender.MALE,
        'female': texttospeech.SsmlVoiceGender.FEMALE,
        'neutral': texttospeech.SsmlVoiceGender.NEUTRAL
    }
    lang_code = {
        '英語': 'en-US',
        '日本語': 'ja-JP'
    }

    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code=lang_code[lang], ssml_gender=gender_type[gender]
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    return response



st.markdown('** Apo cyber present **')
st.markdown('# 音声出力アプリ')

st.markdown('## データの準備')

input_potion=st.selectbox(
    'データを選択',
    ('直接入力', 'テキストファイル')
)

input_data=None

if input_potion=='直接入力' :
    input_data=st.text_area('こちらにテキストを入力してください', 'この際だからなんでも言っちゃえ。')
else:
    uploaded_file = st.file_uploader('テキストファイルをアップロードしてください。',['txt'])
    if uploaded_file is not None:
        content = uploaded_file.read()
        input_data=content.decode()

if input_data is not None:
    st.write('入力データ')
    st.write(input_data)

    st.markdown('## パラメータ設定')
    st.subheader('言語と話者の性別設定')
    lang=st.selectbox(
        '言語と選択して下さい',
        ('日本語', '英語')
    )
    gender=st.selectbox(
        '話者の性別を選択して下さい。',
        ('defalut','male','female','neutral')
    )
    text=input_data

st.write('音声生成')
st.write('こちらの文章で音声ファイルの生成ををおこないますか？')
if st.button('開始'):
    comment=st.empty()
    comment.write('開始します')
    response=synthesize_speech(text, lang, gender)
    st.audio(response.audio_content)
    comment.write('終了しました')
