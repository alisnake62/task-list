import sys

from console import Console
from app import ProgramLoop


def main():
    task_list = ProgramLoop(Console(sys.stdin, sys.stdout))
    task_list.run()


if __name__ == "__main__":
    main()

