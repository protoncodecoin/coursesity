const toastBox = document.querySelector('.toastBox');
const AddedMsg = 
    '<i class="fas fa-check-circle"></i>Added to Wishlist!';
const RemoveMsg = 
    '<i class="fas fa-check-circle"></i>Removed from Wishlist!';
const updatedMsg = 
    '<i class="fas fa-check-circle"></i> Review was updated!!';
const errorMsg = 
    '<i class="fas fa-times-circle"></i> Error Creating Meeting. Try again Later';
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

/**
 * Display snack bar 
 * @param {String} message message to show 
 */
// show snackbar
function snackFunction(message) {
  // Get the snackbar DIV
  var x = document.getElementById("snackbar");
  x.innerHTML = message

  // Add the "show" class to DIV
  x.className = "show";

  // After 3 seconds, remove the show class from DIV
  setTimeout(function(){ x.className = x.className.replace("show", ""); }, 9_000);
} 




// Get the modal
var modal = document.getElementById("myModal");
var btn = document.getElementById("meeting__btn");
var span = document.getElementsByClassName("close")[0];

// When the user clicks on the button, open the modal
btn.onclick = function() {
  modal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
  modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
} 

// window.onload = function(){
//     setTimeout(async function(){

//       const response = await CheckRatingStatus(course_id);

//       if (!response["rating_status"]){
//         // show the modal
//         modal.style.display = "block"
//       }
//     }, 10000)
// }

document.getElementById("meeting__form").addEventListener("submit", async function(e){
    e.preventDefault()

    let restriction = false;
    let checkBox = document.querySelector("#restriction");
    console.log(checkBox)

    if (checkBox.checked == true){
      restriction = true;
    }

    let meeting_name = document.querySelector("#meetingName").value
    let message = document.querySelector("#about").value;

    // remove modal
    modal.style.display = "none";
    
    // send data to api endpoint
    const data = {
      "course": course_id,
      "is_restricted": restriction,
      "about_message": message,
      "meeting_name": meeting_name
    }

    // create meeting
    createMeeting(data);

})

const createMeeting = async (data) => {
  const URL = `/api/create_meeting/`;

  try {
    const response = await fetch(URL, {
      method: "POST",
      body: JSON.stringify(data),
      headers: {
        "X-CSRFToken": token,
        "Content-Type": "application/json"
      }
    },
  )

  if (!response.ok) throw new Error(response)

    const resData = await response.json();
    const {token: meeting_token} = resData;

    if (meeting_token) {
      // show token to host
     const messageHTML = `
        <div style="width: 50%; margin: 10px auto;">
          <p>
                    Your meeting ID: <span style="color:skyblue;">${meeting_token}</span>
                    </p>
                    <p>All enrolled students have been alerted</p>
        </div>
                    `
      snackFunction(messageHTML)
    }

    
  } catch (error) {
    // show notification
    console.log(error)
    showToast(errorMsg, "error")
  }
}