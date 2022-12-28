from typing import List

from console import Console

from copy import deepcopy

class ProjectName:

    _value:str

    def __init__(self, projetNameStr:str) -> None:
        self._value = projetNameStr

    def __str__(self) -> str:
        return self._value

    def __eq__(self, otherProjectName: object) -> bool:
        return self._value == otherProjectName._value

class TaskId:

    _value:int

    def __init__(self, taskIdInt:int) -> None:
        self._value = taskIdInt

    def __str__(self) -> str:
        return str(self._value)

    def __eq__(self, otherTaskId: object) -> bool:
        return self._value == otherTaskId._value

    def _valuePlusOne(self):
        self._value += 1

    def nextOne(self):
        nextTaskId = deepcopy(self)
        nextTaskId._valuePlusOne()
        return nextTaskId

class TaskDescription:

    _value:str

    def __init__(self, taskDescriptionStr:str) -> None:
        self._value = taskDescriptionStr

    def __str__(self) -> str:
        return self._value

class TaskDone:

    _value:bool

    def __init__(self, taskDoneBooleanValue:bool) -> None:
        self._value = taskDoneBooleanValue

    def is_done(self) -> bool:
        return self._value

class TaskIdentity:

    _id: TaskId
    _description: TaskDescription

    def __init__(self, id: TaskId, description:TaskDescription) -> None:
        self._id = id
        self._description = description

    def __str__(self) -> str:
        return f"{self._id}: {self._description}"

    def isThisId(self, id:TaskId) -> bool:
        return self._id == id

class Task:

    _identity: TaskIdentity
    _done: TaskDone

    def __init__(self, identity:TaskIdentity, done:TaskDone=TaskDone(taskDoneBooleanValue=False)) -> None:
        self._identity = identity
        self._done = done

    def __str__(self) -> str:
        return f"  [{'x' if self._done.is_done() else ' '}] {self._identity}"  # à modif

    def set_done(self, done: TaskDone) -> None:
        self._done = done

    def isThisId(self, id:TaskId) -> bool:
        return self._identity.isThisId(id=id)

class Project:

    def __init__(self, name:ProjectName) -> None:
        self._name = name
        self._tasks:List[Task] = []

    def __str__(self) -> str:
        return str(self._name)

    def addTask(self, task:Task) -> None:
        self._tasks.append(task)

    def isThisName(self, name:ProjectName) -> bool:
        return self._name == name

    def findTaskById(self, id:TaskId) -> Task:
        for task in self._tasks:
            if task.isThisId(id=id): return task
        return None

class ProjectList:

    _projects:List[Project] = []
    _lastTaskId:TaskId = TaskId(taskIdInt=0)

    # 2 indentation, à revoir
    def __str__(self) -> str:
        strValue = ""
        for project in self._projects:
            strValue += f"{project}\n"
            for task in project._tasks:
                strValue += f"{task}\n"
            strValue += "\n"
        return strValue

    # 2 indentation, à revoir
    def _findTaskById(self, taskId:TaskId, console:Console) -> Task:
        for project in self._projects:
            findedTask = project.findTaskById(id=taskId)
            if findedTask is not None:
                return findedTask

        console.printTaskNotFound(taskId=taskId)

    # 2 indentation, à revoir
    def addTask(self, projectName:ProjectName, taskDescription:TaskDescription, console:Console):

        projectFound = False
        for project in self._projects:
            if project.isThisName(name=projectName):
                projectFound = True
                taskId = self._lastTaskId.nextOne()
                taskIdentity = TaskIdentity(id=taskId, description=taskDescription)
                project.addTask(Task(identity=taskIdentity))
                self._lastTaskId = taskId
                break

        if not projectFound:
            console.printProjectNotFound(projectName=projectName)

    def addProject(self, project:Project) -> None:
        self._projects.append(project)

    def checkTask(self, taskId:TaskId, console:Console) -> None:
        task = self._findTaskById(taskId=taskId, console=console)
        if task is not None:
            task.set_done(done=TaskDone(taskDoneBooleanValue=True))

    def uncheckTask(self, taskId:TaskId, console:Console) -> None:
        task = self._findTaskById(taskId=taskId, console=console)
        if task is not None:
            task.set_done(done=TaskDone(taskDoneBooleanValue=False))

class ArgumentLine:
    pass

class ArgumentLineAdd(ArgumentLine):

    _projectName:ProjectName
    _taskDescription:TaskDescription = None

    def __init__(self, projectName:ProjectName, taskDescription:TaskDescription=None) -> None:
        self._projectName = projectName
        self._taskDescription = taskDescription

    def addProject(self, projects:ProjectList) -> None:
        projects.addProject(Project(name=self._projectName))

    def addTask(self, projects:ProjectList, console:Console) -> None:
        projects.addTask(projectName=self._projectName, taskDescription=self._taskDescription, console=console)

class ArgumentLineSetDone(ArgumentLine):

    _taskId:TaskId

    def __init__(self, taskId:TaskId) -> None:
        self._taskId = taskId

    def checkTask(self, projects:ProjectList, console:Console) -> None:
        projects.checkTask(taskId=self._taskId, console=console)

    def uncheckTask(self, projects:ProjectList, console:Console) -> None:
        projects.uncheckTask(taskId=self._taskId, console=console)

