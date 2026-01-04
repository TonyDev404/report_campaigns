<script lang="ts">
    import { reportParams } from "../stores/report.store";
    import { downloadReport } from "../api/campaigns";
    import "../../styles/downloadbutton.css";

    let loading = false;
    let progress = 0;
    let error: string | null = null;
    let timer: number | null = null;

    // Para el efecto de luz que sigue el cursor
    let x = 0;
    let y = 0;

    function handleMove(e: MouseEvent) {
        const rect = (e.currentTarget as HTMLElement).getBoundingClientRect();
        x = e.clientX - rect.left;
        y = e.clientY - rect.top;
    }

    function startProgress() {
        progress = 0;
        timer = window.setInterval(() => {
            if (progress < 90) {
                progress = Math.min(progress + Math.random() * 6, 90);
            }
        }, 200);
    }

    function finishProgress() {
        if (timer) clearInterval(timer);
        progress = 100;

        setTimeout(() => {
            progress = 0;
            loading = false;
        }, 500);
    }

    async function handleDownload() {
        if (loading) return;

        loading = true;
        error = null;
        startProgress();

        try {
            const { brand, channel } = $reportParams;
            await downloadReport(brand, channel);
            finishProgress();
        } catch (e) {
            if (timer) clearInterval(timer);
            progress = 0;
            loading = false;
            error = (e as Error).message || "Failed to fetch";
        }
    }
</script>

<button
    class="neon-btn"
    disabled={loading}
    on:click={handleDownload}
    on:mousemove={handleMove}
    style="--x:{x}px; --y:{y}px;"
>
    <!-- Barra de progreso -->
    <div
        class="progress-bar"
        style="width:{progress}%"
    ></div>

    <!-- Texto -->
    <span class="label">
        {loading ? "Generando reporte..." : "Descargar reporte"}
    </span>
</button>

{#if error}
    <p class="error">{error}</p>
{/if}