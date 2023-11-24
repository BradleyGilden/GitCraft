const ctx = document.querySelector('.board__chart1-pie');
let repoSpace = ctx.parentNode.dataset.repospace;
let availableSpace = ctx.parentNode.dataset.availablespace;

repoSpace = parseInt(repoSpace);
availableSpace = Math.floor(parseInt(availableSpace) / 1000);
const otherSpace = 2000000 - repoSpace - availableSpace;

new Chart(ctx, {
  type: 'doughnut',
  data: {
    labels: ['repositories', 'available', 'other'],
    datasets: [{
      label: 'Space (kb)',
      data: [repoSpace, availableSpace, otherSpace],
      borderWidth: 2,
      backgroundColor: [
        'rgb(4, 217, 61)',
        'rgb(25, 163, 255)',
        'rgb(163, 163, 163)'
      ],
      hoverOffset: 10
    }],
  },
  options: {
    plugins: {
      title: {
        display: true,
        text: 'Account Space',
        color : "black",
        font: {
          family: 'Poppins, sans-serif',
          size: 18
        }
      },
      legend: {
        position: 'bottom',
        labels: {
          color : "black",
          font: {
            family: 'Poppins, sans-serif'
          }
        }
      }
    }
  }
});
