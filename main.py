import os
import rlcompleter
import readline
from system.comploader import CompLoader
from system.commandhandler import CommandHandler


readline.parse_and_bind('tab: complete')

comp_libraries = [os.path.abspath(os.path.join(os.getcwd(), 'complib'))]

CompLoader().load_components(comp_libraries)
CommandHandler()

while True:
    # Wait for user input
    line = raw_input('pyframe # ')

    if line == 'exit' or line == 'quit' or  line == 'q':
        break
        
    try:
        CommandHandler().handle_command(line)
    except Exception as exc:
        # Execute the command in the shell
        raise
    
