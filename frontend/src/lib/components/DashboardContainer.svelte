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

  let isModalOpen = $state(false);
</script>

<div
  class="border border-slate-100 dark:border-white/10 rounded-none bg-white dark:bg-[#111111] backdrop-blur-xl dark:backdrop-blur-none shadow-[0_8px_30px_rgb(0,0,0,0.04)] dark:shadow-none mb-8 transition-shadow hover:shadow-[0_8px_30px_rgb(0,0,0,0.08)] dark:shadow-none"
>
  <!-- Header -->
  <div
    class="border-b border-slate-100 dark:border-white/10 px-4 sm:px-8 py-6 sm:py-8 bg-gradient-to-b from-slate-50/50 to-white dark:to-[#111111] dark:from-[#111111] rounded-none"
  >
    <div class="flex items-start sm:items-center">
      <span
        class="font-slab text-xl md:text-3xl font-bold text-slate-900 dark:text-slate-100 tracking-tight mb-2 sm:mb-0"
      >
        {titulo}
      </span>
      {#if tooltip}
        <div class="ml-4 mt-2 sm:mt-0">
          <button
            onclick={() => isModalOpen = true}
            class="w-6 h-6 rounded-none bg-slate-100 dark:bg-[#0a0a0a] border border-slate-200 dark:border-white/10 text-slate-400 flex items-center justify-center font-sans font-bold text-sm hover:bg-slate-200 hover:text-slate-600 dark:text-slate-300 dark:hover:bg-[#1a1a1a] transition-colors focus:outline-none"
            aria-label="Más información"
          >
            ?
          </button>
        </div>
      {/if}
    </div>
    {#if subtitulo}
      <div
        class="text-xl text-slate-600 dark:text-slate-400 mt-4 font-light leading-relaxed max-w-4xl"
      >
        {subtitulo}
      </div>
    {/if}
  </div>

  <!-- Body -->
  <div class="p-4 sm:p-6">
    {#if children}
      {@render children()}
    {/if}
  </div>
</div>

{#if isModalOpen}
  <div 
    class="fixed inset-0 bg-slate-900/50 dark:bg-[#000000]/80 z-50 flex items-center justify-center p-4 backdrop-blur-sm dark:backdrop-blur-none"
    transition:fade={{ duration: 150 }}
    onclick={() => isModalOpen = false}
    role="button"
    tabindex="0"
    onkeydown={(e) => e.key === 'Escape' && (isModalOpen = false)}
  >
    <div 
      class="bg-white dark:bg-[#111111] rounded-none max-w-lg w-full p-6 sm:p-8 shadow-xl dark:shadow-none border border-slate-100 dark:border-white/10 cursor-default"
      transition:fly={{ y: 20, duration: 200 }}
      onclick={(e) => e.stopPropagation()}
      role="dialog"
      aria-modal="true"
    >
      <div class="flex justify-between items-start mb-4">
        <h3 class="font-slab font-bold text-xl text-slate-900 dark:text-slate-100">Información</h3>
        <button 
          class="text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 transition-colors focus:outline-none"
          onclick={() => isModalOpen = false}
          aria-label="Cerrar"
        >
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-6 h-6">
            <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
      <div class="text-slate-600 dark:text-slate-400 leading-relaxed font-light text-base">
        {#if Array.isArray(tooltip)}
          <ul class="list-disc pl-5 space-y-2">
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
          class="px-5 py-2.5 bg-slate-100 dark:bg-[#0a0a0a] text-slate-700 dark:text-slate-300 border border-transparent dark:border-white/10 rounded-none hover:bg-slate-200 dark:hover:bg-[#1a1a1a] transition-colors font-medium text-sm focus:outline-none"
          onclick={() => isModalOpen = false}
        >
          Cerrar
        </button>
      </div>
    </div>
  </div>
{/if}
