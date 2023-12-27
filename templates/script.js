const startingMinutes = 1;
    let time = startingMinutes * 60;

    const countdownEl = document.getElementById('countdown');

    setInterval(updateCountdown, 1000);

    function updateCountdown() {
        if (time == 0) {
            location.replace("http://localhost:5001/activitycomplete");
        }
        const minutes = Math.floor(time / 60);
        let seconds = time % 60;

        seconds = seconds < 10 ? '0' + seconds : seconds;

        countdownEl.innerHTML = `${minutes}: ${seconds}`;
        time--;
    };