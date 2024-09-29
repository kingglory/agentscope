from codeact_agent import CodeActAgent
import agentscope

agentscope.init(model_configs="./config/model_config.json")
YOUR_MODEL_CONFIGURATION_NAME = "dashscope_qwen_turbo_chat-temperature-0.1"
import nest_asyncio
nest_asyncio.apply()
agent = CodeActAgent(
    name="assistant",
    model_config_name=YOUR_MODEL_CONFIGURATION_NAME,
)

from loguru import logger
from agentscope.message import Msg

mss = Msg(
    name="user",
    content="Given y = 0.9x + 6.1, randomly sample data points as pairs of (x, y). Then fit a linear regression on the sampled data and plot the points, fitted line, and ground-truth line.",
    role="user"
)
logger.chat(mss)
answer_mss1 = agent(mss)