import streamlit as st
import anthropic

st.title("PGA Tour Predictor")

question = st.text_area("What do you want to know?", "Who are the best PGA Tour players right now?", height=100)

if st.button("Run", type="primary"):
    client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
    with st.spinner("Thinking..."):
        response = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=1024,
            messages=[{"role": "user", "content": question}]
        )
        st.markdown(response.content[0].text)
