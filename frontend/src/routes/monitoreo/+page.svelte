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
        <!-- Filtros integrados (Ecosistema y Periodo) Brutalista -->
        <div class="flex flex-col md:flex-row items-center justify-between bg-white dark:bg-[#0a0a0a] border-4 border-slate-900 dark:border-white p-0 mb-8 rounded-none shadow-[8px_8px_0px_rgba(0,0,0,1)] dark:shadow-[8px_8px_0px_rgba(255,255,255,1)]">
          <div class="flex w-full md:w-auto">
            {#each Object.keys(etiquetas) as tab}
              <button
                class="flex-1 md:flex-none px-6 py-4 text-xs font-black uppercase tracking-widest transition-colors rounded-none border-b-4 md:border-b-0 md:border-r-4 {tabActiva === tab ? 'border-slate-900 dark:border-white text-white dark:text-slate-900 bg-slate-900 dark:bg-white' : 'border-slate-900 dark:border-white text-slate-900 dark:text-white hover:bg-slate-900 hover:text-white dark:hover:bg-white dark:hover:text-slate-900'}"
                onclick={() => (tabActiva = tab)}
              >
                {tab}
              </button>
            {/each}
          </div>
          
          {#if periodosDisponibles.length > 1}
            <div class="flex w-full md:w-auto border-t-4 md:border-t-0 md:border-l-4 border-slate-900 dark:border-white">
              {#each periodosDisponibles as p}
                <button
                  class="flex-1 md:flex-none px-6 py-4 text-xs font-black uppercase tracking-widest transition-colors rounded-none md:border-l-0 {periodoActivo === p ? 'bg-slate-900 dark:bg-white text-white dark:text-slate-900' : 'text-slate-900 dark:text-white hover:bg-slate-900 hover:text-white dark:hover:bg-white dark:hover:text-slate-900'}"
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
          <!-- Metadata Info Brutalista -->
          <div class="flex flex-wrap items-center gap-x-4 gap-y-2 mb-6 text-[10px] sm:text-[11px] font-black uppercase tracking-widest text-slate-900 dark:text-white">
            {#if mapaActual.generado}
              <span>Generado: <span class="text-slate-500 dark:text-slate-400 font-mono">{mapaActual.generado}</span></span>
            {/if}
            {#if mapaActual.desde && mapaActual.hasta}
              <span class="text-slate-900 dark:text-white">|</span>
              <span>Composición: <span class="text-slate-500 dark:text-slate-400 font-mono">{mapaActual.desde} a {mapaActual.hasta}</span></span>
            {/if}
            {#if mapaActual.kpi !== null && mapaActual.kpi !== undefined}
              <span class="text-slate-900 dark:text-white">|</span>
              <span>Media {mapaActual.banda}: <strong class="text-slate-900 dark:text-white text-sm font-mono">{mapaActual.kpi}</strong>{etiquetas[tabActiva].unidad}</span>
            {/if}
            {#if mapaActual.error_ultimo_intento}
              <span class="text-white bg-slate-900 dark:bg-white dark:text-slate-900 px-3 py-1 rounded-none border-2 border-slate-900 dark:border-white font-bold tracking-widest">⚠️ Fallo regeneración</span>
            {/if}
          </div>

          <div class="flex flex-col border-4 border-slate-900 dark:border-white rounded-none bg-white dark:bg-[#0a0a0a] shadow-[12px_12px_0px_rgba(0,0,0,1)] dark:shadow-[12px_12px_0px_rgba(255,255,255,1)]">
            <!-- Map Container -->
            <div class="relative w-full aspect-[26/25] bg-slate-50 dark:bg-[#111111] overflow-hidden border-b-4 border-slate-900 dark:border-white">
              <img
                src={urlMapa}
                alt="Mapa de {etiquetas[tabActiva].titulo}"
                class="absolute inset-0 w-full h-full object-fill"
                loading="lazy"
              />

              <!-- City Overlays Brutalist -->
              {#each CIUDADES as ciudad}
                <div class="absolute flex flex-col items-center justify-center -translate-x-1/2 -translate-y-1/2 pointer-events-none" style={getPointStyle(ciudad.lon, ciudad.lat)}>
                  <div class="w-2 h-2 rounded-none bg-slate-900 dark:bg-white shadow-[2px_2px_0_rgba(0,0,0,1)] dark:shadow-[2px_2px_0_rgba(255,255,255,1)]"></div>
                  <span class="mt-2 text-[10px] font-black tracking-widest text-white dark:text-slate-900 bg-slate-900 dark:bg-white px-2 py-1 rounded-none border-2 border-transparent">
                    {ciudad.nombre}
                  </span>
                </div>
              {/each}
            </div>

            <!-- Inline Legend Brutalist -->
            <div class="w-full flex flex-col sm:flex-row items-center justify-between p-6 gap-4">
              <span class="text-xs font-black uppercase tracking-widest text-slate-900 dark:text-white shrink-0">Escala de Valores</span>
              <div class="flex-1 w-full max-w-md flex items-center">
                <span class="text-xs font-black font-mono text-slate-900 dark:text-white mr-4">{leyendas[tabActiva].min}</span>
                <div class="h-4 w-full rounded-none border-2 border-slate-900 dark:border-white bg-gradient-to-r {leyendas[tabActiva].gradiente}"></div>
                <span class="text-xs font-black font-mono text-slate-900 dark:text-white ml-4">{leyendas[tabActiva].max}</span>
              </div>
            </div>
          </div>
        {/if}
      </DashboardContainer>
    {/if}
  </main>
</div>
