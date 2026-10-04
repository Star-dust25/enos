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

<div
  class="min-h-screen flex flex-col bg-[#F8FAFC] dark:bg-[#0a0a0a] font-sans selection:bg-amber-100 selection:text-amber-900 dark:selection:bg-amber-900/50 dark:selection:text-amber-100 overflow-x-hidden transition-colors duration-300"
>
  <!-- Navbar -->
  <nav
    class="bg-white/80 dark:bg-[#0a0a0a]/95 backdrop-blur-lg dark:backdrop-blur-none border-b border-slate-200/60 dark:border-white/10 sticky top-0 z-50 shadow-sm dark:shadow-none transition-colors duration-300"
  >
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between h-16">
        <!-- Logo -->
        <div class="flex-shrink-0 flex items-center gap-2">
          <span
            class="font-slab font-bold text-5xl tracking-tight bg-clip-text text-transparent bg-gradient-to-br from-slate-900 via-slate-800 to-slate-600 dark:from-white dark:via-slate-200 dark:to-slate-400"
            >Pulso</span
          >
        </div>

        <div class="flex items-center gap-2 sm:gap-4">
          <!-- Desktop Nav -->
          <div class="hidden sm:flex sm:space-x-8">
            {#each navItems as item}
              <a
                href={item.path}
                class="relative inline-flex items-center px-2 py-2 text-lg font-medium transition-colors group
                                  {$page.url.pathname === item.path
                  ? 'text-red-600 dark:text-red-400'
                  : 'text-slate-500 hover:text-slate-900 dark:text-slate-400 dark:hover:text-slate-100'}"
              >
                {item.label}
                <!-- Animated Bottom Line Indicator -->
                <span
                  class="absolute bottom-2 left-0 w-full h-[2.5px] rounded-full transform origin-left transition-transform duration-300 ease-out
                  {$page.url.pathname === item.path
                    ? 'bg-red-500 dark:bg-red-400 scale-x-100'
                    : 'bg-slate-300 dark:bg-slate-600 scale-x-0 group-hover:scale-x-100'}"
                ></span>
              </a>
            {/each}
          </div>

          <!-- Dark Mode Toggle -->
          <button
            onclick={toggleDarkMode}
            class="p-2 rounded-full text-slate-500 hover:bg-slate-100 dark:text-slate-400 dark:hover:bg-slate-800 transition-colors focus:outline-none focus:ring-2 focus:ring-inset focus:ring-red-500 dark:focus:ring-red-400"
            aria-label="Toggle dark mode"
          >
            {#if isDarkMode}
              <!-- Sun icon -->
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
                <path stroke-linecap="round" stroke-linejoin="round" d="M12 3v2.25m6.364.386-1.591 1.591M21 12h-2.25m-.386 6.364-1.591-1.591M12 18.75V21m-4.773-4.227-1.591 1.591M5.25 12H3m4.227-4.773L5.636 5.636M15.75 12a3.75 3.75 0 1 1-7.5 0 3.75 3.75 0 0 1 7.5 0Z" />
              </svg>
            {:else}
              <!-- Moon icon -->
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
                <path stroke-linecap="round" stroke-linejoin="round" d="M21.752 15.002A9.72 9.72 0 0 1 18 15.75c-5.385 0-9.75-4.365-9.75-9.75 0-1.33.266-2.597.748-3.752A9.753 9.753 0 0 0 3 11.25C3 16.635 7.365 21 12.75 21a9.753 9.753 0 0 0 9.002-5.998Z" />
              </svg>
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
        class="sm:hidden border-t border-slate-200 dark:border-white/10 bg-white/95 dark:bg-[#0a0a0a] backdrop-blur-lg dark:backdrop-blur-none absolute w-full z-40 shadow-lg"
        transition:fly={{ y: -10, duration: 200 }}
      >
        <div class="px-4 pt-2 pb-4 space-y-1">
          {#each navItems as item}
            <a
              href={item.path}
              class="block px-3 py-3 rounded-md text-base font-medium transition-colors
                {$page.url.pathname === item.path
                ? 'bg-red-50 dark:bg-red-900/20 text-red-600 dark:text-red-400'
                : 'text-slate-600 dark:text-slate-300 hover:text-slate-900 dark:hover:text-white hover:bg-slate-50 dark:hover:bg-slate-800'}"
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

  <!-- Footer -->
  <footer class="bg-slate-50 dark:bg-[#0a0a0a] border-t border-slate-200 dark:border-white/10 mt-16 py-12 transition-colors duration-300">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="grid grid-cols-1 md:grid-cols-12 gap-8 md:gap-12">
        <div class="md:col-span-5">
          <span
            class="font-slab font-bold text-3xl tracking-tight text-slate-800 dark:text-slate-200"
            >Pulso</span
          >
          <p
            class="text-[15px] text-slate-500 dark:text-slate-400 mt-3 leading-relaxed font-light max-w-md"
          >
            Sistema satelital de Alerta Temprana ante El Niño Costero. Monitoreo
            acoplado del precursor térmico oceánico y confirmación territorial.
          </p>
        </div>

        <div class="md:col-span-4 flex flex-col gap-1.5">
          <span class="text-xs font-bold text-slate-400 dark:text-slate-500 tracking-widest uppercase mb-1">Fuentes de Datos</span>
          <p class="text-[13px] text-slate-500 dark:text-slate-400 leading-relaxed">
            NOAA OISST v2.1 (T.S.M.)<br>
            USGS Landsat 8 (MSAVI)<br>
            Mapa de Ecosistemas (GORE Piura)<br>
            INDECI (SINPAD)
          </p>
        </div>

        <div class="md:col-span-3 flex flex-col gap-1.5">
          <span class="text-xs font-bold text-slate-400 dark:text-slate-500 tracking-widest uppercase mb-1">Metodología</span>
          <p class="text-[13px] text-slate-500 dark:text-slate-400 leading-relaxed">
            Categorías del ICEN según ENFEN (2024), Nota Técnica 01-2024.
          </p>
          <p class="text-[13px] font-medium text-slate-600 dark:text-slate-300 mt-auto pt-4">
            Desarrollado para el Perú.
          </p>
        </div>
      </div>
    </div>
  </footer>
</div>
