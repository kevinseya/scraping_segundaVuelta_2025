// Noticias Sentimientos
const ctxNoticias = document.getElementById('sentimientosNoticiasChart').getContext('2d');
new Chart(ctxNoticias, {
    type: 'pie',
    data: {
        labels: Object.keys(data.sentimientos_noticias),
        datasets: [{
            label: 'Sentimientos Noticias',
            data: Object.values(data.sentimientos_noticias),
            backgroundColor: ['#22c55e', '#ef4444', '#3b82f6']
        }]
    },
    options: { responsive: true }
});

// Twitter Sentimientos
const ctxTweets = document.getElementById('sentimientosTweetsChart').getContext('2d');
new Chart(ctxTweets, {
    type: 'pie',
    data: {
        labels: Object.keys(data.sentimientos_tweets),
        datasets: [{
            label: 'Sentimientos Twitter',
            data: Object.values(data.sentimientos_tweets),
            backgroundColor: ['#10b981', '#f59e0b', '#ef4444', '#3b82f6']
        }]
    },
    options: { responsive: true }
});

// Temas
const ctxTemas = document.getElementById('temasChart').getContext('2d');
new Chart(ctxTemas, {
    type: 'bar',
    data: {
        labels: Object.keys(data.temas),
        datasets: [{
            label: 'Temas',
            data: Object.values(data.temas),
            backgroundColor: '#f59e0b'
        }]
    },
    options: {
        indexAxis: 'y',
        responsive: true,
        scales: { x: { beginAtZero: true } }
    }
});

// Menciones
const ctxMenciones = document.getElementById('mencionesChart').getContext('2d');
new Chart(ctxMenciones, {
    type: 'doughnut',
    data: {
        labels: ['Daniel Noboa', 'Luisa González / Rafael Correa'],
        datasets: [{
            label: 'Menciones',
            data: [data.menciones['Daniel Noboa'], data.menciones['Luisa González / Rafael Correa']],
            backgroundColor: ['#3b82f6', '#ef4444']
        }]
    },
    options: { responsive: true }
});

// Fuentes
const ctxFuentes = document.getElementById('fuentesChart').getContext('2d');
new Chart(ctxFuentes, {
    type: 'bar',
    data: {
        labels: Object.keys(data.fuentes),
        datasets: [{
            label: 'Noticias por Fuente',
            data: Object.values(data.fuentes),
            backgroundColor: '#6366f1'
        }]
    },
    options: {
        responsive: true,
        scales: { y: { beginAtZero: true } }
    }
});

// Conclusión
document.getElementById('conclusion-text').innerText = data.conclusion;

// Últimos Tweets
const tweetsContainer = document.getElementById('tweets-container');
data.ultimos_tweets.forEach(tweet => {
    const div = document.createElement('div');
    div.className = 'p-4 bg-white rounded shadow';
    div.innerHTML = `<p><strong>${tweet.usuario}</strong> - ${new Date(tweet.fecha).toLocaleDateString()}</p><p class="mt-2 text-gray-700">${tweet.contenido}</p>`;
    tweetsContainer.appendChild(div);
});
