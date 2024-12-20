document.getElementById("createCollectionButton").addEventListener("click", createCollection);

function createCollection() {
  const name = document.getElementById("collectionName").value;
  const description = document.getElementById("collectionDescription").value;
  const royalty = parseFloat(document.getElementById("collectionRoyalty").value);
  const imageInput = document.getElementById("collectionImage").files[0];

  if (!name || !description || !royalty || !imageInput) {
    alert("Заполните все поля.");
    return;
  }

  if (royalty < 0 || royalty > 50) {
    alert("Royalty должно быть в диапазоне от 0 до 50%");
    return;
  }

  const reader = new FileReader();
  reader.onload = () => {
    const base64Image = reader.result.split(",")[1];
    const sessionId = getCookie("session_id");  // Получаем session_id из куки
    const addressWallet = getCookie('address_wallet')

    const data = {
      session_id: sessionId,  // Используем session_id из куки
      name: name,
      description: description,
      royalty_base: Math.floor(royalty),
      royalty_factor: 100,
      base64_image: base64Image
    };

    console.log(data)

    const socket = new WebSocket("ws://api.rarebay.ru/main/api/v1/ws/create/collection");

    socket.onopen = () => {
      console.log("WebSocket connection opened for creating collection");
      socket.send(JSON.stringify(data));
    };

    socket.onmessage = (event) => {
      const response = JSON.parse(event.data);
      console.log(response); // Логируем ответ для проверки

      // Обработка первого ответа
      if (response.type === "mint_collection_data_processed") {
        console.log("Коллекция успешно обработана! Ожидание подтверждения");


        return;  // Ожидаем второй ответ
      }

      // Обработка второго ответа
      if (response.type === "mint_collection_success") {
        alert("Коллекция создана успешно!");
        window.location.href = `/profile/${addressWallet}/`;
        socket.close(); // Закрываем соединение после успешной обработки
      } else if (response.type === "mint_collection_user_rejects") {
        alert("Отклонение транзакции пользователем");
        socket.close(); // Закрываем соединение в случае отклонения
      }
    };

    socket.onerror = (error) => {
      console.error("Ошибка при отправке данных через WebSocket", error);
      alert("Произошла ошибка. Попробуйте снова.");
    };
  };

  reader.onerror = () => {
    alert("Не удалось загрузить изображение.");
  };

  reader.readAsDataURL(imageInput);
}
