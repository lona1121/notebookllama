import streamlit as st
import os
from openai import OpenAI
from PyPDF2 import PdfReader

st.set_page_config(page_title="文件对话AI", page_icon="📄")
st.title("📄 文件对话AI（上传文件直接聊天）")

# 读取你的NVIDIA配置
api_key = os.getenv("OPENAI_API_KEY")
base_url = os.getenv("OPENAI_BASE_URL")
model = os.getenv("OPENAI_MODEL", "moonshotai/kimi-k2.5")

client = OpenAI(api_key=api_key, base_url=base_url)

# 上传文件
uploaded_file = st.file_uploader("上传 PDF 文件", type="pdf")

# 提取PDF文字
def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# 存储文件内容
if uploaded_file:
    text = extract_text_from_pdf(uploaded_file)
    st.session_state["file_content"] = text
    st.success("✅ 文件上传成功！可以开始聊天了")

# 聊天记录
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "你好！请上传文件，我就能帮你解读内容～"}
    ]

# 显示聊天
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# 输入框
if prompt := st.chat_input("请输入你的问题..."):
    messages = []

    # 如果有文件，把文件内容放进对话
    if "file_content" in st.session_state:
        messages.append({
            "role": "user",
            "content": f"文件内容：{st.session_state['file_content'][:8000]}"
        })

    messages.append({"role": "user", "content": prompt})
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # AI回复
    response = client.chat.completions.create(model=model, messages=messages)
    reply = response.choices[0].message.content

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.chat_message("assistant").write(reply)
