// JS file
// Function to show the content of the selected option
function showContent(option) {
  // Get all the content divs
  var contents = document.getElementsByClassName("content");
  // Loop through the content divs and hide them
  for (var i = 0; i < contents.length; i++) {
    contents[i].style.display = "none";
  }
  // Show the content of the selected option
  document.getElementById(option).style.display = "block";
}

//Function to submit the form data and get the prediction or feedback
function submitForm(event, option) {
    // Prevent the default form submission behavior
    event.preventDefault();
    // Get the form element
    var form = document.getElementById(option + "-form");
    // Get the result element
    var result = document.getElementById(option + "-result");
    // Create a FormData object from the form data
    var formData = new FormData(form);

    // Fetch the Flask server based on the option (heart, diabetes, lung)
    var url = "/predict/" + option;

    // Fetch the Flask server with the form data as POST parameters
    fetch(url, {
        method: "POST",
        body: formData
    })
    .then(function (response) {
        // Return the response JSON
        return response.json();
    })
    .then(function (json) {
        // Set the result element's innerHTML to the response JSON
        result.innerHTML = JSON.stringify(json);
    })
    .catch(function (error) {
        // Log the error to the console
        console.error(error);
    });
}