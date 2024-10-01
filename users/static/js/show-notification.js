const toastBox = document.querySelector('.toastBox');
const AddedMsg = 
    '<i class="fas fa-check-circle"></i>Added to Wishlist!';
const RemoveMsg = 
    '<i class="fas fa-check-circle"></i>Removed from Wishlist!';
const updatedMsg = 
    '<i class="fas fa-check-circle"></i> Review was updated!!';
const errorMsg = 
    '<i class="fas fa-times-circle"></i> Error sending data. Try again ';
const wishListError = 
    '<i class="fas fa-times-circle"></i>Login to add to wishlist';

/**
 * 
 * @param {HTMLElement} message 
 * @param {String} type messag type
 */
function showToast(message, type) {
    const toast = document.createElement('div');
    toast.classList.add('toast', type);
    toast.innerHTML = 
        '<button class="close-btn">X</button>' 
                                    + message;
    toastBox.appendChild(toast);

    const closeButton = 
            toast.querySelector('.close-btn');
    closeButton.addEventListener('click', () => {
        toast.remove();
    });

    setTimeout(() => {
        toast.remove();
    }, 3000);
}

// show snackbar
function snackFunction(message) {
  // Get the snackbar DIV
  var x = document.getElementById("snackbar");
  x.textContent = message

  // Add the "show" class to DIV
  x.className = "show";

  // After 3 seconds, remove the show class from DIV
  setTimeout(function(){ x.className = x.className.replace("show", ""); }, 7000);
} 



// html
    //  <div class="toastBox">
    //  </div>



    // css


/* toast notification */

// .toastBox {
//     position: fixed;
//     bottom: 50px;
//     right: 30px;
//     display: flex;
//     flex-direction: column;
//     align-items: flex-end;
//     overflow: hidden;
//     padding: 20px;
// }

// .toast {
//     width: 400px;
//     height: 80px;
//     background: #fff;
//     font-weight: 500;
//     margin: 15px 0;
//     box-shadow: 0 0 20px rgba(0, 0, 0, 0.3);
//     display: flex;
//     align-items: center;
//     position: relative;
//     transform: translateX(100%);
//     animation: moveleft 0.5s linear forwards;
// }

// @keyframes moveleft {
//     100% {
//         transform: translateX(0);
//     }
// }

// .toast i {
//     margin: 0 20px;
//     font-size: 35px;
// }

// .toast.success i {
//     color: green;
// }

// .toast.error i {
//     color: red;
// }

// .toast.invalid i {
//     color: orange;
// }

// .toast::after {
//     content: '';
//     position: absolute;
//     left: 0;
//     bottom: 0;
//     width: 100%;
//     height: 5px;
//     animation: anim 3s linear forwards;
// }

// @keyframes anim {
//     100% {
//         width: 0;
//     }
// }

// .toast.success::after {
//     background: green;
// }

// .toast.error::after {
//     background: red;
// }

// .toast.invalid::after {
//     background: orange;
// }

// .close-btn {
//     background: none;
//     border: none;
//     cursor: pointer;
//     position: absolute;
//     top: 0;
//     right: 0;
//     padding: 5px;
//     width: 20px;
//     height: 20px;
//     display: flex;
//     align-items: center;
//     justify-content: center;
//     z-index: 1;
// }

// .close-btn i {
//     color: #666;
// }

// .toast.error .close-btn i,
// .toast.invalid .close-btn i {
//     color: #666;
// }