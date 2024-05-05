function addRoom() {
    const roomNumber = document.getElementById('room-number').value;
    const roomCapacity = document.getElementById('room-capacity').value;
    const rpn = document.getElementById('rate-per-night').value;
    const roomType = document.getElementById('room-type').value;

    const occupancy = 0;




    const roomData = {
        roomNumber: roomNumber,
        roomCapacity: roomCapacity,
        rpn: rpn,
        roomType: roomType,
        occupancy: occupancy,
    };



    $.ajax({
        url: '/add_room',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(roomData),
        success: function (response) {
            $('#response').html(response);
        },
        error: function (error) {
            console.error('Error', error);
            $('#response').html('Error');
        }
    });

    $.ajax({
        url: '/set_housekeeper',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(roomData),
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
        document.getElementById('room-number').value = '';
        document.getElementById('room-capacity').value = '';
        document.getElementById('rate-per-night').value = '';
        document.getElementById('room-type').value = '';
    }


}

function deleteRoom(id) {



    const ID = {
        roomId: id,
    };


    $.ajax({
        url: '/delete_room',
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

function updateRoom(rID, rNumb, capacity, rpn, type) {

    resetForm();
    function resetForm() {
        document.getElementById('room-number').value = rNumb;
        document.getElementById('room-capacity').value = capacity;
        document.getElementById('rate-per-night').value = rpn;
        document.getElementById('room-type').value = type;
    }

    deleteRoom(rID);

}

