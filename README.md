# Simple photo (and video) Sync (with a little sorting)

## General Information
This is a simple from my point of view still static PhotoSync-script with a few simple options.
The Script basically looks into up to 4 different sourcefolders and syncs the media into one destinationpath.

### Syncing Camerapaths or the Mobilecam-path
If the source is no Messengerpath the script looks up the last edit timestamp of the media file and depending on that puts it into a new [QUARTER][YEAR] folder in the destnation path. So if your syncing your Fotos of 2020 there will be four folders in the destination path with the names 
"2020-Q1"
"2020-Q2"
"2020-Q3"
"2020-Q4"
and your files will be sorted into these folders.

### Messenger syncing
If the source path is the messengerpath, the script does basically the same, but differs in not creating quarter folders but just one folder for every synced year.

## Configuration
RENAME the example.env into just .env and replace the properties accordingly to your paths.
There is one option you can choose for every path and this is wether you want to copy the files or move them.

## Supported file formats
['jpg', 'jpeg', 'mov', 'mp4', 'png']

### TODO
- more generic configfile (probably .yaml) for endless folders and options
- english language / different language files