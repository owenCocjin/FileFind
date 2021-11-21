#!/usr/bin/python3
## Author:	Owen Cocjin
## Version:	4.3.1
## Date:	2021.04.11
## Description:	Holds MenuEntry and subclasses
## Notes:
##    - Requires verbose to be setup BEFORE parsing.
## Updates:
##    - Added "default" arg to MenuEntryExecute.
##    - When default is passed, this value will be used when a flag if a flag isn't called
##    - Added "defaults" to EntryFlag
class MenuEntry():
	'''Menu entry class.
name: Entry's name. This is how it will be referenced through the PARSER dictionary.
labels: The flags that will trigger this entry.
	- NOTE: If multiple entries have the same flags, all will trigger!
function: The function that will run when this entry is triggered. If you just want to determine if the flag is caught, use: 'lambda: True' (without quotes).
mode: The mode the entry should be in (see below).
	Mode status:
		- 0=flags (No arguments will be accepted. Must return True)
		- 1=assigned (Exactly 1 positional argument is expected)
		- 2=flags&assigned (Exactly 1 keyword argument is expected)
strict: If True, the strict entry's flag MUST be called when parsed strictly.
recurse: A list of entry names who's outputs are used as arguments to the Entry.
	- NOTE: The recurse outputs are passed last, and are passed in the same order as the list is in.
	'''
	all_entries=[]  #Class-wide list of all menu entries

	def __init__(self, name, labels, function, mode=0, strict=False, recurse=None, default=None):
		'''name=Entry name
		labels=Flags used to address entry
		function=Function called by entry
		mode=Mode of entry (see above)
		strict=Mandatory flag if MENU.parser has strict set to True
		recurse=A list of other flag names who's output will be used in this entry
		'''
		self.name=name
		self.labels=labels  #Labels being a list of the flags/args
		self.function=function
		self.mode=mode
		self.strict=strict
		self.recurse=recurse
		self.vrecurse=None  #Values of recurse
		self.default=default
		self.beenrun=False  #Tells parser if already been executed
		MenuEntry.all_entries.append(self)

	def __str__(self):
		return f"{self.name}"

	def __call__(self, *args, **kwargs):
		return self.function(*args, **kwargs)

	@classmethod
	def help(cls):
		'''Returns a list of entry names and their labels.'''
		toRet={}
		for e in cls.all_entries:
			toRet[e.getName()]=e.getLabels()
		return toRet
	@classmethod
	def addEntry(cls, new):
		'''Add an entry to the class-wide list'''
		MenuEntry.all_entries.append(new)
	@classmethod
	def removeEntry(cls, e):
		'''Removes an entry by name.
		Returns True if entry was found/deleted, False otherwise.'''
		for i in range(len(MenuEntry.all_entries)):
			if MenuEntry.all_entries[i].getName()==e:
				del MenuEntry.all_entries[i]
				return True
		return False
	@classmethod
	def listNames(cls):
		'''Returns a list of names of entries in order of creation.'''
		return [i.getName() for i in MenuEntry.all_entries]
	@classmethod
	def printEntries(cls):
		'''Prints entries'''
		[print(i) for i in MenuEntry.all_entries]
	@classmethod
	def getMenuEntries(cls):
		return cls.all_entries
	@classmethod
	def sgetMenuEntry(cls, e):
		'''Return specific menu entry by name or entries labels.'''
		for i in cls.all_entries:
			if i.getName()==e or (e in i.getLabels()):
				return i
		return False
	@classmethod
	def getEntryNames(cls):
		return [i.getName() for i in MenuEntry.all_entries]

	def run(self, *args, **kwargs):
		return self.function(*args, **kwargs)

	def getName(self):
		return self.name
	def setName(self, new):
		self.name=new
	def getLabels(self):
		return self.labels
	def addLabel(self, new):
		self.labels.append(new)
	def removeLabel(self, old):
		self.labels.remove(old)
	def getWorkingLabel(self, menu):
		'''Returns the first found working label, None if none found'''
		for l in self.labels:
			if l in menu:
				return l
		return None
	def setFunction(self, new):
		self.function=new
	def getMode(self):
		return self.mode
	def setMode(self, new):
		self.mode=new
	def getStrict(self):
		return self.strict
	def setStrict(self, new):
		self.strict=new
	def getRecurse(self):
		return self.recurse
	def setRecurse(self, new):
		self.recurse=new
	def getVRecurse(self):
		return self.vrecurse
	def setVRecurse(self, new):
		self.vrecurse=new
	def getDefault(self):
		return self.default
	def setDefault(self, new):
		self.default=new
	def getBeenRun(self):
		return self.beenrun
	def setBeenRun(self, new):
		self.beenrun=new

class MenuEntryExecute(MenuEntry):
	'''Menu Entry with executable qualities'''
	def __init__(self, name, labels, function, mode=0, *, strict=False, recurse=None, default=None):
		MenuEntry.__init__(self, name, labels, function, mode, strict=strict, recurse=recurse, default=default)
		self.value=None

	def getValue(self):
		return self.value
	def setValue(self, new):
		self.value=new

	def execute(self):
		'''Runs self.function with self.value only'''
		return self.function(self.value)

class EntryFlag(MenuEntry):
	'''MenuEntry with default mode 0'''
	def __init__(self, name, labels, function, *, strict=False, recurse=None, default=None):
		MenuEntry.__init__(self, name, labels, function, strict=strict, recurse=recurse, default=default)
		self.mode=0

	def execute(self):
		if self.recurse!=None:
			return self.function(*self.vrecurse)
		else:
			return self.function()

class EntryArg(MenuEntryExecute):
	'''MenuEntryExecute with default mode 1'''
	def __init__(self, name, labels, function, *, strict=False, recurse=None, default=None):
		MenuEntryExecute.__init__(self, name, labels, function, 1, strict=strict, recurse=recurse, default=default)
		self.value=None

	def execute(self):
		'''Return None if self.value is None'''
		if self.value==None:
			return None
		if self.recurse!=None:
			return self.function(*self.vrecurse, self.value)
		else:
			return self.function(self.value)

class EntryKeyArg(MenuEntryExecute):
	'''MenuEntryExecute with default mode 2'''
	def __init__(self, name, labels, function, *, strict=False, recurse=None, default=None):
		MenuEntryExecute.__init__(self, name, labels, function, 2, strict=strict, recurse=recurse, default=default)
		self.value=[]  #Uses a list because otherwise None would always be passed

	def setValue(self, v):
		'''Sets value'''
		self.value.append(v)

	def execute(self):
		'''Runs self.function'''
		if self.recurse!=None:
			return self.function(*self.vrecurse, *self.value)
		else:
			return self.function(*self.value)
