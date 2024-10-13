const selectEl = document.getElementById("id_subject")
const getSubjectTitles = async () => {
    const URL = "/api/subject-titles/";

    try {
        const response = await fetch(URL, {
            headers: {
                "Content-Type": "application/json"
            }
        });

        if (!response.ok) throw new Error(error)
        const res = await response.json();

        console.log(res)

        const htmlRes = res.map((el) => {
            return `<option value="${el.id}">${el.title}</option>
`        }).join("")
        
        // selectEl.innerHTML = "";
        selectEl.insertAdjacentHTML("afterbegin", htmlRes)

        console.log(htmlRes);

        return res;

    } catch (error) {
        console.log(error)
    }
}

getSubjectTitles()