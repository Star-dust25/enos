import os
import re

src_dir = 'src'

replacements = {
    # Layout y fondos principales
    r'dark:bg-slate-900(?!/)\b': 'dark:bg-[#0a0a0a]',
    r'dark:bg-slate-900/80': 'dark:bg-[#0a0a0a]/95',
    r'dark:bg-slate-900/50': 'dark:bg-[#0a0a0a]',
    r'dark:bg-slate-900/95': 'dark:bg-[#0a0a0a]',
    
    # Contenedores y tarjetas (minimalistas, flat)
    r'dark:bg-slate-800(?!/)\b': 'dark:bg-[#111111]',
    r'dark:bg-slate-800/70': 'dark:bg-[#111111]',
    r'dark:bg-slate-800/50': 'dark:bg-[#111111]',
    
    # Bordes sutiles
    r'dark:border-slate-800/60': 'dark:border-white/10',
    r'dark:border-slate-700/60': 'dark:border-white/10',
    r'dark:border-slate-800': 'dark:border-white/10',
    
    # Eliminar blurs en modo oscuro (o hacerlos solidos)
    r'backdrop-blur-lg': 'backdrop-blur-lg dark:backdrop-blur-none',
    r'backdrop-blur-xl': 'backdrop-blur-xl dark:backdrop-blur-none',
    r'backdrop-blur\b(?!-)': 'backdrop-blur dark:backdrop-blur-none',
    
    # Eliminar sombras en modo oscuro para un look flat
    r'shadow-sm': 'shadow-sm dark:shadow-none',
    r'shadow-md': 'shadow-md dark:shadow-none',
    r'shadow-\[.*?\]': r'\g<0> dark:shadow-none',
    
    # Alertas de +page.svelte (quitar gradientes en oscuro)
    r'dark:from-amber-900/20 dark:to-slate-800': 'dark:from-[#111111] dark:to-[#111111] dark:bg-[#111111]',
    r'dark:from-red-900/20 dark:to-slate-800': 'dark:from-[#111111] dark:to-[#111111] dark:bg-[#111111]',
    r'dark:from-emerald-900/20 dark:to-slate-800': 'dark:from-[#111111] dark:to-[#111111] dark:bg-[#111111]',
    
    r'dark:border-amber-700/30': 'dark:border-amber-500/20',
    r'dark:border-red-700/30': 'dark:border-red-500/20',
    r'dark:border-emerald-700/30': 'dark:border-emerald-500/20',
    
    # Header de DashboardContainer
    r'dark:to-slate-800/50': 'dark:to-[#111111] dark:from-[#111111]',
}

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Apply replacements
    for orig, rep in replacements.items():
        # Avoid double replacing dark:shadow-none if run multiple times
        if "dark:shadow-none" in rep and "dark:shadow-none" in content:
            # We still want to replace the shadow-[...] if it doesn't have dark:shadow-none right after
            # Simple approach: just clean up double dark:shadow-none later
            content = re.sub(orig, rep, content)
        elif "dark:backdrop-blur-none" in rep and "dark:backdrop-blur-none" in content:
            content = re.sub(orig, rep, content)
        else:
            content = re.sub(orig, rep, content)
            
    # Cleanup possible duplications
    content = content.replace("dark:shadow-none dark:shadow-none", "dark:shadow-none")
    content = content.replace("dark:backdrop-blur-none dark:backdrop-blur-none", "dark:backdrop-blur-none")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

for root, _, files in os.walk(src_dir):
    for file in files:
        if file.endswith('.svelte'):
            process_file(os.path.join(root, file))
print("Estilo minimalista aplicado.")
