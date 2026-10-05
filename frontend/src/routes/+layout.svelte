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

<div class="min-h-screen flex flex-col bg-[#F5F5F7] dark:bg-black font-sans selection:bg-blue-500 selection:text-white transition-colors duration-300">
  <!-- Navbar Clean Minimalism -->
  <nav class="bg-white/70 dark:bg-[#1C1C1E]/80 backdrop-blur-xl border-b border-slate-200/50 dark:border-white/5 sticky top-0 z-50 transition-all duration-300">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between items-center h-[80px]">
        
        <!-- Logo Clean -->
        <div class="flex items-center">
          <span class="font-bold text-2xl tracking-tight text-apple-dark dark:text-white">
            ENOS
          </span>
        </div>

        <div class="flex items-center gap-4">
          <!-- Desktop Nav -->
          <div class="hidden sm:flex items-center gap-1 h-full">
            {#each navItems as item}
              <a
                href={item.path}
                class="px-5 py-2 text-[14px] font-medium transition-all rounded-full
                  {$page.url.pathname === item.path
                  ? 'bg-apple-blue text-white shadow-sm'
                  : 'text-apple-dark/60 hover:text-apple-dark dark:text-apple-gray dark:hover:text-white hover:bg-slate-100 dark:hover:bg-white/10'}"
              >
                {item.label}
              </a>
            {/each}
          </div>

          <!-- Dark Mode Toggle -->
          <button
            onclick={toggleDarkMode}
            class="p-2 rounded-full text-slate-500 hover:text-slate-900 dark:text-slate-400 dark:hover:text-white hover:bg-slate-100 dark:hover:bg-white/10 transition-all focus:outline-none"
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

    <!-- Mobile Menu Panel -->
    {#if isMobileMenuOpen}
      <div
        class="sm:hidden border-b border-slate-200/50 dark:border-white/5 bg-white/90 dark:bg-[#1C1C1E]/95 backdrop-blur-xl absolute w-full z-40 shadow-sm"
        transition:fly={{ y: -10, duration: 150 }}
      >
        <div class="px-4 py-4 flex flex-col gap-1">
          {#each navItems as item}
            <a
              href={item.path}
              class="block px-6 py-3 text-[15px] font-medium rounded-2xl transition-all
                {$page.url.pathname === item.path
                ? 'bg-apple-blue text-white'
                : 'text-apple-dark/70 dark:text-apple-gray hover:bg-slate-100 dark:hover:bg-white/5'}"
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

  <!-- Footer Clean Minimalism -->
  <footer class="bg-transparent mt-16 py-12 transition-colors duration-300 border-t border-slate-200/50 dark:border-white/5">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
        <div class="max-w-md">
          <span class="inline-block text-slate-900 dark:text-white font-bold text-lg tracking-tight mb-2">ENOS</span>
          <p class="text-[13px] text-slate-500 dark:text-slate-400 leading-relaxed">
            Sistema satelital de alerta temprana ante El Niño Costero.
          </p>
        </div>

        <div class="flex flex-col gap-1 md:text-right">
          <span class="text-[11px] font-medium text-slate-400 uppercase tracking-wide">Desarrollado por</span>
          <p class="text-[14px] font-medium text-slate-800 dark:text-slate-200">
            Diego Alexander Garcia Espinoza
          </p>
          <a href="mailto:stardust.alx25@gmail.com" class="text-[13px] text-blue-500 hover:text-blue-600 dark:text-blue-400 dark:hover:text-blue-300 transition-colors">
            stardust.alx25@gmail.com
          </a>
        </div>
      </div>
    </div>
  </footer>
</div>
