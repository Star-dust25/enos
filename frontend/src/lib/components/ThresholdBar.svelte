<script lang="ts">
  let {
    valor,
    minVal,
    maxVal,
    umbral,
    titulo,
    valorTexto,
    estadoActivo,
    estadoTexto,
    umbralTexto,
    fechaTexto,
    state = "normal",
    theme = "blue",
  } = $props<{
    valor: number;
    minVal: number;
    maxVal: number;
    umbral: number;
    titulo: string;
    valorTexto: string;
    estadoActivo: boolean;
    estadoTexto: string;
    umbralTexto: string;
    fechaTexto: string;
    state?: "normal" | "alerta";
    theme?: "red" | "green";
  }>();

  // Clamp value for visual representation
  let v_clamp = $derived(Math.max(minVal, Math.min(maxVal, valor)));
  let percentage = $derived(((v_clamp - minVal) / (maxVal - minVal)) * 100);
  let umbralPercentage = $derived(
    ((umbral - minVal) / (maxVal - minVal)) * 100,
  );

  let fueraPorArriba = $derived(valor > maxVal);
  let fueraPorAbajo = $derived(valor < minVal);
  let fueraDeRango = $derived(fueraPorArriba || fueraPorAbajo);

  let colorFill = $derived(
    theme === "red"
      ? "bg-red-500"
      : "bg-emerald-500"
  );
  
  let colorText = $derived(
    theme === "red"
      ? "text-red-500"
      : "text-emerald-500"
  );

  let activeBadge = $derived(
    estadoActivo
      ? theme === "red"
        ? "bg-red-50 text-red-600 dark:bg-red-500/10 dark:text-red-400"
        : "bg-emerald-50 text-emerald-600 dark:bg-emerald-500/10 dark:text-emerald-400"
      : "bg-slate-50 dark:bg-white/5 text-slate-500 dark:text-slate-400"
  );
</script>

<style>
  @keyframes wave {
    0% { transform: translateX(0); }
    100% { transform: translateX(-50%); }
  }
  .animate-wave-slow {
    animation: wave 6s linear infinite;
  }
  .animate-wave-fast {
    animation: wave 3s linear infinite;
  }
</style>

<div class="flex flex-col flex-1 w-full bg-white dark:bg-[#1C1C1E] p-6 sm:p-8 rounded-3xl shadow-sm border border-slate-200/60 dark:border-white/5 h-full relative overflow-hidden group">
  
  <!-- Subtle animated ambient glow behind the card -->
  <div class="absolute -top-10 -right-10 w-48 h-48 rounded-full blur-3xl opacity-0 transition-opacity duration-1000 group-hover:opacity-20 pointer-events-none {colorFill}"></div>

  <div class="flex justify-between items-center mb-6">
     <h3 class="text-sm font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-widest">{titulo}</h3>
     <span class="px-3 py-1 rounded-full text-[10px] font-bold tracking-wider uppercase {activeBadge}">
        {estadoTexto}
     </span>
  </div>

  <div class="flex flex-col sm:flex-row items-center gap-8 mt-2 flex-1">
    
    <!-- Typography Left -->
    <div class="flex-1 flex flex-col justify-center gap-1 min-w-0 w-full">
      <div class="text-6xl sm:text-7xl font-semibold tracking-tighter {colorText} drop-shadow-sm truncate">
        {valorTexto}
      </div>
      
      <div class="flex flex-col gap-2 mt-4 border-t border-slate-100 dark:border-white/5 pt-4">
        <div class="flex justify-between items-center">
           <span class="text-[12px] text-slate-500 dark:text-slate-400 font-medium uppercase">Criterio</span>
           <span class="text-[13px] font-semibold text-slate-900 dark:text-white text-right max-w-[60%] leading-tight">{umbralTexto}</span>
        </div>
        <div class="flex justify-between items-center">
           <span class="text-[12px] text-slate-500 dark:text-slate-400 font-medium uppercase">Medición</span>
           <span class="text-[13px] font-semibold text-slate-900 dark:text-white">{fechaTexto}</span>
        </div>
      </div>
    </div>

    <!-- Organic Fluid Sphere Right -->
    <div class="relative w-36 h-36 sm:w-40 sm:h-40 rounded-full border-[8px] border-[#F5F5F7] dark:border-[#2C2C2E] shadow-[inset_0_4px_12px_rgba(0,0,0,0.15)] overflow-hidden shrink-0 group-hover:scale-105 transition-transform duration-700 ease-out bg-white dark:bg-[#151515]">
       
       <!-- Umbral Line (Fixed) -->
       <div class="absolute w-full h-[2px] bg-slate-800/20 dark:bg-white/40 z-20 transition-all shadow-sm" style="bottom: {umbralPercentage}%;">
          <div class="absolute right-2 -top-4 text-[9px] font-extrabold text-slate-800 dark:text-white drop-shadow-md">UMBRAL</div>
       </div>

       <!-- The Fluid Container (Rises with percentage) -->
       <div class="absolute bottom-0 w-full transition-all duration-1500 ease-out z-10 flex flex-col items-center justify-start" style="height: {percentage}%;">
          
          <!-- Wave 1 (Back, lighter, offset) -->
          <div class="absolute top-[-14px] left-0 w-[200%] h-[15px] animate-wave-slow {theme === 'red' ? 'text-red-300 dark:text-red-700' : 'text-emerald-300 dark:text-emerald-700'} opacity-70">
            <svg viewBox="0 0 1200 120" preserveAspectRatio="none" class="w-full h-full fill-current">
              <!-- Symmetrical wave path -->
              <path d="M0,50 C150,100 450,0 600,50 C750,100 1050,0 1200,50 L1200,120 L0,120 Z"></path>
            </svg>
          </div>

          <!-- Wave 2 (Front, dynamic) -->
          <div class="absolute top-[-14px] left-0 w-[200%] h-[15px] animate-wave-fast {colorText}">
            <svg viewBox="0 0 1200 120" preserveAspectRatio="none" class="w-full h-full fill-current">
              <!-- Inverse symmetrical wave path for chaotic water feel -->
              <path d="M0,50 C200,0 400,100 600,50 C800,0 1000,100 1200,50 L1200,120 L0,120 Z"></path>
            </svg>
          </div>
          
          <!-- Solid Liquid Base -->
          <div class="flex-1 w-full {colorFill}"></div>
       </div>
    </div>
  </div>

  {#if fueraDeRango}
    <div class="mt-6 h-px w-full bg-slate-200/60 dark:bg-white/5"></div>
    <p class="text-[11px] text-slate-500 dark:text-slate-400 mt-4 leading-relaxed">
      El valor queda fuera del rango representable en la esfera ({minVal} a {maxVal}).
    </p>
  {/if}
</div>
