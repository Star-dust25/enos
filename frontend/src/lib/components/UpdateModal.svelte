<script lang="ts">
  import { onMount, onDestroy } from "svelte";

  let dialogEl: HTMLDialogElement;

  onMount(() => {
    // Verificamos si ya ha visto el modal
    const hasSeen = localStorage.getItem("seenLiveUpdateModal");
    if (!hasSeen && dialogEl) {
      dialogEl.showModal();
      document.body.style.overflow = "hidden";
      document.documentElement.style.overflow = "hidden";
    }
  });

  function closeModal() {
    // Lo guardamos en el navegador para que no vuelva a salir
    localStorage.setItem("seenLiveUpdateModal", "true");
    if (dialogEl) dialogEl.close();
    document.body.style.overflow = "";
    document.documentElement.style.overflow = "";
  }

  function handleBackdropClick(e: MouseEvent) {
    if (e.target === dialogEl) {
      closeModal();
    }
  }
</script>

  <dialog
    bind:this={dialogEl}
    class="backdrop:bg-white/90 dark:backdrop:bg-[#000000]/95 backdrop:backdrop-blur-sm bg-transparent p-4 sm:p-6 m-auto rounded-none overflow-visible max-w-lg w-full"
    onclick={handleBackdropClick}
    oncancel={(e) => { e.preventDefault(); closeModal(); }}
  >
    <!-- Contenedor Brutalista -->
    <div 
      class="bg-white dark:bg-[#0a0a0a] border-4 border-slate-900 dark:border-peru-red p-6 sm:p-10 w-full max-h-[90vh] overflow-y-auto shadow-[12px_12px_0px_rgba(0,0,0,1)] dark:shadow-[12px_12px_0px_rgba(200,16,46,0.3)] flex flex-col m-0"
      onclick={(e) => e.stopPropagation()}
      role="document"
    >
      
      <!-- Label -->
      <div class="inline-block self-start bg-slate-900 dark:bg-peru-red text-white px-4 py-2 mb-6 border-2 border-slate-900 dark:border-peru-red">
        <span class="text-[11px] font-black tracking-[0.25em] uppercase">
          Sistema Actualizado
        </span>
      </div>

      <h2 class="text-3xl sm:text-4xl font-black font-slab text-slate-900 dark:text-white mb-5 uppercase tracking-tighter leading-none">
        Automatización 100% Integrada
      </h2>
      
      <p class="text-slate-700 dark:text-slate-300 mb-8 leading-relaxed font-mono text-sm sm:text-base">
        El monitoreo satelital de <strong class="text-slate-900 dark:text-white font-black">ENOS</strong> ahora corre de forma autónoma. Los datos oceánicos y territoriales se descargarán sin requerir intervención manual.
      </p>

      <!-- Horarios de Actualización -->
      <div class="bg-slate-50 dark:bg-[#111111] border-2 border-slate-900 dark:border-white/10 p-5 sm:p-6 mb-8">
        <h3 class="text-[11px] sm:text-xs font-black text-slate-900 dark:text-slate-300 uppercase tracking-widest mb-5">Programa de Actualización Diaria</h3>
        
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
  </dialog>
