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
  // mismo número y cuesta cien veces menos, pero conviene no dar a entender
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
  <title>Monitoreo Satelital — ENOS</title>
</svelte:head>

<div class="max-w-6xl mx-auto mt-4 px-4 sm:px-6 lg:px-8 py-8">
  <main class="w-full max-w-5xl mx-auto">
    {#if loading}
      <div class="flex justify-center py-20">
        <div class="animate-spin h-8 w-8 border-b-2 border-slate-800"></div>
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
        <!-- Filtros integrados (Ecosistema y Periodo) -->
        <div class="flex flex-col md:flex-row items-center justify-between bg-slate-50 dark:bg-[#111111] border border-slate-200 dark:border-white/10 p-0 mb-6 rounded-none">
          <div class="flex w-full md:w-auto">
            {#each Object.keys(etiquetas) as tab}
              <button
                class="flex-1 md:flex-none px-5 py-3 text-xs font-bold uppercase tracking-wider transition-all rounded-none border-b-2 {tabActiva === tab ? 'border-blue-500 text-slate-900 dark:text-slate-100 bg-white dark:bg-slate-800/50' : 'border-transparent text-slate-500 hover:text-slate-700 dark:hover:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800/30'}"
                onclick={() => (tabActiva = tab)}
              >
                {tab}
              </button>
            {/each}
          </div>
          
          {#if periodosDisponibles.length > 1}
            <div class="flex w-full md:w-auto border-t md:border-t-0 md:border-l border-slate-200 dark:border-white/10">
              {#each periodosDisponibles as p}
                <button
                  class="flex-1 md:flex-none px-5 py-3 text-xs font-bold uppercase tracking-wider transition-all rounded-none border-b-2 {periodoActivo === p ? 'border-amber-500 text-slate-900 dark:text-slate-100 bg-white dark:bg-slate-800/50' : 'border-transparent text-slate-500 hover:text-slate-700 dark:hover:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800/30'}"
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
          <!-- Metadata Info -->
          <div class="flex flex-wrap items-center gap-x-4 gap-y-2 mb-4 text-[11px] font-bold uppercase tracking-widest text-slate-500 dark:text-slate-400">
            {#if mapaActual.generado}
              <span>Generado: <span class="text-slate-800 dark:text-slate-200">{mapaActual.generado}</span></span>
            {/if}
            {#if mapaActual.desde && mapaActual.hasta}
              <span class="text-slate-300 dark:text-slate-600">|</span>
              <span>Composición: <span class="text-slate-800 dark:text-slate-200">{mapaActual.desde} a {mapaActual.hasta}</span></span>
            {/if}
            {#if mapaActual.kpi !== null && mapaActual.kpi !== undefined}
              <span class="text-slate-300 dark:text-slate-600">|</span>
              <span>Media {mapaActual.banda}: <strong class="text-blue-600 dark:text-blue-400 text-sm">{mapaActual.kpi}</strong>{etiquetas[tabActiva].unidad}</span>
            {/if}
            {#if mapaActual.error_ultimo_intento}
              <span class="text-red-500 bg-red-100 dark:bg-red-900/30 px-2 py-0.5 rounded-none">⚠️ Fallo regeneración</span>
            {/if}
          </div>

          <div class="flex flex-col border border-slate-200 dark:border-white/10 rounded-none bg-slate-50 dark:bg-[#111111] shadow-sm dark:shadow-none">
            <!-- Map Container -->
            <div class="relative w-full aspect-[26/25] bg-[#eef2f5] dark:bg-[#0a0a0a] overflow-hidden">
              <img
                src={urlMapa}
                alt="Mapa de {etiquetas[tabActiva].titulo}"
                class="absolute inset-0 w-full h-full object-fill"
                loading="lazy"
              />

              <!-- City Overlays -->
              {#each CIUDADES as ciudad}
                <div class="absolute flex flex-col items-center justify-center -translate-x-1/2 -translate-y-1/2 pointer-events-none" style={getPointStyle(ciudad.lon, ciudad.lat)}>
                  <div class="w-1.5 h-1.5 rounded-none bg-slate-900 dark:bg-white shadow-[0_0_0_2px_rgba(255,255,255,0.9)] dark:shadow-[0_0_0_2px_rgba(0,0,0,0.9)]"></div>
                  <span class="mt-1 text-[10px] font-bold text-slate-800 dark:text-slate-200 bg-white/90 dark:bg-black/90 px-1.5 py-0.5 rounded-none border border-slate-300 dark:border-slate-700">
                    {ciudad.nombre}
                  </span>
                </div>
              {/each}
            </div>

            <!-- Inline Legend -->
            <div class="w-full flex flex-col sm:flex-row items-center justify-between p-4 border-t border-slate-200 dark:border-white/10 gap-4">
              <span class="text-xs font-bold uppercase tracking-widest text-slate-500 shrink-0">Escala de Valores</span>
              <div class="flex-1 w-full max-w-md flex items-center">
                <span class="text-xs font-bold text-slate-700 dark:text-slate-300 mr-3">{leyendas[tabActiva].min}</span>
                <div class="h-2.5 w-full rounded-none bg-gradient-to-r {leyendas[tabActiva].gradiente}"></div>
                <span class="text-xs font-bold text-slate-700 dark:text-slate-300 ml-3">{leyendas[tabActiva].max}</span>
              </div>
            </div>
          </div>
        {/if}
      </DashboardContainer>
    {/if}
  </main>
</div>
