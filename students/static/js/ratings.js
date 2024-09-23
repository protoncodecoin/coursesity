const toastBox = document.querySelector('.toastBox');
const successMsg = 
    '<i class="fas fa-check-circle"></i> Thanks for the review!!';
const updatedMsg = 
    '<i class="fas fa-check-circle"></i> Review was updated!!';
const errorMsg = 
    '<i class="fas fa-times-circle"></i> Error sending data. Try again ';

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
 * check to see if current user has rated the course or not
 * @param {Number} course_id id of the course 
 * @returns object containing the status showing if the course has been rated or not
 */
async function CheckRatingStatus (course_id){
  const checkRatingURL = `/api/rating_status/?course_id=${course_id}`;

  try {
    const response = await fetch(checkRatingURL, {
      headers: {
        "X-CSRFToken": token,
        "Content-Type": "application/json",
      }
    })

    if (!response.ok) throw new Error(response);

    const resData = await response.json();
    console.log(resData)

    return resData;

  } catch (error) {
    console.log(error)
  }

}

/**
 * send user review to the api endpoint
 * @param {Object} data review data
 * @returns Object showing if the post was successful or failed
 */
async function postRatings (data) {
  const URL =  `/api/rating/`;

   try {
    const response = await fetch(URL, {
      headers: {
        "X-CSRFToken": token,
        "Content-Type": "application/json",
      },
      method: "POST",
      body: JSON.stringify(data)
    })

    if (!response.ok) throw new Error(response);

    const resData = await response.json();
    return resData;

  } catch (error) {
    console.log(error)
  }
}


// Get the modal
var modal = document.getElementById("myModal");
var btn = document.getElementById("myBtn");
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

window.onload = function(){
    setTimeout(async function(){

      const response = await CheckRatingStatus(course_id);

      if (!response["rating_status"]){
        // show the modal
        modal.style.display = "block"
      }
    }, 10000)
}


// handle rating form
document.getElementById("feedbackForm").addEventListener("submit", async function (event) {
    event.preventDefault();
    var rating = document.querySelector('input[name="rating"]:checked').value;
    var comment = document.getElementById("comment").value;

    // send the data to ratings endpoint
  data = {
    "course": course_id,
    "rating": +rating,
    "comment": comment
  }
  // send data
  const response = await postRatings(data);

    // hide modal window
  modal.style.display = 'none';

  if (response["created"]){
    // show message
    showToast(successMsg, "success")
  } else if(response["updated"]){
    // show message
    showToast(updatedMsg, "success")
  }


});
