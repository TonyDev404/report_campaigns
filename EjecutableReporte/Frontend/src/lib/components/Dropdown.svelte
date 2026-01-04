<script context="module" lang="ts">
    export type Option<T extends string> = {
        label: string,
        value: T,
    }
</script>

<script lang="ts">
    import { scale, fade } from "svelte/transition";
    import "../../styles/dropdown.css";
    import { reportParams, type Channel } from '../stores/report.store';

    export let options: Option<any>[];
    export let value: string;

    let open = false;

    function select(option: Option<any>) {
        value = option.value;
        open = false;
    }
</script>

<div class="dropdown">
    <button
        type="button"
        class="trigger"
        onclick={() => (open = !open)}
        aria-expanded={open}
    >
        {options.find(o => o.value === value)?.label ?? "Seleccionar"}
        <span class="arrow" class:open={open}>▾</span>
    </button>

    {#if open}
        <ul
            class="menu"
            in:scale={{ start: 0.95, duration: 120 }}
            out:fade={{ duration: 100 }}
        >
            {#each options as option, i}
                <li>
                    <button
                        type="button"
                        class="option"
                        onclick={() => select(option)}
                    >
                        {option.label}
                    </button>
                </li>
            {/each}
        </ul>
    {/if}
</div>
