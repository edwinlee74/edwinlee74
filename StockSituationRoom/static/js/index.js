
function update_chart ( stock_no ) {
   $("#id01").css("display", "block");
   $("#myheader").html('股票代號: ' + stock_no);
   $.ajax({
              url: '/api/revenue/' + stock_no,
              type: 'get',
              data: {},
              dataType: 'json',
              success: function (revenue) {
                  myChart.data.datasets[0].data = revenue.thisYear;
                  myChart.data.datasets[1].data = revenue.lastYear; 
                  myChart.update();
              }
    });
};