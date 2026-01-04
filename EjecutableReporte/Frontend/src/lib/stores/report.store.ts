import { writable } from 'svelte/store';

export type Channel = 'digital' | 'dialer' | 'all';
export type Brand = 'unitec' | 'uvm';

export type ReportParams = {
    brand: Brand,
    channel: Channel
};

export const reportParams = writable<ReportParams>({
    brand: 'unitec',
    channel: 'digital'
});