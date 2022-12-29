from typing import List, IO, TYPE_CHECKING

if TYPE_CHECKING: from app import Console

from copy import deepcopy

class ConsoleOuput:

    _outputStr:str

    def __init__(self, outputStr:str = None) -> None:

        self._outputStr = outputStr
        if self._outputStr is None:
            self._outputStr = "\n".join([
                "Commands:",
                "  show",
                "  add project <project name>",
                "  add task <project name> <task description>",
                "  check <task ID>",
                "  uncheck <task ID>"
            ])

    def __str__(self) -> str:
        return self._outputStr

    def addNewLine(self):
        self._outputStr += "\n"

class ConsoleInput:

    _inputStr:str

    def __init__(self, inputStr) -> None:
        self._inputStr = inputStr

class Console:
    def __init__(self, input_reader: IO, output_writer: IO) -> None:
        self.input_reader = input_reader
        self.output_writer = output_writer

    def _write(self, output:ConsoleOuput):

        self.output_writer.write(f"{output}")
        self.output_writer.flush()

    def _printPrompt(self) -> None:
        promptOutput = ConsoleOuput(outputStr="> ")
        self._write(output=promptOutput)

    def print(self, output:ConsoleOuput) -> None:
        output.addNewLine()
        self._write(output=output)

    def inputPrompt(self) -> str:
        self._printPrompt()
        return self.input_reader.readline()

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

    def __init__(self, taskIdInt:int=0) -> None:
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

    def __init__(self, taskDoneBooleanValue:bool = False) -> None:
        self._value = taskDoneBooleanValue

    def is_done(self) -> bool:
        return self._value

class TaskFounded:

    _value:bool

    def __init__(self, taskFoundedBooleanValue:bool = False) -> None:
        self._value = taskFoundedBooleanValue

    def __eq__(self, otherTaskFounded: object) -> bool:
        return self._value == otherTaskFounded._value

class ProjectFounded:

    _value:bool

    def __init__(self, projectFoundedBooleanValue:bool = False) -> None:
        self._value = projectFoundedBooleanValue

    def __eq__(self, otherProjectFounded: object) -> bool:
        return self._value == otherProjectFounded._value

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

    def taskFounded(self,taskId:TaskId) -> TaskFounded:
        if self._id == taskId:
            return TaskFounded(taskFoundedBooleanValue=True)
        return TaskFounded(taskFoundedBooleanValue=False)

class Task:

    _identity: TaskIdentity
    _done: TaskDone

    def __init__(self, identity:TaskIdentity, done:TaskDone=TaskDone()) -> None:
        self._identity = identity
        self._done = done

    def __str__(self) -> str:
        return f"  [{'x' if self._done.is_done() else ' '}] {self._identity}"  # à modif, degager la method is done

    def _setDoneIfFounded(self, taskId:TaskId, taskDone:TaskDone, taskFounded:TaskFounded) -> TaskFounded:
        if taskFounded == TaskFounded(taskFoundedBooleanValue=True):
            return taskFounded

        taskFounded = self._identity.taskFounded(taskId=taskId)
        if taskFounded == TaskFounded(taskFoundedBooleanValue=True):
            self._done = taskDone

        return taskFounded

    def set_done(self, done: TaskDone) -> None:
        self._done = done

    def checkIfFounded(self, taskId:TaskId, taskFounded:TaskFounded) -> TaskFounded:
        taskDone = TaskDone(taskDoneBooleanValue=True)
        return self._setDoneIfFounded(taskId=taskId, taskDone=taskDone, taskFounded=taskFounded)

    def uncheckIfFounded(self, taskId:TaskId, taskFounded:TaskFounded) -> TaskFounded:
        taskDone = TaskDone(taskDoneBooleanValue=False)
        return self._setDoneIfFounded(taskId=taskId, taskDone=taskDone, taskFounded=taskFounded)


class TaskList:

    _tasks:List[Task]

    def __init__(self) -> None:
        self._tasks = []

    def __str__(self) -> str:
        toString = ""
        for task in self._tasks:
            toString += f"{task}\n"
        toString += "\n"

        return toString

    def addTask(self, task:Task) -> None:
        self._tasks.append(task)

    def checkIfFounded(self, taskId:TaskId, taskFounded:TaskFounded) -> TaskFounded:

        for task in self._tasks:
            taskFounded = task.checkIfFounded(taskId=taskId, taskFounded=taskFounded)

        return taskFounded

    def uncheckIfFounded(self, taskId:TaskId, taskFounded:TaskFounded) -> TaskFounded:

        for task in self._tasks:
            taskFounded = task.uncheckIfFounded(taskId=taskId, taskFounded=taskFounded)

        return taskFounded

