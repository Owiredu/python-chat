from prompt_toolkit.lexers import Lexer
from prompt_toolkit.document import Document
from constants import CHAT_MESSAGE_INDENT

class ChatLexer(Lexer):
    """
    This is controls syntax highlighting in the chat area
    """

    def lex_document(self, document:Document) -> list:

        def get_line(lineno:int) -> list:
            style = []
            line = document.lines[lineno]
            if line.startswith('(') and line.endswith(']'):
                # style for message prefix. Eg. (2020-12-26 22:58:09)-nanakofiowiredu@gmail.com[Owiredu]--{
                parts:list = line.split(')') # (2020-12-26 22:58:09 and nanakofiowiredu@gmail.com[Owiredu]
                datetime_with_left_bracket:str = parts[0]
                email_username_symbols:str = parts[1]
                parts:list = email_username_symbols[:-1].split('[') # nanakofiowiredu@gmail.com and Owiredu
                email:str = parts[0]
                username:str = parts[1]
                style.append(('bg:red fg:white', datetime_with_left_bracket + ')'))
                # style.append(('bg:#00aa00 fg:white', '-'))
                style.append(('bg:green fg:white', email))
                style.append(('bg:magenta fg:white', '['))
                style.append(('bg:magenta fg:white', username))
                style.append(('bg:magenta fg:white', ']'))
                # style.append(('bg:orange fg:white', '--{'))
            elif line.startswith(CHAT_MESSAGE_INDENT):
                # style for actual message
                style.append(('bg:blue fg:white', '#=>'))
                style.append(('', ' '))
                style.append(('#ffffff', line[len(CHAT_MESSAGE_INDENT):]))
            # elif line.startswith('}'):
            #     # style for message suffix
            #     style.append(('bg:orange fg:white', '}'))
            return style

        return get_line