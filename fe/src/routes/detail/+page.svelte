<script lang="ts">
	import { onMount } from 'svelte';
	import type { NetworkSample } from '../stores';

	let sample: NetworkSample | null = null;
	let sampleIndex: number = 0;

	function formatNumber(num: number): string {
		return num.toLocaleString(undefined, { maximumFractionDigits: 2 });
	}

	onMount(() => {
		const urlParams = new URLSearchParams(window.location.search);
		const sampleData = urlParams.get('sample');
		const index = urlParams.get('index');
		
		if (sampleData && index) {
			sample = JSON.parse(decodeURIComponent(sampleData));
			sampleIndex = parseInt(index);
		}
	});

	const metricGroups = [
		{
			title: "Basic Information",
			metrics: ['proto', 'service', 'state', 'dur', 'attack_cat', 'label']
		},
		{
			title: "Packet Statistics",
			metrics: ['spkts', 'dpkts', 'sbytes', 'dbytes', 'rate']
		},
		{
			title: "Time and Load",
			metrics: ['sttl', 'dttl', 'sload', 'dload', 'tcprtt', 'synack', 'ackdat']
		},
		{
			title: "Packet Intervals and Jitter",
			metrics: ['sinpkt', 'dinpkt', 'sjit', 'djit']
		},
		{
			title: "Window and TCP Information",
			metrics: ['swin', 'dwin', 'stcpb', 'dtcpb']
		},
		{
			title: "Loss and Mean Values",
			metrics: ['sloss', 'dloss', 'smean', 'dmean']
		},
		{
			title: "Connection Statistics",
			metrics: [
				'trans_depth', 'response_body_len', 'ct_srv_src', 'ct_state_ttl',
				'ct_dst_ltm', 'ct_src_dport_ltm', 'ct_dst_sport_ltm', 'ct_dst_src_ltm',
				'ct_src_ltm', 'ct_srv_dst'
			]
		},
		{
			title: "Additional Flags",
			metrics: ['is_ftp_login', 'ct_ftp_cmd', 'ct_flw_http_mthd', 'is_sm_ips_ports']
		}
	];

    const labelMap = {
        'proto': 'Protocol',
        'service': 'Service',
        'state': 'State',
        'dur': 'Duration',
        'attack_cat': 'Attack Category',
        'label': 'Label',
        'spkts': 'Source Packets',
        'dpkts': 'Destination Packets',
        'sbytes': 'Source Bytes',
        'dbytes': 'Destination Bytes',
        'rate': 'Rate',
        'sttl': 'Source Time to Live',
        'dttl': 'Destination Time to Live',
        'sload': 'Source Load',
        'dload': 'Destination Load',
        'tcprtt': 'TCP Round Trip Time',
        'synack': 'SYN-ACK Packets',
        'ackdat': 'ACK Data',
        'sinpkt': 'Source In-Packets',
        'dinpkt': 'Destination In-Packets',
        'sjit': 'Source Jitter',
        'djit': 'Destination Jitter',
        'swin': 'Source Window',
        'dwin': 'Destination Window',
        'stcpb': 'Source TCP Bytes',
        'dtcpb': 'Destination TCP Bytes',
        'sloss': 'Source Loss',
        'dloss': 'Destination Loss',
        'smean': 'Source Mean',
        'dmean': 'Destination Mean',
        'trans_depth': 'Transaction Depth',
        'response_body_len': 'Response Body Length',
        'ct_srv_src': 'Connection Type (Server Source)',
        'ct_state_ttl': 'Connection Type (State Time to Live)',
        'ct_dst_ltm': 'Connection Type (Destination Last Time)',
        'ct_src_dport_ltm': 'Connection Type (Source Destination Port Last Time)',
        'ct_dst_sport_ltm': 'Connection Type (Destination Source Port Last Time)',
        'ct_dst_src_ltm': 'Connection Type (Destination Source Last Time)',
        'ct_src_ltm': 'Connection Type (Source Last Time)',
        'ct_srv_dst': 'Connection Type (Server Destination)',
        'is_ftp_login': 'Is FTP Login',
        'ct_ftp_cmd': 'Connection Type (FTP Command)',
        'ct_flw_http_mthd': 'Connection Type (Flow HTTP Method)',
        'is_sm_ips_ports': 'Is Small IP or Port'
    }

	function getMetricLabel(metric: string): string {
		return labelMap[metric as keyof typeof labelMap] || metric
	}

	function formatValue(key: string, value: NetworkSample[keyof NetworkSample]): string {
		if (typeof value === 'number') {
			if (key.includes('dur') || key.includes('rtt') || key.includes('synack') || key.includes('ackdat')) {
				return `${formatNumber(value)}s`;
			}
			if (key.includes('rate') || key.includes('load')) {
				return `${formatNumber(value)} B/s`;
			}
			if (key.includes('bytes')) {
				return `${formatNumber(value)} B`;
			}
			return formatNumber(value);
		}
		console.log({key, value})
		if (key.includes('proto') || key.includes('service')) {
			return value.toString().toUpperCase();
		}
		// if (key.includes)
		return value.toString();
	}
