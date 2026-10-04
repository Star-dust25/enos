<script lang="ts">
  import { onMount } from "svelte";

  let showModal = $state(false);

  onMount(() => {
    // Verificamos si ya ha visto el modal
    const hasSeen = localStorage.getItem("seenLiveUpdateModal");
    if (!hasSeen) {
      showModal = true;
    }
  });

  function closeModal() {
    // Lo guardamos en el navegador para que no vuelva a salir
    localStorage.setItem("seenLiveUpdateModal", "true");
    showModal = false;
  }
</script>

{#if showModal}
  <div class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/90 backdrop-blur-md">
    <!-- Contenedor cuadrado premium -->
    <div class="bg-white dark:bg-[#0a0a0a] border border-slate-200 dark:border-white/10 border-t-[6px] border-t-emerald-500 p-8 sm:p-10 max-w-lg w-full shadow-[0_0_50px_rgba(16,185,129,0.15)] relative rounded-none transform transition-all">
      
      <!-- Label -->
      <div class="inline-block bg-emerald-50 dark:bg-emerald-900/30 border border-emerald-200 dark:border-emerald-800/50 px-3 py-1 mb-5 rounded-none">
        <span class="text-[10px] font-bold tracking-[0.25em] uppercase text-emerald-700 dark:text-emerald-400">
          Sistema Actualizado
        </span>
      </div>

      <h2 class="text-3xl font-bold font-slab text-slate-900 dark:text-white mb-4 leading-tight tracking-tight">
        Automatización 100% Integrada
      </h2>
      
      <p class="text-slate-600 dark:text-slate-400 mb-6 leading-relaxed font-light text-lg">
        El monitoreo satelital de <strong class="text-slate-900 dark:text-slate-200 font-semibold">Pulso</strong> ahora corre de forma autónoma. Los datos oceánicos y territoriales se descargarán sin requerir intervención manual.
      </p>

      <!-- Horarios de Actualización -->
      <div class="bg-slate-50 dark:bg-[#111111] border border-slate-200 dark:border-white/10 p-5 mb-8 rounded-none">
        <h3 class="text-xs font-bold text-slate-500 dark:text-slate-400 uppercase tracking-widest mb-4">Programa de Actualización Diaria</h3>
        
        <div class="flex flex-col gap-3">
          <div class="flex justify-between items-center">
            <span class="text-sm font-semibold text-slate-700 dark:text-slate-300">Ventana de ejecución (PET)</span>
            <span class="text-sm font-mono font-bold text-emerald-600 dark:text-emerald-400 bg-emerald-50 dark:bg-emerald-900/20 px-2 py-0.5 border border-emerald-100 dark:border-emerald-800/30">~08:30 AM - 11:30 AM</span>
          </div>
          <div class="flex justify-between items-center pt-3 mt-1 border-t border-slate-200 dark:border-white/10">
            <span class="text-sm font-semibold text-slate-700 dark:text-slate-300">Próxima descarga</span>
            <span class="text-sm font-bold tracking-widest uppercase text-slate-900 dark:text-white">Cada mañana</span>
          </div>
        </div>
      </div>
      
      <div class="flex justify-end pt-2 border-t border-slate-100 dark:border-white/5">
        <button
          onclick={closeModal}
          class="bg-emerald-500 hover:bg-emerald-600 text-white font-bold py-3 px-8 uppercase tracking-widest text-xs transition-colors rounded-none w-full sm:w-auto text-center"
        >
          Entendido
        </button>
      </div>
    </div>
  </div>
{/if}
