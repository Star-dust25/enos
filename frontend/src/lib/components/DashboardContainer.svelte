<script lang="ts">
  import type { Snippet } from "svelte";
  import { fade, fly } from "svelte/transition";

  let {
    titulo,
    subtitulo = "",
    tooltip = "",
    children,
  } = $props<{
    titulo: string;
    subtitulo?: string;
    tooltip?: string | string[];
    children?: Snippet;
  }>();

  let dialogEl: HTMLDialogElement;

  function openModal() {
    if (dialogEl) dialogEl.showModal();
    if (typeof document !== "undefined") {
      document.body.style.overflow = "hidden";
      document.documentElement.style.overflow = "hidden";
    }
  }

  function closeModal() {
    if (dialogEl) dialogEl.close();
    if (typeof document !== "undefined") {
      document.body.style.overflow = "";
      document.documentElement.style.overflow = "";
    }
  }

  function handleBackdropClick(e: MouseEvent) {
    if (e.target === dialogEl) {
      closeModal();
    }
  }
</script>

<div>
  <!-- Header Minimalista -->
  <div class="mb-6 px-2">
    <div class="flex items-start sm:items-center">
      <h2 class="text-2xl font-semibold text-apple-dark dark:text-white tracking-tight mb-2 sm:mb-0">
        {titulo}
      </h2>
      {#if tooltip}
        <div class="ml-3 mt-1 sm:mt-0">
          <button
            onclick={openModal}
            class="w-6 h-6 rounded-full bg-apple-gray/20 text-apple-dark/60 dark:text-apple-gray flex items-center justify-center text-xs hover:bg-apple-gray/40 transition-colors focus:outline-none"
            aria-label="Más información"
          >
            ?
          </button>
        </div>
      {/if}
    </div>
    {#if subtitulo}
      <p class="text-[15px] text-apple-gray dark:text-apple-gray mt-1 leading-relaxed max-w-4xl">
        {subtitulo}
      </p>
    {/if}
  </div>

  <!-- Body: Los hijos flotan libremente -->
  <div class="w-full">
    {#if children}
      {@render children()}
    {/if}
  </div>
</div>

  <dialog
    bind:this={dialogEl}
    class="backdrop:bg-slate-900/20 dark:backdrop:bg-black/60 backdrop:backdrop-blur-md bg-transparent p-4 sm:p-6 m-auto rounded-none overflow-visible max-w-lg w-full"
    onclick={handleBackdropClick}
    oncancel={(e) => { e.preventDefault(); closeModal(); }}
  >
    <div 
      class="bg-white dark:bg-[#1C1C1E] rounded-3xl w-full max-h-[90vh] overflow-y-auto p-8 shadow-[0_20px_40px_rgba(0,0,0,0.1)] dark:shadow-[0_20px_40px_rgba(0,0,0,0.5)] border border-slate-200/60 dark:border-white/10 flex flex-col m-0"
      onclick={(e) => e.stopPropagation()}
      role="document"
    >
      <div class="flex justify-between items-start mb-6 pb-4 border-b border-slate-200/60 dark:border-white/10">
        <h3 class="font-semibold text-xl tracking-tight text-slate-900 dark:text-white">Información</h3>
        <button 
          class="text-slate-400 hover:text-slate-600 dark:hover:text-slate-300 transition-colors focus:outline-none flex-shrink-0 ml-4"
          onclick={closeModal}
          aria-label="Cerrar"
        >
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-6 h-6">
            <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
      <div class="text-[15px] text-slate-500 dark:text-slate-400 leading-relaxed">
        {#if Array.isArray(tooltip)}
          <ul class="list-disc pl-5 space-y-3">
            {#each tooltip as item}
              <li>{item}</li>
            {/each}
          </ul>
        {:else}
          {tooltip}
        {/if}
      </div>
      <div class="mt-8 flex justify-end">
        <button 
          class="px-6 py-2.5 bg-slate-900 text-white dark:bg-white dark:text-slate-900 rounded-full hover:bg-slate-800 dark:hover:bg-slate-200 transition-colors font-medium text-sm focus:outline-none shadow-sm"
          onclick={closeModal}
        >
          Cerrar
        </button>
      </div>
    </div>
  </dialog>
