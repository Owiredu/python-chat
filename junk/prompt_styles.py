from prompt_toolkit.shortcuts import prompt
from prompt_toolkit import print_formatted_text
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.styles import Style
# from constants import *


class SenderPrompt:

    def __init__(self, email, username, menu):
        self.style = Style.from_dict({
            # User input (default text).
            '':         '#ffffff',
            # Prompt.
            'username': '#ff0066',
            'at':       '#00aa00',
            'colon':    '#0000aa',
            'arrows':    '#00aa00',
            'host':     '#ffa500',
            'email':     'ansicyan underline',
            'bracket':    '#00aa00',
            'menu': '#ffff00',
        })

        self.message = [
            ('class:username', username),
            ('class:at',       '@'),
            ('class:host',     'sChat'),
            ('class:colon',    ':'),
            ('class:email',     email),
            ('class:bracket',    ' ['),
            ('class:menu',    menu),
            ('class:bracket',    '] '),
            ('class:arrows',    '>>> '),
        ]

    def message(self):
        return self.message

    def style(self):
        return self.style

    def get_prompt(self):
        return prompt(self.message, style=self.style, multiline=True, mouse_support=True, wrap_lines=True)


class ReceiptPrompt:

    def __init__(self, email, username, time, message):
        self.style = Style.from_dict({
            # User input (default text).
            'message':         '#ffffff',
            # Prompt.
            'username': '#ffff00',
            'time':       '#ff0066',
            'c_bracket':    '#00aa00',
            'hash':    '#00aa00',
            'host':     '#ffa500',
            'email':     'ansicyan underline',
            'bracket':    '#00aa00',
            'menu': '#ffff00',
        })

        self.message = FormattedText([
            ('class:c_bracket',    '('),
            ('class:time',    time),
            ('class:c_bracket',    ') '),
            ('class:email',     email),
            ('class:bracket',    '['),
            ('class:username', username),
            ('class:bracket',    '] '),
            ('class:hash',    '# '),
            ('class:message', message)
        ])

    def message(self):
        return self.message

    def style(self):
        return self.style

    def print_text(self):
        print_formatted_text(self.message, style=self.style)


class SystemPrompt:

    def __init__(self, time, message, msg_type):
        self.style = Style.from_dict({
            # User input (default text).
            'message':         'ansicyan underline' if msg_type==SUCCESS else '#ff0066',
            # Prompt.
            'username': '#ffff00',
            'time':       '#ff0066',
            'c_bracket':    '#00aa00',
            'hash':    '#00aa00',
            'host':     '#ffa500',
            'bracket':    '#00aa00',
            'menu': '#ffff00',
        })

        self.message = FormattedText([
            ('class:c_bracket',    '('),
            ('class:time',    time),
            ('class:c_bracket',    ') '),
            ('class:bracket',    '['),
            ('class:username', 'SYSTEM'),
            ('class:bracket',    '] '),
            ('class:hash',    '==> '),
            ('class:message', message)
        ])

    def message(self):
        return self.message

    def style(self):
        return self.style

    def print_text(self):
        print_formatted_text(self.message, style=self.style)


sender_text = SenderPrompt('nk@gmail.com', 'Owiredu', 'Chat').get_prompt()
# print(sender_text)
# ReceiptPrompt('nk@gmail.com', 'Owiredu', 'Tue, Jan 20, 2020 04:32 GMT', 'Hello world').print_text()
# SystemPrompt('Tue, Jan 20, 2020 04:32 GMT', 'Connected to server', SUCCESS).print_text()