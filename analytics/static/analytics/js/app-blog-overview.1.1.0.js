/*
 |--------------------------------------------------------------------------
 | Shards Dashboards: Blog Overview Template
 |--------------------------------------------------------------------------
 */

'use strict';


//
(function ($) {
  $(document).ready(function () {

    // Blog overview date range init.
    $('#blog-overview-date-range').datepicker({});

    //
    // Small Stats
    //

    // Datasets
    var boSmallStatsDatasets = [
      {
        backgroundColor: 'rgba(0, 184, 216, 0.1)',
        borderColor: 'rgb(0, 184, 216)',
        data: [1, 2, 1, 3, 5, 4, 7],
      },
      {
        backgroundColor: 'rgba(23,198,113,0.1)',
        borderColor: 'rgb(23,198,113)',
        data: [1, 2, 3, 3, 3, 4, 4]
      },
      {
        backgroundColor: 'rgba(255,180,0,0.1)',
        borderColor: 'rgb(255,180,0)',
        data: [2, 3, 3, 3, 4, 3, 3]
      },
      {
        backgroundColor: 'rgba(255,65,105,0.1)',
        borderColor: 'rgb(255,65,105)',
        data: [1, 7, 1, 3, 1, 4, 8]
      },
      {
        backgroundColor: 'rgb(0,123,255,0.1)',
        borderColor: 'rgb(0,123,255)',
        data: [3, 2, 3, 2, 4, 5, 4]
      }
    ];

    // Options
    function boSmallStatsOptions(max) {
      return {
        maintainAspectRatio: true,
        responsive: true,
        // Uncomment the following line in order to disable the animations.
        // animation: false,
        legend: {
          display: false
        },
        tooltips: {
          enabled: false,
          custom: false
        },
        elements: {
          point: {
            radius: 0
          },
          line: {
            tension: 0.3
          }
        },
        scales: {
          xAxes: [{
            gridLines: false,
            scaleLabel: false,
            ticks: {
              display: false
            }
          }],
          yAxes: [{
            gridLines: false,
            scaleLabel: false,
            ticks: {
              display: false,
              // Avoid getting the graph line cut of at the top of the canvas.
              // Chart.js bug link: https://github.com/chartjs/Chart.js/issues/4790
              suggestedMax: max
            }
          }],
        },
      };
    }

    // Generate the small charts
    boSmallStatsDatasets.map(function (el, index) {
      var chartOptions = boSmallStatsOptions(Math.max.apply(Math, el.data) + 1);
      var ctx = document.getElementsByClassName('blog-overview-stats-small-' + (index + 1));
      new Chart(ctx, {
        type: 'line',
        data: {
          labels: ["Label 1", "Label 2", "Label 3", "Label 4", "Label 5", "Label 6", "Label 7"],
          datasets: [{
            label: 'Today',
            fill: 'start',
            data: el.data,
            backgroundColor: el.backgroundColor,
            borderColor: el.borderColor,
            borderWidth: 1.5,
          }]
        },
        options: chartOptions
      });
    });


    // Get data 
    var worldIdList = JSON.parse(document.getElementById('world-id-list').textContent);
    
    // Options
    var options = {
      legend: {
        position: 'bottom',
        labels: {
          padding: 25,
          boxWidth: 20
        }
      },
      cutoutPercentage: 0,
      // Uncomment the following line in order to disable the animations.
      // animation: false,
      tooltips: {
        custom: false,
        mode: 'index',
        position: 'nearest'
      }
    };
    
    // Portion Chart
    for (var ele of worldIdList) {
      var portionObject = JSON.parse(document.getElementById(ele+'-portion').textContent);
      var portionData = {
        datasets: [{
          hoverBorderColor: '#ffffff',
          data: [portionObject['done'], portionObject['doing'], portionObject['not']],
          backgroundColor: [
            'rgba(23, 198, 113, 0.9)',
            'rgba(255, 180, 0, 0.9)',
            'rgba(196, 24, 60, 0.9)'
          ]
        }],
        labels: ["Finished", "In Progress", "Not Started"]
      };

      var chartElement = document.getElementById(ele+'-portion-chart');
      new Chart(chartElement, {
        type: 'pie',
        data: portionData,
        options: options,
      });
    }

    for (var ele of worldIdList) {
      var correctObject = JSON.parse(document.getElementById(ele+'-correct').textContent);
      var correctData = {
        datasets: [{
          hoverBorderColor: '#ffffff',
          data: [correctObject['correct'], correctObject['incorrect']],
          backgroundColor: [
            'rgba(23, 198, 113, 0.9)',
            'rgba(196, 24, 60, 0.9)'
          ]
        }],
        labels: ["Correct Answer", "Incorrect Answer"]
      };

      var chartElement = document.getElementById(ele+'-correct-chart');
      new Chart(chartElement, {
        type: 'pie',
        data: correctData,
        options: options,
      });
    }


  });
})(jQuery);

