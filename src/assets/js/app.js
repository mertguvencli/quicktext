const applicationUrl = `${baseUrl}/${key}`
const text = document.getElementById("text")
const viewerCanEdit = $('#viewer_can_edit')
const shareOnNetwork = $('#share_on_network')
const password = $('#password')
const ipWhitelist = $('#ip_whitelist')
const furtherSettings = $('#furtherSettings')
const share = $('#share')
const copy = $('#copy')
const qrcode = $('#qrcode')
const image = document.getElementById('image')
const toolboxGroup1 = $('#tool-box-group-1')

var socket = io();
socket.emit('join', {room: key})

const handleCopy = () => {
    let _text = text.value
    let dummy = document.createElement("textarea");
    document.body.appendChild(dummy);
    dummy.value = _text;
    dummy.select();
    document.execCommand("copy");
    document.body.removeChild(dummy);

    const options = {html: true, delay: 1000, template: '<p>Copied</p>', customClass: 'color'};
    let popover = new bootstrap.Popover(document.getElementById('copyButton'), options);
    popover.show();
    setTimeout(()=>{ popover.hide() }, 1000);
}
const hideTools = () => {
    furtherSettings.addClass('d-none')
    toolboxGroup1.addClass('d-none')

    copy.removeClass('d-none')
    qrcode.removeClass('d-none')
}
const showTools = () => {
    furtherSettings.removeClass('d-none')
    toolboxGroup1.removeClass('d-none')
    copy.addClass('d-none')
    qrcode.addClass('d-none')
}        
const handleShare = () => {
    fetch("/share", {
        method: 'POST',
        headers: {
            "Content-type": "application/json; charset=UTF-8",
            "key": key
        },
        body: JSON.stringify({
            text : text.value,
            viewer_can_edit: viewerCanEdit.is(":checked"),
            password: password.val(),
            ip_whitelist: ipWhitelist.val(),
            share_on_network: shareOnNetwork.is(":checked")
        }),
    })
    .then(response => response.json())
    .then(json => {
        hideTools()
        new bootstrap.Toast(document.getElementById('toast'), {delay: 3000}).show();
    })
}
const handleImageToText = (img) => {
    let formData = new FormData();
    formData.append("image", img);

    fetch("/convert-image-to-text", {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(json => {
        $('#text').val(json.text)
    })
}
text.addEventListener('keyup', () => {
    socket.emit('typing', { room: key, text: text.value })
    socket.emit('channel_event', { room: key, text: text.value })
})
let hasInitiate = false;
socket.on('channel', (message) => {
    if (message) {
        response = JSON.parse(JSON.stringify(message));

        if (response.viewer_count) $('#viewer').text(response.viewer_count);

        if (response.data) {
            if(!response.data.viewer_can_edit && response.data.owner_client_id != clientId) {
                $('#text').prop('disabled', true);
            }
            hideTools()
        }
        else{
            showTools()
        }
    }
})
socket.on('channel_typing', (message) => {
    if (message) {
        response = JSON.parse(JSON.stringify(message));
        if (response.client_id != clientId) {
            $('#typing').removeClass('d-none');
            $('#text').val(message.text);
        }
    }
})
//Typing status check..
const textarea = $('#text');
const typingDelayMillis = 1000;
let lastTypedTime = new Date(0);
const updateLastTypedTime = () => { lastTypedTime = new Date() }
const refreshTypingStatus = () => {
    if (!textarea.is(':focus') || textarea.val() == '' || new Date().getTime() - lastTypedTime.getTime() > typingDelayMillis) {
        $('#typing').addClass('d-none')
    }
}
setInterval(refreshTypingStatus, 3000);
textarea.keypress(updateLastTypedTime);
textarea.blur(refreshTypingStatus);

// detect leaving room
window.onbeforeunload = (e) => {
    socket.emit('leave', {room: key})
}
new QRCode(document.getElementById("qrcode"), {
    text: applicationUrl,
    width: 60,
    height: 60,
    colorDark : "black",
    colorLight : "white",
    correctLevel : QRCode.CorrectLevel.H
});
const handleOpenNewTab = () => {
    window.open(applicationUrl, '_blank')
}
const handleShowSettings = () => {
    new bootstrap.Modal(document.getElementById('furtherSettingsModal'), {}).show();
}
const handleBrowse = () => {
    $('#image').click();
}
image.addEventListener('change', () => {
    if (image.files.length > 0) {
        const imageToConvert = image.files[0];
        response = handleImageToText(imageToConvert)
    }
})