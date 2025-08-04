import asyncio
import streamlit as st
from .clients import get_mcp_client
from .agents import get_all_agents
from .supervisor import create_supervisor_graph
from .utils import format_agent_output, format_final_output
import time

async def run_analysis(query):
    client = get_mcp_client()
    tools = await client.get_tools()
    agents = await get_all_agents(tools)
    supervisor = create_supervisor_graph(agents)
    
    messages = []
    container = st.empty()
    
    async for chunk in supervisor.astream(
        {"messages": [{"role": "user", "content": query}]}
    ):
        new_messages = format_agent_output(chunk, last_message=True)
        messages.extend(new_messages)
        
        with container:
            st.subheader("Analysis Progress")
            for msg in messages:
                with st.expander(f"{msg['sender']} ({msg['timestamp']})"):
                    st.write(msg['content'])
            st.progress(min(len(messages) * 10, 100))
    
    return messages

def main():
    st.set_page_config(page_title="NSE Stock Advisor", layout="wide")
    st.title("📈 AI-Powered NSE Stock Recommendations")
    
    with st.sidebar:
        st.header("Configuration")
        st.caption("Powered by LangGraph & MCP Tools")
        st.divider()
        query = st.text_area("Analysis Request:", 
                            "Find promising NSE stocks for short-term trading with full analysis")
        
        if st.button("Run Analysis", type="primary"):
            with st.spinner("Processing..."):
                start_time = time.time()
                messages = asyncio.run(run_analysis(query))
                duration = time.time() - start_time
                
            st.success(f"Analysis completed in {duration:.2f} seconds")
            st.download_button(
                label="Download Report",
                data=format_final_output(messages),
                file_name="stock_analysis.md",
                mime="text/markdown"
            )
    
    st.subheader("Live Analysis Dashboard")
    st.caption("Agent outputs will appear here during processing...")

if __name__ == "__main__":
    main()