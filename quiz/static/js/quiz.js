"use strict"

// const URL = "/quiz/api/quizzes/1/";
const URL = "/quiz/api/questions/";
const questionEl = document.querySelector(".question");
const answersContainer = document.querySelector(".answers-container");
const questionNumTrackEl = document.querySelector(".question-numb");
const tempStorage = [];


let QUESTIONS = [];
let TOTALNUMQUESTIONS = 0;
let currentQuestionNum = 0


/**
 * 
 * @param {NodeList} optionsEl  
 * @returns true || undefined
 */
const hasAnswered = (optionsEl) => {
    for (let choice of optionsEl){
        if(choice.checked){
            return true;
        }else  {
            continue;
        }
    }
       
    }

/**
 * Get list of questions from the api
 */
const getQuiz = async () => {
    
    try {
        
    const response = await fetch(URL, {
            headers: {
                "X-CSRFToken": token,
                "Content-Type": "application/json",
            }
        });

    if (!response.ok) {
        throw new Error(response);
    }

    const responseData = await response.json();
    QUESTIONS = responseData;
    TOTALNUMQUESTIONS = QUESTIONS.length;

    displayQuestion()

    } catch (error) {
        console.log("catch scope: = ",error)
    }
    
}

const displayQuestion = () => {
   
    // get questions from the api
    //  console.log("length: ",QUESTIONS.length, TOTALNUMQUESTIONS, currentQuestionNum)
    
    // get the current question number and take it from the question list 
    // get the list of answers for the question and display them to
    
    let currQuestion = QUESTIONS[currentQuestionNum];
    console.log("currentQuestion: ", currQuestion) 

    // update the current question numbe showing in the browser
    questionNumTrackEl.innerHTML = `<h2><span class=>${currentQuestionNum + 1}</span>/${TOTALNUMQUESTIONS}</h2>`;

    // render question to the browser
    questionEl.textContent = currQuestion["question_text"];

    // render possible answers to the browser
    // answersContainer.innerHTML = "";
    const answersHTML = currQuestion["answers"].map((ans) => {
        return `
        
        <div >
          <input name="ans" type="radio" />
          <label for="ans"
            > ${ans.text}</label
          >
        </div>
        
        `
    }).join("");

    answersContainer.innerHTML = ""
    answersContainer.insertAdjacentHTML("afterbegin", answersHTML)


}



document.querySelector("#next").addEventListener("click", function(e){
    // increase CURRENTQUESTIONNUM by one and get the next question
    e.preventDefault()

    // get selected answer and save it in the localstorage
    const optionsEl = e.target.previousElementSibling.ans;

    // check if user has selected answer
    const hasUserSelectedAns = hasAnswered(optionsEl);

    if (hasUserSelectedAns){

        for (let ans of optionsEl) {
            if (ans.checked){
                let userChoice = ans.parentElement.querySelector("label").textContent;
                
                // structure user choice and answer and push it to tempStorage array
                let questionInfo = {
                    questionNumber: currentQuestionNum,
                    userAns: userChoice
                }
                tempStorage.push(questionInfo)
                
                // check if current question number is equal to the total question number 
                // move to the next question if not
                if (currentQuestionNum + 1 === TOTALNUMQUESTIONS){
                    // save user answers to the localstorage

                    let currenhrefParams = window.location.href;
                    currenhrefParams = currenhrefParams.split("/")

                    'http://localhost:8000/course/6/quizzes/1/python-programming/render/'

                    const quiz_slug = currenhrefParams[7];
                    const quiz_id = currenhrefParams[6];

                    // if true
                    // display result page
                    window.location.href = `/course/quizzes/${quiz_id}/${quiz_slug}/result/`
                }

                currentQuestionNum += 1;

                // call display question
                displayQuestion()

                
                
            }
        }
    } else {
        // ask user to select answer
        console.log("user has not selected answer")
    }
        
})

getQuiz();