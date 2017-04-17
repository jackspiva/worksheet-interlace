var createBarGraph = function(labels, data, id) {
    var ctx = document.getElementById(id);

    var myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels,
            datasets: [{
                backgroundColor: poolColors(data.length),
                data
            }]
        },
        options: {
            legend: {
                display: false,
                labels: {
                    display: false
                }
            }
        }
    });
    return myChart;
};
var poolColors = function(a) {
    var pool = [];
    for (i = 0; i < a; i++) {
        pool.push(dynamicColors());
    }
    return pool;
};
var dynamicColors = function() {
    var r = Math.floor(Math.random() * 255);
    var g = Math.floor(Math.random() * 255);
    var b = Math.floor(Math.random() * 255);
    return "rgb(" + r + "," + g + "," + b + ")";
};
