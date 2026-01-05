export async function downloadReport(
    brand: string,
    channel: string
) {
    const response = await fetch(
        `/campaigns/export?brand=${brand}&channel=${channel}`,
        {method: 'GET'}
    );

    if (!response.ok) {
        throw new Error('Error al generar el reporte');
    }

    const blob = await response.blob();

    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `campaign_report_${brand}_${channel}.xlsx`;
    a.click();

    window.URL.revokeObjectURL(url);
}