let questions = [];
let currentIndex = 0;
let score = 0;
let selectedOption = null;
let timerInterval = null;
let timeLeft = 0;
let userAnswers = [];

// Ekranlarni almashtirish funksiyasi
function showScreen(screenId) {
    document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
    document.getElementById(screenId).classList.add('active');
}

// Testni boshlash
document.getElementById('start-btn').addEventListener('click', async () => {
    const category = document.getElementById('category-select').value;
    const difficulty = document.getElementById('difficulty-select').value;
    
    const res = await fetch(`/api/questions/${category}/${difficulty}`);
    questions = await res.json();

    if (questions.length === 0) {
        alert("Savollar topilmadi!");
        return;
    }

    currentIndex = 0;
    score = 0;
    userAnswers = [];
    showScreen('quiz-screen');
    
    // Qiyinchilik darajasiga qarab adolatli vaqt ajratish:
    let timePerQuestion = 10; // Oson daraja uchun har bir savolga 10 soniya
    if (difficulty === 'medium') {
        timePerQuestion = 15; // O'rta daraja uchun 15 soniya
    } else if (difficulty === 'hard') {
        timePerQuestion = 25; // Qiyin daraja uchun 25 soniya
    }

    const totalTime = questions.length * timePerQuestion;
    
    startTimer(totalTime);
    loadQuestion();
});

// Savolni ekranga yuklash
function loadQuestion() {
    selectedOption = null;
    const q = questions[currentIndex];
    
    document.getElementById('question-tracker').innerText = `Savol ${currentIndex + 1}/${questions.length}`;
    document.getElementById('question-text').innerText = q.question;

    const optionsDiv = document.getElementById('options-container');
    optionsDiv.innerHTML = '';

    q.options.forEach(opt => {
        const btn = document.createElement('button');
        btn.className = 'option-btn';
        btn.innerText = opt;
        btn.onclick = () => {
            document.querySelectorAll('.option-btn').forEach(b => b.classList.remove('selected'));
            btn.classList.add('selected');
            selectedOption = opt;
        };
        optionsDiv.appendChild(btn);
    });
}

// Keyingi savolga o'tish
document.getElementById('next-btn').addEventListener('click', () => {
    if (!selectedOption) {
        alert("Iltimos, biror variantni tanlang!");
        return;
    }

    const currentQuestion = questions[currentIndex];
    const isCorrect = selectedOption === currentQuestion.answer;

    if (isCorrect) score++;

    userAnswers.push({
        question: currentQuestion.question,
        userAnswer: selectedOption,
        correctAnswer: currentQuestion.answer,
        isCorrect: isCorrect
    });

    currentIndex++;

    if (currentIndex < questions.length) {
        loadQuestion();
    } else {
        finishQuiz();
    }
});

// Taymerni ishga tushirish
function startTimer(seconds) {
    timeLeft = seconds;
    updateTimerDisplay();
    clearInterval(timerInterval);
    
    timerInterval = setInterval(() => {
        timeLeft--;
        updateTimerDisplay();
        if (timeLeft <= 0) {
            finishQuiz();
        }
    }, 1000);
}

// Taymer ko'rinishini formatlash
function updateTimerDisplay() {
    const mins = String(Math.floor(timeLeft / 60)).padStart(2, '0');
    const secs = String(timeLeft % 60).padStart(2, '0');
    document.getElementById('timer').innerText = `Vaqt: ${mins}:${secs}`;
}

// Testni yakunlash
function finishQuiz() {
    clearInterval(timerInterval);
    showScreen('result-screen');

    const total = questions.length;
    const percent = Math.round((score / total) * 100);

    document.getElementById('score-val').innerText = `${score}/${total}`;
    document.getElementById('percent-val').innerText = `${percent}%`;
}

// Xatolarni ko'rish oynasi
document.getElementById('review-btn').addEventListener('click', () => {
    const reviewList = document.getElementById('review-list');
    reviewList.innerHTML = '';

    userAnswers.forEach((ans, idx) => {
        const item = document.createElement('div');
        item.className = `review-item ${ans.isCorrect ? 'correct' : 'wrong'}`;
        item.innerHTML = `
            <p><strong>${idx + 1}. ${ans.question}</strong></p>
            <p>Sizning javob: <span class="${ans.isCorrect ? 'text-success' : 'text-danger'}">${ans.userAnswer}</span></p>
            ${!ans.isCorrect ? `<p>To'g'ri javob: <span class="text-success">${ans.correctAnswer}</span></p>` : ''}
        `;
        reviewList.appendChild(item);
    });

    document.getElementById('review-modal').style.display = 'block';
});

// Modal oynani yopish
document.getElementById('close-review-btn').addEventListener('click', () => {
    document.getElementById('review-modal').style.display = 'none';
});

// Qayta urinish
document.getElementById('retry-btn').addEventListener('click', () => {
    document.getElementById('start-btn').click();
});

// Bosh sahifaga qaytish
document.getElementById('home-btn').addEventListener('click', () => {
    showScreen('home-screen');
});