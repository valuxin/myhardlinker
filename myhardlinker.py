# myhardlinker v0.1
# by valuxin
# 2021
import os
import io
import sys
import shutil
import hashlib
try:
    import pandas as pd
    from tqdm import tqdm
except ImportError:
    print('\nInstalling dependencies...')
    import pip
    pip.main(['install', 'pandas tqdm'])
    import pandas as pd
    from tqdm import tqdm

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if os.path.exists(sys.argv[1]):
            path=sys.argv[1]
        else:
            print('\nProvided path does not exist!\n')
            exit()
    else:
        print('\nPlease, give me the path to work on :)\nUsage example: myhardlinker.py C:\\test\n')
        exit()

def getmd5hash(file2hash):
    md5_object = hashlib.md5()
    block_size = 128 * md5_object.block_size
    a_file = open(file2hash, 'rb')
    chunk = a_file.read(block_size)
    while chunk:
        md5_object.update(chunk)
        chunk = a_file.read(block_size)

    return md5_object.hexdigest()

def linkfile(src,dst):
    try:
        os.remove(dst)
    except Exception as e:
        e=e
    try:
        os.link(src,dst)
    except Exception as e:
        if not os.path.exists(dst):
            shutil.copyfile(src,dst)

# Indexing files recuresively on path specified
c=0
print('\nIndexing files recuresively on path specified...')
pbar = tqdm(unit=' files')
flist="path;size\n"
for root, directories, files in os.walk(path, topdown=False):
    for name in files:
        full_name=os.path.join(root, name)
        flist+=full_name+";"+str(os.path.getsize(full_name))+"\n"
        pbar.update(1)
        c+=1        
pbar.close()
print('Total '+str(c)+' files found! Processing the data...')
# Create Dataframe from indexing result
fdf=pd.read_csv(io.StringIO(flist), sep=';')
# Free memory from useless data
del flist
# Remove files from DataFrame with unique file size
fdf = fdf.groupby('size').filter(lambda x: len(x) > 1)
fc=len(fdf.index)
print('\n'+str(fc)+' files might be linked based on file size. Calculating MD5 hash...')
# Calculate md5 hash for remaining files
pbar = tqdm(total=fc,unit=' hashes')
fdf['hash'] = [(getmd5hash(x), pbar.update(1)) for x in fdf['path']]
pbar.close()
# Remove files from DataFrame with unique hash
fdf = fdf.groupby('hash').filter(lambda x: len(x) > 1)
# Create DataFrame with source files for linking
fdf_s=fdf.drop_duplicates(subset=['hash'])
# Remove source files from target DataFrame
fdf=fdf[~fdf.index.isin(fdf_s.index.tolist())]
fc=len(fdf.index)
print('\n'+str(fc)+' files will be hardlinked to '+str(len(fdf_s.index))+' unique files. '+str(round(fdf['size'].sum()/1048576,2))+'Mb could be freed :)')
# Set hash as index in source DataFrame
fdf_s.set_index('hash',inplace=True)
# Adding source file paths to target DataFrame for linking
fdf['source']=[fdf_s.at[x,'path'] for x in fdf['hash']]
fdf=fdf[['path','source']].reset_index(drop=True)
# Free memory from useless data
del fdf_s
# Link target files with source
print('\nLinking files...')
pbar = tqdm(total=fc,unit=' files')
[(linkfile(y,x), pbar.update(1)) for x, y in zip(fdf['path'], fdf['source'])]
pbar.close()
print('\nDone! Have a nice day :)\n')
