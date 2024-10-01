// let form = document.getElementById("lobby__form");

// let displayName = sessionStorage.getItem("displayName");
// if (displayName) {
//   form.name.value = displayName;
// }

// form.addEventListener("submit", (e) => {
//   e.preventDefault();

//   sessionStorage.setItem("displayName", e.target.name.value);

//   let inviteCode = e.target.room.value;
//   if (!inviteCode) {
//     inviteCode = String(Math.floor(Math.random() * 1_000_000));
//   }

//   window.location = `room.html?room=${inviteCode}`;
// });
