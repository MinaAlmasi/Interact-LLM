"""
Currently heavily based on
https://textual.textualize.io/blog/2024/09/15/anatomy-of-a-textual-user-interface/#were-in-the-pipe-five-by-five
"""

from interfaces.base_hf import ChatHF
from interfaces.chat import ChatMessage
from textual import on, work
from textual.app import App, ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import Footer, Header, Input, Markdown
from transformers.utils.logging import disable_progress_bar

disable_progress_bar()

# temp
MODEL_ID = "BSC-LT/salamandra-2b-instruct"


def get_response():
    """
    dummy fn
    """
    string = "¿En serio? ¡A mí también me gusta ver películas!"
    return string


# classes for formatting
class Prompt(Markdown):
    pass


class Response(Markdown):
    BORDER_TITLE = "Interact-LLM"


class ChatApp(App):
    """
    Texttual app for chatting with llm
    """

    AUTO_FOCUS = "INPUT"

    CSS = """
    Prompt {
        background: $primary 10%;
        color: $text;
        margin: 1;        
        margin-right: 8;
        padding: 1 2 0 2;
    }

    Response {
        border: wide $success;
        background: $success 10%;   
        color: $text;             
        margin: 1;      
        margin-left: 8; 
        padding: 1 2 0 2;
    }
    """

    def on_mount(self) -> None:
        self.model = ChatHF(model_id=MODEL_ID)
        self.model.load()

    def compose(self) -> ComposeResult:
        yield Header()
        with VerticalScroll(id="chat-view"):
            yield Response("¿Hola quieres practicar conmigo?")
        yield Input(placeholder="Escribe tu mensaje aquí")
        yield Footer()

    @on(Input.Submitted)
    async def on_input(self, event: Input.Submitted) -> None:
        chat_view = self.query_one("#chat-view")
        event.input.clear()
        await chat_view.mount(Prompt(event.value))
        await chat_view.mount(response := Response())
        response.anchor()
        self.send_prompt(event.value, response)

    @work(thread=True)
    def send_prompt(self, prompt: str, response: Response) -> None:
        response_content = ""
        chat_messages = [ChatMessage(role="user", content=prompt)]
        llm_response = self.model.generate(chat_messages)

        # replace weird <|im_end|> ()
        llm_response["content"] = llm_response["content"].replace("<|im_end|>", "")

        for chunk in llm_response["content"]:
            response_content += chunk  # add words in a "stream-like" way
            self.call_from_thread(response.update, response_content)


def main():
    app = ChatApp()
    app.run()


if __name__ == "__main__":
    main()
