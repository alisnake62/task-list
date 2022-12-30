from typing import List

from primitiveWrapper import ConsoleOuput, TaskDescription, TaskDone, TaskFounded, TaskId, ProjectFounded, ProjectName, CommandType, SubCommandType, LoopContinue
from console import Console

class TaskIdentity:

    _id         : TaskId
    _description: TaskDescription

    def __init__(self, id: TaskId, description:TaskDescription) -> None:
        self._id            = id
        self._description   = description

    def __str__(self) -> str:
        return f"{self._id}: {self._description}"

    def taskFounded(self,taskId:TaskId) -> TaskFounded:
        if self._id == taskId:
            return TaskFounded(taskFoundedBooleanValue=True)
        return TaskFounded(taskFoundedBooleanValue=False)

class Task:

    _identity   : TaskIdentity
    _done       : TaskDone

    def __init__(self, identity:TaskIdentity, done:TaskDone=TaskDone()) -> None:
        self._identity  = identity
        self._done      = done

    def __str__(self) -> str:
        return f"  {self._done} {self._identity}"

    def _setDoneIfFounded(self, taskId:TaskId, taskDone:TaskDone, taskFounded:TaskFounded) -> TaskFounded:
        if taskFounded == TaskFounded(taskFoundedBooleanValue=True):
            return taskFounded

        taskFounded = self._identity.taskFounded(taskId=taskId)
        if taskFounded == TaskFounded(taskFoundedBooleanValue=True):
            self._done = taskDone

        return taskFounded

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

    _name       :ProjectName
    _taskList   :TaskList

    def __init__(self, name:ProjectName) -> None:
        self._name      = name
        self._taskList  = TaskList()

    def __str__(self) -> str:
        return f"{self._name}\n{self._taskList}"

    def addTask(self, task:Task) -> None:
        self._taskList.addTask(task=task)

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
            console.print(output=ConsoleOuput(outputStr=outputStr))

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
    _lastTaskId :TaskId

    def __init__(self) -> None:
        self._projectList   = ProjectList()
        self._lastTaskId    = TaskId()

    def __str__(self) -> str:
        return str(self._projectList)

    def addTask(self, projectName:ProjectName, taskDescription:TaskDescription, console:Console) -> None:

        taskId          = self._lastTaskId.nextOne()
        taskIdentity    = TaskIdentity(id=taskId, description=taskDescription)
        projectFounded  = self._projectList.addTaskIfProjectFounded(projectName=projectName, taskIdentity=taskIdentity)

        if projectFounded == ProjectFounded(projectFoundedBooleanValue=False):
            outputStr = f"Could not find a project with the name {projectName}."
            console.print(output=ConsoleOuput(outputStr=outputStr))
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

    _projectName    :ProjectName
    _taskDescription:TaskDescription = None

    def __init__(self, projectName:ProjectName, taskDescription:TaskDescription=None) -> None:
        self._projectName       = projectName
        self._taskDescription   = taskDescription

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
            projectName         = ProjectName(projetNameStr=argumentLineSplited[0])
            taskDescription     = TaskDescription(taskDescriptionStr=argumentLineSplited[1])
            return ArgumentLineAdd(projectName=projectName, taskDescription=taskDescription)

    def executeAdd(self, argumentLine:ArgumentLineAdd, programDatas:ProgramDatas, console:Console) -> None:
        if self._type.isProject():
            argumentLine.addProject(programDatas=programDatas)

        if self._type.isTask():
            argumentLine.addTask(programDatas=programDatas, console=console)

class CommandRest:

    _subCommand     :SubCommand
    _argumentLine   :ArgumentLine

    def __init__(self, subCommand:SubCommand=None, argumentLineStr:str=None, taskId:TaskId=None) -> None:
        if subCommand is not None:
            self._subCommand    = subCommand
            self._argumentLine  = self._subCommand.createArgumentLineAdd(argumentLineStr=argumentLineStr)
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

class Command:

    _type:CommandType

    def __init__(self, type:CommandType) -> None:
        self._type = type

    def createCommandRest(self, commandRestStr:str) -> CommandRest:
        if self._type.isAdd():
            commandRestStrSplited   = commandRestStr.split(" ", 1)
            subCommandStr           = commandRestStrSplited[0]
            argumentLineStr         = commandRestStrSplited[1]
            subCommand              = SubCommand(type=SubCommandType(subCommandStr=subCommandStr))
            return CommandRest(subCommand=subCommand, argumentLineStr=argumentLineStr)

        if self._type.isCheck() or self._type.isUncheck():
            taskId = TaskId(taskIdInt=int(commandRestStr))
            return CommandRest(taskId=taskId)

    def loopContinue(self) -> LoopContinue:
        if self._type.isQuit():
            return LoopContinue(loopContinueBooleanValue=False)
        return LoopContinue(loopContinueBooleanValue=True)

    def execute(self, commandRest:CommandRest, programDatas:ProgramDatas, console:Console) -> None:

        if self._type.isShow():
            console.print(output=ConsoleOuput(outputStr=str(programDatas)))
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
            console.print(output=ConsoleOuput())
            return

        if self._type.isError():
            outputStr = f"I don't know what the command {self._type} is."
            console.print(output=ConsoleOuput(outputStr=outputStr))
            return

class CommandLine:

    _command    :Command
    _commandRest:CommandRest = None

    def __init__(self, commandLineStr:str) -> None:

        commandLineStr      = commandLineStr.strip()
        commandLineSplited  = commandLineStr.split(" ", 1)
        commandStr          = commandLineSplited[0]
        self._command       = Command(type=CommandType(commandStr=commandStr))

        if len(commandLineSplited) > 1:
            self._commandRest = self._command.createCommandRest(commandRestStr=commandLineSplited[1])

    def execute(self, programDatas:ProgramDatas, console:Console) -> None:
        self._command.execute(commandRest=self._commandRest, programDatas=programDatas, console=console)

    def loopContinue(self) -> LoopContinue:
        return self._command.loopContinue()

class ProgramLoop:

    _console        :Console
    _programDatas   :ProgramDatas

    def __init__(self, console: Console) -> None:

        self._console       = console
        self._programDatas  = ProgramDatas()

    def run(self) -> None:
        
        loopContinue = LoopContinue()
        while loopContinue == LoopContinue(loopContinueBooleanValue=True):

            commandLineStr  = self._console.inputPrompt()
            commandLine     = CommandLine(commandLineStr=commandLineStr)

            loopContinue = commandLine.loopContinue()

            commandLine.execute(programDatas=self._programDatas, console=self._console)