class SubCommandType:

    _expectedValue = ["project", "task"]

    def __init__(self, subCommandStr:str) -> None:
        self._value = subCommandStr

    def isProject(self):
        return self._value == "project"

    def isTask(self):
        return self._value == "task"

    def isError(self):
        return self._value not in self._expectedValue

class SubCommand:

    _type:SubCommandType

    def __init__(self, type:SubCommandType) -> None:
        self._type = type

    def createArgumentLineAdd(self, argumentLineStr:str) -> ArgumentLineAdd:
        if self._type.isProject():
            projectName = ProjectName(projetNameStr=argumentLineStr)
            return ArgumentLineAdd(projectName=projectName)

        if self._type.isTask():
            argumentLineSplited = argumentLineStr.split(" ")
            projectName = ProjectName(projetNameStr=argumentLineSplited[0])
            taskDescription = TaskDescription(taskDescriptionStr=argumentLineSplited[1])
            return ArgumentLineAdd(projectName=projectName, taskDescription=taskDescription)

    def executeAdd(self, argumentLine:ArgumentLineAdd, projects:ProjectList, console:Console) -> None:
        if self._type.isProject():
            argumentLine.addProject(projects=projects)

        if self._type.isTask():
            argumentLine.addTask(projects=projects, console=console)

class CommandRest:

    _subCommand:SubCommand = None
    _argumentLine:ArgumentLine

    def __init__(self, subCommand:SubCommand=None, argumentLineStr:str=None, taskId:TaskId=None) -> None:
        if subCommand is not None:
            self._subCommand = subCommand
            self._argumentLine = self._subCommand.createArgumentLineAdd(argumentLineStr=argumentLineStr)
            return

        if taskId is not None:
            self._argumentLine = ArgumentLineSetDone(taskId=taskId)
            return

    def executeAdd(self, projects:ProjectList, console:Console) -> None:
        self._subCommand.executeAdd(argumentLine=self._argumentLine, projects=projects, console=console)

    def executeCheck(self, projects:ProjectList, console:Console) -> None:
        self._argumentLine.checkTask(projects=projects, console=console)

    def executeUncheck(self, projects:ProjectList, console:Console) -> None:
        self._argumentLine.uncheckTask(projects=projects, console=console)

class CommandType:
    
    _expectedValue:List[str] = ["show", "add", "check", "uncheck", "help"]

    def __init__(self, commandStr:str) -> None:
        self._value = commandStr

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

    def printError(self, console:Console):
        console.printError(command=self._value)

class Command:

    _type:CommandType

    def __init__(self, type:CommandType) -> None:
        self._type = type

    def createCommandRest(self, commandRestStr:str) -> CommandRest:
        if self._type.isAdd():
            commandRestStrSplited = commandRestStr.split(" ", 1)
            subCommandStr   = commandRestStrSplited[0]
            argumentLineStr    = commandRestStrSplited[1]
            subCommand = SubCommand(type=SubCommandType(subCommandStr=subCommandStr))
            return CommandRest(subCommand=subCommand, argumentLineStr=argumentLineStr)

        if self._type.isCheck() or self._type.isUncheck():
            taskId = TaskId(taskIdInt=int(commandRestStr))
            return CommandRest(taskId=taskId)

    def execute(self, commandRest:CommandRest, projects:ProjectList, console:Console) -> None:

        if self._type.isShow():
            console.printShow(projects=projects)
            return

        if self._type.isAdd():
            commandRest.executeAdd(projects=projects, console=console)
            return

        if self._type.isCheck():
            commandRest.executeCheck(projects=projects, console=console)
            return

        if self._type.isUncheck():
            commandRest.executeUncheck(projects=projects, console=console)
            return

        if self._type.isHelp():
            console.printHelp()
            return

        if self._type.isError():
            self._type.printError(console=console)
            return

class CommandLine:

    _command:Command
    _commandRest:CommandRest = None

    def __init__(self, commandLineStr:str) -> None:

        commandLineSplited = commandLineStr.split(" ", 1)
        commandStr = commandLineSplited[0]
        self._command = Command(type=CommandType(commandStr=commandStr))

        if len(commandLineSplited) > 1:
            self._commandRest = self._command.createCommandRest(commandRestStr=commandLineSplited[1])

    def execute(self, projects:ProjectList, console:Console) -> None:
        self._command.execute(commandRest=self._commandRest, projects=projects, console=console)

class TaskList:
    QUIT = "quit"
    _console:Console
    _projects:ProjectList

    def __init__(self, console: Console) -> None:

        self._console = console
        self._projects = ProjectList()

    def run(self) -> None:
        while True:
            command = self._console.input("> ")
            if command == self.QUIT:
                break
            self.execute(command)

    def execute(self, command_line: str) -> None:
        commandLine = CommandLine(commandLineStr=command_line)
        commandLine.execute(projects=self._projects, console=self._console)
