<script lang="ts">
  let email = $state("");
  let status = $state("idle"); // 'idle', 'loading', 'success'

  function handleSubmit(e: Event) {
    e.preventDefault();
    if (!email) return;
    
    status = "loading";
    
    // Aquí iría la llamada POST a tu backend para guardar el correo en DB
    // Por ahora simulamos la carga
    setTimeout(() => {
      status = "success";
      email = "";
      setTimeout(() => {
        status = "idle";
      }, 3000);
    }, 1500);
  }
</script>

<div class="bg-white dark:bg-[#1C1C1E] rounded-3xl p-6 sm:p-8 border border-slate-200/60 dark:border-white/5 shadow-sm mt-8 flex flex-col md:flex-row items-center justify-between gap-6 overflow-hidden relative">
  
  <!-- Overlay "En Desarrollo" -->
  <div class="absolute inset-0 z-30 backdrop-blur-[3px] bg-white/40 dark:bg-black/40 flex items-center justify-center">
    <span class="bg-[#1D1D1F]/90 dark:bg-white/90 text-white dark:text-[#1D1D1F] text-[11px] font-bold uppercase tracking-widest px-4 py-1.5 rounded-full shadow-sm backdrop-blur-md">
      En Desarrollo
    </span>
  </div>

  <!-- Decorative background blob (opcional para darle un toque premium) -->
  <div class="absolute -right-20 -top-20 w-64 h-64 bg-[#007AFF]/5 dark:bg-[#007AFF]/10 rounded-full blur-3xl pointer-events-none"></div>

  <div class="flex-1 text-center md:text-left z-10">
    <div class="flex items-center justify-center md:justify-start gap-2 mb-2">
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-5 h-5 text-[#007AFF]">
        <path stroke-linecap="round" stroke-linejoin="round" d="M14.857 17.082a23.848 23.848 0 005.454-1.31A8.967 8.967 0 0118 9.75v-.7V9A6 6 0 006 9v.75a8.967 8.967 0 01-2.312 6.022c1.733.64 3.56 1.085 5.455 1.31m5.714 0a24.255 24.255 0 01-5.714 0m5.714 0a3 3 0 11-5.714 0M3.124 7.5A8.969 8.969 0 015.292 3m13.416 0a8.969 8.969 0 012.168 4.5" />
      </svg>
      <h3 class="text-xl font-semibold text-[#1D1D1F] dark:text-white tracking-tight">Alertas Tempranas</h3>
    </div>
    <p class="text-[#1D1D1F]/60 dark:text-[#AAAAAA] text-sm max-w-md mx-auto md:mx-0">
      Suscríbete para recibir un correo automático en el instante exacto en que detectemos una anomalía térmica sostenida.
    </p>
  </div>
  
  <div class="w-full md:w-[400px] z-10">
    <form onsubmit={handleSubmit} class="flex items-center w-full relative">
      <input 
        type="email" 
        bind:value={email}
        placeholder="Ingresa tu correo" 
        class="w-full bg-[#F5F5F7] dark:bg-black/40 border border-slate-200/60 dark:border-white/10 text-[#1D1D1F] dark:text-white rounded-full pl-5 pr-32 py-3.5 outline-none focus:border-[#007AFF] dark:focus:border-[#007AFF] transition-all text-sm placeholder:text-[#1D1D1F]/40 dark:placeholder:text-white/30"
        required
        disabled={status === 'loading' || status === 'success'}
      />
      <button 
        type="submit" 
        disabled={status === 'loading' || status === 'success'}
        class="absolute right-1.5 top-1.5 bottom-1.5 bg-[#007AFF] text-white rounded-full px-5 font-medium text-sm hover:bg-[#005bb5] transition-colors disabled:opacity-50 disabled:hover:bg-[#007AFF] flex items-center justify-center min-w-[110px]"
      >
        {#if status === 'loading'}
          <svg class="animate-spin h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
        {:else if status === 'success'}
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="w-4 h-4"><path stroke-linecap="round" stroke-linejoin="round" d="M4.5 12.75l6 6 9-13.5" /></svg>
        {:else}
          Suscribirme
        {/if}
      </button>
    </form>
    {#if status === 'success'}
      <p class="text-emerald-600 dark:text-emerald-400 text-xs mt-3 text-center md:text-left transition-all">
        ¡Excelente! Te avisaremos si hay peligro.
      </p>
    {/if}
  </div>
</div>
