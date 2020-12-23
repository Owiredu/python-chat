from prompt_toolkit.shortcuts import prompt
from prompt_toolkit.styles import Style


class PromptObj:

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
        return prompt(self.message, style=self.style)


text = PromptObj('nk@gmail.com', 'Owiredu', 'Register').get_prompt()
print(text)