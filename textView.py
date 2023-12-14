import sys
import socket
import struct
from textual import events
from textual import on
from textual.app import App, ComposeResult
from textual.validation import Function, Number, ValidationResult, Validator
from textual.widgets import Input, Label, Pretty, Placeholder, Log
import json
from lib import gen_word_packet


class InputApp(App):

    CSS = """                                                                                    
    Input.-valid {                                                                               
        border: tall $success 60%;                                                               
    }                                                                                            
    Input.-valid:focus {                                                                         
        border: tall $success;                                                                   
    }                                                                                            
    Input {                                                                                      
        margin: 1 1;                                                                             
    }                                                                                            
    Label {                                                                                      
        margin: 1 2;                                                                             
    }                                                                                            
    Pretty {                                                                                     
        margin: 1 2;                                                                             
    }                                                                                            
    Log{                                                                                         
                                                                                                 
     padding: 1 2 0 2;                                                                           
    }                                                                                            
                                                                                                 
                                                                                                 
    """

    def __init__(self, sock):
        super().__init__()
        self.messages = []
        self.socket = sock

    def display_messages(self, new_message=False, a_message="") -> None:
        try:
            log = self.query_one(Log)
            if new_message:
                log.write_line(a_message)
            else:
                for message in self.messages:
                    log.write_line(message)
        except Exception as e:
            print(f"An error occurred: {e}")

    def append_message(self, a_message) -> None:
        name, message = a_message
        self.messages.append((name, message))
        self.display_messages(True, f"{name}: {message}")

    def push_message(self, message) -> None:
        if message:
            data = {'message': message}
            word = gen_word_packet(data)  # Use the imported function
            self.socket.sendall(word)
            self.display_messages(True, message)

    def open_log():
        try:
            with open("logs.txt", "w") as file:
                sys.stdout = file
        except Exception as e:
            print(f"An error occurred: {e}")

    def compose(self) -> ComposeResult:
        yield Label("CHAT APP")
        yield Log()
        yield Label("Enter Message")
        yield Input(placeholder="HELLO FROM CHAT APP",
                    type="text",
                    )

    @on(Input.Submitted)
    def submit(self, event: Input.Submitted) -> None:
        log = self.query_one(Log)
        self.push_message(event.value)
        input_widget = self.query_one(Input)
        input_widget.value = ""


if __name__ == "__main__":
    try:
        app = InputApp()
        app.run()
    except Exception as e:
        print(f"An error occurred: {e}")
