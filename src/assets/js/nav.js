new TypeIt('#banner', {
    strings: ["quick and safe", "easiest way of text sharing"],
    speed: 70,
    breakLines: false,
    waitUntilVisible: true,
    cursor: false,
}).go();
const handleHomePage = () => { window.location.assign('/') }