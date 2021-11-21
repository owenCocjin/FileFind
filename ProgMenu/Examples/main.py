#!/usr/bin/python3
## Author:	Owen Cocjin
## Version:	1.2
## Date:	2021.03.30
## Description:	Example main program
## Notes:
##    - Run this like any python program.
## Updates:
##    - Changed menuentries import to avoid function collisions
from progmenu import MENU
import menuentries
#If you use verbose printing and menu entries, make sure you initialize verbose first!
#Otherwise it will throw errors when parsing strictly!
vprint=MENU.verboseSetup(['v', "verbose"])
PARSE=MENU.parse(True, strict=True)
print(f"{MENU}\n")
print(f"PARSE: {PARSE}\n")
vprint("This is verbose printing!")
