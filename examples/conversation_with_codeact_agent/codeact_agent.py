# -*- coding: utf-8 -*-
# pylint: disable=C0301
"""An agent class that implements the CodeAct agent.
This agent can execute code interactively as actions.
More details can be found at the paper of CodeAct agent
https://arxiv.org/abs/2402.01030
and the original repo of codeact https://github.com/xingyaoww/code-act
一个实现了CodeAct代理的代理类。
该代理可以交互式地执行代码作为动作。
更多细节可以在CodeAct代理的论文
https://arxiv.org/abs/2402.01030
"""
from agentscope.agents import AgentBase
from agentscope.message import Msg
from agentscope.service import (
    ServiceResponse,
    ServiceExecStatus,
    NoteBookExecutor,
)
from agentscope.parsers import RegexTaggedContentParser

SYSTEM_MESSAGE = """
You are a helpful assistant that gives helpful, detailed, and polite answers to the user's questions.
You should interact with the interactive Python (Jupyter Notebook) environment and receive the corresponding output when needed. The code written by assistant should be enclosed using <execute> tag, for example: <execute> print('Hello World!') </execute>.
You should attempt fewer things at a time instead of putting too much code in one <execute> block. You can install packages through PIP by <execute> !pip install [package needed] </execute> and should always import packages and define variables before starting to use them.
You should stop <execute> and provide an answer when they have already obtained the answer from the execution result. Whenever possible, execute the code for the user using <execute> instead of providing it.
Your response should be concise, but do express their thoughts. Always write the code in <execute> block to execute them.
You should not ask for the user's input unless necessary. Solve the task on your own and leave no unanswered questions behind.
You should do every thing by your self.
"""  # noqa
# 系统消息
# SYSTEM_MESSAGE = """
# 你是一个乐于助人的助手，会给出对用户问题的详细、礼貌的回答。
# 你应该与交互式的Python（Jupyter Notebook）环境进行交互，并在需要时接收相应的输出。
# 助手编写的代码应使用<execute>标签括起来，例如：<execute> print('Hello World!') </execute>。
# 你应该每次都尽量少做一些事情，而不是在一个<execute>块中放太多代码。
# 你可以通过<execute> !pip install [所需包] </execute>安装包，并且在开始使用之前始终导入包并定义变量。
# 当已经从执行结果中获得答案时，你应该停止<execute>并提供答案。
# 尽可能地为用户执行代码，而不是提供代码。
# 你的回答应尽量简明扼要，但也要表达出用户的想法。
# 你应该在必要时才询问用户的输入。独立解决问题，不留未解答的问题。
# 你应该独立完成所有任务。
# """
EXAMPLE_MESSAGE = """
Additionally, you are provided with the following code available:
{example_code}
The above code is already available in your interactive Python (Jupyter Notebook) environment, allowing you to directly use these variables and functions without needing to redeclare them.
"""  # noqa

# 示例代码消息
# EXAMPLE_MESSAGE = """
# 此外，你还可以使用以下代码：
# {example_code}
# 上述代码已经在你的交互式Python（Jupyter Notebook）环境中可用，允许你直接使用这些变量和函数，而无需重新声明它们。
# """

