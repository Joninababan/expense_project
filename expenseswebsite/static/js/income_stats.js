const renderChart = (data,labels)=>{
    const ctx = document.getElementById('myChart');

    new Chart(ctx, {
        type: 'bar',
        data: {
        labels: labels,
        datasets: [{
            label: 'Last 6 months Incomes',
            data: data,
            borderWidth: 1
        }]
        },
        options: {
            plugins: {
                title: {
                    display: true,
                    text: 'Incomes by Source'
                }
            }
        }
    });
} 

const getChartData=()=>{
    // fetch url not name
    fetch('income-source-summary')
        .then((res) => res.json())
        .then((results) => {
        const source_data = results.income_source_data;
        const [labels, data] = [
            Object.keys(source_data), 
            Object.values(source_data)]
        renderChart(data, labels);
    });
};

document.onload = getChartData();
