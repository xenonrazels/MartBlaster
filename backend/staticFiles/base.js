
function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
          var cookie = cookies[i].trim();
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}

// Function to update cart count
function updateCartCount() {
  // Get the cart count from the cookie
  var cartCount = getCookie("cart_count");
  console.log(cartCount)

  if (cartCount) {

    document.querySelector('#cart-count').textContent = cartCount;
  }
}
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

  document.addEventListener('click', function(event) {
    if (event.target.id === 'add-to-cart') {
      event.preventDefault();
      var productId = event.target.getAttribute('data-product-id');
      fetch('/add_to_cart/' + productId + '/')
        .then(function (response) {
          alert("received response");
          return response.json();
        })
        .then(function(data) {
          document.cookie = "cart_count=" + data.cart_count + "; path=/";
          updateCartCount();
        })
        .catch(function(error) {
          console.error(error);
        });
    }
  });

  // Call the updateCartCount function on page load
  updateCartCount();
});
