from typing import Dict, List, TYPE_CHECKING

if TYPE_CHECKING: from app import TaskList

from console import Console

class Command:

    _expectedValue = ["show", "add", "check", "uncheck", "help"]

    def __init__(self, value:str) -> None:
        self._value = value

    def isShow(self):
        return self._value == "show"

    def isAdd(self):
        return self._value == "add"

    def isCheck(self):
        return self._value == "check"

    def isUncheck(self):
        return self._value == "uncheck"

    def isHelp(self):
        return self._value == "help"

    def isError(self):
        return self._value not in self._expectedValue

    def error(self, taskList:'TaskList'):
        taskList.error(self._value)

class Argument:
    def __init__(self, value:str) -> None:
        self._value = value

    def add(self, taskList:'TaskList'):
        taskList.add(self._value)

    def check(self, taskList:'TaskList'):
        taskList.check(self._value)

    def uncheck(self, taskList:'TaskList'):
        taskList.uncheck(self._value)

class CommandLine:

    _command    = None
    _argument   = None
    def __init__(self, value:str) -> None:

        command_rest = value.split(" ", 1)
        self._command   = Command(value=command_rest[0])
        if len(command_rest) > 1: 
            self._argument  = Argument(value=command_rest[1])

    def execute(self, taskList:'TaskList') -> None:
        if self._command.isShow()   : taskList.show()
        if self._command.isAdd()    : self._argument.add(taskList=taskList)
        if self._command.isCheck()  : self._argument.check(taskList=taskList)
        if self._command.isUncheck(): self._argument.uncheck(taskList=taskList)
        if self._command.isHelp()   : taskList.help()
        if self._command.isError()  : self._command.error(taskList=taskList)

class Task:
    def __init__(self, id_: int, description: str, done: bool) -> None:
        self.id = id_
        self.description = description
        self.done = done

    def set_done(self, done: bool) -> None:
        self.done = done

    def is_done(self) -> bool:
        return self.done

    def isGoodId(self, id:int) -> bool:
        return self.id == id

class Project:

    def __init__(self, name:str) -> None:
        self._name = name
        self._tasks:List[Task] = []

    def addTask(self, task:Task) -> None:
        self._tasks.append(task)

    def isGoodName(self, name:str) -> bool:
        return self._name == name

    def findTaskById(self, id:int) -> Task:
        for task in self._tasks:
            if task.isGoodId(id=id): return task
        return None

class TaskList:
    QUIT = "quit"

    def __init__(self, console: Console) -> None:

        self.console = console
        self.last_id: int = 0
        self.tasks: List[Project] = []

    def run(self) -> None:
        while True:
            command = self.console.input("> ")
            if command == self.QUIT:
                break
            self.execute(command)

    def execute(self, command_line: str) -> None:

        commandLine = CommandLine(value=command_line)
        commandLine.execute(taskList=self)

    def show(self) -> None:
        for project in self.tasks:
            self.console.print(project._name)
            for task in project._tasks:
                self.console.print(f"  [{'x' if task.is_done() else ' '}] {task.id}: {task.description}")
            self.console.print()

    def add(self, command_line: str) -> None:
        sub_command_rest = command_line.split(" ", 1)
        sub_command = sub_command_rest[0]
        if sub_command == "project":
            self.add_project(sub_command_rest[1])
        elif sub_command == "task":
            project_task = sub_command_rest[1].split(" ", 1)
            self.add_task(project_task[0], project_task[1])

    def findProjectByName(self, name:str) -> Project:
        for project in self.tasks:
            if project.isGoodName(name=name):
                return project
        return None

    def add_project(self, name: str) -> None:
        self.tasks.append(Project(name=name))

    def add_task(self, project: str, description: str) -> None:
        project_tasks = self.findProjectByName(name=project)
        if project_tasks is None:
            self.console.print(f"Could not find a project with the name {project}.")
            self.console.print()
            return
        task = Task(self.next_id(), description, False)
        project_tasks.addTask(task=task)

    def check(self, id_string: str) -> None:
        self.set_done(id_string, True)

    def uncheck(self, id_string: str) -> None:
        self.set_done(id_string, False)

    def set_done(self, id_string: str, done: bool) -> None:
        id_ = int(id_string)
        for project in self.tasks:
            task = project.findTaskById(id=id_)
            if task is not None: 
                task.set_done(done)
                return
        self.console.print(f"Could not find a task with an ID of {id_}")
        self.console.print()

    def help(self) -> None:
        self.console.print("Commands:")
        self.console.print("  show")
        self.console.print("  add project <project name>")
        self.console.print("  add task <project name> <task description>")
        self.console.print("  check <task ID>")
        self.console.print("  uncheck <task ID>")
        self.console.print()

    def error(self, command: str) -> None:
        self.console.print(f"I don't know what the command {command} is.")
        self.console.print()

    def next_id(self) -> int:
        self.last_id += 1
        return self.last_id

