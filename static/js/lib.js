function show_fps(c=0) {
    var fps = frameRate();
    fill(c);
    noStroke();
    textSize(10);
    text(fps.toFixed(0) + " FPS", 10, height - 10);
}