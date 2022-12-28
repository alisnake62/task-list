import sys

from app import ProgramLoop, Console


def main():
    task_list = ProgramLoop(Console(sys.stdin, sys.stdout))
    task_list.run()


if __name__ == "__main__":
    main()

