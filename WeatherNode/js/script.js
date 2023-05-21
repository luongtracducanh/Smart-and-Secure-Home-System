$(document).ready(function () {
  $.ajax({
    url: "http://localhost/SWE30011-Assignment3/php/data.php",
    type: "GET",
    success: function (data) {
      let numOfStatement = 11;
      for (let i = 0; i < numOfStatement; i++) {
        console.log(data[i])
      }

      let elements = ["maxTemp", "minTemp", "maxHumid", "minHumid", "avgTemp", "avgHumid", "gasLevel", "alertTemp", "alertHumid", "alertGas"]
      if (!data[i]) {
        for (let i = 0; i < numOfStatement - 5; i++) {
          document.getElementById(elements[i]).innerHTML = 0;
        }
      }
      else {
        for (let i = 0; i < numOfStatement - 5; i++) {
          document.getElementById(elements[i]).innerHTML = data[i + 1][elements[i]];
        }
      }

      try {
        if (data[7][elements[6]] < data[10][elements[9]]) document.getElementById(elements[6]).innerHTML = "Safe";
        else document.getElementById(elements[6]).innerHTML = "Dangerous";
      }
      catch (error) {
        document.getElementById(elements[6]).innerHTML = 0;
      }

      try {
        document.getElementById("alertTemp").defaultValue = data[8][elements[7]];
        document.getElementById("alertHumid").defaultValue = data[9][elements[8]];
        document.getElementById("alertGas").defaultValue = data[10][elements[9]];
      }
      catch (error) {
        document.getElementById("alertTemp").defaultValue = 0;
        document.getElementById("alertHumid").defaultValue = 0;
        document.getElementById("alertGas").defaultValue = 0;
      }

      var id = [];
      var temp = [];
      var humid = [];

      for (var i in data[0]) {
        id.push(data[0][i].ID);
        temp.push(data[0][i].Temperature);
        humid.push(data[0][i].Humidity);
      }

      var tempChartData = {
        labels: id,
        datasets: [
          {
            label: "Temperature (C)",
            fill: false,
            lineTension: 0.1,
            backgroundColor: "rgba(59, 89, 152, 0.75)",
            borderColor: "rgba(59, 89, 152, 1)",
            pointHoverBackgroundColor: "rgba(59, 89, 152, 1)",
            pointHoverBorderColor: "rgba(59, 89, 152, 1)",
            data: temp
          }
        ]
      };

      var humidChartData = {
        labels: id,
        datasets: [
          {
            label: "Humidity (%)",
            fill: false,
            lineTension: 0.1,
            backgroundColor: "rgba(29, 202, 255, 0.75)",
            borderColor: "rgba(29, 202, 255, 1)",
            pointHoverBackgroundColor: "rgba(29, 202, 255, 1)",
            pointHoverBorderColor: "rgba(29, 202, 255, 1)",
            data: humid
          }
        ]
      };

      var ctx = $("#mycanvas");
      var ctx2 = $("#mycanvas2");

      var LineGraph = new Chart(ctx, {
        type: 'line',
        data: tempChartData,
        options: {
          scales: {
            yAxes: [{
              display: true,
              ticks: {
                suggestedMax: 100,
                suggestedMin: 0,    // minimum will be 0, unless there is a lower value.
                // OR //
                beginAtZero: true   // minimum value will be 0.
              }
            }]
          }
        }
      });

      var LineGraph2 = new Chart(ctx2, {
        type: 'line',
        data: humidChartData,
        options: {
          scales: {
            yAxes: [{
              display: true,
              ticks: {
                suggestedMax: 100,
                suggestedMin: 0,    // minimum will be 0, unless there is a lower value.
                // OR //
                beginAtZero: true   // minimum value will be 0.
              }
            }]
          }
        }
      });
    },
    error: function (data) {
      console.log("error");
    }
  });
});