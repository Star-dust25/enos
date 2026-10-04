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
    theme?: "blue" | "green";
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
    theme === "blue"
      ? "bg-blue-500 dark:bg-blue-500"
      : "bg-emerald-500 dark:bg-emerald-500"
  );
  
  let colorText = $derived(
    theme === "blue"
      ? "text-blue-600 dark:text-blue-400"
      : "text-emerald-600 dark:text-emerald-400"
  );

  let activeBadge = $derived(
    estadoActivo
      ? theme === "blue"
        ? "bg-blue-50 dark:bg-blue-900/30 text-blue-700 dark:text-blue-400 border border-blue-200 dark:border-blue-800/50"
        : "bg-emerald-50 dark:bg-emerald-900/30 text-emerald-700 dark:text-emerald-400 border border-emerald-200 dark:border-emerald-800/50"
      : "bg-slate-50 dark:bg-[#111111] text-slate-500 dark:text-slate-400 border border-slate-200 dark:border-white/10"
  );

  let borderTheme = $derived(
    theme === "blue" ? "border-l-blue-500 dark:border-l-blue-500" : "border-l-emerald-500 dark:border-l-emerald-500"
  );
</script>

<div class="flex flex-col flex-1 w-full p-2">
  <!-- Header -->
  <div class="flex justify-between items-end mb-6">
    <div>
      <h3
        class="text-sm font-bold text-slate-500 dark:text-slate-400 uppercase tracking-[0.15em] mb-1"
      >
        {titulo}
      </h3>
      <!-- The value itself in Oswald -->
      <div
        class="text-5xl sm:text-6xl font-oswald font-bold tracking-tight {colorText}"
      >
        {valorTexto}
      </div>
    </div>
  </div>

  <!-- Threshold Bar Container -->
  <div
    class="relative w-full h-4 bg-slate-200 dark:bg-[#0a0a0a] rounded-none overflow-hidden my-3 border border-transparent dark:border-white/5"
  >
    <!-- Progress Fill -->
    <div
      class="absolute top-0 left-0 h-full rounded-none transition-all duration-1000 ease-out {colorFill}"
      style="width: {percentage}%"
    ></div>

    <!-- Threshold Marker -->
    <div
      class="absolute top-0 bottom-0 w-[2px] bg-slate-900 dark:bg-white z-10"
      style="left: {umbralPercentage}%"
    ></div>
  </div>

  <!-- Threshold Label -->
  <div
    class="relative w-full h-8 text-[11px] text-slate-500 dark:text-slate-400 font-bold tracking-widest uppercase"
  >
    <div
      class="absolute -translate-x-1/2 mt-1 flex flex-col items-center"
      style="left: {umbralPercentage}%"
    >
      <div class="w-px h-2 bg-slate-400 dark:bg-slate-500 mb-1"></div>
      Umbral ({umbral > 0 ? "+" : ""}{umbral})
    </div>
  </div>

  <!-- Subtitle / Details Card -->
  <div
    class="mt-4 flex flex-col justify-center gap-4 bg-slate-50 dark:bg-[#0a0a0a] border-y border-r border-slate-200 dark:border-white/5 border-l-[4px] {borderTheme} p-6 rounded-none flex-1"
  >
    <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
      <span class="text-sm text-slate-600 dark:text-slate-400 font-bold uppercase tracking-wider shrink-0"
        >Estado actual</span
      >
      <span
        class="px-3 py-1 rounded-none text-xs font-bold tracking-[0.2em] uppercase {activeBadge}"
      >
        {estadoTexto}
      </span>
    </div>

    <div class="h-px w-full bg-slate-200 dark:bg-white/5"></div>

    <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-2 sm:gap-5">
      <span class="text-sm text-slate-600 dark:text-slate-400 font-bold uppercase tracking-wider shrink-0"
        >Criterio</span
      >
      <span class="text-sm font-semibold text-slate-900 dark:text-slate-100 text-left sm:text-right"
        >{umbralTexto}</span
      >
    </div>

    <div class="h-px w-full bg-slate-200 dark:bg-white/5"></div>

    <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-2 sm:gap-4">
      <span class="text-sm text-slate-600 dark:text-slate-400 font-bold uppercase tracking-wider shrink-0"
        >Última medición</span
      >
      <span class="text-sm font-bold text-slate-800 dark:text-slate-200 tracking-widest"
        >{fechaTexto}</span
      >
    </div>

    {#if fueraDeRango}
      <div class="h-px w-full bg-slate-200 dark:bg-white/5"></div>
      <p class="text-[11px] text-slate-500 dark:text-slate-400 leading-relaxed">
        El valor queda fuera del rango representable en la barra ({minVal} a {maxVal});
        la barra aparece {fueraPorArriba ? "completa" : "vacía"} y no refleja la
        magnitud real.
      </p>
    {/if}
  </div>
</div>
