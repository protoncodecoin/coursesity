const queryField = document.querySelector(".q-search")


queryField.addEventListener("submit", function(e){
    e.preventDefault()

    const q = document.querySelector("#search-input");
    const encodedQuery = encodeURIComponent(q.value);


    // redirect to search page
    window.location.href = `/course/search/?query=${encodedQuery}`;
})