class Project:

    _name:ProjectName
    _taskList:TaskList

    def __init__(self, name:ProjectName) -> None:
        self._name = name
        self._taskList = TaskList()

    def __str__(self) -> str:
        toString = f"{self._name}\n"
        toString += f"{self._taskList}"
        return toString

    def addTask(self, task:Task) -> None:
        self._taskList.addTask(task=task)

    def isThisName(self, name:ProjectName) -> bool:
        return self._name == name

    def checkTaskIfFounded(self, taskId:TaskId, taskFounded:TaskFounded) -> TaskFounded:
        if taskFounded == TaskFounded(taskFoundedBooleanValue=True):
            return taskFounded
        return self._taskList.checkIfFounded(taskId=taskId, taskFounded=taskFounded)

    def uncheckTaskIfFounded(self, taskId:TaskId, taskFounded:TaskFounded) -> TaskFounded:
        if taskFounded == TaskFounded(taskFoundedBooleanValue=True):
            return taskFounded
        return self._taskList.uncheckIfFounded(taskId=taskId, taskFounded=taskFounded)

    def addTaskIfProjectFounded(self, projectName:ProjectName, taskIdentity:TaskIdentity, projectFounded:ProjectFounded) -> ProjectFounded:
        if projectFounded == ProjectFounded(projectFoundedBooleanValue=True):
            return projectFounded

        if self._name == projectName:
            task = Task(identity=taskIdentity)
            self._taskList.addTask(task=task)
            return ProjectFounded(projectFoundedBooleanValue=True)

        return ProjectFounded(projectFoundedBooleanValue=False)

class ProjectList:

    _projects:List[Project]

    def __init__(self) -> None:
        self._projects = []

    def __str__(self) -> str:
        toString = ""
        for project in self._projects:
            toString += f"{project}"
        return toString

    def _consolePrintIfTaskNotFound(self, taskFounded:TaskFounded, taskId:TaskId, console:Console) -> None:
        if taskFounded == TaskFounded(taskFoundedBooleanValue=False):
            outputStr = f"Could not find a task with an ID of {taskId}"
            output = ConsoleOuput(outputStr=outputStr)
            console.print(output)

    def checkTask(self, taskId:TaskId, console:Console) -> None:
        taskFounded = TaskFounded()
        for project in self._projects:
            taskFounded = project.checkTaskIfFounded(taskId=taskId, taskFounded=taskFounded)

        self._consolePrintIfTaskNotFound(taskFounded=taskFounded, taskId=taskId, console=console)

    def uncheckTask(self, taskId:TaskId, console:Console) -> None:
        taskFounded = TaskFounded()
        for project in self._projects:
            taskFounded = project.uncheckTaskIfFounded(taskId=taskId, taskFounded=taskFounded)

        self._consolePrintIfTaskNotFound(taskFounded=taskFounded, taskId=taskId, console=console)

    def addTaskIfProjectFounded(self, projectName:ProjectName, taskIdentity:TaskIdentity) -> ProjectFounded:
        projectFounded = ProjectFounded()
        for project in self._projects:
            projectFound = project.addTaskIfProjectFounded(projectName=projectName, taskIdentity=taskIdentity, projectFounded=projectFounded)

        return projectFound

    def addProject(self, project:Project) -> None:
        self._projects.append(project)


class ProgramDatas:

    _projectList:ProjectList
    _lastTaskId:TaskId

    def __init__(self) -> None:
        self._projectList = ProjectList()
        self._lastTaskId = TaskId()

    def __str__(self) -> str:
        return str(self._projectList)

    def addTask(self, projectName:ProjectName, taskDescription:TaskDescription, console:Console) -> None:

        taskId = self._lastTaskId.nextOne()
        taskIdentity = TaskIdentity(id=taskId, description=taskDescription)
        projectFounded = self._projectList.addTaskIfProjectFounded(projectName=projectName, taskIdentity=taskIdentity)

        if projectFounded == ProjectFounded(projectFoundedBooleanValue=False):
            outputStr = f"Could not find a project with the name {projectName}."
            output = ConsoleOuput(outputStr=outputStr)
            console.print(output)
            return None

        self._lastTaskId = taskId

    def addProject(self, project:Project) -> None:
        self._projectList.addProject(project=project)

    def checkTask(self, taskId:TaskId, console:Console) -> None:
        self._projectList.checkTask(taskId=taskId, console=console)

    def uncheckTask(self, taskId:TaskId, console:Console) -> None:
        self._projectList.uncheckTask(taskId=taskId, console=console)

class ArgumentLine:
    pass

