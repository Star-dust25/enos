<script lang="ts">
  import type { Snippet } from "svelte";
  import { fade, fly } from "svelte/transition";
  import { driver } from "driver.js";
  import "driver.js/dist/driver.css";

  let {
    titulo,
    subtitulo = "",
    tooltip = "",
    tourSteps = [],
    children,
  } = $props<{
    titulo: string;
    subtitulo?: string;
    tooltip?: string | string[];
    tourSteps?: Array<{ element: string; popover: { title: string; description: string; side?: string; align?: string } }>;
    children?: Snippet;
  }>();

  let tourActive = $state(false);
  let currentStep = $state(0);

  function startTour() {
    if (tourSteps && tourSteps.length > 0) {
      const driverObj = driver({
        showProgress: true,
        steps: tourSteps,
        nextBtnText: 'Siguiente &rarr;',
        prevBtnText: '&larr; Anterior',
        doneBtnText: 'Finalizar',
        progressText: 'Paso {{current}} de {{total}}',
        popoverClass: 'driver-theme-apple'
      });
      driverObj.drive();
      return;
    }

    tourActive = true;
    currentStep = 0;
  }

  function nextStep() {
    if (Array.isArray(tooltip) && currentStep < tooltip.length - 1) {
      currentStep++;
    } else {
      endTour();
    }
  }

  function endTour() {
    tourActive = false;
  }
</script>

<div>
  <!-- Header Minimalista -->
  <div class="mb-2 px-2">
    <div class="flex items-start sm:items-center">
      <h2 class="text-2xl font-semibold text-[#1D1D1F] dark:text-white tracking-tight mb-2 sm:mb-0">
        {titulo}
      </h2>
      {#if tooltip || (tourSteps && tourSteps.length > 0)}
        <div class="ml-4 mt-1 sm:mt-0 relative">
          <button
            onclick={startTour}
            class="w-8 h-8 rounded-full bg-[#007AFF]/10 text-[#007AFF] dark:bg-[#007AFF]/20 dark:text-[#007AFF] flex items-center justify-center font-bold text-sm hover:bg-[#007AFF]/20 dark:hover:bg-[#007AFF]/30 transition-colors focus:outline-none"
            aria-label="Más información"
          >
            ?
          </button>

          {#if tourActive}
            <!-- Floating Guided Tour Popover -->
            <div 
              class="absolute top-12 left-0 sm:-left-4 z-50 w-72 sm:w-80 bg-white dark:bg-[#1C1C1E] rounded-3xl shadow-[0_20px_40px_rgba(0,0,0,0.1)] dark:shadow-[0_20px_40px_rgba(0,0,0,0.5)] border border-slate-200/60 dark:border-white/10 p-5 sm:p-6"
              in:fly={{ y: -10, duration: 200 }}
              out:fade={{ duration: 150 }}
            >
               <!-- Flecha indicadora (Triangle) -->
               <div class="absolute -top-2 left-6 w-4 h-4 bg-white dark:bg-[#1C1C1E] rotate-45 border-l border-t border-slate-200/60 dark:border-white/10"></div>
               
               <div class="relative z-10">
                 <div class="flex justify-between items-center mb-4">
                   <span class="text-[11px] font-bold text-[#007AFF] uppercase tracking-widest">
                     Paso {currentStep + 1} de {Array.isArray(tooltip) ? tooltip.length : 1}
                   </span>
                   <button onclick={endTour} class="text-slate-400 hover:text-slate-600 dark:hover:text-white transition-colors focus:outline-none">
                     <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="w-4 h-4">
                       <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
                     </svg>
                   </button>
                 </div>
                 
                 <p class="text-[14px] text-slate-700 dark:text-slate-200 leading-relaxed mb-6 font-medium">
                   {Array.isArray(tooltip) ? tooltip[currentStep] : tooltip}
                 </p>
                 
                 <div class="flex justify-between items-center">
                   <button onclick={endTour} class="text-[12px] text-slate-500 font-semibold hover:text-slate-700 dark:hover:text-slate-300 transition-colors focus:outline-none">
                     Omitir
                   </button>
                   <button onclick={nextStep} class="px-5 py-2.5 bg-[#007AFF] text-white text-[13px] font-semibold rounded-full hover:opacity-90 transition-opacity shadow-sm focus:outline-none">
                     {(Array.isArray(tooltip) && currentStep === tooltip.length - 1) || !Array.isArray(tooltip) ? 'Finalizar' : 'Siguiente'}
                   </button>
                 </div>
               </div>
            </div>
          {/if}
        </div>
      {/if}
    </div>
    {#if subtitulo}
      <p class="text-[15px] text-[#AAAAAA] dark:text-[#AAAAAA] mt-1 leading-relaxed max-w-4xl">
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

  
