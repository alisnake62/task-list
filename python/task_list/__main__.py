import sys

from console import Console
from app import TaskList


def main():
    task_list = TaskList(Console(sys.stdin, sys.stdout))
    task_list.run()


if __name__ == "__main__":
    main()

