import os

# 读取环境变量
# DASHSCOPE_API_KEY_text = os.getenv('DASHSCOPE_API_KEY')
# OPENAI_API_KEY_text = os.getenv('OPENAI_API_KEY')
# print(DASHSCOPE_API_KEY_text)
# print(OPENAI_API_KEY_text)

# class ModelConfig:
#     def __init__(self, config_name, model_type, model_name, generate_args, organization=None):
#         self.config_name = config_name
#         self.model_type = model_type
#         self.model_name = model_name
#         self.generate_args = generate_args
#         self.api_key = os.getenv('DASHSCOPE_API_KEY')
#         self.OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
#         self.organization = organization

# 示例配置
configs = {"gpt-4-temperature-0.0":{
        "config_name":"gpt-4-temperature-0.0",
        "model_type":"openai_chat",
        "model_name":"gpt-4",
        "generate_args":{"temperature": 0.0},
        #organization="example_org"
            },
"dashscope_chat-temperature-0.1":{
        "config_name":"dashscope_chat-temperature-0.1",
        "model_type":"dashscope_chat",
        "model_name":"qwen-turbo",
        "generate_args":{"temperature": 0.1},
        }
}

def get_config(config_name):
    if config_name in  configs:
        return configs[config_name]
    return None

# 示例调用
# if __name__ == "__main__":
#     gpt4_config = get_config("gpt-4-temperature-0.0")
#     print(f"GPT-4 Config: {gpt4_config}")
#
#     dashscope_config = get_config("dashscope_chat-temperature-0.1")
#     print(f"Dashscope Config: {dashscope_config}")