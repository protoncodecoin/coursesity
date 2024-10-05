const msgEl = document.querySelector(".result");
const resultComparisonEl  = document.querySelector(".answers");


/**
 * 
 * @param {Object} data serializied data to post to the api endpoint
 * @returns {Object} data containing 'ok' or 'error' depending on the status of the request 
 */
const postStudentScore = async (data) => {
    // post score the api
    const saveScoreURL = '/quiz/api/save-score/'
    
    try {
        const response = await fetch(saveScoreURL, {
        headers: {
            "X-CSRFToken": token,
            "Content-Type": "application/json"
        },
        method: 'post',
        body: data
    })

    if (!response.ok){
        throw new Error(response)
    }

    await response.json();

    } catch (error) {
        console.log(error)
    }
}

// function to get data from localstorage
// get user answers from the data and compare with original answers

const getStoredData = () => {
    const userAns = JSON.parse(localStorage.getItem("result"));
    const quizQuestions = JSON.parse(localStorage.getItem("quiz-questions"));

    compareAnswers(quizQuestions, userAns)
}

/**
 * 
 * @param {Array} quiz data from the api 
 * @param {Array} userChoice user choices
 */
const compareAnswers = (quiz, userChoice) => {
    const resultSummary = [];
    let studentTotalScore = 0;
    let quizTotalScore = 0;

    for (let i = 0; i < quiz.length; i++) {
        // loop through the current question's answers
        for (let ans of quiz[i]['answers']){
           // check if the current answer is the correct answer
           if (ans["is_correct"]){
            // check if user answers is the same as the correct answer
            if ( ans['text'].trim() == userChoice[i]['userAns'].trim()){

                // increase studentScore by the current question's score
                console.log("api score: ", quiz[i]['score'])
                studentTotalScore += +quiz[i]['score'];

                // increase quiz total score
                quizTotalScore += +quiz[i]['score'];


               let rightAnsHtml = `<div class="q-a correct">
                    <p class="q">${quiz[i]['question_text']}</p>
                    <p class="a">
                        ${ans['text']}
                    </p>
                    </div>`
                
                // add right answer html to resultSummary
                resultSummary.push(rightAnsHtml);
            } else {

                // increase quiz total score
                quizTotalScore += +quiz[i]['score'];

                // wrong answer
                let wrongAnsHtml = `<div class="q-a wrong">
                                    <p class="q">${quiz[i]['question_text']}</p>
                                    <p class="a">${ans['text']}</p>
                                </div>`;
                
                // add wrong answer html to resultSummary
                resultSummary.push(wrongAnsHtml);
            }
           }
        }
        
    };

    const summaryHtml = resultSummary.map((el) => el).join("");

    resultComparisonEl.innerHTML = "";
    resultComparisonEl.insertAdjacentHTML("afterbegin", summaryHtml)

    // score the scores to the student
    // check against 0 to avoid dividing quiztotalscore by zero
    if (studentTotalScore !== 0){
            if ((quizTotalScore % studentTotalScore) > studentTotalScore){
                console.log((quizTotalScore % studentTotalScore) > studentTotalScore)
                // student didn't pass
                msgEl.innerHTML = '';
                msgEl.innerHTML = `Sorry, you scored <span>${studentTotalScore}</span> out of ${quizTotalScore} questions. Go back and revise on the module and come back.`;
            } else if ((quizTotalScore % studentTotalScore) < studentTotalScore) {
                console.log((quizTotalScore % studentTotalScore) > studentTotalScore)
                // student passed the text
                msgEl.innerHTML = "";
                msgEl.innerHTML = `Congratulations, you scored <span>${studentTotalScore}</span> out of ${quizTotalScore}. You're amazing`;
        }
    } else {
       // student didn't pass
        msgEl.innerHTML = '';
        msgEl.innerHTML = `Sorry, you scored <span>${studentTotalScore}</span> out of ${quizTotalScore} questions. Go back and revise on the module and come back.`;   
    }

    // post user score to the backend
    let quiz_id = window.location.href;
    quiz_id = quiz_id.split("/")[5]

    const scoreData = {
        "score": studentTotalScore,
        "quiz": +quiz_id,
    }

    // send data to the api
    postStudentScore(JSON.stringify(scoreData))
}

getStoredData();