const groupName = document.querySelector("#group-name").innerText;

const ws_url = `ws://${window.location.host}/ws/ac/${groupName}`;
const ws = new WebSocket(ws_url);

ws.onopen = () => {
  console.log("Websocket connection open...");
};
ws.onmessage = (event) => {
  const chatData = JSON.parse(event.data);
  console.log(chatData);

  if (chatData.type === "websocket.send") {
    const timeSince = parseInt(
      (new Date() - new Date(chatData.user.msg_age)) / 60000
    );
    let roomContentScroll = document.getElementById("room-content-scroll");
    roomContentScroll.innerHTML += `
    <div class="message">
    <div class="msg-head">
      <small>
        <div>
          <div class="profile-sm">
            <a href="{% url 'chat:userProfileView' room.host.username %}">
              <div class="avatar avatar-small">
                <img src="${chatData.user.avatar_url}" />
              </div>
              @${chatData.user.username}
            </a>
          </div>
          ${timeSince} minutes ago
        </div>
      </small>
    </div>
    <div class="msg-body">
      <p>${chatData.user.msg}</p>
    </div>`;
  }
};

// Send Message Form
const sendMsgForm = document.getElementById("send-msg-form");
sendMsgForm.addEventListener("submit", (e) => {
  e.preventDefault();
  const message = e.target.msgbody.value;
  ws.send(
    JSON.stringify({
      message: message,
    })
  );
  sendMsgForm.reset();
});
