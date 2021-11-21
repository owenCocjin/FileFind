# ProgMenu

> A lil library to help with cmd line flags and stuff (stuff being verbose printing)

***

## Installation

- Clone or download into a folder
- Move progMenu.py into the working directory of a project

OR

- Copy Python/progmenu.py to your Python path (probably /usr/lib/pythonX.X ; Check your path with `python -c "import sys; print(sys.path)"`)

<br/>

## Usage

### Testing

Run this code as a script to test if it's working:

```
from progmenu import MENU
print(MENU)
#Prints all the passed flags, assigned, and args in that order
```

- A *flag* is: `-f or --flag`
- An *assigned* is a flag with an associated arg: `-s 12` or `--seed=12`
- An *arg* is pretty much anything else: `$ cmd -s <arg> <lonelyArg>`
- <u>**NOTE:**</u> Multiple flags passed via one tick will be treated as 2 separate flags, with the last flag getting any assigns (ex. `-fh 'Hello'` is the same as `-f -h 'Hello'`)

<br/>

### Main Usage
> This is a super basic example! Checkout the Examples in the Python directory for more options

In the main file:
```
from progmenu import MENU
from menuentries import *
PARSER=MENU.parse(True)  #True means run the functions instead of just returning True/None if the entry was called.
print(f"PARSER: {PARSER}")  #Just so you can see what PARSER is. It's a dictionary of the entry names and what they returned (if called in the cmd line).
```

In another file containing the entries (in this case named `menuentries.py`):
```
from progmenu import MenuEntry
def aFunc():
	print("This is an entry function!")
	return True

#This doesn't/shouldn't be saved to a variable as this may cause collisions. When an Entry class is created it adds itself to a class-wide list!
EntryFlag("entryName", ['f', "flag"], aFunc)  #help(MenuEntry) for more details)
```

Now when you run the main file without using `f` or `flag` as a flag, nothing will happen. But if you do, it prints "This is an entry function!"

>Note: You can just add entries in the main file if you want, but PARSER must be created after the declarations. The best way to do this is to structure the script as such:
```
from progmenu import MENU
def main():
	'''Add main code here'''
	print(MENU)

EntryFlag("xmpl", ['x'], lambda:True)

if __name__=="__main__":
	'''Only called when the script itself is run.
	Won't run if imported'''
	PARSER=MENU.parse(True)
	main()
```
> This ensures that everything required is loaded first.

---

### Strict Parsing
> Strict parsing brings up warning when certain conditions aren't met

When calling `MENU.parse()`, you can pass a boolean to the keyword 'strict'. By default this is False. When True, the parse will display warnings and quit the program when any of these conditions are met:
- An invalid flag is passed
- An argument is passed to a flag
- A flag was called but it requires an argument
- An entry is marked strict, but wasn't called

To use strict parsing, simply pass the keyword argument `strict=True` to parse:
```
PARSER=MENU.parse(True, strict=True)
```

To mark an entry as strict, either pass True as a final argument, or pass True to `strict` as a keyword:
```
EntryFlag("flg", ['f'], fFunc, True)
#OR
EntryFlag("strct", ['s'], sFunc, strict=True)
```

### Recursed Entries
> Recursed allows an entry to use return values of other entries as it's own arguments

Sometimes it's handy and cleaner to use return values of other flags as an argument in an entry. For this, you need to use 'recurse'. When making an entry, pass a list of entry names to the keyword `recurse`. When the recursed flag is called it will be passed arguments from other flags in the same order as the recurse list!

Create a recursed entry liek this:
```
def flagFunc(a):
	'''Returns "Yes" if the "argie" flag was called'''
	if a:
		return "Yes"
	else:
		return "No"

EntryFlag("flagname", ['f', "flag"], flagFunc, recurse=["argie"]])
EntryFlag("argie", ['a', "argie"], lambda: True)
```

Now if "argie" is called (by using the flag "-a" or "--argie") "flagname" will return "Yes".

