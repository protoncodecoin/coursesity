
document.addEventListener("DOMContentLoaded", function(e){

    // select the module btn
    document.querySelectorAll(".check_status").forEach((el) => {
        el.addEventListener("click", function(e){
        // e.preventDefault()

        // post module id to the backend
        let moduleID = e.target.dataset.moduleId;

        const data = {
            course_id: course_id,
            module_id: moduleID
        }

        saveProgress(data)        
    })
    })
})

/**
 * 
 * @param {Object} data data to send to the api endpoint
 */
const saveProgress = async (data) => {

    const URL = `/api/save_progress/`

    try {
       const response =  await fetch(URL, {
            method: "POST",
            body: JSON.stringify(data),
            headers: {
             "X-CSRFToken": token,
            "Content-Type": "application/json",
           }
        },
    )

    if (!response.ok) throw new Error(response)

    const {progress_status} = await response.json();

    if (progress_status == "saved"){
        // do nothing
    }

    } catch (error) {
        // try again
        console.log(error)
        console.log("sorry couldn't have progress")
    }
}

const circularProgress = document.querySelectorAll(".circular-progress");

Array.from(circularProgress).forEach((progressBar) => {
  const progressValue = progressBar.querySelector(".percentage");
  const innerCircle = progressBar.querySelector(".inner-circle");
  let startValue = 0,
    endValue = Number(progressBar.getAttribute("data-percentage")),
    speed = 50,
    progressColor = progressBar.getAttribute("data-progress-color");

  const progress = setInterval(() => {
    startValue++;
    progressValue.textContent = `${startValue}%`;
    progressValue.style.color = `${progressColor}`;

    innerCircle.style.backgroundColor = `${progressBar.getAttribute(
      "data-inner-circle-color"
    )}`;

    progressBar.style.background = `conic-gradient(${progressColor} ${
      startValue * 3.6
    }deg,${progressBar.getAttribute("data-bg-color")} 0deg)`;
    if (startValue === endValue) {
      clearInterval(progress);
    }
  }, speed);
});

console.log(document.querySelector(".floater"))

document.querySelector(".floater").addEventListener("onclick", function(e){
    console.log("clicked or hovered")
     document.querySelector(".info").style.display="block";
})