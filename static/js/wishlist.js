const baseURL = `/api/wishlist/`;

const wishlistEl = document.querySelector("#wishlist");


const getUserWishList = async () => {
    try {
        const response = await fetch(baseURL, {
            // headers: 
            method: "POST",
            credentials: "same-origin",
            headers: {
                "X-CSRFToken": csrf_token,
                "content-Type": "application/json"
            }
        },
    )

    // error
    if (!response.ok){
        throw new Error(response.statusText);
    }

    // success
    const responseData = await response.json()
    console.log(responseData);
    } catch (error) {
        console.log(error)
    }
}

getUserWishList()

