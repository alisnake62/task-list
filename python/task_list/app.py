from typing import List

from console import Console

class Task:
    def __init__(self, id: int, description: str, done: bool = False) -> None:
        self._id = id
        self._description = description
        self._done = done

    def __str__(self) -> str:
        return f"  [{'x' if self.is_done() else ' '}] {self._id}: {self._description}"

    def set_done(self, done: bool) -> None:
        self._done = done

    def is_done(self) -> bool:
        return self._done

    def isThisId(self, id:int) -> bool:
        return self._id == id

class Project:

    def __init__(self, name:str) -> None:
        self._name = name
        self._tasks:List[Task] = []

    def __str__(self) -> str:
        return self._name

    def addTask(self, id:int, description:str) -> None:
        self._tasks.append(Task(id=id, description=description))

    def isThisName(self, name:str) -> bool:
        return self._name == name

    def findTaskById(self, id:int) -> Task:
        for task in self._tasks:
            if task.isThisId(id=id): return task
        return None

    def lastTaskId(self) -> int:
        taskIds = [task._id for task in self._tasks]   # à modif
        if len(taskIds) == 0:
            return 0
        return max(taskIds)

class ArgumentLine:
    pass

class ArgumentLineAdd(ArgumentLine):

    _projectName:str
    _taskDescription:str = None

    def __init__(self, projectName:str, taskDescription:str=None) -> None:
        self._projectName = projectName
        self._taskDescription = taskDescription

    def _nextTaskId(self, projects:List[Project]) -> int:
        maxTaskIds = [project.lastTaskId() for project in projects]
        return max(maxTaskIds) + 1

    def addProject(self, projects:List[Project]) -> None:
        projects.append(Project(name=self._projectName))

    def addTask(self, projects:List[Project], console:Console) -> None:

        projectFound = False
        for project in projects:
            if project.isThisName(name=self._projectName):
                projectFound = True
                taskId = self._nextTaskId(projects=projects)
                project.addTask(id=taskId, description=self._taskDescription)
                break

        if not projectFound:
            console.printProjectNotFound(projectName=self._projectName)

class ArgumentLineSetDone(ArgumentLine):

    _taskId:int

    def __init__(self, taskIdStr:str) -> None:
        self._taskId = int(taskIdStr)

    def _findTaskById(self, projects:List[Project], console:Console) -> Task:
        for project in projects:
            findedTask = project.findTaskById(id=self._taskId)
            if findedTask is not None:
                return findedTask

        console.printTaskNotFound(taskId=self._taskId)

    def checkTask(self, projects:List[Project], console:Console) -> None:
        task = self._findTaskById(projects=projects, console=console)
        if task is not None:
            task.set_done(done=True)

    def uncheckTask(self, projects:List[Project], console:Console) -> None:
        task = self._findTaskById(projects=projects, console=console)
        if task is not None:
            task.set_done(done=False)

class SubCommand:

    _expectedValue = ["project", "task"]

    def __init__(self, value:str) -> None:
        self._value = value

    def createArgumentLineAdd(self, argumentLineStr:str) -> ArgumentLineAdd:
        if self._isProject():
            return ArgumentLineAdd(projectName=argumentLineStr)

        if self._isTask():
            argumentLineSplited = argumentLineStr.split(" ")
            projectName = argumentLineSplited[0]
            taskDescription = argumentLineSplited[1]
            return ArgumentLineAdd(projectName=projectName, taskDescription=taskDescription)

    def executeAdd(self, argumentLine:ArgumentLineAdd, projects:List[Project], console:Console) -> None:
        if self._isProject():
            argumentLine.addProject(projects=projects)

        if self._isTask():
            argumentLine.addTask(projects=projects, console=console)

    def _isProject(self):
        return self._value == "project"

    def _isTask(self):
        return self._value == "task"

class CommandRest:

    _subCommand:SubCommand = None
    _argumentLine:ArgumentLine

    def __init__(self, subCommandStr:str=None, argumentLineStr:str=None, taskIdStr:str=None) -> None:
        if subCommandStr is not None:
            self._subCommand = SubCommand(value=subCommandStr)
            self._argumentLine = self._subCommand.createArgumentLineAdd(argumentLineStr=argumentLineStr)
            return

        if taskIdStr is not None:
            self._argumentLine = ArgumentLineSetDone(taskIdStr=taskIdStr)
            return

    def executeAdd(self, projects:List[Project], console:Console) -> None:
        self._subCommand.executeAdd(argumentLine=self._argumentLine, projects=projects, console=console)

    def executeCheck(self, projects:List[Project], console:Console) -> None:
        self._argumentLine.checkTask(projects=projects, console=console)

    def executeUncheck(self, projects:List[Project], console:Console) -> None:
        self._argumentLine.uncheckTask(projects=projects, console=console)

class Command:

    _expectedValue = ["show", "add", "check", "uncheck", "help"]

    def __init__(self, value:str) -> None:
        self._value = value

    def createCommandRest(self, commandRestStr:str) -> CommandRest:
        if self._isAdd():
            commandRestStrSplited = commandRestStr.split(" ", 1)
            subCommandStr   = commandRestStrSplited[0]
            argumentLineStr    = commandRestStrSplited[1]
            return CommandRest(subCommandStr=subCommandStr, argumentLineStr=argumentLineStr)

        if self._isCheck() or self._isUncheck():
            return CommandRest(taskIdStr=commandRestStr)

    def execute(self, commandRest:CommandRest, projects:List[Project], console:Console) -> None:

        if self._isShow():
            console.printShow(projects=projects)
            return

        if self._isAdd():
            commandRest.executeAdd(projects=projects, console=console)
            return

        if self._isCheck():
            commandRest.executeCheck(projects=projects, console=console)
            return

        if self._isUncheck():
            commandRest.executeUncheck(projects=projects, console=console)
            return

        if self._isHelp():
            console.printHelp()
            return

        if self._isError():
            console.printError(command=self._value)
            return

    def _isShow(self):
        return self._value == "show"

    def _isAdd(self):
        return self._value == "add"

    def _isCheck(self):
        return self._value == "check"

    def _isUncheck(self):
        return self._value == "uncheck"

    def _isHelp(self):
        return self._value == "help"

    def _isError(self):
        return self._value not in self._expectedValue

class CommandLine:

    _command:Command
    _commandRest:CommandRest = None

    def __init__(self, value:str) -> None:

        commandLineSplited = value.split(" ", 1)
        self._command = Command(value=commandLineSplited[0])

        if len(commandLineSplited) > 1:
            self._commandRest = self._command.createCommandRest(commandRestStr=commandLineSplited[1])

    def execute(self, projects:List[Project], console:Console) -> None:
        self._command.execute(commandRest=self._commandRest, projects=projects, console=console)

class TaskList:
    QUIT = "quit"

    def __init__(self, console: Console) -> None:

        self._console = console
        self._projects: List[Project] = []

    def run(self) -> None:
        while True:
            command = self._console.input("> ")
            if command == self.QUIT:
                break
            self.execute(command)

    def execute(self, command_line: str) -> None:

        commandLine = CommandLine(value=command_line)
        commandLine.execute(projects=self._projects, console=self._console)
        test = "toto"