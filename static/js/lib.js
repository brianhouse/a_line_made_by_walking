function show_fps() {
    var fps = frameRate();
    fill(0);
    noStroke();
    textSize(10);
    text(fps.toFixed(0) + " FPS", 10, height - 10);
}