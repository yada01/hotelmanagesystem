function getPayment(){
  const phoneNumber = document.getElementById('phone-number').value;

  fetch('/get_room_number_billing', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ phoneNumber: phoneNumber })
  })
    .then(response => response.json())
    .then(data => {
      if (data.length > 0) {
        document.getElementById('room-number').innerHTML = data;
      } else {
        document.getElementById('room-number').innerHTML = 'No such room reserved';
      }
      return fetch('/get_total_amount', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
      });
    })
    .then(response => response.json())
    .then(data => {
      let rpn = data.rate_per_night
      let numberOfDays = Math.abs(data.number_of_days)

      let totalNumber = rpn * numberOfDays


      document.getElementById('total-cost').innerHTML = totalNumber.toString()

    })
    .catch(error => {
      console.error('Error:', error);
    });
}

function addBilling(){
  const totalNumber = document.getElementById('total-cost').innerHTML;
  const phoneNumber = document.getElementById('phone-number').value;
  const amountPaid = document.getElementById('cash').value;
  const amountLeft = amountPaid - totalNumber;

  const billingData = {
    totalNumber: totalNumber,
    amountPaid: amountPaid,
    amountLeft: Math.abs(amountLeft.toString()),
    phoneNumber: phoneNumber
  };


  $.ajax({
    url: '/add_billing',
    type: 'POST',
    contentType: 'application/json',
    data: JSON.stringify(billingData),
    success: function (response) {
      $('#response').html(response);
    },
    error: function (error) {
      console.error('Error', error);
      $('#response').html('Error');
    }
  });
}

function deleteBilling(id) {

  const ID = {
    billingID: id,
  };


  $.ajax({
    url: '/delete_billing',
    type: 'POST',
    contentType: 'application/json',
    data: JSON.stringify(ID),
    success: function (response) {
      $('#response').html(response);
    },
    error: function (error) {
      console.error('Error', error);
      $('#response').html('Error');
    }
  });

  const row = event.target.closest("tr");

  row.remove();
}
