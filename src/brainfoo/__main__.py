"""
Way to access app.py
"""

import argparse
from brainfoo.app import BrainfooApp


print("""
    \033[35;1m,-~-^*-**^~~.\033[0m
   \033[35;1m/             \\\033[0m
  \033[35;1m(    \033[32;1m.\033[0;35m \033[32;1;5m>\033[0;35m \033[32;1m.\033[0;35m \033[32;1m.\033[35m    |\033[0m
  \033[35;1m|    \033[30;43mf\033[0;1;35m   \033[30;43mo\033[0;1;35m \033[30;43mo\033[0;1;35m    )\033[0m
  \033[35;1m(          _.-./\033[0m
   \033[35;1m\\        /*\033[0m
    \033[35;1m~%/__~*^\033[0m
     \033[35;1m,%\033[0m
""")

parser = argparse.ArgumentParser(
                    prog='brainfoo',
                    description='A TUI Brainfk debugger',
                    epilog='https://github.com/Sim3-14159/Brainfoo')

parser.add_argument('filename', nargs='?', default=None)
args = parser.parse_args()

def main() -> None:
    """The main function, runs BrainfooApp"""
    BrainfooApp().run()

if __name__ == "__main__":
    main()
