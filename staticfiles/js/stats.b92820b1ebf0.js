const renderChart = (data,labels)=>{
    const ctx = document.getElementById('myChart');

    new Chart(ctx, {
        type: 'bar',
        width:10,
        data: {
        labels: labels,
        datasets: [{
            label: 'Last 6 months Expenses',
            data: data,
            borderWidth: 1
        }]
        },
        options: {
            plugins: {
                title: {
                    display: true,
                    text: 'Expenses by Category'
                }
            }
        }
    });
} 

const getChartData=()=>{
    console.log('tset')
    // fetch url not name
    fetch('expense-category-summary')
        .then((res) => res.json())
        .then((results) => {
        console.log('resultsasd', results);
        const category_data = results.expense_category_data;
        const [labels, data] = [
            Object.keys(category_data), 
            Object.values(category_data)]
        renderChart(data, labels);
    });
};

document.onload = getChartData();
