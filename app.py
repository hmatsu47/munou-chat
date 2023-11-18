import os
import boto3
import streamlit as st
from dotenv import load_dotenv
from langchain.embeddings import BedrockEmbeddings
from langchain.docstore.document import Document
from langchain.vectorstores.pgvector import PGVector

load_dotenv()

MAX_LENGTH = 300

CONNECTION_STRING = PGVector.connection_string_from_db_params(
    driver=os.environ.get("PGVECTOR_DRIVER", "psycopg2"),
    host=os.environ.get("PGVECTOR_HOST", "localhost"),
    port=int(os.environ.get("PGVECTOR_PORT", "5432")),
    database=os.environ.get("PGVECTOR_DATABASE", "postgres"),
    user=os.environ.get("PGVECTOR_USER", "postgres"),
    password=os.environ.get("PGVECTOR_PASSWORD", ""),
)
COLLECTION_NAME = "munou_goroku"

st.title("人工無能たいたん🧠🍥🌀")

# 会話履歴がない場合は初期化
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({"role": "assistant", "content": "よろしくね！"})

# 会話履歴を表示
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 入力欄を表示
prompt = st.chat_input("おはなししましょ！")

if prompt:
    trimed_prompt = prompt.strip()
    # 入力を表示
    with st.chat_message("user"):
        st.markdown(trimed_prompt)
    # 入力を会話履歴の末尾に追加
    st.session_state.messages.append({"role": "user", "content": trimed_prompt})
    response = "ごめんなさい、長すぎてよくわかりません！もうちょっと短い言葉で話してね！"
    # 文字数チェック
    if len(trimed_prompt) < MAX_LENGTH:
        # ベクターストアから応答を取得
        bedrock_client = boto3.client('bedrock-runtime', region_name="ap-northeast-1")
        embeddings = BedrockEmbeddings(
            client=bedrock_client,
            model_id="amazon.titan-embed-text-v1"
        )
        store = PGVector(
            collection_name=COLLECTION_NAME,
            connection_string=CONNECTION_STRING,
            embedding_function=embeddings,
        )
        docs = store.similarity_search_with_score(trimed_prompt)
        count = len(docs)
        add_flag = True
        if count == 0:
            # ベクターストアに文章がなければおうむ返しする
            response = trimed_prompt
        else:
            # 近い文章を返す
            response = docs[0][0].page_content
            if trimed_prompt == response:
                # すでに登録済みの文章と同じならベクターストアに登録しない
                add_flag = False
        if add_flag:
            # ベクターストアに入力を追加
            store.add_documents([Document(page_content=trimed_prompt)])
    # 人工無能の応答を表示
    with st.chat_message("assistant"):
        st.markdown(response)
    # 応答を会話履歴の末尾に追加
    st.session_state.messages.append({"role": "assistant", "content": response})