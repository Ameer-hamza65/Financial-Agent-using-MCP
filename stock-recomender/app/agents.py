from langgraph.prebuilt import create_react_agent
from langchain.chat_models import init_chat_model
from config import Config

async def create_agent(tools, prompt, name):
    model = init_chat_model("gemini-2.5-flash", model_provider="google_genai", api_key=Config.OPENAI_API_KEY)
    return create_react_agent(model, tools, prompt=prompt, name=name)

async def get_all_agents(tools):
    agents = {}
    
    agents["stock_finder"] = await create_agent(
        tools,
        prompt="""[Stock Finder Agent] You are a stock research analyst specializing in Indian Stock Market (NSE). 
        Select 2 promising, actively traded NSE-listed stocks for short term trading based on:
        - Recent performance - News buzz - Volume - Technical strength
        Output: Stock names, tickers, and brief reasoning. Avoid penny stocks.""",
        name="stock_finder_agent"
    )
    
    agents["market_data"] = await create_agent(
        tools,
        prompt="""[Market Data Agent] Gather recent market data for given NSE tickers:
        - Current price - Previous close - Today's volume 
        - 7/30-day trends - RSI/Moving averages - Volatility spikes
        Format: Structured per stock, use INR currency.""",
        name="market_data_agent"
    )
    
    agents["news_analyst"] = await create_agent(
        tools,
        prompt="""[News Analyst Agent] For given NSE stocks:
        - Find recent news (3-5 days) 
        - Summarize key updates 
        - Classify sentiment (Positive/Negative/Neutral)
        - Impact on short-term price
        Format: One section per stock with bullet points.""",
        name="news_analyst_agent"
    )
    
    agents["recommender"] = await create_agent(
        tools,
        prompt="""[Recommender Agent] Based on:
        - Market data - News sentiment
        For each stock recommend:
        1. Action (Buy/Sell/Hold)
        2. Target price (INR)
        3. Brief reasoning
        Focus: Near-term trading advice.""",
        name="price_recommender_agent"
    )
    
    return agents