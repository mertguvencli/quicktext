const redirectToCode = (code) => {
  window.location.assign(`/${code}`);
};
const checkCode = (code) => {
  fetch("/check", {
    method: "POST",
    headers: {
      "Content-type": "application/json; charset=UTF-8",
    },
    body: JSON.stringify({
      key: code,
    }),
  })
    .then((response) => response.json())
    .then((json) => {
      if (json.found) {
        $("#search-result").text("You are directing now.");
        redirectToCode(code);
      } else {
        $("#search-result").text("Couldn't found.");
      }
    });
};

const sharingCode = document.getElementById("sharing-code");
sharingCode.addEventListener("keypress", (e) => {
  if (String(e.target.value).length === 3) {
    setTimeout(() => checkCode(sharingCode.value), 100);
  }
});
sharingCode.addEventListener("keypress", (e) => {
  if (e.key === 'Enter') {
    setTimeout(() => checkCode(sharingCode.value), 100);
  }
});
