<script lang="ts">
	import { onMount } from 'svelte';
	import { samplesStore, sampleCountStore, type NetworkSample } from './stores';

	let samples: NetworkSample[] = [];
	let loading = false;
	let sampleCount = 10;

	// Subscribe to store changes
	samplesStore.subscribe(value => {
		samples = value;
	});

	sampleCountStore.subscribe(value => {
		sampleCount = value;
	});

	async function generateNewSamples() {
		loading = true;
		try {
			const response = await fetch(`http://127.0.0.1:5000/run?count=${sampleCount}`);
			const newSamples: NetworkSample[] = await response.json();
			samplesStore.set(newSamples);
		} catch (error) {
			console.error('Error fetching samples:', error);
		}
		loading = false;
	}

	function formatNumber(num: number): string {
		return num.toLocaleString(undefined, { maximumFractionDigits: 2 });
	}

	function getSampleUrl(sample: NetworkSample, index: number): string {
		const sampleData = encodeURIComponent(JSON.stringify(sample));
		return `/detail?sample=${sampleData}&index=${index + 1}`;
	}

	function handleSampleCountChange(event: Event) {
		const newCount = parseInt((event.target as HTMLSelectElement).value);
		sampleCountStore.set(newCount);
	}
</script>

<svelte:head>
	<title>Network Traffic Generator</title>
	<meta name="description" content="Network Traffic Generation Model Demo" />
</svelte:head>

<main class="container">
	<h1>Network Traffic Generator</h1>
	
	<div class="controls">
		<div class="select-container">
			<label for="sampleCount">Number of Samples:</label>
			<select 
				id="sampleCount" 
				value={sampleCount} 
				on:change={handleSampleCountChange}
				disabled={loading}
			>
				<option value={10}>10 samples</option>
				<option value={20}>20 samples</option>
				<option value={50}>50 samples</option>
				<option value={100}>100 samples</option>
				<option value={1000}>1000 samples</option>
			</select>
		</div>
		<button on:click={generateNewSamples} disabled={loading}>
			{loading ? 'Generating...' : 'Generate New Samples'}
		</button>
	</div>

	{#if loading}
		<div class="loading-container">
			<div class="spinner"></div>
			<p>Generating {sampleCount} samples...</p>
		</div>
	{:else if samples.length > 0}
		<div class="samples-container">
			{#each samples as sample, i}
				<div class="sample-card">
					<h3>Sample {i + 1}</h3>
					<div class="sample-grid">
						<div class="metric">
							<strong>Protocol:</strong> {sample.proto.toUpperCase()}
						</div>
						<div class="metric">
							<strong>Service:</strong> {sample.service.toUpperCase()}
						</div>
						<div class="metric">
							<strong>State:</strong> {sample.state}
						</div>
						<div class="metric">
							<strong>Duration:</strong> {formatNumber(sample.dur)}s
						</div>
						<div class="metric">
							<strong>Packets:</strong> ↑{sample.spkts} ↓{sample.dpkts}
						</div>
						<div class="metric">
							<strong>Bytes:</strong> ↑{formatNumber(sample.sbytes)} ↓{formatNumber(sample.dbytes)}
						</div>
						<div class="metric">
							<strong>Rate:</strong> {formatNumber(sample.rate)} B/s
						</div>
						<div class="metric">
							<strong>Load:</strong> ↑{formatNumber(sample.sload)} ↓{formatNumber(sample.dload)} B/s
						</div>
					</div>
					<div class="label-info" class:attack={sample.label === 1}>
						<strong>Classification:</strong> {sample.attack_cat} (Label: {sample.label})
					</div>
					<a href={getSampleUrl(sample, i)} class="view-details">Click to view all details →</a>
				</div>
			{/each}
		</div>
	{:else}
		<div class="no-data">
			Click "Generate New Samples" to see network traffic data
		</div>
	{/if}
</main>

<style>
	.container {
		max-width: 1200px;
		margin: 0 auto;
		padding: 2rem;
	}

	h1 {
		text-align: center;
		margin-bottom: 2rem;
	}

	.controls {
		text-align: center;
		margin-bottom: 2rem;
		display: flex;
		gap: 1rem;
		justify-content: center;
		align-items: center;
	}

	.select-container {
		display: flex;
		gap: 0.5rem;
		align-items: center;
	}

	select {
		padding: 0.5rem;
		font-size: 1rem;
		border-radius: 4px;
		border: 1px solid #ccc;
		background-color: white;
		cursor: pointer;
	}

	select:hover {
		border-color: #999;
	}

	label {
		font-weight: 500;
	}

	button {
		padding: 0.8rem 1.5rem;
		font-size: 1.1rem;
		background-color: #4CAF50;
		color: white;
		border: none;
		border-radius: 4px;
		cursor: pointer;
		transition: background-color 0.3s;
	}

	button:hover {
		background-color: #45a049;
	}

	button:disabled {
		background-color: #cccccc;
		cursor: not-allowed;
	}

	.samples-container {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
		gap: 1.5rem;
	}

	.sample-card {
		background-color: #f5f5f5;
		border-radius: 8px;
		padding: 1.5rem;
		box-shadow: 0 2px 4px rgba(0,0,0,0.1);
		cursor: pointer;
		transition: transform 0.2s, box-shadow 0.2s;
		text-decoration: none;
		color: inherit;
		display: block;
	}

	.sample-card:hover {
		transform: translateY(-2px);
		box-shadow: 0 4px 8px rgba(0,0,0,0.15);
	}

	.sample-grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
		gap: 1rem;
		margin-bottom: 1rem;
	}

	.metric {
		font-size: 0.9rem;
	}

	.label-info {
		padding: 0.5rem;
		border-radius: 4px;
		background-color: #e8f5e9;
		text-align: center;
	}

	.label-info.attack {
		background-color: #ffebee;
	}

	.no-data {
		text-align: center;
		grid-column: 1 / -1;
		padding: 2rem;
		background-color: #f5f5f5;
		border-radius: 8px;
	}

	strong {
		color: #333;
	}

	.loading-container {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		padding: 3rem;
		text-align: center;
	}

	.spinner {
		width: 50px;
		height: 50px;
		border: 5px solid #f3f3f3;
		border-top: 5px solid #4CAF50;
		border-radius: 50%;
		animation: spin 1s linear infinite;
		margin-bottom: 1rem;
	}

	@keyframes spin {
		0% { transform: rotate(0deg); }
		100% { transform: rotate(360deg); }
	}

	.loading-container p {
		color: #666;
		font-size: 1.1rem;
		margin: 0;
	}

	select:disabled {
		opacity: 0.7;
		cursor: not-allowed;
	}

	button:disabled {
		background-color: #cccccc;
		cursor: not-allowed;
	}

	.view-details {
		margin-top: 1rem;
		text-align: right;
		color: #4CAF50;
		font-size: 0.9rem;
		font-weight: 500;
	}
</style>
