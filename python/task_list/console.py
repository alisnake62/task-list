from typing import Optional, IO, TYPE_CHECKING, List

if TYPE_CHECKING: 
    from console import Console
    from app import Project

class Console:
    def __init__(self, input_reader: IO, output_writer: IO) -> None:
        self.input_reader = input_reader
        self.output_writer = output_writer

    def print(self, string: Optional[str]="", end: str="\n", flush: bool=True) -> None:
        self.output_writer.write(string + end)
        if flush:
            self.output_writer.flush()

    def printShow(self, projects:List['Project']) -> None:
        for project in projects:
            self.print(str(project))
            for task in project._tasks:
                self.print(str(task))
            self.print()

    def printProjectNotFound(self, projectName: str) -> None:
        self.print(f"Could not find a project with the name {projectName}.")
        self.print()

    def printTaskNotFound(self, id: int) -> None:
        self.print(f"Could not find a task with an ID of {id}")
        self.print()

    def printHelp(self) -> None:
        self.print("Commands:")
        self.print("  show")
        self.print("  add project <project name>")
        self.print("  add task <project name> <task description>")
        self.print("  check <task ID>")
        self.print("  uncheck <task ID>")
        self.print()

    def printError(self, command:str) -> None:
        self.print(f"I don't know what the command {command} is.")
        self.print()

    def input(self, prompt: Optional[str]="") -> str:
        self.print(prompt, end="")
        return self.input_reader.readline().strip()

    
