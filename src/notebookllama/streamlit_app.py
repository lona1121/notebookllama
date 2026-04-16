import streamlit as st
import os

st.title("✅ 文件对话AI（直接可用）")
st.write("上传文件后，直接对内容提问")

# 上传文件
uploaded_file = st.file_uploader("上传 TXT 文件", type="txt")

# 聊天
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "你好！上传文件就能提问～"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# 读取文件
file_content = ""
if uploaded_file:
    file_content = uploaded_file.read().decode("utf-8", errors="ignore")
    st.success("✅ 文件上传成功")

# 输入框
prompt = st.chat_input("输入你的问题...")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    reply = f"我收到你的问题：{prompt}\n\n文件内容预览：\n{file_content[:500]}..."
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()
