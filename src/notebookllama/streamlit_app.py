import streamlit as st
from openai import OpenAI
import os

st.title("💬 NVIDIA AI 聊天助手")
st.caption("✅ 部署成功！直接聊天")

# 读取配置
api_key = os.getenv("OPENAI_API_KEY")
base_url = os.getenv("OPENAI_BASE_URL")
model = os.getenv("OPENAI_MODEL", "moonshotai/kimi-k2.5")

# 初始化客户端
client = OpenAI(api_key=api_key, base_url=base_url)

# 聊天记录
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "你好！我是你的AI助手～"}
    ]

# 显示历史
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# 输入框
if prompt := st.chat_input("请输入你的问题..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # 请求AI
    response = client.chat.completions.create(
        model=model,
        messages=st.session_state.messages
    )
    reply = response.choices[0].message.content

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.chat_message("assistant").write(reply)
