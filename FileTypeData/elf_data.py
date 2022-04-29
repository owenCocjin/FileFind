## Author: Owen Cocjin
## Refs:
##  - https://linux-audit.com/elf-binaries-on-linux-understanding-and-analysis/#version
##  - https://en.wikipedia.org/wiki/Executable_and_Linkable_Format
from FileTypeData.parsing import returnSeek
from FileTypeData.genericdataparse import parseBytes,gap

def elfParse(target):
	start=target.tell()

	data=parseBytes(target,[
		gap(4),
		("class",1,lambda i:"x86" if i==1 else "x86_64"),
		("endianness",1,lambda i:"little" if i==1 else "big"),
		("version",1),
		("target_os",1,lambda i:os_table[i])
	])

	returnSeek(start,target)

	return str(data)

os_table={
	0x00:"System V",
	0x01:"HP-UX",
	0x02:"NetBSD",
	0x03:"Linux",
	0x04:"GNU Hurd",
	0x06:"Solaris",
	0x07:"AIX (Monterey)",
	0x08:"IRIX",
	0x09:"FreeBSD",
	0x0a:"Tru64",
	0x0b:"Novell Modesto",
	0x0c:"OpenBSD",
	0x0d:"OpenVMS",
	0x0e:"NonStop Kernel",
	0x0f:"AROS",
	0x10:"FenixOS",
	0x11:"Nuix CloudABI",
	0x12:"Stratus Technologies OpenVOS"
}
