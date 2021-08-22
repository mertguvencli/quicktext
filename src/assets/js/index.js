const handleOpenApp = (key) => { window.location.assign(`/${key}`) }
const StartApp = () => { handleOpenApp(key) }
new TypeIt('#type-and-share', {
    strings: ["Type & Share Now!"],
    speed: 100,
    breakLines: false,
    waitUntilVisible: true,
    cursor: false,
}).go();