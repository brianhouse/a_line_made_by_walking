var MARGIN = 50;

function setup() {
    console.log("Hello world");
    var canvas = createCanvas(windowWidth, windowHeight);
    canvas.parent('p5');
    textFont("monospace");    
}

function draw() {

    background(255);

    var notes = data['notes'];
    var ids = data['walk_ids'];

    textSize(10);
    fill(0);
    noStroke();
    for (var i in ids) {
        var id = ids[i];

        text(id, 20, (i/ids.length) * (height - 2 * MARGIN) + MARGIN + 7);
    }

    stroke(0);
    strokeWeight(2);
    for (var n in notes) {
        var note = notes[n];

        var x = note[0] * (width - 2 * MARGIN) + MARGIN;
        var y = (note[1] / ids.length) * (height - 2 * MARGIN) + MARGIN;
        if (note[2] == 0) {
            fill(255);  // left
        } else {
            fill(0);    // right
            y += 5;
        }
        var size = 5.0;
        arc(x, y, size * 2, size, 0, 2*PI);
    }


    show_fps();

}
