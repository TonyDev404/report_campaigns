/// <reference types="svelte" />
/// <reference types="vite/client" />

declare module '*.svelte' {
    import type {SvelteComponentTyped} from 'svelte';
    export default class Component extends SvelteComponentTyped {}
}

declare module '*.css';