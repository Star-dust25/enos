<script lang="ts">
  import "./layout.css";
  import { page } from "$app/stores";
  import { fly } from "svelte/transition";
  import { onMount } from "svelte";
  import type { Snippet } from "svelte";

  let { children } = $props<{ children: Snippet }>();

  let isMobileMenuOpen = $state(false);
  let isDarkMode = $state(false);

  onMount(() => {
    isDarkMode = document.documentElement.classList.contains('dark');
  });

  function toggleDarkMode() {
    isDarkMode = !isDarkMode;
    if (isDarkMode) {
      document.documentElement.classList.add('dark');
      localStorage.theme = 'dark';
    } else {
      document.documentElement.classList.remove('dark');
      localStorage.theme = 'light';
    }
  }

  $effect(() => {
    // Cerrar el menú al cambiar de ruta
    $page.url.pathname;
    isMobileMenuOpen = false;
  });

  // Navigation routes
  const navItems = [
    { path: "/", label: "Resumen" },
    { path: "/monitoreo", label: "Monitoreo Satelital" },
    { path: "/backtest", label: "Backtest" },
    { path: "/impacto", label: "Validación" },
  ];
</script>

<div class="min-h-screen flex flex-col bg-[#F4F4F4] dark:bg-[#0a0a0a] font-sans selection:bg-peru-red selection:text-white transition-colors duration-300">
  <!-- Navbar Glassmorphism -->
  <nav class="bg-white/70 dark:bg-slate-900/70 backdrop-blur-md border-b border-white/40 dark:border-white/10 shadow-sm sticky top-0 z-50 transition-all duration-300">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between items-center h-[72px]">
        
        <!-- Logo Glass/Gradient -->
        <div class="flex items-center">
          <span class="bg-clip-text text-transparent bg-gradient-to-r from-peru-red to-rose-500 font-slab font-black text-3xl tracking-tighter uppercase drop-shadow-sm">
            ENOS
          </span>
        </div>

        <div class="flex items-center gap-4">
          <!-- Desktop Nav (Pills) -->
          <div class="hidden sm:flex items-center gap-2 h-full">
            {#each navItems as item}
              <a
                href={item.path}
                class="px-5 py-2 text-[12px] font-bold uppercase tracking-[0.1em] transition-all rounded-full
                  {$page.url.pathname === item.path
                  ? 'bg-peru-red text-white shadow-[0_4px_10px_rgba(200,16,46,0.3)]'
                  : 'text-slate-600 dark:text-slate-300 hover:bg-slate-200/50 dark:hover:bg-white/10 hover:text-peru-red dark:hover:text-white'}"
              >
                {item.label}
              </a>
            {/each}
          </div>

          <!-- Dark Mode Toggle -->
          <button
            onclick={toggleDarkMode}
            class="p-2.5 rounded-full bg-white/60 dark:bg-slate-800/60 border border-slate-200 dark:border-white/10 text-slate-700 dark:text-slate-300 hover:bg-white dark:hover:bg-slate-700 hover:shadow-md transition-all focus:outline-none"
            aria-label="Toggle dark mode"
          >
            {#if isDarkMode}
              <!-- Sun icon -->
              <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 24 24" class="w-5 h-5"><path d="M12 2.25a.75.75 0 0 1 .75.75v2.25a.75.75 0 0 1-1.5 0V3a.75.75 0 0 1 .75-.75ZM7.5 12a4.5 4.5 0 1 1 9 0 4.5 4.5 0 0 1-9 0ZM18.894 6.166a.75.75 0 0 0-1.06-1.06l-1.591 1.59a.75.75 0 1 0 1.06 1.061l1.591-1.59ZM21.75 12a.75.75 0 0 1-.75.75h-2.25a.75.75 0 0 1 0-1.5H21a.75.75 0 0 1 .75.75ZM17.834 18.894a.75.75 0 0 0 1.06-1.06l-1.59-1.591a.75.75 0 1 0-1.061 1.06l1.59 1.591ZM12 18a.75.75 0 0 1 .75.75V21a.75.75 0 0 1-1.5 0v-2.25A.75.75 0 0 1 12 18ZM7.758 17.303a.75.75 0 0 0-1.061-1.06l-1.591 1.59a.75.75 0 0 0 1.06 1.061l1.591-1.59ZM6 12a.75.75 0 0 1-.75.75H3a.75.75 0 0 1 0-1.5h2.25A.75.75 0 0 1 6 12ZM6.697 7.757a.75.75 0 0 0 1.06-1.06l-1.59-1.591a.75.75 0 0 0-1.061 1.06l1.59 1.591Z" /></svg>
            {:else}
              <!-- Moon icon -->
              <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 24 24" class="w-5 h-5"><path fill-rule="evenodd" d="M9.528 1.718a.75.75 0 0 1 .162.819A8.97 8.97 0 0 0 9 6a9 9 0 0 0 9 9 8.97 8.97 0 0 0 3.463-.69.75.75 0 0 1 .981.98 10.503 10.503 0 0 1-9.694 6.46c-5.799 0-10.5-4.701-10.5-10.5 0-4.368 2.667-8.112 6.46-9.694a.75.75 0 0 1 .818.162Z" clip-rule="evenodd" /></svg>
            {/if}
          </button>

          <!-- Mobile Menu Button -->
          <div class="flex items-center sm:hidden">
            <button
              type="button"
              class="inline-flex items-center justify-center p-2 rounded-md text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-100 hover:bg-slate-100 dark:hover:bg-slate-800 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-red-500 transition-colors"
              onclick={() => (isMobileMenuOpen = !isMobileMenuOpen)}
              aria-expanded={isMobileMenuOpen}
            >
              <span class="sr-only">Open main menu</span>
              {#if isMobileMenuOpen}
                <svg
                  class="block h-6 w-6"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                  aria-hidden="true"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M6 18L18 6M6 6l12 12"
                  />
                </svg>
              {:else}
                <svg
                  class="block h-6 w-6"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                  aria-hidden="true"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M4 6h16M4 12h16M4 18h16"
                  />
                </svg>
              {/if}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Mobile Menu Panel Glassmorphism -->
    {#if isMobileMenuOpen}
      <div
        class="sm:hidden border-b border-white/20 bg-white/80 dark:bg-slate-900/80 backdrop-blur-xl absolute w-full z-40 shadow-lg"
        transition:fly={{ y: -10, duration: 150 }}
      >
        <div class="px-4 py-4 flex flex-col gap-2">
          {#each navItems as item}
            <a
              href={item.path}
              class="block px-6 py-4 text-sm font-bold uppercase tracking-widest rounded-xl transition-all
                {$page.url.pathname === item.path
                ? 'bg-peru-red/10 text-peru-red dark:bg-peru-red/20 dark:text-red-400'
                : 'text-slate-700 dark:text-slate-300 hover:bg-slate-100/50 dark:hover:bg-white/5'}"
              onclick={() => (isMobileMenuOpen = false)}
            >
              {item.label}
            </a>
          {/each}
        </div>
      </div>
    {/if}
  </nav>

  <!-- Main Content -->
  <main class="flex-grow">
    {@render children()}
  </main>

  <!-- Footer Flat/Brutalist -->
  <footer class="bg-white dark:bg-[#0a0a0a] border-t-4 border-slate-900 dark:border-white mt-16 py-12 transition-colors duration-300">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex flex-col md:flex-row items-start md:items-center justify-between gap-8">
        <div class="max-w-md">
          <span class="inline-block bg-peru-red text-white px-3 py-1 font-slab font-black text-xl tracking-tighter uppercase mb-3">ENOS</span>
          <p class="text-[13px] text-slate-600 dark:text-slate-400 font-mono leading-relaxed">
            SISTEMA SATELITAL DE ALERTA TEMPRANA ANTE EL NIÑO COSTERO.
          </p>
        </div>

        <div class="flex flex-col gap-1 md:text-right border-l-4 border-peru-red pl-4 md:border-l-0 md:pl-0 md:border-r-4 md:pr-4">
          <span class="text-[10px] font-black text-slate-400 dark:text-slate-500 tracking-[0.2em] uppercase">Desarrollado por</span>
          <p class="text-sm font-bold text-slate-900 dark:text-white uppercase tracking-wider">
            Diego Alexander Garcia Espinoza
          </p>
          <a href="mailto:stardust.alx25@gmail.com" class="text-xs font-mono text-peru-red dark:text-peru-red hover:text-slate-900 dark:hover:text-white transition-colors">
            stardust.alx25@gmail.com
          </a>
        </div>
      </div>
    </div>
  </footer>
</div>
