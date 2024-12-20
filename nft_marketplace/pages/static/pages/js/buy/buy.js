document.getElementById("buyNFTButton").addEventListener("click", buyNFT);

function buyNFT() {
  // Получение session_id и nft_address
  const sessionId = getCookie("session_id");
  console.log("NFT Address: " + nft_item_address); // Убедимся, что адрес получен

  if (!sessionId || !nft_item_address) {
    alert("Session ID or NFT address not found. Please try again.");
    return;
  }

  // Формируем JSON для отправки
  const data = {
    session_id: sessionId,
    nft_address: nft_item_address
  };

  // Инициализация WebSocket
  const socket = new WebSocket("wss://api.rarebay.ru/main/api/v1/ws/buy/nft");

  socket.onopen = () => {
    console.log("WebSocket connection opened for buying NFT");
    socket.send(JSON.stringify(data));
    console.log("Sent data:", data);
  };

  socket.onmessage = (event) => {
    const response = JSON.parse(event.data);
    console.log("Received WebSocket message:", response);

    // Обработка ответа
    if (response.type === "buy_nft_success") {
      alert("Покупка прошла успешно!");
      window.location.href = "/profile";
      socket.close();
    } else if (response.type === "buy_nft_user_rejects") {
      alert("Покупка отклонена пользователем.");
      window.location.href = `/nfts/collections//${nft_item_address}`;
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
