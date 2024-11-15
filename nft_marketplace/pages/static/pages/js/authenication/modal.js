// Получаем элементы
const openModalButton = document.getElementById('connectButton');
const closeModalButton = document.getElementById('closeModal');
const overlay = document.getElementById('overlay');
const modal = document.querySelector('.modal');

// Функция для открытия модального окна
openModalButton.addEventListener('click', () => {
    overlay.style.display = 'flex'; // Показываем оверлей
    modal.style.display = 'block'; // Показываем само модальное окно
});

// Функция для закрытия модального окна
closeModalButton.addEventListener('click', () => {
    overlay.style.display = 'none'; // Скрываем оверлей
    modal.style.display = 'none'; // Скрываем само модальное окно
});

// Закрытие модального окна при клике на оверлей
overlay.addEventListener('click', (event) => {
    if (event.target === overlay) {
        overlay.style.display = 'none'; // Скрываем оверлей
        modal.style.display = 'none'; // Скрываем само модальное окно
    }
});
