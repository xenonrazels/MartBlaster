
// Get the button that opens the modal
var btn = document.getElementById("capture_image");

// Get the <span> element that closes the modal
var span = document.getElementById("close_icon");
var modal = document.getElementById("upload_model");
console.log(modal)
// When the user clicks the button, open the modal 
btn.onclick = function (e) {
   
    e.preventDefault();
    modal.classList.remove('hidden');
}
// When the user clicks on <span> (x), close the modal
span.onclick = function() {
    modal.classList.add('hidden');
  }

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
      modal.classList.add('hidden');
  }
}

