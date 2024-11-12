window.onload = function showAlert() {
    const alertBox = document.getElementById("alert");
    alertBox.style.display = "block"; // Show the alert box
    setTimeout(() => {
        alertBox.style.display = "none"; // Hide the alert box after 1 second
    }, 3000);
}
