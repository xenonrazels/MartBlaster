
// // function getCookie(name) {
// //   var cookieValue = null;
// //   if (document.cookie && document.cookie !== '') {
// //       var cookies = document.cookie.split(';');
// //       for (var i = 0; i < cookies.length; i++) {
// //           var cookie = cookies[i].trim();
// //           if (cookie.substring(0, name.length + 1) === (name + '=')) {
// //               cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
// //               break;
// //           }
// //       }
// //   }
// //   return cookieValue;
// // }

// // // Function to update cart count
// // function updateCartCount() {
// //   // Get the cart count from the cookie
// //   var cartCount = getCookie("cart_count");
// //   console.log(cartCount)

// //   if (cartCount) {

// //     document.querySelector('#cart-count').textContent = cartCount;
// //   }
// // }
// Get the button that opens the modal
document.addEventListener("DOMContentLoaded", function () {
  var btn = document.getElementById("capture_image");
  var span = document.getElementById("close_icon");
  var modal = document.getElementById("upload_model");

  btn.onclick = function(e) {
    e.preventDefault();
    modal.classList.remove("hidden");
  };

  span.onclick = function() {
    modal.classList.add("hidden");
  };

  window.onclick = function(event) {
    if (event.target == modal) {
      modal.classList.add("hidden");
    }
  };
  setTimeout(function() {
    var messagesDiv = document.getElementById('messages');
    messagesDiv.classList.add('opacity-0', 'transition-opacity', 'duration-500');
    setTimeout(function() {
      messagesDiv.style.display = 'none';
    }, 500);
  }, 5000);
  window.onclick = function(event) {
    if (event.target == modal) {
      modal.classList.add("hidden");
    }
  };

  var dismissButtons = document.querySelectorAll('#messages [data-dismiss="alert"]');
  for (var i = 0; i < dismissButtons.length; i++) {
    dismissButtons[i].addEventListener('click', function() {
      var alertDiv = this.closest('.alert');
      alertDiv.classList.add('opacity-0', 'transition-opacity', 'duration-500');
      setTimeout(function() {
        alertDiv.style.display = 'none';
      }, 500);
    });
  }

 });


 
