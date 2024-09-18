// Toggle navbar js 

  let navLinks = document.getElementById("navLinks");

  function showMenu() {
    navLinks.style.right = "0";
  }

  function hideMenu() {
    navLinks.style.right = "-200px";
  }

  // When click outside menu
document.addEventListener("click", (event) => {
  const computedStyle = getComputedStyle(navLinks);
  const rightValue = computedStyle.getPropertyValue("right");

  if (rightValue === "0px" && !navLinks.contains(event.target)) {
    navLinks.style.right = "-200px";
  }
});



  
//  toggle search bar

  const searchButton = document.getElementById('search-input');
  const searchResults = document.querySelector('.search-results');

  searchButton.onfocus = () => {
    searchResults.classList.toggle("hidden")
  }

  searchButton.onblur = () => {
    searchResults.classList.toggle("hidden")
  }

  searchResults.onclick = () => {

  }

  // mobile version
const mobileSearchButton = document.querySelector('.m-search-icon');
const mobileSearchBar = document.querySelector('.m-searchbar');

mobileSearchButton.addEventListener('click', (event) => {
  event.stopPropagation()
  mobileSearchBar.classList.toggle("hidden")
})

 // close the bar when click outside search
 document.addEventListener("click", (event) => {

  if (!mobileSearchBar.classList.contains('hidden') && !mobileSearchBar.contains(event.target)) {
  mobileSearchBar.classList.toggle("hidden")
  }
});