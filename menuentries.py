from ProgMenu.progmenu import EntryArg,EntryFlag

def excludeFunc(e):
	'''Returns a list of filetypes to ignore'''
	return e.split(',')
def helpFunc():
	print('''filefind.py [-efh]
  Find magic bytes in a file.

  -e; --exclude=<t>: Exclude filetypes.
                     Separate by comma
  -f; --file=<file>:   File to scan
  -h; --help:        Prints this page''')

EntryArg("exclude",['e','x',"exclude","ignore"],excludeFunc,default=[])
EntryArg("file",['f',"file","target"],lambda f:f,strict=True)
EntryFlag("help",['h',"help"],helpFunc)
