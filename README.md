# FileFind
> Finds hidden files via magic bytes

This script was conceived during a CTF, where the solution is found by "unzipping" a given PNG file. The ZIP data was hidden in the IEND header, but this tool would have detected the ZIP and it's containing PNG file!

---

## Usage:
>You can test the tool on the provided example jpg file `latte_art.jpg`

Generic usage is simply passing a file using -f:
```
./filefind.py -f <path to file>
```

You can exclude false negatives by using the `-x` flag:
```
./filefind.py -f <path to file> -x JPEG,ZIP
```
The above command will ignore any magic matching JPEG and ZIP.

## Modifying
If there are any magic bytes missing that you want to add manually, edit `magicdata.py` by:
- Adding an entry to the magic_table. Add the first byte of the magic as the key, and the variable name of the list that will contain the new MagicByte.
- (Maybe) Creating a new list that holds the MagicByte. The naming convention is "magic_0xNN", where "NN" is the hex of the first byte.
- Creating a new MagicByte in it's appropriate list. A generic MagicByte requires just the bytes-object representing the magic bytes, then the name of the file type (this can really be anything you want).

> Check the existing data for help/examples.

## Future Additions:
- Planning on adding more intelligent scans; Checking for generic metadata, and determining the validity of the magic bytes through metadata.
