import curses
import time

def main(stdscr):
    curses.curs_set(0)
    mensaje = "  global game jam 2025  "
    ancho = curses.COLS

    while True:
        for i in range(len(mensaje)):
            stdscr.clear()
            stdscr.addstr(0, 0, mensaje[i:] + mensaje[:i])
            stdscr.refresh()
            time.sleep(0.2)

curses.wrapper(main)
