import os
import fileio
import curses
import logging
logging.basicConfig(
    filename="debug.log",
    level=logging.DEBUG
)
# Document structure: each string is intended to represent one row.
file = [
    " "  # <- cursor starts here
]
lefty = False
screen = curses.initscr()
righty = False
# Cursor position: cursorrow selects the row, cursorcol selects the character.
cursorcol = 0
cursorrow = 0
delete_key_pressed = False
tempfile = file
key = ""
def on_start(screen):
    logging.info("program init...\n")
    screen.keypad(True)
    curses.noecho()
    curses.cbreak()
    global enter_key_pressed, file_name, testgrid
    file_name = "/home/farisz/programming/textedit/text.txt"
    enter_key_pressed = False
    # TODO: This currently flattens all rows into one character list.
    # The row system should eventually preserve file[row].
    testrow = file
    testgrid = [char for item in file for char in item]
    screen.addstr(cursorrow, cursorcol, str(testgrid))
    logging.info("program done initializing, moving to main loop() function\n")
    loop(screen)
def string_to_list(turnlist):
    # TODO: Decide whether this should operate on one row or the whole document.
    turnlist = [char for item in file for char in item]
def list_to_string(turnstring):
    global key, cursorcol, file
    # TODO: This still assumes file is one string instead of multiple rows.
    turnstring = list(file)
    turnstring.insert(cursorcol, key)
def stdin(screen):
    # Read one keypress and turn it into an editor action.
    global lefty, righty, delete_key_pressed
    global cursorcol, cursorrow, enter_key_pressed, key, file
    key = screen.get_wch()
    if key == 19:
        fileio.writefile()
        screen.clear()
        screen.addstr(0, 0, "file saved!")
        screen.refresh()
    if key == '\x13':
        fileio.writefile()
    if key == curses.KEY_LEFT:
        lefty = True
    elif key == curses.KEY_RIGHT:
        righty = True
    elif key == curses.KEY_UP:
        if cursorrow > 0:
            cursorrow -= 1
            if cursorcol > len(file[cursorrow]):
                cursorcol = len(file[cursorrow])

    elif key == curses.KEY_DOWN:
        if cursorrow < len(file) - 1:
            cursorrow += 1
            if cursorcol > len(file[cursorrow]):
                cursorcol = len(file[cursorrow])
        else:
            file.append("")
            cursorrow += 1
            cursorcol = 0
    elif key == curses.KEY_BACKSPACE:
        delete_key_pressed = True
    elif key == curses.KEY_ENTER:
        # TODO: Enter needs to split the current row into two rows.
        enter_key_pressed = True
    else:
        if key != '\x13' and isinstance(key, str):
            insertion(cursorrow,cursorcol,key)
            cursorcol += 1
            if cursorcol >= curses.COLS:
                if cursorrow < len(file) - 1:
                    cursorrow += 1
                else:
                    file.insert(cursorrow + 1, "")
                    cursorrow += 1
                cursorcol = 0
def insertion(cursorrow, cursorcol, key):
    global tempfile
    tempfile = list(file[cursorrow])
    tempfile.insert(cursorcol, key)
    tempfile = "".join(tempfile)
    file[cursorrow] = tempfile
def action_move_r():
    global righty
    if righty:
        righty = False
        return True
def action_move_l():
    global lefty
    if lefty:
        lefty = False
        return True
def cursor():
    global testgrid
    global grid
    global cursorcol
    global cursorrow
    if action_move_l() and cursorcol > 0:
        cursorcol -= 1
    if action_move_r() and cursorcol < len(file[cursorrow]):
        cursorcol += 1
    
    # TODO:
    # Left/right should eventually use the length of file[cursorrow].
    # Up/down will modify cursorrow and need to handle different row lengths.
def check_item_on_left():
    global delete_key_pressed, cursorcol, file
    if delete_key_pressed:
        # TODO: Backspace must operate on file[cursorrow],
        # not on the entire document.
        line = list(file[cursorrow])
        if cursorcol > 0:
            line.pop(cursorcol - 1)
            screen.clear()
            file[cursorrow] = "".join(line)
            cursorcol -= 1
    delete_key_pressed = False
def loop(screen):
    try:
        global testgrid
        fileio.readfile()
        while True:
            stdin(screen)
            cursor()
            check_item_on_left()
            # TODO: This flattening step defeats the row system.
            # Eventually rendering should work directly with file[row].
            testgrid = [char for item in file for char in item]
            logging.info("about to write")
            fileio.writefile()
            logging.info("write function returned value")
            screen.refresh()
            # TODO: Rendering will eventually need to draw each row
            # at its corresponding screen row.
            screen.clear()
            for row, text in enumerate(file):
                screen.addstr(row, 0, text)
            screen.move(cursorrow, cursorcol)
            screen.refresh()
    except KeyboardInterrupt:
        logging.critical("keyboard interrupt\n")
        screen.addstr(0, 0, "quitting..")
        fileio.writefile()
        screen.addstr(0, 1, "done! exiting shortly")
        logging.info("program exited safely\n")
def testfunc():
    print("test passed")
