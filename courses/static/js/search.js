const queryField = document.querySelector(".q-search")


document.getElementById("search-input").addEventListener("keypress", function(e){

    if (e.key === "Enter"){
        
        e.preventDefault()
        console.log(e.currentTarget);
        console.log(e.currentTarget.classList.contains("q-search"))
    
       const q = document.querySelector("#search-input");
       const encodedQuery = encodeURIComponent(q.value);
   
   
       // redirect to search page
       window.location.href = `/course/search/?query=${encodedQuery}`;
   } 
})
