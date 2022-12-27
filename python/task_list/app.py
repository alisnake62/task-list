from typing import Dict, List, TYPE_CHECKING

if TYPE_CHECKING: from app import TaskList, ActionUtils

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

class SubCommand:

    _expectedValue = ["project", "task"]

    def __init__(self, value:str) -> None:
        self._value = value

    def isProject(self):
        return self._value == "project"

    def isTask(self):
        return self._value == "task"

class Argument:
    def __init__(self, value:str) -> None:
        self._value = value

class CommandLine:

    _command    = None
    _subCommand = None
    _arguments   = []
    def __init__(self, value:str) -> None:

        command_rest = value.split(" ", 1)
        self._command = Command(value=command_rest[0])

        if len(command_rest) >= 2:
            command_rest2 = command_rest[1].split(" ", 1)
            if command_rest2[0] in ["project", "task"]:
                self._subCommand = SubCommand(value=command_rest2[0])
                self._arguments = [Argument(value=argStr) for argStr in command_rest2[1].split(" ")]
            else:
                self._arguments = [Argument(value=argStr) for argStr in command_rest[1].split(" ")]

    def execute(self, actionUtils:'ActionUtils') -> None:
        if self._command.isShow()   : actionUtils.show()
        if self._command.isAdd()    : actionUtils.add(commandLine=self)
        if self._command.isCheck()  : actionUtils.check(commandLine=self)
        if self._command.isUncheck(): actionUtils.uncheck(commandLine=self)
        if self._command.isHelp()   : actionUtils.help()
        if self._command.isError()  : actionUtils.error(commandLine=self)

    def subCommandIsProject(self):
        return self._subCommand.isProject()

    def subCommandIsTask(self):
        return self._subCommand.isTask()

class Task:
    def __init__(self, id_: int, description: str, done: bool) -> None:
        self.id = id_
        self.description = description
        self.done = done

    def __str__(self) -> str:
        return f"  [{'x' if self.is_done() else ' '}] {self.id}: {self.description}"

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

    def __str__(self) -> str:
        return self._name

    def addTask(self, id:int, description:str) -> None:
        task = Task(id_=id, description=description, done=False)
        self._tasks.append(task)

    def isGoodName(self, name:str) -> bool:
        return self._name == name

    def findTaskById(self, id:int) -> Task:
        for task in self._tasks:
            if task.isGoodId(id=id): return task
        return None

    def lastTaskId(self) -> int:
        taskIds = [task.id for task in self._tasks]
        if len(taskIds) == 0:
            return 0
        return max(taskIds)

class ActionUtils:

    def __init__(self, console:Console, projects:List[Project]) -> None:
        self._console = console
        self._projects = projects

    def _nextTaskId(self) -> int:
        maxTaskIds = [project.lastTaskId() for project in self._projects]
        return max(maxTaskIds) + 1

    def show(self) -> None:
        self._console.printShow(projects=self._projects)

    def add(self, commandLine: CommandLine) -> None:
        if commandLine.subCommandIsProject():
            self._addProject(commandLine=commandLine)
        if commandLine.subCommandIsTask():
            self._addTask(commandLine=commandLine)

    def _findProjectByName(self, name:str) -> Project:
        for project in self._projects:
            if project.isGoodName(name=name):
                return project
        return None

    def _addProject(self, commandLine: CommandLine) -> None:
        self._projects.append(Project(name=commandLine._arguments[0]._value))

    def _addTask(self, commandLine:CommandLine) -> None:
        arguments = commandLine._arguments
        project = arguments[0]._value
        description = arguments[1]._value
        project_tasks = self._findProjectByName(name=project)
        if project_tasks is None:
            self._console.printProjectNotFound(projectName=project)
            return
        taskId = self._nextTaskId()
        project_tasks.addTask(id=taskId, description=description)

    def check(self, commandLine: CommandLine) -> None:
        id_string = commandLine._arguments[0]._value
        self._setDone(id_string, True)

    def uncheck(self, commandLine: CommandLine) -> None:
        id_string = commandLine._arguments[0]._value
        self._setDone(id_string, False)

    def _setDone(self, id_string: str, done: bool) -> None:
        id_ = int(id_string)
        for project in self._projects:
            task = project.findTaskById(id=id_)
            if task is not None: 
                task.set_done(done)
                return
        self._console.printTaskNotFound(id=id_)

    def help(self) -> None:
        self._console.printHelp()

    def error(self, commandLine: CommandLine) -> None:
        self._console.printError(command=commandLine._command._value)

class TaskList:
    QUIT = "quit"

    def __init__(self, console: Console) -> None:

        self.console = console
        self.tasks: List[Project] = []

    def run(self) -> None:
        while True:
            command = self.console.input("> ")
            if command == self.QUIT:
                break
            self.execute(command)

    def execute(self, command_line: str) -> None:

        actionUtils = ActionUtils(console=self.console, projects=self.tasks)
        commandLine = CommandLine(value=command_line)
        commandLine.execute(actionUtils=actionUtils)