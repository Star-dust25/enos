<script lang="ts">
  import { onMount } from "svelte";
  import DashboardContainer from "$lib/components/DashboardContainer.svelte";
  import { assetUrl, getJSON } from "$lib/api";

  let mapasData: Record<string, any> = $state({});
  let loading = $state(true);
  let error = $state("");

  let tabActiva = $state("LITORAL"); // LITORAL, MONTES, ANDES
  let periodoActivo = $state("actual_2026"); // actual_2026, nino_2017, nino_2015_16

  // 'res' describe la resolución NATIVA del sensor, no la del mapa que se
  // muestra. La miniatura son 900 px sobre un recuadro de ~2.6° × 2.5°, así
  // que cada píxel de pantalla ronda los 300 m; el KPI también se promedia a
  // 300 m. Promediar a esa escala sobre miles de km² da prácticamente el
  // mismo número y cuesta cien veces mpulso, pero conviene no dar a entender
  // que la imagen está a 30 m.
  const etiquetas: Record<
    string,
    { titulo: string; unidad: string; sensor: string; res: string }
  > = {
    LITORAL: {
      titulo: "Temperatura Superficial del Mar",
      unidad: "°C",
      sensor: "NOAA OISST v2.1",
      res: "0.25° (~28 km) nativo · Cadencia diaria",
    },
    MONTES: {
      titulo: "Vigor Vegetal Bosque Seco (MSAVI)",
      unidad: "",
      sensor: "Landsat 8 C2 L2",
      res: "30 m nativo · Compuesto mediano, remuestreado para el visor",
    },
    ANDES: {
      titulo: "Humedad del Páramo (NDMI)",
      unidad: "",
      sensor: "Landsat 8 C2 L2",
      res: "30 m nativo · Compuesto mediano, remuestreado para el visor",
    },
  };

  // Los periodos que genera construir_mapas.py. El orden importa: es el
  // orden en que aparecen las píldoras.
  const PERIODOS: Record<string, string> = {
    actual_2026: "Actual",
    nino_2017: "El Niño 2017",
    nino_2015_16: "El Niño 2015-16",
  };

  // Coordenadas y límites para sobreponer ciudades
  const BBOX = { lon_min: -81.6, lat_min: -6.5, lon_max: -79.0, lat_max: -4.0 };
  const CIUDADES = [
    { nombre: "Piura", lon: -80.632, lat: -5.194 },
    { nombre: "Sullana", lon: -80.685, lat: -4.903 },
    { nombre: "Talara", lon: -81.271, lat: -4.577 },
    { nombre: "Paita", lon: -81.107, lat: -5.078 },
    { nombre: "Chulucanas", lon: -80.162, lat: -5.093 },
    { nombre: "Sechura", lon: -80.822, lat: -5.556 },
    { nombre: "Ayabaca", lon: -79.714, lat: -4.639 },
    { nombre: "Huancabamba", lon: -79.45, lat: -5.239 },
  ];

  function getPointStyle(lon: number, lat: number) {
    const x = ((lon - BBOX.lon_min) / (BBOX.lon_max - BBOX.lon_min)) * 100;
    const y = ((BBOX.lat_max - lat) / (BBOX.lat_max - BBOX.lat_min)) * 100;
    return `left: ${x}%; top: ${y}%;`;
  }

  const leyendas: Record<
    string,
    { min: string; max: string; gradiente: string }
  > = {
    LITORAL: {
      min: "17 °C",
      max: "29 °C",
      gradiente: "from-[#2C5D73] via-[#5B8FA8] via-[#D68910] to-[#C0392B]",
    },
    MONTES: {
      min: "0.0",
      max: "0.6",
      gradiente: "from-[#8C6D46] via-[#B08D57] via-[#7D9E73] to-[#ACC8A2]",
    },
    ANDES: {
      min: "-0.2",
      max: "0.4",
      gradiente: "from-[#C0392B] via-[#D68910] via-[#5B8FA8] to-[#2C5D73]",
    },
  };

  onMount(async () => {
    try {
      mapasData = await getJSON("/api/mapas/indice");
    } catch (err) {
      // El mensaje real. "No se pudo cargar el índice" no distingue
      // entre backend apagado, 500 y CORS: tres problemas distintos
      // con tres arreglos distintos.
      error = err instanceof Error ? err.message : String(err);
      console.error(err);
    } finally {
      loading = false;
    }
  });

  // La clave se CONSTRUYE, no se busca.
  //
  // Antes esto era `Object.keys(mapasData).find(k => k.startsWith(tabActiva))`,
  // que devolvía siempre el primer periodo del ecosistema. Con tres
  // periodos por ecosistema, seis de los nueve mapas eran inalcanzables
  // desde la interfaz: los de 2017 y 2015-16, justo los que sostienen
  // el argumento de dosis-respuesta.
  let claveActual = $derived(`${tabActiva}__${periodoActivo}`);
  let mapaActual = $derived(mapasData[claveActual] ?? null);

  // Solo ofrecemos los periodos que el backend realmente publicó para
  // este ecosistema. Una píldora que lleva a un hueco es peor que una
  // píldora ausente.
  let periodosDisponibles = $derived(
    Object.keys(PERIODOS).filter((p) => `${tabActiva}__${p}` in mapasData),
  );

  let urlMapa = $derived(assetUrl(mapaActual?.url));
