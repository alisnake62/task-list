from typing import List

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

    def addNewLine(self) -> None:
        self._outputStr += "\n"

class ProjectName:

    _value:str

    def __init__(self, projetNameStr:str) -> None:
        self._value = projetNameStr

    def __str__(self) -> str:
        return self._value

    def __eq__(self, otherProjectName: object) -> bool:
        return self._value == otherProjectName._value

class ProjectFounded:

    _value:bool

    def __init__(self, projectFoundedBooleanValue:bool = False) -> None:
        self._value = projectFoundedBooleanValue

    def __eq__(self, otherProjectFounded: object) -> bool:
        return self._value == otherProjectFounded._value

class TaskId:

    _value:int

    def __init__(self, taskIdInt:int=0) -> None:
        self._value = taskIdInt

    def __str__(self) -> str:
        return str(self._value)

    def __eq__(self, otherTaskId: object) -> bool:
        return self._value == otherTaskId._value

    def _valuePlusOne(self) -> None:
        self._value += 1

    def nextOne(self) -> 'TaskId':
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

    def __str__(self) -> str:
        if self._value:
            return "[x]"
        return "[ ]"

class TaskFounded:

    _value:bool

    def __init__(self, taskFoundedBooleanValue:bool = False) -> None:
        self._value = taskFoundedBooleanValue

    def __eq__(self, otherTaskFounded: object) -> bool:
        return self._value == otherTaskFounded._value

class SubCommandType:

    _expectedValue = ["project", "task"]
    _value: str

    def __init__(self, subCommandStr:str) -> None:
        self._value = subCommandStr

    def isProject(self) -> bool:
        return self._value == "project"  # degager les method is et faire un __eq__ (faire 2 version)

    def isTask(self) -> bool:
        return self._value == "task"

    def isError(self) -> bool:
        return self._value not in self._expectedValue

class CommandType:

    _expectedValue:List[str] = ["show", "add", "check", "uncheck", "help", "quit"]
    _value:str

    def __init__(self, commandStr:str) -> None:
        self._value = commandStr

    def __str__(self) -> str:
        return self._value

    def isShow(self) -> bool:
        return self._value == "show"   # degager les method is et faire un __eq__ (faire 2 version)

    def isAdd(self) -> bool:
        return self._value == "add"

    def isCheck(self) -> bool:
        return self._value == "check"

    def isUncheck(self) -> bool:
        return self._value == "uncheck"

    def isHelp(self) -> bool:
        return self._value == "help"

    def isQuit(self) -> bool:
        return self._value == "quit"

    def isError(self) -> bool:
        return self._value not in self._expectedValue