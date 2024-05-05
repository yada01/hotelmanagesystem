function addReserve() {
  const guestName = document.getElementById('name').value;
  const phoneNumber = document.getElementById('phone').value;
  const checkIn = document.getElementById('check-in').value;
  const checkOut = document.getElementById('check-out').value;
  const numberOfGuests = document.getElementById('number_of_guests').value;

  const reserveData = {
    guestName: guestName,
    phoneNumber: phoneNumber,
    checkIn: checkIn,
    checkOut: checkOut,
    numberOfGuests: numberOfGuests
  };



  $.ajax({
    url: '/add_reserve',
    type: 'POST',
    contentType: 'application/json',
    data: JSON.stringify(reserveData),
    success: function (response) {
      $('#response').html(response);
    },
    error: function (error) {
      console.error('Error', error);
      $('#response').html('Error');
    }
  });

  resetForm();
  function resetForm() {
    document.getElementById('name').value = '';
    document.getElementById('phone').value = '';
    document.getElementById('check-in').value = '';
    document.getElementById('check-out').value = '';
    document.getElementById('number_of_guests').value = '';
  }


}

function setRoomNumber() {
  let numberOfGuests = Number(document.getElementById('number_of_guests').value);

  if (numberOfGuests === 3) {
    numberOfGuests = 4;
  }

  fetch('/get_room_number', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ capacity: numberOfGuests })
  })
    .then(response => response.json())
    .then(data => {
      if (data.length > 0) {
        document.getElementById('room-number').innerHTML = data[0];
        fetchRoomRate(data[0]);
      } else {
        document.getElementById('room-number').innerHTML = 'No room exists for this number of guests';
      }
    })
    .catch(error => {
      console.error('Error fetching room number:', error);
      $('#response').html('Error');
    });
}

function fetchRoomRate(roomNumber) {
  fetch('/get_rpn', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ roomNumber })
  })
    .then(response => response.json())
    .then(data => {
      document.getElementById('ppn').innerHTML = "$" + data[0];
    })
    .catch(error => {
      console.error('Error fetching RPN:', error);
    });
}

function deleteReserve(id) {

  const ID = {
    reserveID: id,
  };


  $.ajax({
    url: '/delete_reserve',
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

function updateReserve(rID, gName, pNumber, ciDate, coDate, noGuests) {

  resetForm();
  function resetForm() {
    document.getElementById('name').value = gName;
    document.getElementById('phone').value = pNumber;
    document.getElementById('check-in').value = ciDate;
    document.getElementById('check-out').value = coDate;
    document.getElementById('number_of_guests').value = noGuests;
  }

  deleteRoom(rID);

}



