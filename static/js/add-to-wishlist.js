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



const addWishListBtn = document.querySelector(".add-to-wishlist");
const wishListURL = '/api/wishlist/'


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



addWishListBtn.addEventListener("click", async function(e){
    e.preventDefault();

    // get the id of the course
    const courseId = e.target.dataset.id;

    if (user === "None") return showToast(wishListError, "error")

    const postData = {
        "course": courseId
    }    

    // post data to the api endpoint

    try {
        const response = await fetch(wishListURL, {
            method:"POST",
            body: JSON.stringify(postData),
            headers: {
                "X-CSRFToken": token,
                "Content-Type": "application/json"
            }
        })

        // if promise fails
        if (!response.ok) throw new Error(response)

        // if promise is resolved
        const responseData = await response.json();

        const {action} = responseData;

        switch (action) {
            case "created":
                // show modal or toast notification
                showToast(AddedMsg, "success")
                addWishListBtn.textContent = "Remove from Wishlist";
                addWishListBtn.classList.add("added");
                break;
            case "deleted":
                // show modal or toast notification
                showToast(RemoveMsg, "success")
                addWishListBtn.textContent = "Add to WishList";
                addWishListBtn.classList.remove("added");
                break;
            default:
                showToast(errorMsg, "error")
       
        }


    } catch (error) {
        console.log("failed to add to wishlist", error)
    }
    
})