import lualex
import luaparse
import luainterp
import sys


if __name__ == '__main__':
    l = luainterp.LuaInterpreter([])

    while True:
        try:
            line = input("[LUA] ")
        except EOFError:
            raise SystemExit
        if not line:
            continue
        line += "\n"
        prog = luaparse.parse(line)
        if not prog:
            continue
        l.add_statements(prog)
        l.run()