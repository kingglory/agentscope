# -*- coding: utf-8 -*-
""" Group chat utils."""
import re
from typing import Sequence


def select_next_one(agents: Sequence, rnd: int) -> Sequence:
    """
    Select next agent.
    当发言列表为空时随机选择下一个发言的智能体
    """
    return agents[rnd % len(agents)]


def filter_agents(string: str, agents: Sequence) -> Sequence:
    """
    This function filters the input string for occurrences of the given names
    prefixed with '@' and returns a list of the found names.
    该函数会筛选输入字符串中以 ”@“ 为前缀的给定名称的出现，并返回找到的名称列表
    """
    if len(agents) == 0:
        return []

    # Create a pattern that matches @ followed by any of the candidate names
    """
    创建一个匹配@ 后跟任何候选名字的模式
    """
    pattern = (
        r"@(" + "|".join(re.escape(agent.name) for agent in agents) + r")\b"
    )

    # Find all occurrences of the pattern in the string
    '''
    在字符串中找到所有模式的出现
    '''
    matches = re.findall(pattern, string)

    # Create a dictionary mapping agent names to agent objects for quick lookup
    '''为了快速查找，创建一个将代理名映射到代理对象的字典'''
    agent_dict = {agent.name: agent for agent in agents}

    # Return the list of matched agent objects preserving the order
    '''返回匹配的代理对象列表，保持顺序'''
    ordered_agents = [
        agent_dict[name] for name in matches if name in agent_dict
    ]
    return ordered_agents
