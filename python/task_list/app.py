from typing import Dict, List, TYPE_CHECKING

if TYPE_CHECKING: from app import TaskList, ActionUtils, CommandLine

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

    def isGoodId(self, id:int) -> bool:
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

    def add(self, commandLine: 'CommandLine') -> None:
        if commandLine.subCommandIsProject():
            self._addProject(commandLine=commandLine)
        if commandLine.subCommandIsTask():
            self._addTask(commandLine=commandLine)

    def _findProjectByName(self, commandLine: 'CommandLine') -> Project:
        for project in self._projects:
            if project.isThisName(commandLine=commandLine):
                return project
        return None

    def _addProject(self, commandLine: 'CommandLine') -> None:
        commandLine.addProject(projects=self._projects)

    def _addTask(self, commandLine:'CommandLine') -> None:
        project = self._findProjectByName(commandLine=commandLine)
        if project is None:
            self._console.printProjectNotFound(projectName=commandLine._arguments[0]._value)  # à modif
            return
        taskId = self._nextTaskId()
        project.addTask(id=taskId, commandLine=commandLine)

    def check(self, commandLine: 'CommandLine') -> None:
        commandLine.setTaskDone(projects=self._projects, done=True)
        self._console.printTaskNotFound(id=3)   # à modif

    def uncheck(self, commandLine: 'CommandLine') -> None:
        commandLine.setTaskDone(projects=self._projects, done=False)
        self._console.printTaskNotFound(id=3)   # à modif

    def help(self) -> None:
        self._console.printHelp()

    def error(self, commandLine: 'CommandLine') -> None:
        self._console.printError(command=commandLine._command._value)  # à modif

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

    def addTask(self, projects:List[Project]) -> None:
        for project in projects:
            if project.isThisName(name=self._projectName):

                taskId = self._nextTaskId(projects=projects)
                project.addTask(id=taskId, description=self._taskDescription)
                break

class ArgumentLineSetDone(ArgumentLine):

    _taskId:int

    def __init__(self, taskIdStr:str) -> None:
        self._taskId = int(taskIdStr)

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

    def executeAdd(self, argumentLine:ArgumentLineAdd, projects:List[Project]) -> None:
        if self._isProject():
            argumentLine.addProject(projects=projects)

        if self._isTask():
            argumentLine.addTask(projects=projects)

    def _isProject(self):
        return self._value == "project"

    def _isTask(self):
        return self._value == "task"

# class Argument:
#     def __init__(self, value:str) -> None:
#         self._value = value

#     def isThis(self, argument:str):
#         return self._value == argument

#     def createTask(self, id:int) -> 'Task':
#         return Task(id_=id, description=self._value, done=False)

#     def setTaskDone(self, projects:List['Project'], done:bool) -> None:
#         id = int(self._value)
#         for project in projects:
#             task = project.findTaskById(id=id)
#             if task is not None: 
#                 task.set_done(done)
#                 return

#     def addProject(self, projects:List['Project']) -> None:
#         projects.append(Project(name=self._value))


class CommandRest:

    _subCommand:SubCommand = None
    _argumentLine:ArgumentLine

    def __init__(self, subCommandStr:str=None, argumentLineStr:str=None, taskIdStr:str=None) -> None:
        if subCommandStr is not None:
            self._subCommand = SubCommand(value=subCommandStr)
            self._argumentLine = self._subCommand.createArgumentLineAdd(argumentLineStr=argumentLineStr)

        if taskIdStr is not None:
            self._argumentLine = ArgumentLineSetDone(taskIdStr=taskIdStr)

    def executeAdd(self, projects:List[Project]) -> None:
        self._subCommand.executeAdd(argumentLine=self._argumentLine, projects=projects)

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

    def execute(self, commandRest:CommandRest, projects:List[Project]) -> None:
        if self._isAdd():
            commandRest.executeAdd(projects=projects)

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

    def error(self, taskList:'TaskList'):
        taskList.error(self._value)



class CommandLine:

    _command:Command
    _commandRest:CommandRest = None

    def __init__(self, value:str) -> None:

        commandLineSplited = value.split(" ", 1)
        self._command = Command(value=commandLineSplited[0])

        if len(commandLineSplited) > 1:
            self._commandRest = self._command.createCommandRest(commandRestStr=commandLineSplited[1])

    def execute(self, projects:List[Project]) -> None:
        self._command.execute(commandRest=self._commandRest, projects=projects)

    def subCommandIsProject(self):
        return self._subCommand.isProject()

    def subCommandIsTask(self):
        return self._subCommand.isTask()

    def isThisProject(self, projectName:str):
        if len(self._arguments) > 0:
            return self._arguments[0].isThis(argument=projectName)
        return False

    # def createTask(self, id:int) -> 'Task':
    #     if len(self._arguments) > 1:
    #         return self._arguments[1].createTask(id=id)

    def setTaskDone(self, projects:List['Project'], done:bool) -> None:
        if len(self._arguments) > 0:
            self._arguments[0].setTaskDone(projects=projects, done=done)

    def addProject(self, projects:List['Project']) -> None:
        if len(self._arguments) > 0:
            self._arguments[0].addProject(projects=projects)


class TaskList:
    QUIT = "quit"

    def __init__(self, console: Console) -> None:

        self.console = console
        self._projects: List[Project] = []

    def run(self) -> None:
        while True:
            command = self.console.input("> ")
            if command == self.QUIT:
                break
            self.execute(command)

    def execute(self, command_line: str) -> None:

        # actionUtils = ActionUtils(console=self.console, projects=self.tasks)
        commandLine = CommandLine(value=command_line)
        commandLine.execute(projects=self._projects)
        test = "toto"