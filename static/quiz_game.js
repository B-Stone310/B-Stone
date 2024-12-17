let score = 0;  // 점수 초기화
let totalQuestions = 20;  // 전체 문제 수
let currentQuestion = 0;  // 현재 문제 번호

// 문제를 불러오는 함수
async function loadQuestion() {
    // 모든 문제를 다 풀었으면 퀴즈 종료
    if (currentQuestion >= totalQuestions) {
        document.getElementById("question").innerText = "퀴즈 종료";
        document.getElementById("options").innerHTML = `점수: ${score} / ${totalQuestions}`;
        
        // "다시 시작" 버튼을 추가합니다.
        const restartButton = document.createElement("button");
        restartButton.innerText = "다시 시작";
        restartButton.onclick = () => location.reload(); // 페이지 새로 고침
        document.getElementById("options").appendChild(restartButton);
        
        return;
    }

    try {
        // 서버에서 문제를 가져옵니다.
        const response = await fetch("/get_question");
        
        // 응답이 성공적이지 않으면 오류 메시지를 표시
        if (!response.ok) {
            throw new Error("문제를 불러오는 데 실패했습니다.");
        }

        const data = await response.json();  // JSON 데이터로 파싱

        // 문제와 선택지를 화면에 표시
        document.getElementById("question").innerText = data.word;
        const optionsDiv = document.getElementById("options");
        optionsDiv.innerHTML = "";  // 기존 선택지를 지웁니다.

        // 선택지를 버튼으로 만들어서 추가합니다.
        data.options.forEach(option => {
            const btn = document.createElement("button");
            btn.innerText = option;
            btn.onclick = () => checkAnswer(option, data.correct);  // 클릭 시 정답 체크
            optionsDiv.appendChild(btn);
        });
    } catch (error) {
        document.getElementById("question").innerText = "문제를 불러오는 데 오류가 발생했습니다. 다시 시도해주세요.";
        console.error(error);  // 콘솔에 에러를 출력
    }
}

// 사용자가 선택한 답과 정답을 비교하는 함수
function checkAnswer(selected, correct) {
    if (selected === correct) {
        score++;  // 정답이면 점수를 올립니다.
        alert("정답입니다!");
    } else {
        alert(`오답입니다. 정답은: ${correct}`);
    }

    // 문제를 풀고 나면 다음 문제로 넘어갑니다.
    currentQuestion++;
    loadQuestion();  // 다음 문제를 로드합니다.
}

// 페이지가 로드되면 첫 번째 문제를 불러옵니다.
window.onload = loadQuestion;
