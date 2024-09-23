
let uid = sessionStorage.getItem("uid");

if (!uid) {
  uid = String(Math.floor(Math.random() * 1_000_000)); // uid to user
  sessionStorage.setItem("uid", uid);
}

let token = null;
let client; // store information about the user to used in the streaming

const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);
let roomId = urlParams.get("room");

if (!roomId) {
  roomId = "main";
}

let localTracks = [];
let remoteUsers = {};

/**
 * Let user join a room and display their stream
 */
let joinRoomInit = async () => {
  client = AgoraRTC.createClient({ mode: "rtc", codec: "vp8" });
  await client.join(APP_ID, roomId, token, uid);

  client.on("user-published", handleUserPublished);
  client.on("user-left", handleUserLeft);

  joinStream();
};

/**
 * Gets user video and microphone streams and it to the dom
 */
let joinStream = async () => {
  localTracks = await AgoraRTC.createMicrophoneAndCameraTracks(
    {},
    {
      encoderConfig: {
        width: {
          min: 640,
          ideal: 1920,
          max: 1920,
        },
        height: {
          min: 480,
          ideal: 1080,
          max: 1080,
        },
      },
    }
  );

  let player = `<div  class="video__container" id="user-container-${uid}">
                    <div class="video-player" id="user-${uid}"></div>
                </div>
`;
  document
    .getElementById("streams__container")
    .insertAdjacentHTML("beforeend", player);

  document
    .getElementById(`user-container-${uid}`)
    .addEventListener("click", expandVideoFrame);

  localTracks[1].play(`user-${uid}`);
  await client.publish([localTracks[0], localTracks[1]]);
};

/**
 * Lets user publish their stream to the channel for remote users to see
 * @param {Object} user
 * @param {String} mediaType
 */
let handleUserPublished = async (user, mediaType) => {
  remoteUsers[user.uid] = user;

  await client.subscribe(user, mediaType);

  let player = document.getElementById(`user-container-${user.uid}`);
  if (player === null) {
    player = `<div  class="video__container" id="user-container-${user.uid}">
                          <div class="video-player" id="user-${user.uid}"></div>
                      </div>
      `;
    document
      .getElementById("streams__container")
      .insertAdjacentHTML("beforeend", player);
    document
      .getElementById(`user-container-${user.uid}`)
      .addEventListener("click", expandVideoFrame);
  }

  if (displayFrame.style.display) {
    player.style.height = "100px";
    player.style.width = "100px";
  }

  if (mediaType === "video") {
    user.videoTrack.play(`user-${user.uid}`);
  }

  if (mediaType === "audio") {
    user.audioTrack.play();
  }
};

/**
 * Removes user from the dom when the user leaves the channel
 * @param {Object} user
 */
let handleUserLeft = async (user) => {
  delete remoteUsers[user.uid];
  document.getElementById(`user-container-${user.uid}`).remove();

  // check to see if the user who left is the user in the displayFrame
  if (userIdInDisplayFrame === `user-container-${user.uid}`) {
    displayFrame.style.display = null;

    // change videoFrames display style to default
    let videoFrames = document.getElementsByClassName("video__container");

    for (let i = 0; videoFrames.length > i; i++) {
      videoFrames[i].style.height = "300px";
      videoFrames[i].style.width = "300px";
    }
  }
};

joinRoomInit();