**Notes:**
- If "argie" isn't called, by default it will return None, which is boolean False!
- When using recurse with EntryArg or EntryKeyArg, make sure the recurse args are defined first, in the order defined by the `recurse` keyword. (See Examples/menuentries for more details.)

### Verbose Printing

To use verbose printing, simply print like normal, but use the function "vprint" instead of "print" (And make sure the verbose flag was set).
To use verbose printing in other files, you MUST make sure you import vprint in each file (you don't need to set verbosity anywhere other than main), otherwise Python will complain that vprint wasn't defined.

> Currently, there is an issue where in order to politely use verbose and menu entries, you must setup verbose __BEFORE__ parsing strictly! Without strict parsing, verbose works as expected.

### Default Substituting
> Normally if a flag isn't called, it's value in PARSER is None. This can be changed.

By using the keyword `default` in the Entry declaration, we can change the default value of "None":

```
from progmenu import MENU, EntryArg
PARSER=MENU.parse(True)

EntryArg("default", ['d'], lambda a:a, default="Nothing")
```
Now if the -d flag isn't called, `PARSER["default"]="Nothing"`. If it is called, it will be whatever arg is passed to it.

---

## Advanced Examples:

#### Using main:
- In main file (main.py):
```
from progmenu import MENU
vprint=MENU.verboseSetup(['v' "verbose"]) #menu.findFlag() returns True if any passed flags were found, meaning you can hardcode verbosity with: menu.verboseSetup(True)
print("This is without verbose!")
vprint("This is WITH verbose!")
```
- Now run the file with `-v` or `--verbose`:
```
$ python ./main.py
This is without verbose!
$python ./main.py -v
This is without verbose!
This is WITH verbose!
```

#### Using external files:
> TLDR; You only need to import verbosity in the files where you're calling it literally

- In main file (main.py):
```
import verboseTest
verboseTest.testFunc()
```
- In another file (verboseTest.py):
```
from progmenu import MENU  #MENU is required to catch flags
vprint=MENU.verboseSetup(['v', "verbose"])  #menu.findFlag() returns True if any passed flags were found, meaning you can hardcode verbosity with: menu.verboseSetup(True)
def testFunc():
	'''Prints normally and with verbose'''
	print("This is a normal print from testFunc!")
	vprint("This is verbose print from testFunc!")
```
- Now when the main file is run without '-v', only the normal print will work. When it's run with '-v', both print statements will print:
```
$ python main.py
This is a normal print from testFunc!
$ python main.py -v
This is a normal print from testFunc!
This is verbose print from testFunc!
```

#### Ignoring Functions:
> Most times it is easier to simply use lambda instead of making an entire function

```
EntryFlag("flag", ['f'], lambda:True)
EntryArg("arg", ['a'], lambda a:a)
EntryKeyArg("key", ['k'], lambda k="Blank":k)
```

---

## Bugs:

#### Recursed
- <b>`[bug:0.0]`</b>: ~~Recursed entries call sub-recurses. This means any print statements in the sub-recurse <b>will</b> be printed. Be cautious when using recurse on any entry that prints anything.~~
- <b>`[bug:0.1]`</b>: ~~Recursed entries <b>should</b> only allow a max recursion depth of 2, but due to how sub-recurses are processed, the depth may be extended based on the order the recurses are called. This honestly isn't that much of an issue as it benefits the user (adds potential to evade Recurse error), but is essentially unpredictable/unreliable to implement. Because of this unpredictability, any recursed function that goes beyond a depth of 2 can run sub-recurses an unpredictable number of times.~~
- <b>`[bug:0.2]`</b>: ~~Luckily, these recursed bugs don't seem to affect looped recurses and will appropriately raise an error.~~
- <b>`[bug:0.3]`</b>: If multiple entries use the same recurse, that recurse will run multiple times (similar to `[bug:0.0]`).
- <b>`[bug:0.4]`</b>: ~~Recurse doesn't work with EntryKeyArg.~~
