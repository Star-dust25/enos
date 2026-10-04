import os
import re

src_dir = 'src'

def process_file(filepath):
    if '+layout.svelte' in filepath:
        return
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace /60/80, /50/80, /60/60, etc with just the first one or a clean one
    content = re.sub(r'(dark:border-slate-\d+)/\d+/\d+', r'\1/60', content)
    content = re.sub(r'(dark:bg-slate-\d+)/\d+/\d+', r'\1/50', content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

for root, _, files in os.walk(src_dir):
    for file in files:
        if file.endswith('.svelte'):
            process_file(os.path.join(root, file))
print("Clases malformadas corregidas.")
