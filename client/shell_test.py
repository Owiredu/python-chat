# from prompt_toolkit import Application
# from prompt_toolkit.buffer import Buffer
# from prompt_toolkit.layout.containers import VSplit, HSplit, Window
# from prompt_toolkit.layout.controls import BufferControl, FormattedTextControl
# from prompt_toolkit.layout.layout import Layout
# from prompt_toolkit.key_binding import KeyBindings
# from prompt_toolkit.formatted_text import HTML
# from constants import *
# from prompt_styles import SenderPrompt, ReceiptPrompt
# import utils
# from prompt_toolkit.styles import Style

# # Editable buffers
# text_field_buffer = Buffer()

# # key binding object
# kb = KeyBindings()

# # formatted text controls for chat section
# chat_title = FormattedTextControl(focusable=False)
# chat_display = FormattedTextControl(style=('bg:ansiblack fg:ansicyan'), focusable=True)
# user_info = FormattedTextControl(focusable=False)

# # formatted text controls for contacts section
# contacts_title = FormattedTextControl(text=HTML('<aaa align="center">CONTACTS</aaa>'), focusable=False)
# contacts_display = FormattedTextControl(focusable=True)
# status_bar_content = FormattedTextControl(focusable=False)

# # borders
# horizonal_border = Window(height=1, char='+', style=('bg:ansiblack fg:ansigreen'))
# vertical_border = Window(width=1, char='|', style=('bg:ansiblack fg:ansigreen'))

# # chat sending and display windows
# chat_title_window = Window(content=chat_title, height=2, style=('bg:ansigreen fg:ansiwhite'))
# chat_display_window = Window(content=chat_display, wrap_lines=True, style=('bg:ansiblack fg:ansiwhite'))
# user_info_window = Window(content=user_info, height=2, style=('bg:ansigreen fg:ansiwhite'))
# text_field_window = Window(content=BufferControl(buffer=text_field_buffer), height=5, wrap_lines=True, style=('bg:ansiblack fg:ansiwhite'))

# # contacts display windows
# contacts_title_window = Window(content=contacts_title, width=30, height=2, wrap_lines=True, style=('bg:ansigreen fg:ansiwhite'))
# contacts_display_window = Window(content=contacts_display, width=30, wrap_lines=True, style=('bg:ansiblack fg:ansiwhite'))

# # status bar window
# status_bar_window = Window(content=status_bar_content, height=1, style=('bg:ansigreen fg:ansiwhite'))

# # create root container with all windows arranged
# chat_container = HSplit([
#     chat_title_window,
#     # horizonal_border,
#     chat_display_window,
#     # horizonal_border,
#     user_info_window,
#     # horizonal_border,
#     text_field_window,
# ])

# contacts_container = HSplit([
#     contacts_title_window,
#     # horizonal_border,
#     contacts_display_window,
# ])

# chat_and_contacts_container = VSplit([
#     contacts_container,
#     vertical_border,
#     chat_container,
# ])

# root_container = HSplit([
#     chat_and_contacts_container,
#     status_bar_window,
# ])

# # add events
# @kb.add('c-q')
# def _(event):
#     """
#     Press CTRL-Q to exit the user interface.
#     """
#     event.app.exit()

# @kb.add('tab')
# def _(event):
#     """
#     Press TAB to switch to next focusable window
#     """
#     event.app.layout.focus_next()

# @kb.add('c-e')
# def _(event):
#     """
#     Press CTRL-E to switch to message text field
#     """
#     event.app.layout.focus(text_field_window)

# @kb.add('c-r')
# def _(event):
#     """
#     Press CTRL-R to switch to chat display
#     """
#     event.app.layout.focus(chat_display_window)

# @kb.add('c-c')
# def _(event):
#     """
#     Press CTRL-C to switch to contacts display
#     """
#     event.app.layout.focus(contacts_display_window)

# @kb.add('c-m')
# def _(event):
#     """
#     Press enter to send messages
#     """
#     newlines = '\n\n' if not chat_display.text.strip() == '' else ''
#     chat_display.text = f'{chat_display.text}{newlines}{text_field_buffer.document.text}'
#     text_field_buffer.text = ''

# # @kb.add('down')
# # def _(event):
# #     text_field_buffer.join_next_line()


# layout = Layout(root_container)
# app = Application(layout=layout, key_bindings=kb, full_screen=True, mouse_support=True)
# app.run()



"""
A simple example of a calculator program.
This could be used as inspiration for a REPL.
"""
from prompt_toolkit.application import Application
from prompt_toolkit.document import Document
from prompt_toolkit.filters import has_focus
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout.containers import HSplit, Window
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.styles import Style
from prompt_toolkit.widgets import SearchToolbar, TextArea

help_text = """
Type any expression (e.g. "4 + 4") followed by enter to execute.
Press Control-C to exit.
"""


def main():
    # The layout.
    search_field = SearchToolbar()  # For reverse search.

    output_field = TextArea(style="class:output-field", text=help_text)
    input_field = TextArea(
        height=1,
        prompt=">>> ",
        style="class:input-field",
        multiline=False,
        wrap_lines=False,
        search_field=search_field,
    )

    container = HSplit(
        [
            output_field,
            Window(height=1, char="-", style="class:line"),
            input_field,
            search_field,
        ]
    )

    # Attach accept handler to the input field. We do this by assigning the
    # handler to the `TextArea` that we created earlier. it is also possible to
    # pass it to the constructor of `TextArea`.
    # NOTE: It's better to assign an `accept_handler`, rather then adding a
    #       custom ENTER key binding. This will automatically reset the input
    #       field and add the strings to the history.
    def accept(buff):
        # Evaluate "calculator" expression.
        try:
            output = "\n\nIn:  {}\nOut: {}".format(
                input_field.text, eval(input_field.text)
            )  # Don't do 'eval' in real code!
        except BaseException as e:
            output = "\n\n{}".format(e)
        new_text = output_field.text + output

        # Add text to output buffer.
        output_field.buffer.document = Document(
            text=new_text, cursor_position=len(new_text)
        )

    input_field.accept_handler = accept

    # The key bindings.
    kb = KeyBindings()

    @kb.add("c-c")
    @kb.add("c-q")
    def _(event):
        " Pressing Ctrl-Q or Ctrl-C will exit the user interface. "
        event.app.exit()

    # Style.
    style = Style(
        [
            ("output-field", "bg:#000044 #ffffff"),
            ("input-field", "bg:#000000 #ffffff"),
            ("line", "#004400"),
        ]
    )

    # Run application.
    application = Application(
        layout=Layout(container, focused_element=input_field),
        key_bindings=kb,
        style=style,
        mouse_support=True,
        full_screen=True,
    )

    application.run()


if __name__ == "__main__":
    main()