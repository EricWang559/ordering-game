document.addEventListener('DOMContentLoaded', () => {
    const itemList = document.getElementById('item-list');
    const message = document.getElementById('message');
    const resetButton = document.getElementById('reset-button');
    const instruction = document.querySelector('#game-container p');
    const timerDisplay = document.getElementById('timer');

    let items = [];
    let correctOrder = [];
    let selectedItem = null;
    let timer;
    let seconds = 0;

    function shuffle(array) {
        for (let i = array.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [array[i], array[j]] = [array[j], array[i]];
        }
        return array;
    }

    function startTimer() {
        seconds = 0;
        timerDisplay.textContent = 'Time: 0s';
        timer = setInterval(() => {
            seconds++;
            timerDisplay.textContent = `Time: ${seconds}s`;
        }, 1000);
    }

    function stopTimer() {
        clearInterval(timer);
    }

    function initGame() {
        instruction.textContent = 'Click two items to swap them. Get them in order!';
        items = [1, 2, 3, 4, 5];
        correctOrder = shuffle([...items]);
        let shuffledItems = shuffle([...items]);

        // Ensure the shuffled order is not the correct order
        while (JSON.stringify(shuffledItems) === JSON.stringify(correctOrder)) {
            shuffledItems = shuffle([...items]);
        }

        itemList.innerHTML = '';
        shuffledItems.forEach(itemText => {
            const item = document.createElement('li');
            item.textContent = itemText;
            item.classList.add('item');
            item.addEventListener('click', () => handleItemClick(item));
            itemList.appendChild(item);
        });

        selectedItem = null;
        message.textContent = `0 out of ${correctOrder.length} are in the correct position.`;
        message.style.color = 'red';
        stopTimer(); // Stop any existing timer
        startTimer();
    }

    function handleItemClick(item) {
        if (!selectedItem) {
            // First item selected
            selectedItem = item;
            item.classList.add('selected');
        } else {
            // Second item selected, swap them
            const tempText = selectedItem.textContent;
            selectedItem.textContent = item.textContent;
            item.textContent = tempText;

            // Deselect
            selectedItem.classList.remove('selected');
            selectedItem = null;
            checkOrder(); // Check after every swap
        }
    }

    function checkOrder() {
        const currentOrder = Array.from(itemList.children).map(item => parseInt(item.textContent));
        let correctCount = 0;
        for (let i = 0; i < correctOrder.length; i++) {
            if (currentOrder[i] === correctOrder[i]) {
                correctCount++;
            }
        }

        if (correctCount === correctOrder.length) {
            message.textContent = `Congratulations! You got the order right in ${seconds} seconds!`;
            message.style.color = 'green';
            stopTimer();
        } else {
            message.textContent = `${correctCount} out of ${correctOrder.length} are in the correct position.`;
            message.style.color = 'red';
        }
    }

    resetButton.addEventListener('click', initGame);

    initGame();
});
