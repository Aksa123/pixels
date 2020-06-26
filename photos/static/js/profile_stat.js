const stats_data = JSON.parse(document.getElementById('stats-data').textContent);
var days = stats_data.days
var daily_views = stats_data.daily_views
var daily_likes = stats_data.daily_likes
var daily_favorites = stats_data.daily_favorites
var daily_downloads = stats_data.daily_downloads
var dummy = [{x:"2020-05-01", y:20}, {x: "2020-05-02", y:40}]
var aggregate_value_style = document.querySelectorAll(".aggregate-value-style")
var ctx = document.getElementById('myChart');

var myChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: days,
        datasets: [{
            label: 'Views',
            data: daily_views,
            fill: false,
            backgroundColor: "rgba(205, 236, 230, 0.5)",
            borderColor: "rgba(131, 208, 193, 1.0)",
            pointBorderWidth: 5
        },
        {
            label: 'Likes',
            data: daily_likes,
            fill: false,
            backgroundColor: "rgba(255, 224, 230, 0.5)",
            borderColor: "rgba(25, 94, 133, 1.0)",
            pointBorderWidth: 5
        },
        {
            label: 'Favorites',
            data: daily_favorites,
            fill: false,
            backgroundColor: "rgba(255, 224, 230, 0.5)",
            borderColor: "rgba(224, 123, 57, 1.0)",
            pointBorderWidth: 5
        },
        {
            label: 'Downloads',
            data: daily_downloads,
            fill: false,
            backgroundColor: "rgba(115, 252, 3, 0.5)",
            borderColor: "rgba(115, 252, 3, 1.0)",
            pointBorderWidth: 5
        }
        
    ]
    },
    options: {
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero: true,
                    stepSize: 2
                }
            }]
        }
    }
});


for (let i=0; i< aggregate_value_style.length; i++){
    aggregate_value_style[i].innerHTML = parseInt(aggregate_value_style[i].innerHTML).toLocaleString()
}