class ArgumentLineAdd(ArgumentLine):

    _projectName:ProjectName
    _taskDescription:TaskDescription = None

    def __init__(self, projectName:ProjectName, taskDescription:TaskDescription=None) -> None:
        self._projectName = projectName
        self._taskDescription = taskDescription

    def addProject(self, programDatas:ProgramDatas) -> None:
        programDatas.addProject(Project(name=self._projectName))

    def addTask(self, programDatas:ProgramDatas, console:Console) -> None:
        programDatas.addTask(projectName=self._projectName, taskDescription=self._taskDescription, console=console)

class ArgumentLineSetDone(ArgumentLine):

    _taskId:TaskId

    def __init__(self, taskId:TaskId) -> None:
        self._taskId = taskId

    def check(self, programDatas:ProgramDatas, console:Console) -> None:
        programDatas.checkTask(taskId=self._taskId, console=console)

    def uncheck(self, programDatas:ProgramDatas, console:Console) -> None:
        programDatas.uncheckTask(taskId=self._taskId, console=console)

class SubCommandType:

    _expectedValue = ["project", "task"]
    _value: str

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

    def executeAdd(self, argumentLine:ArgumentLineAdd, programDatas:ProgramDatas, console:Console) -> None:
        if self._type.isProject():
            argumentLine.addProject(programDatas=programDatas)

        if self._type.isTask():
            argumentLine.addTask(programDatas=programDatas, console=console)

class CommandRest:

    _subCommand:SubCommand
    _argumentLine:ArgumentLine

    def __init__(self, subCommand:SubCommand=None, argumentLineStr:str=None, taskId:TaskId=None) -> None:
        if subCommand is not None:
            self._subCommand = subCommand
            self._argumentLine = self._subCommand.createArgumentLineAdd(argumentLineStr=argumentLineStr)
            return

        if taskId is not None:
            self._argumentLine = ArgumentLineSetDone(taskId=taskId)
            return

    def executeAdd(self, programDatas:ProgramDatas, console:Console) -> None:
        self._subCommand.executeAdd(argumentLine=self._argumentLine, programDatas=programDatas, console=console)

    def executeCheck(self, programDatas:ProgramDatas, console:Console) -> None:
        self._argumentLine.check(programDatas=programDatas, console=console)

    def executeUncheck(self, programDatas:ProgramDatas, console:Console) -> None:
        self._argumentLine.uncheck(programDatas=programDatas, console=console)

class CommandType:

    _expectedValue:List[str] = ["show", "add", "check", "uncheck", "help", "quit"]
    _value:str

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

    def isQuit(self):
        return self._value == "quit"

    def isError(self):
        return self._value not in self._expectedValue

    def printError(self, console:Console):
        outputStr = f"I don't know what the command {self._value} is."
        output = ConsoleOuput(outputStr=outputStr)
        console.print(output)

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

    def isQuit(self) -> bool:
        return self._type.isQuit()

    def execute(self, commandRest:CommandRest, programDatas:ProgramDatas, console:Console) -> None:

        if self._type.isShow():
            output = ConsoleOuput(outputStr=str(programDatas))
            console.print(output=output)
            return

        if self._type.isAdd():
            commandRest.executeAdd(programDatas=programDatas, console=console)
            return

        if self._type.isCheck():
            commandRest.executeCheck(programDatas=programDatas, console=console)
            return

        if self._type.isUncheck():
            commandRest.executeUncheck(programDatas=programDatas, console=console)
            return

        if self._type.isHelp():
            output = ConsoleOuput()
            console.print(output=output)
            return

        if self._type.isError():
            self._type.printError(console=console)
            return

class CommandLine:

    _command:Command
    _commandRest:CommandRest = None

    def __init__(self, commandLineStr:str) -> None:

        commandLineStr = commandLineStr.strip()
        commandLineSplited = commandLineStr.split(" ", 1)
        commandStr = commandLineSplited[0]
        self._command = Command(type=CommandType(commandStr=commandStr))

        if len(commandLineSplited) > 1:
            self._commandRest = self._command.createCommandRest(commandRestStr=commandLineSplited[1])

    def execute(self, programDatas:ProgramDatas, console:Console) -> None:
        self._command.execute(commandRest=self._commandRest, programDatas=programDatas, console=console)

    def isQuit(self) -> bool:
        return self._command.isQuit()

class ProgramLoop:

    _console:Console
    _programDatas:ProgramDatas

    def __init__(self, console: Console) -> None:

        self._console = console
        self._programDatas = ProgramDatas()

    def run(self) -> None:
        # 2 identation, à modif
        while True:

            commandLineStr = self._console.inputPrompt()
            commandLine = CommandLine(commandLineStr=commandLineStr)
            if commandLine.isQuit():
                break

            commandLine.execute(programDatas=self._programDatas, console=self._console)