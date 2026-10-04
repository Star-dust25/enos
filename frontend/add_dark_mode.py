import os
import re

# Directorio de los componentes de svelte
src_dir = 'src'

# Diccionario de reemplazos (clase original -> clase original + variante oscura)
replacements = {
    r'\bbg-white\b': 'bg-white dark:bg-slate-800',
    r'\btext-slate-900\b': 'text-slate-900 dark:text-slate-100',
    r'\btext-slate-800\b': 'text-slate-800 dark:text-slate-200',
    r'\btext-slate-700\b': 'text-slate-700 dark:text-slate-300',
    r'\btext-slate-600\b': 'text-slate-600 dark:text-slate-400',
    r'\btext-slate-500\b': 'text-slate-500 dark:text-slate-400',
    r'\bborder-slate-200\b': 'border-slate-200 dark:border-slate-700/60',
    r'\bborder-slate-100\b': 'border-slate-100 dark:border-slate-800/60',
    r'\bbg-slate-50\b': 'bg-slate-50 dark:bg-slate-800/50',
    r'\bbg-slate-100\b': 'bg-slate-100 dark:bg-slate-800',
    r'\bhover:bg-slate-50\b': 'hover:bg-slate-50 dark:hover:bg-slate-700/50',
    r'\bhover:bg-slate-100\b': 'hover:bg-slate-100 dark:hover:bg-slate-700',
    r'\bfrom-amber-50/80\b': 'from-amber-50/80 dark:from-amber-900/20',
    r'\bto-white\b': 'to-white dark:to-slate-800',
    r'\bborder-amber-200/60\b': 'border-amber-200/60 dark:border-amber-700/30',
    r'\bfrom-red-50/80\b': 'from-red-50/80 dark:from-red-900/20',
    r'\bborder-red-200/60\b': 'border-red-200/60 dark:border-red-700/30',
    r'\bfrom-emerald-50/80\b': 'from-emerald-50/80 dark:from-emerald-900/20',
    r'\bborder-emerald-200/60\b': 'border-emerald-200/60 dark:border-emerald-700/30',
    r'\btext-amber-700\b': 'text-amber-700 dark:text-amber-400',
    r'\btext-red-700\b': 'text-red-700 dark:text-red-400',
    r'\btext-emerald-700\b': 'text-emerald-700 dark:text-emerald-400',
    r'\bbg-red-50\b': 'bg-red-50 dark:bg-red-900/20',
    r'\btext-red-600\b': 'text-red-600 dark:text-red-400',
    r'\bborder-red-100\b': 'border-red-100 dark:border-red-800/50',
    r'\bbg-amber-50\b': 'bg-amber-50 dark:bg-amber-900/20',
    r'\btext-amber-600\b': 'text-amber-600 dark:text-amber-400',
    r'\bborder-amber-100\b': 'border-amber-100 dark:border-amber-800/50',
}

def process_file(filepath):
    if '+layout.svelte' in filepath:
        return
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Prevenir duplicar si se ejecuta varias veces
    for orig, rep in replacements.items():
        if rep in content:
            continue
        content = re.sub(orig, rep, content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

for root, _, files in os.walk(src_dir):
    for file in files:
        if file.endswith('.svelte'):
            process_file(os.path.join(root, file))
print("Reemplazo completado.")
