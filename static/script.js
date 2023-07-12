function openEditForm(userName, userPass ,userType ) {


    // Set the values in the edit form
    document.getElementById('edit-name').value = userName;
    document.getElementById('edit-pass').value = userPass;
    try {document.getElementById('edit-type').value = userType;
}
    catch{
        
    }
    
    // Display the edit form
    document.querySelector('.edit-form-container').style.display = 'block';
}

function closeEditForm() {
    // Hide the edit form with a fade-out animation
    var editFormContainer = document.querySelector('.edit-form-container');
    editFormContainer.style.animation = 'fade-out 0.3s ease-in-out';
    setTimeout(function() {
        editFormContainer.style.display = 'none';
        editFormContainer.style.animation = '';
    }, 300);
}



function addItemToInventory() {
    document.querySelector('.edit-form-container').style.display = 'block';
}
