/**
 * 
 * order items to create 
 */
const createOrder = async () => {
    const URL = `/api/create-order/`;

    try {
        const response = await fetch(URL, {
            headers: {
                "X-CSRFToken": token,
                "Content-Type": "application/json",
            },
            method: "POST",
            // body: JSON.stringify(data)
        })

        if (!response.ok) throw new Error(response)
        
        const resData = await response.json()
        console.log(resData);
    } catch (error) {
        console.log("error: ", error)
    }
}


/**
 * 
 * @param {Object} data transaction information to verify transaction 
 */
const verifyTransaction = async (data) => {
    const URL = "/api/verify-transaction/";

    try {
        const response = await fetch(URL, {
            headers: {
                "X-CSRFToken": token,
                "Content-Type": "application/json",
            },
            method: "POST",
            body: JSON.stringify(data)
        })

        if (!response.ok) throw new Error(response)
        
        const resData = await response.json()
        console.log(resData);
    } catch (error) {
        console.log("error: ", error)
    }
}