const addWishListBtn = document.querySelector(".add-to-wishlist");

const wishListURL = '/api/wishlist/'

addWishListBtn.addEventListener("click", async function(e){
    e.preventDefault();

    // get the id of the course
    const courseId = e.target.dataset.id;

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
                addWishListBtn.textContent = "Remove from Wishlist";
                addWishListBtn.classList.add("added");
                break;
            case "deleted":
                // show modal or toast notification
                addWishListBtn.textContent = "Add to WishList";
                addWishListBtn.classList.remove("added");
                break;
            default:
                // an error occurred 
                console.log("An error occurred. Couldn't add to wishlist")
       
        }


    } catch (error) {
        console.log("failed to add to wishlist", error)
    }
    
})