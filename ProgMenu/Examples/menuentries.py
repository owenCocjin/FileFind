##
## Author:	Owen Cocjin
## Version:	1.4.4
## Date:	2021.06.19
## Description:	Example menuentries file
## Notes:
##    - Added recurse examples
## Updates:
##    - Allows recurse to work on EntryKeyArgs
##    - Fixed syntax to recursed EntryArg
from progmenu import EntryFlag, EntryArg, EntryKeyArg
#Menu Entry functions
def noargFunc():
	'''Takes no arguments'''
	print("NOARG: This takes no args!")
	return True

def argFunc(x):
	'''Normally you use this mode to get an arg from the user.
	This is ignored if no arg passed'''
	print(f"ARG: You gave me: {x}!")
	return x

def kwargFunc(r, x='Bad'):
	'''Like mode 1, but has a value if no arg given.
	If not called, uses default value (passed in EntryKeyArg)!'''
	print(f"KWARG: What I have is: {x}! Recurse has: {r}")
	return x

def strictFunc():
	'''This flag MUST be called if PARSER is strict'''
	print("STRICT: You have to call me!")
	return True

def strictArgFunc(x):
	'''This takes an arg and is strict'''
	print(f"STRICTARG: You've given me {x}!")
	return x

def recurseFunc(x, y):
	'''This reads arguments from other flags!'''
	print(f"RECURSE: Arg is '{x}' and noarg is '{y}'!")
	return x, y

def argcurseFunc(rec, arg):
	'''This takes an arg AND recurse.
The recurse vars are called first, then the arg var.'''
	print(f"ARGCURSE: The recurse is '{rec}' and your arg is '{arg}'")
	return arg

#Menu Entries
EntryArg("argcurse", ['z', "argcurse"], argcurseFunc, recurse=["recurse"])
EntryFlag("noarg", ['n', "noarg"], noargFunc, default='Nothing')
EntryArg("arg", ['a', "arg"], argFunc)
EntryKeyArg("kwarg", ['k', "kwarg"], kwargFunc, default="default", recurse=["recurse"])
EntryFlag("strictflag", ['s', "strict"], strictFunc, strict=True)
EntryArg("strictarg", ['r', "sarg", "strictarg"], strictArgFunc, strict=False)
EntryFlag("recurse", ['c', "recurse"], recurseFunc, recurse=["arg", "noarg"])
#Uncomment these to test invalid recurses
#EntryFlag("nested", ['d'], lambda _:True, recurse=["looped"])
#EntryFlag("looped", ['l'], lambda _:True, recurse=["toodeep"])
#EntryFlag("toodeep", ['t'], lambda _:True, recurse=["nested"])
