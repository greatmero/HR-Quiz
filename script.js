function checkAnswer(selectedIndex) {
    const questionData = questions[currentQuestionIndex];
    const feedback = document.getElementById("feedback");
    const explanation = document.getElementById("explanation");

    if (!feedback || !explanation) {
        console.error("Feedback or explanation element not found!");
        return;
    }

    if (selectedIndex === questionData.correct) {
        feedback.innerText = "✅ Correct! Well done.";
        feedback.style.color = "green";
    } else {
        feedback.innerText = "❌ Incorrect. Try again!";
        feedback.style.color = "red";
    }
    feedback.style.display = "block";
    explanation.innerText = questionData.explanation;
    explanation.style.display = "block";
}
