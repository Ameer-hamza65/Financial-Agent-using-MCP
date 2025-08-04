from langgraph_supervisor import create_supervisor
from langchain.chat_models import init_chat_model
from config import Config

def create_supervisor_graph(agents):
    supervisor_model = init_chat_model(Config.MODEL_NAME, api_key=Config.OPENAI_API_KEY)
    
    return create_supervisor(
        model=supervisor_model,
        agents=list(agents.values()),
        prompt=(
            "Supervisor managing 4 specialized agents:\n"
            "1. stock_finder_agent: Identifies promising NSE stocks\n"
            "2. market_data_agent: Fetches market data\n"
            "3. news_analyst_agent: Analyzes news sentiment\n"
            "4. price_recommender_agent: Generates trade recommendations\n\n"
            "Workflow Rules:\n"
            "- Execute agents sequentially\n"
            "- Do not parallelize agent calls\n"
            "- Complete full analysis cycle\n"
            "- Final output must include trading recommendations"
        ),
        add_handoff_back_messages=True,
        output_mode="full_history",
    ).compile()