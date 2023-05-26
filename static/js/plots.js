// Grab data
let apiTitanic = "/api/v1.0/passengersbyclass";

function init() {
  d3.json(apiTitanic).then(function(data) {
      let filter = "Survived"
      data = data['Survived']
      console.log(data);
      let dataPlot = [{
        x: Object.keys(data),
        y: Object.values(data),
        type: 'bar'
      }]
      Plotly.newPlot("plot", dataPlot);
    });
  }

// Function called by DOM changes
function refreshPlot() {
  let dropdownMenu = d3.select("#selDataset");
  // Assign the value of the dropdown menu option to a letiable
  let filter = dropdownMenu.property("value");
  // Call function to update the chart
  d3.json(apiTitanic).then(function(data) {
    data = data[filter]
    console.log(data);
    let dataPlot = [{
      x: Object.keys(data),
      y: Object.values(data),
      type: 'bar'
    }]
    Plotly.newPlot("plot", dataPlot);
  });
}

// On change to the DOM, call getData()
d3.selectAll("#selDataset").on("change", refreshPlot);

init();
