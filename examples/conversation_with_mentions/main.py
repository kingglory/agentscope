# -*- coding: utf-8 -*-
""" A group chat where user can talk any time implemented by agentscope. """
from groupchat_utils import (
    select_next_one,
    filter_agents,
)
import logging
import agentscope
from agentscope.agents import UserAgent
from agentscope.message import Msg
from agentscope.msghub import msghub

# 数定义了用户在回合制中发言的时间限制
USER_TIME_TO_SPEAK = 60
DEFAULT_TOPIC = """
这是一个群组聊天室，你可以自由而简短地发言。
"""

SYS_PROMPT = """
你可以指定一个成员来回复你的信息，你可以使用@符号。
这意味着在你的消息中包含@符号，@符号后跟着是某人(你想要对话的人)的姓名，并在姓名后留出空格。

所有参与者的名单：｛agent_names｝
"""
# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main() -> None:
    """group chat"""
    npc_agents = agentscope.init(
        model_configs="./configs/model_configs.json",
        agent_configs="./configs/agent_configs.json",
        project="Conversation with Mentions",
    )

    user = UserAgent()

    agents = list(npc_agents) + [user]

    hint = Msg(
        name="Host",
        content=DEFAULT_TOPIC
        + SYS_PROMPT.format(
            agent_names=[agent.name for agent in agents],
        ),
        role="assistant",
    )

    rnd = 0
    speak_list = []
    with msghub(agents, announcement=hint):
        while True:
            try:
                x = user(timeout=USER_TIME_TO_SPEAK)
                if x.content == "exit":
                    break
            except TimeoutError:
                x = {'content':""}
                logger.info(
                    f"User has not typed text for {USER_TIME_TO_SPEAK} seconds, skip."
                )

            speak_list += filter_agents(x.content, npc_agents)

            if len(speak_list) > 0:
                next_agent = speak_list.pop(0)
                x = next_agent()
            else:
                next_agent = select_next_one(npc_agents, rnd)
                x = next_agent()

            speak_list += filter_agents(x.content, npc_agents)

            rnd += 1


if __name__ == "__main__":
    main()
