const rand_0_99 = Math.floor(Math.random() * 1000);
const chatBox = document.querySelector('.chat-box');
var btnEnter = 1
let intervalId;

const sendMessage = async () => {
    document.querySelector('.chat-input button').disabled = true;
    document.querySelector('.chat-input button').textContent = "Load";
    btnEnter = 0;
    
    const chatInput = document.querySelector('.chat-input input');
    
    const chatMessage = document.createElement('div');
    chatMessage.classList.add('chat-message');
    chatMessage.innerHTML = `<p>${chatInput.value}</p>`;


    if (chatInput.value.trim().length != 0) {
        const userMessages = chatInput.value;
        chatInput.value = '';

        chatBox.appendChild(chatMessage);
        chatBox.scroll(0, chatBox.scrollHeight)
    
        const astrologerMessage = document.createElement('div');
        astrologerMessage.classList.add('bodY');
        astrologerMessage.innerHTML = `
        <div class="center">
        <div class="wave"></div>
        <div class="wave"></div>
        <div class="wave"></div>
        <div class="wave"></div>
        <div class="wave"></div>
        <div class="wave"></div>
        <div class="wave"></div>
        <div class="wave"></div>
        <div class="wave"></div>
        <div class="wave"></div>
        </div>`;
        chatBox.appendChild(astrologerMessage);
        chatBox.scroll(0, chatBox.scrollHeight);

        const datas = JSON.stringify({
                userMessages: userMessages,
                id : rand_0_99

            });
        console.log(datas)

        // fetchAuthorName(datas)
        // const iter = main(datas);
        // const request = iter.next().value; /* axios.get(...)을 받는다. */
        // request.then(res => {
        //     iter.next(res); /* iter에 res를 넘겨주면서 iter을 재실행시킨다. */
        // });


        // openai_test(userMessages);


        const response = await fetch(`/gongOwlclassification/${rand_0_99}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                userMessages: userMessages,
                id : rand_0_99
            })
        });

        const data = await response.json();
        
        const ele = document.querySelector(".bodY");
        ele.classList.remove("bodY");

        if (data == '입시') {
            
            astrologerMessage.classList.add('select-btn');
            astrologerMessage.innerHTML = 
            `<button class ='univ' onclick="univ_onclick();this.onclick = null;"> 대학교 정보 </button>
            <button class ='academy'> 학원 정보 </button>
            `;
            disableBtn()
        }
        else {
            astrologerMessage.classList.add('chat-message');
            if (data == "streaming") {
                document.querySelector('.stop-btn button').style.visibility = 'visible';

                fetchAuthorName(astrologerMessage)
            }
            else {
                astrologerMessage.innerHTML = `<p class='assistant'>${data}</p>`;
                disableBtn()
            }
        }

        chatBox.appendChild(astrologerMessage);
        chatBox.scroll(0, chatBox.scrollHeight);

    }
    else {
        disableBtn()
    }
};

document.querySelector('.chat-input button').addEventListener('click', sendMessage);
document.querySelector('.chat-input input').addEventListener('keypress', function (e) {
if (e.key === 'Enter' && btnEnter == 1) {
// code for enter
sendMessage()
}
});

function sleep(ms) {
const wakeUpTime = Date.now() + ms;
while (Date.now() < wakeUpTime) {}
}

async function openai_test(userMessages) {

var url = "https://api.openai.com/v1/chat/completions";

var xhr = new XMLHttpRequest();
xhr.open("POST", url);

xhr.setRequestHeader("Content-Type", "application/json");
xhr.setRequestHeader("Authorization", "Bearer api-key");
xhr.onreadystatechange = function () {
if (xhr.readyState === 4) {
    console.log(xhr.status);
    console.log(xhr.responseText);
    open_ai_response = xhr.responseText;
    console.log(open_ai_response);
}};

messages=[
{"role": "system", "content": "당신은 진로 상담가입니다. 당신은 질문에 대해서 성심성의껏 대답합니다."},
{"role": "user", "content": userMessages}
]

var data = `{
"model": "gpt-3.5-turbo",
"messages": ${messages},
"temperature": 1
}`;

xhr.send(data);
}

function disableBtn() {
document.querySelector('.chat-input button').disabled = false;
document.querySelector('.chat-input button').textContent = "Send";
btnEnter = 1;
}

function fetchAuthorName(astrologerMessage) {
var streamValue = ``;

function fetchData() {
    fetch(`/stream/${rand_0_99}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
        })
    .then((response) => response.json())
    .then((data) => {  
        if (data != "stopStreaming") {
            streamValue = streamValue.concat(data)
        }
        else {
            stopFetching()
        }

        astrologerMessage.innerHTML = `<p class='assistant'>${streamValue}</p>`;
        chatBox.appendChild(astrologerMessage);
        chatBox.scroll(0, chatBox.scrollHeight);

    })
    .catch((error) => {
    console.log(error)
    });
};

function startFetching() {
    intervalId = setInterval(fetchData, 100); // delay 1 second between requests
};

function stopFetching() {
    document.querySelector('.stop-btn button').style.visibility = 'hidden';
    clearInterval(intervalId);
    disableBtn()
};

if (astrologerMessage) {
    startFetching();
}
else {
    stopFetching();
}

}

function univ_onclick(){
const astrologerMessage = document.createElement('div');
astrologerMessage.classList.add('select-box');
astrologerMessage.innerHTML = `
<select name="univ-list" size="5">
    <option value="dongguk"> 동국대학교 </option>
    <option value="gungguk"> 건국대학교 </option>
    <option value="hongik"> 홍악대학교 </option>
</select>
`;

chatBox.appendChild(astrologerMessage);
chatBox.scroll(0, chatBox.scrollHeight);
}