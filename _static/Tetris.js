document.addEventListener('DOMContentLoaded', () => {
    const grid = document.querySelector('#tetrisContainer');
    let squares = Array.from(grid.querySelectorAll('div'));
    const width = 10;
    let currentPosition = 4;

    // Create the Tetris grid
    function createBoard() {
        for (let i = 0; i < 200; i++) {
            const square = document.createElement('div');
            grid.appendChild(square);
        }

        for (let i = 0; i < 10; i++) {
            const square = document.createElement('div');
            square.classList.add('taken');
            grid.appendChild(square);
        }

        squares = Array.from(grid.querySelectorAll('div'));
    }

    // Tetrominoes
    const lTetromino = [
        [1, width+1, width*2+1, 2],
        [width, width+1, width+2, width*2+2],
        [1, width+1, width*2+1, width*2],
        [width, width*2, width*2+1, width*2+2]
    ];

    const tetrominoes = [lTetromino];
    let currentRotation = 0;
    let random = Math.floor(Math.random()*tetrominoes.length);
    let current = tetrominoes[random][currentRotation];

    // Draw the Tetromino
    function draw() {
        current.forEach(index => {
            squares[currentPosition + index].classList.add('tetromino');
        });
    }

    // Undraw the Tetromino
    function undraw() {
        current.forEach(index => {
            squares[currentPosition + index].classList.remove('tetromino');
        });
    }

    // Make the tetromino move down every second
    timerId = setInterval(moveDown, 1000);

    // Move down function
    function moveDown() {
        undraw();
        currentPosition += width;
        draw();
        freeze();
    }

    // Freeze function
    function freeze() {
        if(current.some(index => squares[currentPosition + index + width].classList.contains('taken'))) {
            current.forEach(index => squares[currentPosition + index].classList.add('taken'));
            // Start a new tetromino falling
            random = Math.floor(Math.random() * tetrominoes.length);
            current = tetrominoes[random][currentRotation];
            currentPosition = 4;
            draw();
        }
    }

    createBoard();
    draw();
});
