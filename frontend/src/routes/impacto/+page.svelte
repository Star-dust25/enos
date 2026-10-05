<script lang="ts">
  import { onMount } from "svelte";
  import DashboardContainer from "$lib/components/DashboardContainer.svelte";
  import { api } from "$lib/api";

  let loading = $state(true);

  onMount(() => {
    setTimeout(() => {
      loading = false;
    }, 400);
  });
</script>

<svelte:head>
  <title>Validación y Acoplamiento</title>
</svelte:head>

<div class="max-w-6xl mx-auto mt-4 px-4 sm:px-6 lg:px-8 py-8">
  {#if loading}
    <div class="animate-pulse w-full mt-2">
      <!-- Header Skeleton -->
      <div class="mb-10">
        <div class="h-10 w-3/4 max-w-2xl bg-slate-200/60 dark:bg-white/10 rounded-lg mb-4"></div>
        <div class="h-5 w-full max-w-3xl bg-slate-200/50 dark:bg-white/5 rounded-lg"></div>
      </div>

      <!-- Dashboard Container Skeleton -->
      <div class="w-full">
        <div class="mb-2 px-2">
          <div class="h-8 w-64 bg-slate-200/60 dark:bg-white/10 rounded-lg mb-3"></div>
          <div class="h-4 w-96 bg-slate-200/50 dark:bg-white/5 rounded-lg"></div>
        </div>

        <div class="mt-8">
          <!-- Sec 1 -->
          <div class="h-6 w-96 bg-slate-200/60 dark:bg-white/10 rounded-lg mb-4"></div>
          <div class="h-16 w-full max-w-4xl bg-slate-200/50 dark:bg-white/5 rounded-lg mb-6"></div>
          <div class="w-full aspect-[21/9] bg-slate-100/50 dark:bg-[#1C1C1E] border border-slate-200/60 dark:border-white/5 rounded-3xl mb-12"></div>

          <!-- Sec 2 -->
          <div class="border-t border-slate-200/60 dark:border-white/5 pt-10 mb-6">
            <div class="h-6 w-80 bg-slate-200/60 dark:bg-white/10 rounded-lg mb-4"></div>
            <div class="h-4 w-full max-w-2xl bg-slate-200/50 dark:bg-white/5 rounded-lg mb-6"></div>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
              {#each [1, 2, 3] as i}
                <div class="bg-[#F5F5F7] dark:bg-black/40 p-6 rounded-3xl border border-slate-200/60 dark:border-white/5">
                  <div class="h-3 w-32 bg-slate-200/60 dark:bg-white/10 rounded-md mb-4"></div>
                  <div class="h-10 w-24 bg-slate-200/60 dark:bg-white/10 rounded-lg mb-4"></div>
                  <div class="h-12 w-full bg-slate-200/50 dark:bg-white/5 rounded-md"></div>
                </div>
              {/each}
            </div>
          </div>

          <!-- Sec 3 -->
          <div class="border-t border-slate-200/60 dark:border-white/5 pt-10">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              {#each [1, 2] as i}
                <div class="bg-[#F5F5F7] dark:bg-black/40 p-6 rounded-3xl border border-slate-200/60 dark:border-white/5">
                  <div class="h-5 w-48 bg-slate-200/60 dark:bg-white/10 rounded-lg mb-4"></div>
                  <div class="h-16 w-full bg-slate-200/50 dark:bg-white/5 rounded-md"></div>
                </div>
              {/each}
            </div>
          </div>
        </div>
      </div>
    </div>
  {:else}
    <header class="mb-10">
      <h1 class="text-3xl sm:text-4xl font-bold text-[#1D1D1F] dark:text-white tracking-tight mb-4">
        Validación Científica: ¿Por qué confiar en ENOS?
      </h1>
      <p class="text-lg text-slate-600 dark:text-slate-400 max-w-3xl leading-relaxed">
        El modelo no se basa en asunciones. Medimos matemáticamente la precisión de nuestros satélites contra los índices oficiales y comprobamos el acoplamiento real entre el mar y la tierra.
      </p>
    </header>

    <div class="grid grid-cols-1 gap-8">
      <DashboardContainer
        titulo="El respaldo matemático"
        subtitulo="Validación contra el índice oficial (ICEN) y análisis de correlación cruzada."
      >
        
        <!-- Seccion 1: Visual -->
        <div class="mt-2 mb-10">
          <h3 class="font-bold text-2xl text-[#1D1D1F] dark:text-white mb-4 tracking-tight">
            Réplica casi perfecta del índice oficial
          </h3>
          <p class="text-slate-700 dark:text-slate-300 text-[15px] mb-6 leading-relaxed max-w-4xl">
            Para poder emitir alertas tempranas, primero debemos saber si nuestros sensores leen correctamente la temperatura del mar. 
            Reconstruimos todo el historial del Índice Costero El Niño (ICEN) del ENFEN desde 1982 usando nuestra propia red de datos. 
            La curva generada por ENOS es un reflejo casi exacto de la oficial.
          </p>
          
          <div class="rounded-3xl border border-slate-200/60 dark:border-white/5 shadow-sm bg-[#F5F5F7] dark:bg-black/50 overflow-hidden overflow-x-auto">
            <img
              src={api("/static/mapas/3_validacion_icen.png")}
              alt="Validación ICEN"
              class="w-full h-auto min-w-[800px] lg:min-w-full"
              loading="lazy"
              onerror={(e) => ((e.currentTarget as HTMLElement).style.display = "none")}
            />
          </div>
        </div>

        <!-- Seccion 2: Métricas Cuadradas -->
        <div class="mt-12 mb-10 border-t border-slate-200/60 dark:border-white/5 pt-10">
          <h3 class="font-bold text-2xl text-[#1D1D1F] dark:text-white mb-4 tracking-tight">
            Los números detrás del acoplamiento
          </h3>
          <p class="text-slate-700 dark:text-slate-300 text-[15px] mb-6 leading-relaxed">
            No asumimos simplemente que el bosque seco reacciona al océano, lo calculamos probando múltiples desfases de tiempo con alto rigor estadístico.
          </p>

          <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <!-- Card 1 -->
            <div class="bg-[#F5F5F7] dark:bg-black/40 p-6 rounded-3xl border border-slate-200/60 dark:border-white/5 shadow-sm">
              <div class="text-[12px] font-semibold tracking-wide text-[#1D1D1F]/60 dark:text-[#AAAAAA] uppercase mb-3">Precisión Satelital</div>
              <div class="text-4xl font-bold text-[#1D1D1F] dark:text-white mb-3 tracking-tighter">r = 0.971</div>
              <div class="text-[14px] text-slate-600 dark:text-slate-400 leading-relaxed">Correlación casi perfecta contra el ICEN oficial del IGP tras evaluar 532 meses de historia continua.</div>
            </div>
            
            <!-- Card 2 -->
            <div class="bg-[#F5F5F7] dark:bg-black/40 p-6 rounded-3xl border border-slate-200/60 dark:border-white/5 shadow-sm">
              <div class="text-[12px] font-semibold tracking-wide text-[#1D1D1F]/60 dark:text-[#AAAAAA] uppercase mb-3">Acoplamiento (Mar → Tierra)</div>
              <div class="text-4xl font-bold text-[#1D1D1F] dark:text-white mb-3 tracking-tighter">r = 0.499</div>
              <div class="text-[14px] text-slate-600 dark:text-slate-400 leading-relaxed">Existe un <strong class="text-slate-700 dark:text-slate-300">retraso exacto de 1 mes</strong> entre el calentamiento del mar y la explosión de vegetación anómala en la costa.</div>
            </div>
            
            <!-- Card 3 -->
            <div class="bg-[#F5F5F7] dark:bg-black/40 p-6 rounded-3xl border border-slate-200/60 dark:border-white/5 shadow-sm">
              <div class="text-[12px] font-semibold tracking-wide text-[#1D1D1F]/60 dark:text-[#AAAAAA] uppercase mb-3">Control Nulo (Los Andes)</div>
              <div class="text-4xl font-bold text-[#1D1D1F] dark:text-white mb-3 tracking-tighter">Cero Reacción</div>
              <div class="text-[14px] text-slate-600 dark:text-slate-400 leading-relaxed">El páramo andino no reacciona al Niño costero. Esto confirma que el impacto medido en la costa es un evento específico, no ruido ambiental global.</div>
            </div>
          </div>
        </div>

        <!-- Seccion 3: Notas -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mt-12 border-t border-slate-200/60 dark:border-white/5 pt-10">
          <!-- Info -->
          <div class="bg-[#F5F5F7] dark:bg-black/40 p-6 rounded-3xl border border-slate-200/60 dark:border-white/5 shadow-sm">
            <h4 class="font-bold text-[#1D1D1F] dark:text-white text-lg mb-3 tracking-tight">Rigor Estadístico (Bonferroni)</h4>
            <p class="text-[14px] text-slate-600 dark:text-slate-400 leading-relaxed">
              Al probar 13 desfases de tiempo distintos para encontrar la conexión Mar-Bosque, aumentamos el riesgo de "hallar" algo por puro azar. Para evitar engañarnos, aplicamos la estricta <strong class="text-[#1D1D1F] dark:text-slate-200">Corrección de Bonferroni</strong> (p &lt; 0.0038) y eliminamos los ciclos estacionales. El resultado sobrevivió a la limpieza matemática.
            </p>
          </div>
          <!-- Limits -->
          <div class="bg-[#F5F5F7] dark:bg-black/40 p-6 rounded-3xl border border-slate-200/60 dark:border-white/5 shadow-sm">
            <h4 class="font-bold text-[#1D1D1F] dark:text-white text-lg mb-3 tracking-tight">Notas Técnicas Adicionales</h4>
            <ul class="text-[14px] text-slate-600 dark:text-slate-400 list-disc pl-4 space-y-2">
              <li><strong class="text-[#1D1D1F] dark:text-slate-200">Reconstrucción independiente:</strong> ENOS usa su propia climatología base (1991-2020). Cualquier ligero sesgo respecto a la data del ENFEN se recalcula y resta automáticamente.</li>
              <li><strong class="text-[#1D1D1F] dark:text-slate-200">Autocorrelación temporal:</strong> Al ser datos climáticos seguidos, la significancia exacta podría estar ligeramente subestimada. Sin embargo, el contraste total entre la fuerte reacción de la costa y la nula de la sierra valida firmemente nuestra hipótesis.</li>
            </ul>
          </div>
        </div>
      </DashboardContainer>
    </div>
  {/if}
</div>
