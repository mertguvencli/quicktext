const applicationUrl = `${baseUrl}/${key}`;
const text = document.getElementById("text");
const viewerCanEdit = $("#viewer_can_edit");
const shareOnNetwork = $("#share_on_network");
const ipWhitelist = $("#ip_whitelist");
const furtherSettings = $("#furtherSettings");
const share = $("#share");
const copy = $("#copy");
const qrcode = $("#qrcode");
const image = document.getElementById("image");
const toolboxGroup1 = $("#tool-box-group-1");

const socket = io();
socket.emit("join", { room: key });

const handleCopy = () => {
  const dummy = document.createElement("textarea");
  document.body.appendChild(dummy);
  dummy.value = text.value;
  dummy.select();
  document.execCommand("copy");
  document.body.removeChild(dummy);

  const options = {
    html: true,
    delay: 1000,
    template: "<p>Copied 🎉</p>",
    customClass: "color",
  };
  const popover = new bootstrap.Popover(
    document.getElementById("copyButton"),
    options
  );
  popover.show();
  setTimeout(() => {
    popover.hide();
  }, 1000);
};

const hideTools = () => {
  furtherSettings.addClass("d-none");
  toolboxGroup1.addClass("d-none");
  copy.removeClass("d-none");
  qrcode.removeClass("d-none");
};

const showTools = () => {
  furtherSettings.removeClass("d-none");
  toolboxGroup1.removeClass("d-none");
  copy.addClass("d-none");
  qrcode.addClass("d-none");
};

const handleShare = () => {
  fetch("/share", {
    method: "POST",
    headers: {
      "Content-type": "application/json; charset=UTF-8",
      key, // global variable
    },
    body: JSON.stringify({
      text: text.value,
      viewer_can_edit: viewerCanEdit.is(":checked"),
      ip_whitelist: ipWhitelist.val(),
      share_on_network: shareOnNetwork.is(":checked"),
    }),
  }).then(() => {
    hideTools();
    new bootstrap.Toast(document.getElementById("toast"), {
      delay: 1000,
    }).show();
    $("#sharing-code").removeClass("d-none");
  });
};

const handleImageToText = (img) => {
  const formData = new FormData();
  formData.append("image", img);

  fetch("/convert-image-to-text", {
    method: "POST",
    body: formData,
  })
    .then((response) => response.json())
    .then((json) => {
      $("#text").val(json.text);
    });
};

socket.on("channel", (message) => {
  if (message) {
    response = JSON.parse(JSON.stringify(message));

    if (response.viewer_count) {
      $("#viewer").text(response.viewer_count);
    }

    if (response.data) {
      $("#sharing-code").removeClass("d-none");

      if (
        !response.data.viewer_can_edit &&
        response.data.owner_client_id != clientId
      ) {
        $("#text").prop("disabled", true);
      }
      hideTools();
    } else {
      showTools();
    }
  }
});

socket.on("channel_typing", (message) => {
  if (message) {
    response = JSON.parse(JSON.stringify(message));
    if (response.client_id != clientId) {
      $("#typing").removeClass("d-none");
      $("#text").val(message.text);
    }
  }
});

//Typing status check..
const textarea = $("#text");
const typingDelayMillis = 1000;
let lastTypedTime = new Date(0);
const updateLastTypedTime = () => {
  lastTypedTime = new Date();
};

const refreshTypingStatus = () => {
  if (
    !textarea.is(":focus") ||
    textarea.val() == "" ||
    new Date().getTime() - lastTypedTime.getTime() > typingDelayMillis
  ) {
    $("#typing").addClass("d-none");
  }
};
setInterval(refreshTypingStatus, 3000);
textarea.keypress(updateLastTypedTime);
textarea.blur(refreshTypingStatus);

// detect leaving room
window.onbeforeunload = (e) => {
  socket.emit("leave", { room: key });
};

new QRCode(document.getElementById("qrcode"), {
  text: applicationUrl,
  width: 60,
  height: 60,
  colorDark: "black",
  colorLight: "white",
  correctLevel: QRCode.CorrectLevel.H,
});

const handleOpenNewTab = () => {
  window.open(applicationUrl, "_blank");
};

const handleShowSettings = () => {
  new bootstrap.Modal(
    document.getElementById("furtherSettingsModal"),
    {}
  ).show();
};

const handleBrowse = () => {
  $("#image").click();
};

// Listeners
text.addEventListener("keyup", () => {
  socket.emit("typing", { room: key, text: text.value });
  socket.emit("channel_event", { room: key, text: text.value });
});

image.addEventListener("change", () => {
  if (image.files.length > 0) {
    const imageToConvert = image.files[0];
    response = handleImageToText(imageToConvert);
  }
});
