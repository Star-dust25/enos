<script lang="ts">
  import { onMount, onDestroy } from "svelte";

  let showModal = $state(false);

  onMount(() => {
    // Verificamos si ya ha visto el modal
    const hasSeen = localStorage.getItem("seenLiveUpdateModal");
    if (!hasSeen) {
      showModal = true;
      document.body.style.overflow = "hidden";
    }
  });

  onDestroy(() => {
    // Por precaución, si el componente se destruye sin apretar el botón
    if (typeof document !== "undefined") {
      document.body.style.overflow = "";
    }
  });

  function closeModal() {
    // Lo guardamos en el navegador para que no vuelva a salir
    localStorage.setItem("seenLiveUpdateModal", "true");
    showModal = false;
    document.body.style.overflow = "";
  }
</script>

{#if showModal}
  <div class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-white/90 dark:bg-[#000000]/95 backdrop-blur-sm">
    <!-- Contenedor Brutalista -->
    <div class="bg-white dark:bg-[#0a0a0a] border-4 border-slate-900 dark:border-peru-red p-8 sm:p-12 max-w-lg w-full shadow-[12px_12px_0px_rgba(0,0,0,1)] dark:shadow-[12px_12px_0px_rgba(200,16,46,0.3)] relative rounded-none">
      
      <!-- Label -->
      <div class="inline-block bg-slate-900 dark:bg-peru-red text-white px-4 py-2 mb-6 border-2 border-slate-900 dark:border-peru-red">
        <span class="text-[11px] font-black tracking-[0.25em] uppercase">
          Sistema Actualizado
        </span>
      </div>

      <h2 class="text-3xl md:text-4xl font-black font-slab text-slate-900 dark:text-white mb-6 uppercase tracking-tighter leading-none">
        Automatización 100% Integrada
      </h2>
      
      <p class="text-slate-700 dark:text-slate-300 mb-8 leading-relaxed font-mono text-base">
        El monitoreo satelital de <strong class="text-slate-900 dark:text-white font-black">ENOS</strong> ahora corre de forma autónoma. Los datos oceánicos y territoriales se descargarán sin requerir intervención manual.
      </p>

      <!-- Horarios de Actualización -->
      <div class="bg-slate-50 dark:bg-[#111111] border-2 border-slate-900 dark:border-white/10 p-6 mb-10">
        <h3 class="text-xs font-black text-slate-900 dark:text-slate-300 uppercase tracking-widest mb-6">Programa de Actualización Diaria</h3>
        
        <div class="flex flex-col gap-4">
          <div class="flex justify-between items-center">
            <span class="text-sm font-bold text-slate-700 dark:text-slate-400 uppercase tracking-wide">Ventana de ejecución (PET)</span>
            <span class="text-sm font-mono font-black text-slate-900 dark:text-white border-b-2 border-slate-900 dark:border-peru-red">~08:30 AM - 11:30 AM</span>
          </div>
          <div class="flex justify-between items-center pt-4 border-t-2 border-slate-900 dark:border-white/10">
            <span class="text-sm font-bold text-slate-700 dark:text-slate-400 uppercase tracking-wide">Próxima descarga</span>
            <span class="text-sm font-black tracking-widest uppercase text-slate-900 dark:text-peru-red">Cada mañana</span>
          </div>
        </div>
      </div>
      
      <div class="flex justify-end pt-4 border-t-4 border-slate-900 dark:border-white/10">
        <button
          onclick={closeModal}
          class="bg-slate-900 dark:bg-peru-red text-white border-2 border-slate-900 dark:border-peru-red font-black py-4 px-10 uppercase tracking-[0.2em] text-sm hover:bg-peru-red hover:border-peru-red dark:hover:bg-white dark:hover:text-peru-red transition-colors w-full sm:w-auto text-center focus:outline-none"
        >
          Entendido
        </button>
      </div>
    </div>
  </div>
{/if}