</script>

<main class="container">
	<div class="header">
		<a href="/" class="back-button">← Back to Samples</a>
		{#if sample}
			<h1>Sample {sampleIndex} Details</h1>
		{/if}
	</div>

	{#if sample}
		<div class="status-banner" class:attack={sample.label === 1}>
			<strong>Classification:</strong> {sample.attack_cat}
			<span class="label">Label: {sample.label}</span>
		</div>

		{#each metricGroups as group}
			<div class="metric-group">
				<h2>{group.title}</h2>
				<div class="metrics-grid">
					{#each group.metrics as metric}
						<div class="metric-card">
							<div class="metric-label">{getMetricLabel(metric)}</div>
							<div class="metric-value">{formatValue(metric, sample[metric as keyof NetworkSample])}</div>
						</div>
					{/each}
				</div>
			</div>
		{/each}
	{:else}
		<div class="error">
			<p>Sample data not found. Please return to the main page and select a sample.</p>
		</div>
	{/if}
</main>

<style>
	.container {
		max-width: 1200px;
		margin: 0 auto;
		padding: 2rem;
	}

	.header {
		display: flex;
		align-items: center;
		gap: 2rem;
		margin-bottom: 2rem;
	}

	.back-button {
		text-decoration: none;
		color: #4CAF50;
		font-weight: 500;
		padding: 0.5rem 1rem;
		border-radius: 4px;
		border: 1px solid #4CAF50;
		transition: all 0.3s;
	}

	.back-button:hover {
		background-color: #4CAF50;
		color: white;
	}

	h1 {
		margin: 0;
		font-size: 2rem;
		color: #333;
	}

	.status-banner {
		background-color: #e8f5e9;
		padding: 1rem;
		border-radius: 8px;
		margin-bottom: 2rem;
		display: flex;
		align-items: center;
		gap: 1rem;
	}

	.status-banner.attack {
		background-color: #ffebee;
	}

	.label {
		padding: 0.25rem 0.5rem;
		background-color: rgba(0, 0, 0, 0.1);
		border-radius: 4px;
	}

	.metric-group {
		background-color: white;
		border-radius: 8px;
		padding: 1.5rem;
		margin-bottom: 2rem;
		box-shadow: 0 2px 4px rgba(0,0,0,0.1);
	}

	h2 {
		margin: 0 0 1rem 0;
		color: #333;
		font-size: 1.5rem;
	}

	.metrics-grid {
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
		gap: 1rem;
	}

	.metric-card {
		background-color: #f5f5f5;
		padding: 1rem;
		border-radius: 6px;
	}

	.metric-label {
		color: #666;
		font-size: 0.9rem;
		margin-bottom: 0.5rem;
	}

	.metric-value {
		font-size: 1.1rem;
		font-weight: 500;
		color: #333;
	}

	.error {
		text-align: center;
		padding: 2rem;
		background-color: #f5f5f5;
		border-radius: 8px;
		color: #666;
	}
</style> 