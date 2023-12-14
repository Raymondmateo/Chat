import sys
import socket
import struct
from textual import events
from textual import on
from textual.app import App, ComposeResult
from textual.validation import Function, Number, ValidationResult, Validator
from textual.widgets import Input, Label, Pretty, Placeholder, Log


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
        self.messages.append(a_message)
        self.display_messages(True, a_message)

    def push_message(self, message) -> None:
        if message:
            word = self.gen_word_packet(message)
            self.socket.sendall(word)

    def gen_word_packet(self, word):
        try:
            word_bytes = word.encode('utf-8')
            pkt_len = len(word_bytes)
            len_bytes = struct.pack('>H', pkt_len)
        except Exception as e:
            print(f"An error occurred: {e}")
        return len_bytes + word_bytes

    def open_log():
        try:
            with open("logs.txt", "w") as file:
                sys.stdout = file
        except Exception as e:
            print(f"An error occurred: {e}")

    def compose(self) -> ComposeResult:
        yield Label("CHAT APP")
        yield Log()
        yield Pretty('')
        yield Label("Enter Message")
        yield Input(
            placeholder="HELLO FROM CHAT APP",
            type="text",
            #  validate_on=["submitted"],
            validators=[
                 Number(minimum=10000, maximum=65535),

            ],
        )
        yield Pretty([])

    @on(Input.Submitted)
    def show_invalid_reasons(self, event: Input.Submitted) -> None:
        # Updating the UI to show the reasons why validation failed
        log = self.query_one(Log)
        label_one = self.query(Pretty)[0]
        label_two = self.query(Pretty)[1]
        self.push_message(event.value)
        if not event.validation_result.is_valid:
            label_two.update(event.validation_result.failure_descriptions)
            # self.append_message(event.value)
            label_one.update("Enter Message")
        else:
            label_two.update([])
            # self.display_messages()


# A custom validator
class congfig(Validator):
    def validate(self, value: str) -> ValidationResult:
        """Check a string is equal to its reverse."""
        if self.is_valid(value, "port"):
            return self.success()
        else:
            return self.failure("Wrong Port:/")


if __name__ == "__main__":
    try:
        with open("logs.txt", "w") as file:
            sys.stdout = file
            app = InputApp()
            app.run()

    except Exception as e:
        print(f"An error occurred: {e}")
   # app.open_log