</script>

<svelte:head>
  <title>Monitoreo Satelital — PULSO</title>
</svelte:head>

<div class="max-w-6xl mx-auto mt-4 px-4 sm:px-6 lg:px-8 py-8">
  <main class="w-full max-w-5xl mx-auto">
    {#if loading}
      <div class="animate-pulse w-full mt-2">
        <!-- Header Skeleton -->
        <div class="mb-2 px-2">
          <div class="flex items-start sm:items-center mb-2 sm:mb-0">
            <div class="h-8 w-80 bg-slate-200/60 dark:bg-white/10 rounded-lg"></div>
          </div>
          <div class="h-4 w-full max-w-xl bg-slate-200/50 dark:bg-white/5 rounded-lg mt-3"></div>
        </div>

        <div class="mt-4">
          <!-- Filtros Skeleton -->
          <div class="flex flex-col md:flex-row items-center justify-between gap-4 mb-8">
            <div class="h-[42px] w-full md:w-80 bg-slate-200/60 dark:bg-white/10 rounded-full"></div>
            <div class="h-[42px] w-full md:w-64 bg-slate-200/60 dark:bg-white/10 rounded-full"></div>
          </div>

          <!-- Metadata Skeleton -->
          <div class="flex gap-4 mb-6">
            <div class="h-4 w-40 bg-slate-200/60 dark:bg-white/10 rounded-md"></div>
            <div class="h-4 w-48 bg-slate-200/60 dark:bg-white/10 rounded-md"></div>
          </div>

          <!-- Map Container Skeleton -->
          <div class="flex flex-col bg-white dark:bg-[#1C1C1E] rounded-3xl shadow-sm border border-slate-200/60 dark:border-white/5 overflow-hidden">
            <!-- Map Area -->
            <div class="relative w-full aspect-[26/25] bg-slate-100/50 dark:bg-white/5 border-b border-slate-200/60 dark:border-white/5"></div>
            <!-- Legend Area -->
            <div class="w-full flex flex-col sm:flex-row items-center justify-between p-6 gap-6 bg-[#F5F5F7] dark:bg-black/20">
              <div class="h-4 w-24 bg-slate-200/60 dark:bg-white/10 rounded-md"></div>
              <div class="flex-1 w-full max-w-md h-3 bg-slate-200/60 dark:bg-white/10 rounded-full"></div>
            </div>
          </div>
        </div>
      </div>
    {:else if error}
      <div class="bg-red-50 dark:bg-red-900/20 text-red-700 dark:text-red-400 p-5 rounded-none border border-red-100 dark:border-red-800/50">
        <p class="font-bold mb-1">No se pudo cargar el índice de mapas</p>
        <p class="text-sm">{error}</p>
      </div>
    {:else}
      <DashboardContainer
        titulo={etiquetas[tabActiva].titulo}
        subtitulo={`Sensor: ${etiquetas[tabActiva].sensor} — Resolución: ${etiquetas[tabActiva].res}`}
      >
        <!-- Filtros integrados (Ecosistema y Periodo) Clean Minimalism -->
        <div class="flex flex-col md:flex-row items-center justify-between gap-4 mb-8">
          <!-- Ecosistema -->
          <div class="inline-flex bg-[#AAAAAA]/20 dark:bg-white/10 rounded-full p-1.5 shadow-inner w-full md:w-auto">
            {#each Object.keys(etiquetas) as tab}
              <button
                class="flex-1 md:flex-none px-6 py-2.5 font-medium text-sm transition-all rounded-full {tabActiva === tab ? 'bg-[#007AFF] text-white shadow-sm' : 'text-[#1D1D1F]/60 hover:text-[#1D1D1F] dark:text-[#AAAAAA] dark:hover:text-white'}"
                onclick={() => (tabActiva = tab)}
              >
                {tab}
              </button>
            {/each}
          </div>
          
          <!-- Periodo -->
          {#if periodosDisponibles.length > 1}
            <div class="inline-flex bg-[#AAAAAA]/20 dark:bg-white/10 rounded-full p-1.5 shadow-inner w-full md:w-auto">
              {#each periodosDisponibles as p}
                <button
                  class="flex-1 md:flex-none px-6 py-2.5 font-medium text-sm transition-all rounded-full {periodoActivo === p ? 'bg-[#1D1D1F] dark:bg-white text-white dark:text-[#1D1D1F] shadow-sm' : 'text-[#1D1D1F]/60 hover:text-[#1D1D1F] dark:text-[#AAAAAA] dark:hover:text-white'}"
                  onclick={() => (periodoActivo = p)}
                >
                  {PERIODOS[p]}
                </button>
              {/each}
            </div>
          {/if}
        </div>

        {#if !urlMapa}
          <div class="text-center py-20 text-slate-400 bg-slate-50 dark:bg-[#111111] border border-slate-200 dark:border-white/10 rounded-none">
            <p>No hay mapa disponible para {tabActiva} · {PERIODOS[periodoActivo] ?? periodoActivo}.</p>
            {#if mapaActual?.error}
              <p class="text-xs mt-2 font-mono text-slate-500">{mapaActual.error}</p>
            {/if}
          </div>
        {:else}
          <!-- Metadata Info Clean Minimalism -->
          <div class="flex flex-wrap items-center gap-x-3 gap-y-2 mb-6 text-[12px] font-medium text-[#1D1D1F]/60 dark:text-[#AAAAAA]">
            {#if mapaActual.generado}
              <span>Generado: <span class="font-mono text-[#1D1D1F] dark:text-white">{mapaActual.generado}</span></span>
            {/if}
            {#if mapaActual.desde && mapaActual.hasta}
              <span class="text-[#1D1D1F]/30 dark:text-white/20">|</span>
              <span>Composición: <span class="font-mono text-[#1D1D1F] dark:text-white">{mapaActual.desde} a {mapaActual.hasta}</span></span>
            {/if}
            {#if mapaActual.kpi !== null && mapaActual.kpi !== undefined}
              <span class="text-[#1D1D1F]/30 dark:text-white/20">|</span>
              <span>Media {mapaActual.banda}: <strong class="text-[#007AFF] text-[13px] font-mono">{mapaActual.kpi}</strong>{etiquetas[tabActiva].unidad}</span>
            {/if}
            {#if mapaActual.error_ultimo_intento}
              <span class="text-white bg-red-500 px-3 py-1 rounded-full text-[11px] font-semibold tracking-wide shadow-sm">⚠️ Fallo regeneración</span>
            {/if}
          </div>

          <div class="flex flex-col bg-white dark:bg-[#1C1C1E] rounded-3xl shadow-sm border border-slate-200/60 dark:border-white/5 overflow-hidden">
            <!-- Map Container -->
            <div class="relative w-full aspect-[26/25] bg-slate-50 dark:bg-black/50 border-b border-slate-200/60 dark:border-white/5">
              <img
                src={urlMapa}
                alt="Mapa de {etiquetas[tabActiva].titulo}"
                class="absolute inset-0 w-full h-full object-fill opacity-90 hover:opacity-100 transition-opacity duration-500"
                loading="lazy"
              />

              <!-- City Overlays Clean -->
              {#each CIUDADES as ciudad}
                <div class="absolute flex flex-col items-center justify-center -translate-x-1/2 -translate-y-1/2 pointer-events-none" style={getPointStyle(ciudad.lon, ciudad.lat)}>
                  <div class="w-2.5 h-2.5 rounded-full bg-white dark:bg-[#1D1D1F] border-2 border-[#1D1D1F] dark:border-white shadow-md"></div>
                  <span class="mt-2 text-[10px] font-medium tracking-wide text-[#1D1D1F] dark:text-white bg-white/80 dark:bg-[#1C1C1E]/80 backdrop-blur-sm px-2.5 py-1 rounded-full shadow-sm border border-slate-200/50 dark:border-white/10">
                    {ciudad.nombre}
                  </span>
                </div>
              {/each}
            </div>

            <!-- Inline Legend Clean -->
            <div class="w-full flex flex-col sm:flex-row items-center justify-between p-6 gap-6 bg-[#F5F5F7] dark:bg-black/20">
              <span class="text-[11px] font-semibold uppercase tracking-widest text-[#1D1D1F]/60 dark:text-[#AAAAAA] shrink-0">Escala de Valores</span>
              <div class="flex-1 w-full max-w-md flex items-center">
                <span class="text-[13px] font-medium font-mono text-[#1D1D1F] dark:text-white mr-4">{leyendas[tabActiva].min}</span>
                <div class="h-3 w-full rounded-full border border-slate-200/50 dark:border-white/10 bg-gradient-to-r {leyendas[tabActiva].gradiente} shadow-inner"></div>
                <span class="text-[13px] font-medium font-mono text-[#1D1D1F] dark:text-white ml-4">{leyendas[tabActiva].max}</span>
              </div>
            </div>
          </div>
        {/if}
      </DashboardContainer>
    {/if}
  </main>
</div>
