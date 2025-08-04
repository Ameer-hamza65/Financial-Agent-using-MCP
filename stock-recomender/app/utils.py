from langchain_core.messages import convert_to_messages

def format_agent_output(update, last_message=False):
    if isinstance(update, tuple):
        _, update = update
    
    output = []
    for node_name, node_update in update.items():
        messages = convert_to_messages(node_update["messages"])
        if last_message:
            messages = messages[-1:]
        
        for msg in messages:
            output.append({
                "sender": node_name,
                "content": msg.content,
                "timestamp": msg.additional_kwargs.get("timestamp", "")
            })
    
    return output

def format_final_output(messages):
    return "\n\n".join(
        f"**{msg['sender']}**:\n{msg['content']}" 
        for msg in messages
    )