<script lang="ts">
    import Dropdown from "./lib/components/Dropdown.svelte";
    import DownloadButton from "./lib/components/Button.svelte";
    import {
        reportParams,
        type Channel,
        type Brand,
    } from "./lib/stores/report.store";
    import "./styles/global.css";

    const brandOptions: { label: string; value: Brand }[] =
        [
            { label: "UNITEC", value: "unitec" },
            { label: "UVM", value: "uvm" },
        ];

    const channelOptions: {
        label: string;
        value: Channel;
    }[] = [
        // { label: "Todos", value: "all" },
        { label: "Digital", value: "digital" },
        { label: "Dialer", value: "dialer" },
    ];
</script>

<main class="page">
    <h1>Reporte de Campañas</h1>

    <div class="panel">
        <label>
            Marca
            <Dropdown
                options={brandOptions}
                bind:value={$reportParams.brand}
            />
        </label>

        <label>
            Canal
            <Dropdown
                options={channelOptions}
                bind:value={$reportParams.channel}
            />
        </label>

        {#if $reportParams.channel === "all"}
            <small
                style="opacity:0.8; display:block; margin-top:0.25rem"
            >
                El reporte de todos los canales puede tardar
                unos minutos.
            </small>
        {/if}

        <DownloadButton />
    </div>
</main>

<style>
    .page {
        min-height: 100vh;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }

    h1 {
        margin-bottom: 2rem;
        font-size: 2rem;
        letter-spacing: 0.5px;
    }

    .panel {
        display: flex;
        flex-direction: column;
        gap: 1.2rem;
        width: 100%;
        max-width: 420px;
        align-items: center;
        text-align: ve;
    }

    label {
        display: flex;
        flex-direction: column;
        gap: 0.35rem;
        font-weight: 500;
    }

</style>
