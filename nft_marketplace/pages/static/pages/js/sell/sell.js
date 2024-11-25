document.getElementById("sellNFTButton").addEventListener("click", sellNFT);

function sellNFT() {
  const price = document.getElementById("priceInput").value;

  // Проверка валидности введенной цены
  if (!price || isNaN(price) || price <= 0) {
    alert("Please enter a valid price.");
    return;
  }

  // Получение session_id и nft_address
  const sessionId = getCookie("session_id");
  const addressWallet = getCookie("address_wallet");
  console.log("nft Address: " + nft_item_address); // Убедимся, что адрес получен

  if (!sessionId || !nft_item_address) {
    alert("Session ID or NFT address not found. Please try again.");
    return;
  }

  // Формируем JSON для отправки
  const data = {
    session_id: sessionId,
    nft_address: nft_item_address,
    price: price
  };

  // WS подключение
  const socket = new WebSocket("ws://194.87.131.18/ws/sell/nft");

  socket.onopen = () => {
    console.log("WebSocket connection opened");
    socket.send(JSON.stringify(data));
    console.log("Sent data:", data);
  };

  socket.onmessage = (event) => {
    const response = JSON.parse(event.data);
    console.log("Received WebSocket message:", response);

    // Обработка ответа
    if (response.type === "sell_nft_success") {
      alert("Продажа прошла успешно!");
        window.location.href = `/profile/${addressWallet}/`;
      socket.close();
    } else if (response.type === "sell_nft_user_rejects") {
      alert("Продажа не прошла...");
      window.location.href = `/nfts/sell/${nft_item_address}`;
      socket.close();
    }
  };

  socket.onclose = () => {
    console.log("WebSocket connection closed");
  };

  socket.onerror = (error) => {
    console.error("WebSocket error:", error);
    alert("An error occurred. Please try again.");
  };
}

function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  return parts.length === 2 ? parts.pop().split(";").shift() : null;
}
