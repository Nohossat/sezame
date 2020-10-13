import os
from os import listdir
import re

main_dir = os.path.dirname(os.getcwd())
print(main_dir)
path = os.path.join(main_dir, "data/songs/")

files = listdir(path)

count = 0

for file in files:
    pattern = re.compile(r"\d{1,2}\s*(.+)")
    result = pattern.search(file)

    if result:
        count += 1
        print(result.group(1))
        os.rename(os.path.join(path, file), os.path.join(path,result.group(1)))

print(count)
