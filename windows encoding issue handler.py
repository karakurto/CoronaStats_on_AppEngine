with open('requirements.txt', 'rb') as source_file:
    contents = source_file.read()

with open('requirements.txt', 'w+b') as dest_file:
    dest_file.write(contents.decode('utf-16').encode('utf-8'))