<script lang="ts">
  import { onMount } from "svelte";
  import DashboardContainer from "$lib/components/DashboardContainer.svelte";
  import { api } from "$lib/api";

  let loading = $state(true);

  onMount(() => {
    // Simular tiempo de carga para mostrar el esqueleto (consistencia de UI/UX)
    setTimeout(() => {
      loading = false;
    }, 400);
  });
</script>

<svelte:head>
  <title>Backtest Histórico — PULSO</title>
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
          <div class="h-6 w-96 bg-slate-200/60 dark:bg-white/10 rounded-lg mb-4"></div>
          <div class="h-16 w-full max-w-4xl bg-slate-200/50 dark:bg-white/5 rounded-lg mb-6"></div>
          
          <!-- Image Box Skeleton -->
          <div class="w-full aspect-[21/9] bg-slate-100/50 dark:bg-[#1C1C1E] border border-slate-200/60 dark:border-white/5 rounded-3xl mb-12"></div>

          <div class="border-t border-slate-200/60 dark:border-white/5 pt-10 mb-6">
            <div class="h-6 w-80 bg-slate-200/60 dark:bg-white/10 rounded-lg mb-4"></div>
            <div class="h-4 w-full max-w-2xl bg-slate-200/50 dark:bg-white/5 rounded-lg mb-6"></div>
            
            <!-- 3 Cards Skeleton -->
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

          <div class="border-t border-slate-200/60 dark:border-white/5 pt-10">
            <!-- 2 Notes Skeleton -->
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
        El Niño Costero 2017: Cuando el océano nos engañó
      </h1>
      <p class="text-lg text-slate-600 dark:text-slate-400 max-w-3xl leading-relaxed">
        Un análisis retrospectivo que demuestra por qué medir solo el mar no es suficiente, y cómo PULSO habría anticipado la crisis.
      </p>
    </header>

    <div class="grid grid-cols-1 gap-8">
      <DashboardContainer
        titulo="El desastre en Piura"
        subtitulo="Desborde del Río Piura, 27 de marzo de 2017 (3,468 m³/s)"
      >
        
        <!-- Seccion 1: El Problema Visual -->
        <div class="mt-2 mb-10">
          <h3 class="font-bold text-2xl text-[#1D1D1F] dark:text-white mb-4 tracking-tight">
            El problema: Un mar caliente no equivale a desastre
          </h3>
          <p class="text-slate-700 dark:text-slate-300 text-[15px] mb-6 leading-relaxed max-w-4xl">
            El Niño de 2015-16 calentó el mar <strong class="text-slate-900 dark:text-slate-100">mucho más</strong> que el evento de 2017. Los indicadores oceánicos tradicionales catalogaron a 2015 como "FUERTE" y a 2017 apenas como "MODERADO". 
            Sin embargo, la realidad fue otra: en 2017 hubo <strong class="text-slate-900 dark:text-slate-100">12 veces más damnificados</strong>. Monitorear solo el mar no basta, debemos observar cómo reacciona el territorio vivo.
          </p>
          
          <!-- Image -->
          <div class="rounded-3xl border border-slate-200/60 dark:border-white/5 shadow-sm bg-[#F5F5F7] dark:bg-black/50 overflow-hidden overflow-x-auto">
            <img
              src={api("/static/mapas/5_dos_etapas_2015_vs_2017.png")}
              alt="Comparación 2015 vs 2017"
              class="w-full h-auto min-w-[800px] lg:min-w-full"
              loading="lazy"
              onerror={(e) => ((e.currentTarget as HTMLElement).style.display = "none")}
            />
          </div>
        </div>

        <!-- Seccion 2: La Ventaja PULSO -->
        <div class="mt-12 mb-10 border-t border-slate-200/60 dark:border-white/5 pt-10">
          <h3 class="font-bold text-2xl text-[#1D1D1F] dark:text-white mb-4 tracking-tight">
            La Solución: Anticipación en dos etapas
          </h3>
          <p class="text-slate-700 dark:text-slate-300 text-[15px] mb-6 leading-relaxed">
            Mientras que los índices oficiales declararon el evento <em>después</em> del desborde, el monitoreo satelital diario de PULSO nos habría dado semanas vitales para actuar.
          </p>

          <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <!-- Card 1 -->
            <div class="bg-[#F5F5F7] dark:bg-black/40 p-6 rounded-3xl border border-slate-200/60 dark:border-white/5 shadow-sm">
              <div class="text-[12px] font-semibold tracking-wide text-[#1D1D1F]/60 dark:text-[#AAAAAA] uppercase mb-3">Método Tradicional (ICEN)</div>
              <div class="text-4xl font-bold text-[#1D1D1F] dark:text-white mb-3 tracking-tighter">−5 días</div>
              <div class="text-[14px] text-slate-600 dark:text-slate-400 leading-relaxed">El diagnóstico oficial habría llegado 5 días <strong class="text-slate-700 dark:text-slate-300">después</strong> del desastre principal.</div>
            </div>
            <!-- Card 2 -->
            <div class="bg-[#F5F5F7] dark:bg-black/40 p-6 rounded-3xl border border-slate-200/60 dark:border-white/5 shadow-sm">
              <div class="text-[12px] font-semibold tracking-wide text-[#1D1D1F]/60 dark:text-[#AAAAAA] uppercase mb-3">PULSO Etapa 1 (Océano)</div>
              <div class="text-4xl font-bold text-[#1D1D1F] dark:text-white mb-3 tracking-tighter">+68 días</div>
              <div class="text-[14px] text-slate-600 dark:text-slate-400 leading-relaxed">La alerta oceánica se encendió el 18 de enero. Da mucho tiempo, pero acarrea el riesgo de ser una falsa alarma.</div>
            </div>
            <!-- Card 3 -->
            <div class="bg-[#F5F5F7] dark:bg-black/40 p-6 rounded-3xl border border-slate-200/60 dark:border-white/5 shadow-sm">
              <div class="text-[12px] font-semibold tracking-wide text-[#1D1D1F]/60 dark:text-[#AAAAAA] uppercase mb-3">PULSO Etapa 2 (Territorio)</div>
              <div class="text-4xl font-bold text-[#1D1D1F] dark:text-white mb-3 tracking-tighter">+26 días</div>
              <div class="text-[14px] text-slate-600 dark:text-slate-400 leading-relaxed">El satélite Landsat 8 detectó el verdor anómalo en tierra firme el 1 de marzo. <strong class="text-slate-700 dark:text-slate-300">El peligro quedó confirmado.</strong></div>
            </div>
          </div>
        </div>

        <!-- Seccion 3: Notas Adicionales -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mt-12 border-t border-slate-200/60 dark:border-white/5 pt-10">
          <!-- Info -->
          <div class="bg-[#F5F5F7] dark:bg-black/40 p-6 rounded-3xl border border-slate-200/60 dark:border-white/5 shadow-sm">
            <h4 class="font-bold text-[#1D1D1F] dark:text-white text-lg mb-3 tracking-tight">Complemento, no reemplazo</h4>
            <p class="text-[14px] text-slate-600 dark:text-slate-400 leading-relaxed">
              PULSO no compite con el ENFEN. Los índices oficiales están diseñados para <strong class="text-[#1D1D1F] dark:text-slate-200">diagnosticar</strong> el clima global de manera retrospectiva. PULSO está diseñado para la <strong class="text-[#1D1D1F] dark:text-slate-200">acción inmediata</strong> y localizada.
            </p>
          </div>
          <!-- Limits -->
          <div class="bg-[#F5F5F7] dark:bg-black/40 p-6 rounded-3xl border border-slate-200/60 dark:border-white/5 shadow-sm">
            <h4 class="font-bold text-[#1D1D1F] dark:text-white text-lg mb-3 tracking-tight">Limitaciones del modelo</h4>
            <ul class="text-[14px] text-slate-600 dark:text-slate-400 list-disc pl-4 space-y-2">
              <li><strong class="text-[#1D1D1F] dark:text-slate-200">Historial corto:</strong> El satélite requerido para la Etapa 2 opera desde 2013, excluyendo los Niños de 1983 y 1998 de la data de entrenamiento.</li>
              <li><strong class="text-[#1D1D1F] dark:text-slate-200">Relación probada:</strong> Pese a ello, la regla se cumple: a mayor verdor anómalo detectado, mayor magnitud del desastre posterior.</li>
            </ul>
          </div>
        </div>

      </DashboardContainer>
    </div>
  {/if}
</div>
