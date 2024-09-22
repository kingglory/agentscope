import model_config
from model_config import get_config  # 确保正确导入
import agentscope
from agentscope.agents import DialogAgent, UserAgent
from agentscope.pipelines.functional import sequentialpipeline

def main() -> None:
    dashscope_config = get_config("dashscope_chat-temperature-0.1")
    # print(f"Dashscope Config: {dashscope_config.__dict__}")

    # 1, 加载模型配置
    agentscope.init(model_configs= dashscope_config,
                    project='一个简单的对话demo',
                    save_api_invoke=True)
    # 2, agentscope 智能体
    # 创建 对话Agent 和 用户Agent
    dialog_agent = DialogAgent(name="assistant",
                               sys_prompt="你是一名非常聪明的 AI Agent！！！",
                               model_config_name="dashscope_chat-temperature-0.1")
    # model_config_name 是配置文件里面的 config_name
    user_agent = UserAgent()

    # 3， agentscope 智能对话
    x = None
    while x is None or x.content != "exit":
        x = sequentialpipeline([dialog_agent, user_agent], x)

if __name__ == "__main__":
	main()