from .app import BrainfooApp
import argparse

parser = argparse.ArgumentParser(
                    prog='brainfoo',
                    description='A TUI Brainfk debugger',
                    epilog='https://github.com/Sim3-14159/Brainfoo')

parser.add_argument('filename', nargs='?', default=None) 

args = parser.parse_args()
print(args.filename)

def main() -> None:
    BrainfooApp().run()

if __name__ == "__main__":
    main()
