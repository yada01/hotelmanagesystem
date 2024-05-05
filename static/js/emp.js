function addEmployee() {
    const firstName = document.getElementById('first-name').value;
    const lastName = document.getElementById('last-name').value;
    const position = document.getElementById('position').value;
    const salary = document.getElementById('salary').value;


    const employeeData = {
        firstName: firstName,
        lastName: lastName,
        position: position,
        salary: salary
    };



    $.ajax({
        url: '/add_employee',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(employeeData),
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
        document.getElementById('first-name').value = '';
        document.getElementById('last-name').value = '';
        document.getElementById('position').value = '';
        document.getElementById('salary').value = '';
    }


}

function deleteEmployee(id) {



    const ID = {
        staffId: id,
    };


    $.ajax({
        url: '/delete_employee',
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

function updateEmployee(uID, fName, lName, position, salary) {

    resetForm();
    function resetForm() {
        document.getElementById('first-name').value = fName;
        document.getElementById('last-name').value = lName;
        document.getElementById('position').value = position;
        document.getElementById('salary').value = salary;
    }

    deleteEmployee(uID);



}

