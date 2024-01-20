from UnlimitedGPT import ChatGPT
from UnlimitedGPT.internal.selectors import ChatGPTVariables as CGPTV


class Bot(ChatGPT):
    def new_chat(self) -> None:
        """
        Create a new chat.
        """
        if not self.driver.current_url.startswith("https://chat.openai.com/"):
            return self.logger.debug("Current URL is not chat page, skipping create new chat")

        self.logger.debug("Creating new chat...")
        button = CGPTV.new_chat
        clicked = self.driver.safe_click(button, timeout=60)
        if not clicked:
            self.logger.debug(f"{button[1]} button not found")
            return self._get_out_of_menu()
        self.logger.debug("New chat created")

    def refresh(self) -> None:
        """
        Refresh webpage.
        """
        self.logger.debug("Refreshing...")
        self.driver.refresh()
        self.logger.debug("Refreshed")
