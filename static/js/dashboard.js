const dataElement = document.getElementById("dados-grafico");
const canvas = document.getElementById("graficoCategorias");

if (dataElement && canvas && window.Chart) {
    const categoryTotals = JSON.parse(dataElement.textContent);
    const labels = categoryTotals.map((item) => item[0]);
    const values = categoryTotals.map((item) => Number(item[1]));
    const currency = new Intl.NumberFormat("pt-BR", {
        style: "currency",
        currency: "BRL"
    });
    const colors = ["#4b8dff", "#18bd72", "#f1bd28", "#a55eea", "#21bed0", "#ff796c"];

    new Chart(canvas, {
        type: "bar",
        data: {
            labels,
            datasets: [{
                label: "Total por categoria",
                data: values,
                backgroundColor: labels.map((_, index) => colors[index % colors.length]),
                borderRadius: 7,
                borderSkipped: false,
                maxBarThickness: 28
            }]
        },
        options: {
            indexAxis: "y",
            maintainAspectRatio: false,
            responsive: true,
            plugins: {
                legend: { display: false },
                tooltip: {
                    callbacks: {
                        label: (context) => ` ${currency.format(context.raw)}`
                    }
                }
            },
            scales: {
                x: {
                    beginAtZero: true,
                    grid: { color: "rgba(170, 190, 220, 0.10)" },
                    border: { display: false },
                    ticks: {
                        color: "#93a2b8",
                        callback: (value) => currency.format(value)
                    }
                },
                y: {
                    grid: { display: false },
                    border: { display: false },
                    ticks: { color: "#c5d0df" }
                }
            }
        }
    });
}
