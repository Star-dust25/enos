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
    class="backdrop:bg-slate-900/20 dark:backdrop:bg-black/60 backdrop:backdrop-blur-md bg-transparent p-4 sm:p-6 m-auto rounded-none overflow-visible max-w-lg w-full"
    onclick={handleBackdropClick}
    oncancel={(e) => { e.preventDefault(); closeModal(); }}
  >
    <!-- Contenedor Clean -->
    <div 
      class="bg-white dark:bg-[#1C1C1E] rounded-3xl w-full max-h-[90vh] overflow-y-auto p-8 shadow-[0_20px_40px_rgba(0,0,0,0.1)] dark:shadow-[0_20px_40px_rgba(0,0,0,0.5)] border border-slate-200/60 dark:border-white/10 flex flex-col m-0"
      onclick={(e) => e.stopPropagation()}
      role="document"
    >
      
      <h2 class="text-2xl sm:text-3xl font-semibold text-[#1D1D1F] dark:text-white mb-4 tracking-tight leading-none mt-2">
        Automatización 100% Integrada
      </h2>
      
      <p class="text-slate-500 dark:text-slate-400 mb-8 leading-relaxed text-[15px]">
        El monitoreo satelital de <strong class="text-slate-900 dark:text-white font-medium">ENOS</strong> ahora corre de forma autónoma. Los datos oceánicos y territoriales se descargarán sin requerir intervención manual.
      </p>

      <!-- Horarios de Actualización -->
      <div class="bg-[#F5F5F7] dark:bg-black rounded-2xl p-6 mb-8 border border-slate-200/60 dark:border-white/5">
        <h3 class="text-[11px] font-medium text-slate-500 dark:text-slate-400 uppercase tracking-widest mb-5">Programa de Actualización Diaria</h3>
        
        <div class="flex flex-col gap-4">
          <div class="flex justify-between items-center">
            <span class="text-[13px] font-medium text-slate-500 dark:text-slate-400">Ventana de ejecución (PET)</span>
            <span class="text-[13px] font-semibold text-slate-900 dark:text-white">~08:30 AM - 11:30 AM</span>
          </div>
          <div class="flex justify-between items-center pt-4 border-t border-slate-200/60 dark:border-white/10">
            <span class="text-[13px] font-medium text-slate-500 dark:text-slate-400">Próxima descarga</span>
            <span class="text-[13px] font-semibold text-slate-900 dark:text-white">Cada mañana</span>
          </div>
        </div>
      </div>
      
      <div class="flex justify-end pt-4">
        <button
          onclick={closeModal}
          class="px-8 py-3 bg-[#007AFF] hover:opacity-90 text-white rounded-full transition-opacity font-medium text-[15px] shadow-sm focus:outline-none"
        >
          Entendido
        </button>
      </div>
    </div>
  </dialog>
