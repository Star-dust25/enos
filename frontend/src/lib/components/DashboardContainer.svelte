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

<div
  class="border-4 border-slate-900 dark:border-white rounded-none bg-white dark:bg-[#0a0a0a] shadow-[8px_8px_0px_rgba(0,0,0,1)] dark:shadow-[8px_8px_0px_rgba(255,255,255,1)] mb-12"
>
  <!-- Header -->
  <div
    class="border-b-4 border-slate-900 dark:border-white px-6 sm:px-10 py-6 sm:py-8 bg-slate-50 dark:bg-[#111111] rounded-none"
  >
    <div class="flex items-start sm:items-center">
      <span
        class="font-slab text-2xl md:text-4xl font-black text-slate-900 dark:text-white uppercase tracking-tighter mb-2 sm:mb-0"
      >
        {titulo}
      </span>
      {#if tooltip}
        <div class="ml-4 mt-2 sm:mt-0">
          <button
            onclick={openModal}
            class="w-8 h-8 rounded-none bg-slate-900 dark:bg-white border-2 border-slate-900 dark:border-white text-white dark:text-slate-900 flex items-center justify-center font-bold text-lg hover:bg-slate-700 dark:hover:bg-slate-200 transition-colors focus:outline-none"
            aria-label="Más información"
          >
            ?
          </button>
        </div>
      {/if}
    </div>
    {#if subtitulo}
      <div
        class="text-lg sm:text-xl text-slate-600 dark:text-slate-400 mt-4 font-mono leading-relaxed max-w-4xl"
      >
        {subtitulo}
      </div>
    {/if}
  </div>

  <!-- Body -->
  <div class="p-6 sm:p-10">
    {#if children}
      {@render children()}
    {/if}
  </div>
</div>

  <dialog
    bind:this={dialogEl}
    class="backdrop:bg-slate-900/50 dark:backdrop:bg-[#000000]/80 backdrop:backdrop-blur-sm dark:backdrop:backdrop-blur-none bg-transparent p-4 sm:p-6 m-auto rounded-none overflow-visible max-w-lg w-full"
    onclick={handleBackdropClick}
    oncancel={(e) => { e.preventDefault(); closeModal(); }}
  >
    <div 
      class="bg-white dark:bg-[#0a0a0a] rounded-none w-full max-h-[90vh] overflow-y-auto p-6 sm:p-8 shadow-[8px_8px_0px_rgba(0,0,0,1)] dark:shadow-[8px_8px_0px_rgba(255,255,255,1)] border-4 border-slate-900 dark:border-white cursor-default flex flex-col m-0"
      onclick={(e) => e.stopPropagation()}
      role="document"
    >
      <div class="flex justify-between items-start mb-6 border-b-4 border-slate-900 dark:border-white pb-4">
        <h3 class="font-slab font-black text-2xl uppercase tracking-widest text-slate-900 dark:text-white">Información</h3>
        <button 
          class="text-slate-900 dark:text-white hover:text-slate-700 dark:hover:text-slate-300 transition-colors focus:outline-none flex-shrink-0 ml-4"
          onclick={closeModal}
          aria-label="Cerrar"
        >
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="3" stroke="currentColor" class="w-8 h-8">
            <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
      <div class="text-slate-700 dark:text-slate-300 leading-relaxed font-mono text-base">
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
      <div class="mt-10 flex justify-end">
        <button 
          class="px-8 py-3 bg-slate-900 dark:bg-white text-white dark:text-slate-900 border-4 border-slate-900 dark:border-white rounded-none hover:bg-slate-700 dark:hover:bg-slate-200 transition-colors font-bold uppercase tracking-widest text-sm focus:outline-none"
          onclick={closeModal}
        >
          Cerrar
        </button>
      </div>
    </div>
  </dialog>
