from typing import IO
 
from primitiveWrapper import ConsoleOuput

class Console:

    _input_reader   :IO
    _output_writer  :IO

    def __init__(self, input_reader: IO, output_writer: IO) -> None:
        self._input_reader  = input_reader
        self._output_writer = output_writer

    def _write(self, output:ConsoleOuput) -> None:

        self._output_writer.write(f"{output}")
        self._output_writer.flush()

    def _printPrompt(self) -> None:
        promptOutput = ConsoleOuput(outputStr="> ")
        self._write(output=promptOutput)

    def print(self, output:ConsoleOuput) -> None:
        output.addNewLine()
        self._write(output=output)

    def inputPrompt(self) -> str:
        self._printPrompt()
        return self._input_reader.readline()