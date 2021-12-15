# myhardlinker
Crossplatform fast and robust Python utility to free space on the data volume by hardlinking duplicate files.
# Requirments
- Python 3.x
- Modules: <code>pandas</code> <code>tqdm</code>
- Minimum 512Mb free RAM for optimal performance, 1Gb is recommended
# Usage
<code>myhardlinker.py \<path-to-the-directory\></code>

<code>myhardlinker.py C:\test</code> - this command recursevily scan and deduplicate files in C:\test

<code>myhardlinker.py .</code> - this command recursevily scan and deduplicate files in current location

![Screenshot 2021-12-15 162431](https://user-images.githubusercontent.com/16034419/146194704-f6fc1962-cdbd-4b76-805a-b8a9eac6a676.png)
# Limitations
Files systems have limitations on how many links could be made to one file. For example, NTFS allows maximum 1023 links to a single file, EXT4 - 65000 links. Currently, if the limit is exided for one unique source file the duplicate files over the limit will be left untouched.
# To Do
- Improve RAM usage efficiency
- Workaround the FS limitations by using more unique files with same hash
- Possibility to continue script work from last place after pause/stop 
