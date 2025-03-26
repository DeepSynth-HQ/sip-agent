from agno.tools import Toolkit
from .functions import XFunctions


class XActionsToolkit(Toolkit):
    def __init__(self):
        super().__init__("x_tools")
        self.register(XFunctions.create_tweet)
        self.register(XFunctions.reply_to_tweet)
