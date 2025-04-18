import os
# 修改了urllib文件夹下request 的ProxySever参数 具体是proxyServer: 可以通过ctrl+F 定位到修改的位置
import streamlit as st
import base64
from openai import OpenAI

client = OpenAI(
    api_key="sk-fIRlLTNJO7EpNN1Z1dB3Af71144b450792Fb7cBe12Bd898d",
    base_url="https://free.v36.cm/v1/",
    default_headers = {"x-foo": "true"}
)


# 大模型给出的答案
def chat_stream():
    # 发送流式请求给 OpenAI 服务器
    response = client.chat.completions.create(
        # 公司内部，一般接入的是自己的模型（垂直模型、行业模型）
        # model='net-gpt-3.5-turbo',  # 接入的大模型  gpt-4o mini ,接入 最新的产品 能力
        model='gpt-4o-mini', 
        messages=st.session_state.messages_history,
        temperature=0,
        stream=True  # 设置 stream=True
    )
    return response


def init_chat():
    st.session_state.messages = [{
        "role": "assistant",
        "content": "hello～ 很高兴遇见你！尽情提问吧！"
    }]
    st.session_state.messages_history = [{
        "role": "system",
        "content": st.session_state.system_message
    }]

st.markdown("""
<style>.st-emotion-cache-1c7y2kd {flex-direction: row-reverse; text-align:right }</style>
""", unsafe_allow_html=True)
# with open('pong.png') as image_file:
#     encoded_image = base64.b64encode(image_file.read()).decode()
image_path = 'pong.png'
# 左侧
with st.sidebar:
    # 支持 markdown 语法
    st.markdown(f"""
    <center>
    <img src='data:image/png;base64,{base64.b64encode(open(image_path, "rb").read()).decode()}'  height='100' width='100' border-radius = 50%/>
    <h1> hellobot<h1/>
    </center>
    """, unsafe_allow_html=True)

    # 角色定义输入框 System Message
    system_message = st.text_area("角色定义", "你是一个身经百战的码农。", on_change=init_chat, key='system_message')

    # 创造力调节 Temperature
    temperature = st.slider("创造力调节", min_value=0.0, max_value=2.0, value=1.0, step=0.1, help='值越大约具有创造力',
                            format="%.1f")

    if st.button("🧹 清除聊天记录"):
        init_chat()


# 右侧
# st.title("hellobot")

if "messages_history" not in st.session_state:
    st.session_state.messages_history = [
        {"role": "system", "content": system_message}
    ]

# 初始化界面的聊天列表
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "很高兴遇见你！hellobot有问必答！"
        }
    ]

# 显示对话的历史列表
for message in st.session_state.messages:
    # 聊天窗口
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 用户输入
user_query = st.chat_input("说点什么...")
if user_query:
    # 显示用户输入的内容到聊天窗口
    with st.chat_message("user"):
        st.write(user_query)
    # 在聊天窗口输出用户输入的问题
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_query
        }
    )
    st.session_state.messages_history.append({
        "role": "user",
        "content": user_query
    })

    with st.chat_message("assistant"):
        # 转圈等待
        with st.spinner(""):
            # AI 的回复 ， 接入了 大模型
            response = chat_stream()
            # 创建显示消息的容器
            message_placeholder = st.empty()
            # AI 的答案
            ai_response = ""
            for chunk in response:
                # 从流响应中获得AI的答案
                if chunk.choices and chunk.choices[0].delta.content:
                    ai_response += chunk.choices[0].delta.content
                    # 显示AI的答案
                    message_placeholder.markdown(ai_response + "▌")

            # 在聊天窗口输出完整的 AI 答案
            message_placeholder.markdown(ai_response)
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": ai_response
                }
            )
            st.session_state.messages_history.append({
                "role": "assistant",
                "content": ai_response
            })