class CodeActAgent(AgentBase):
    """
    The implementation of CodeAct-agent.
    The agent can execute code interactively as actions.
    More details can be found at the paper of codeact agent
    https://arxiv.org/abs/2402.01030
    and the original repo of codeact https://github.com/xingyaoww/code-act
    """
    """
    CodeAct代理的实现。
    该代理可以作为 动作 交互式地执行代码。
    更多细节可以在CodeAct代理的论文
    https://arxiv.org/abs/2402.01030
    和原始的codeact仓库 https://github.com/xingyaoww/code-act 中找到
    """

    def __init__(
        self,
        name: str,
        model_config_name: str,
        example_code: str = "",
    ) -> None:
        """
        Initialize the CodeActAgent.
        Args:
            name(`str`):
                The name of the agent.
            model_config_name(`str`):
                The name of the model configuration.
            example_code(Optional`str`):
                The example code to be executed bewfore the interaction.
                You can import reference libs, define variables and functions to be called. For example:

                    ```python
                    from agentscope.service import bing_search
                    import os

                    api_key = "{YOUR_BING_API_KEY}"

                    def search(question: str):
                        return bing_search(question, api_key=api_key, num_results=3).content
                    ```

        """  # noqa
        """
        初始化CodeActAgent。
        参数:
            name(str):
                代理的名称。
            model_config_name(str):
                模型配置的名称。
            example_code(str, 可选):
                在交互前执行的示例代码。
                你可以导入参考库，定义变量和函数。例如：

                    ```python
                    from agentscope.service import bing_search
                    import os

                    api_key = "{YOUR_BING_API_KEY}"

                    def search(question: str):
                        return bing_search(question, api_key=api_key, num_results=3).content
                    ```
        """

        # 调用父类的初始化方法
        super().__init__(
            name=name,
            model_config_name=model_config_name,
        )
        # 最大执行次数
        self.n_max_executions = 5
        # 示例代码
        self.example_code = example_code
        # 代码执行器
        self.code_executor = NoteBookExecutor()

        # 系统消息
        sys_msg = Msg(name="system", role="system", content=SYSTEM_MESSAGE)
        # 示例消息
        example_msg = Msg(
            name="user",
            role="user",
            content=EXAMPLE_MESSAGE.format(example_code=self.example_code),
        )

        # 将系统消息添加到内存
        self.memory.add(sys_msg)

        # 如果有示例代码，则执行并记录结果
        if self.example_code != "":
            # 代码执行结果
            code_execution_result = self.code_executor.run_code_on_notebook(
                self.example_code,
            )
            # 代码执行消息
            code_exec_msg = self.handle_code_result(
                code_execution_result,
                "Example Code excuted: ",
            )
            self.memory.add(example_msg)
            self.memory.add(code_exec_msg)
            self.speak(code_exec_msg)

        # 解析器
        self.parser = RegexTaggedContentParser(try_parse_json=False)

    def handle_code_result(
        self,
        code_execution_result: ServiceResponse,
        content_pre_sring: str = "",
    ) -> Msg:
        """return the message from code result"""
        """
        返回代码执行结果的消息
        """
        code_exec_content = content_pre_sring
        if code_execution_result.status == ServiceExecStatus.SUCCESS:
            code_exec_content += "Excution Successful:\n"
        else:
            code_exec_content += "Excution Failed:\n"
        code_exec_content += "Execution Output:\n" + str(
            code_execution_result.content,
        )
        return Msg(name="user", role="user", content=code_exec_content)

    def reply(self, x: Msg = None) -> Msg:
        """The reply function that implements the codeact agent."""
        """
        实现codeact代理的回复函数。
        """
        self.memory.add(x)

        # 执行计数
        excution_count = 0
        while (
            self.memory.get_memory(1)[-1].role == "user"
            and excution_count < self.n_max_executions # 最大执行次数
        ):
            prompt = self.model.format(self.memory.get_memory())
            model_res = self.model(prompt) # 模型响应
            msg_res = Msg(
                name=self.name,
                content=model_res.text,
                role="assistant",
            )
            self.memory.add(msg_res)
            self.speak(msg_res)
            res = self.parser.parse(model_res)
            code = res.parsed.get("execute")
            if code is not None:
                code = code.strip()
                code_execution_result = (
                    self.code_executor.run_code_on_notebook(code)
                )
                excution_count += 1
                code_exec_msg = self.handle_code_result(code_execution_result)
                self.memory.add(code_exec_msg)
                self.speak(code_exec_msg)

        if excution_count == self.n_max_executions:
            assert self.memory.get_memory(1)[-1].role == "user"
            code_max_exec_msg = Msg(
                name="assitant",
                role="assistant",
                content=(
                    "I have reached the maximum number "
                    f"of executions ({self.n_max_executions=}). "
                    "Can you assist me or ask me another question?"
                ),
            )
            self.memory.add(code_max_exec_msg)
            self.speak(code_max_exec_msg)
            return code_max_exec_msg

        return msg_res
