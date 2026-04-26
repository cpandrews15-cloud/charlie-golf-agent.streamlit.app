import streamlit as st
import anthropic

st.title("PGA Tour Predictor")
st.caption("Powered by Claude AI + live web search")

question = st.text_area("What do you want to know?", "Predict the top 10 finishers for next weeks PGA Tour event with scores.", height=100)

if st.button("Run prediction", type="primary"):
    client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
    messages = [{"role": "user", "content": question}]
    search_list = []
    search_display = st.empty()
    with st.spinner("Claude is searching the web..."):
        while True:
            response = client.messages.create(
                model="claude-sonnet-4-5",
                max_tokens=4096,
                tools=[{"type": "web_search_20250305", "name": "web_search"}],
                system="You are an expert PGA Tour analyst. Search the web for current tournament info, player form, odds, and stats. Give detailed predictions with a numbered leaderboard and scores.",
                messages=messages
            )
            if response.stop_reason == "end_turn":
                for block in response.content:
                    if hasattr(block, "text"):
                        st.markdown(block.text)
                break
            if response.stop_reason == "tool_use":
                messages.append({"role": "assistant", "content": response.content})
                tool_results = []
                for block in response.content:
                    if block.type == "tool_use":
                        search_list.append(block.input.get("query", ""))
                        search_display.info("Searching: " + " | ".join(search_list))
                        tool_results.append({"type": "tool_result", "tool_use_id": block.id, "content": "search completed"})
                messages.append({"role": "user", "content": tool_results})
