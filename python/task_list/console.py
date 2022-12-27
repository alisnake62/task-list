from typing import Optional, IO, TYPE_CHECKING

if TYPE_CHECKING: from console import Console

# class ConsoleOutPut:

#     def __init__(self, console:'Console') -> None:
#         self._console = console

    

class Console:
    def __init__(self, input_reader: IO, output_writer: IO) -> None:
        self.input_reader = input_reader
        self.output_writer = output_writer

    def print(self, string: Optional[str]="", end: str="\n", flush: bool=True) -> None:
        self.output_writer.write(string + end)
        if flush:
            self.output_writer.flush()

    def input(self, prompt: Optional[str]="") -> str:
        self.print(prompt, end="")
        return self.input_reader.readline().strip()

    
