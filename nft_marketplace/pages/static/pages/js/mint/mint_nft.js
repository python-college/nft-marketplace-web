document.getElementById("createNFTButton").addEventListener("click", createNFT);

function createNFT() {
  const name = document.getElementById("nftName").value;
  const description = document.getElementById("nftDescription").value;
  const imageInput = document.getElementById("nftImage").files[0];

  if (!name || !description || !imageInput) {
    alert("Заполните все поля.");
    return;
  }



  const reader = new FileReader();
  reader.onload = () => {
    const base64Image = reader.result.split(",")[1];
    const sessionId = getCookie("session_id");
    const addressWallet = getCookie("address_wallet");
//    const collectionAddress = "{{ collection_address|escapejs }}";
    console.log("Collection Address: " + collectionAddress);

    const data = {
      session_id: sessionId,
      name: name,
      description: description,
      collection_address: collectionAddress,
      base64_image: base64Image
    };

    const socket = new WebSocket("ws://194.87.131.18/main/api/v1/ws/create/nft");

    socket.onopen = () => {
      console.log("WebSocket connection opened for creating NFT");
      socket.send(JSON.stringify(data));
      console.log(data);
    };

    socket.onmessage = (event) => {
      const response = JSON.parse(event.data);
      console.log("Received WebSocket message:", response);

      if (response.type === "mint_nft_data_processed") {
        console.log("Данные для создания NFT успешно получены!");
        return; // Ждем следующего ответа
      }

      if (response.type === "mint_nft_success") {
        alert("Минт успешно завершен!");
        window.location.href = `/profile/${addressWallet}/`;
        socket.close();
      } else if (response.type === "mint_nft_user_rejects") {
        alert("Отклонение транзакции пользователем");
        socket.close();
      }
    };

    socket.onclose = () => {
      console.log("WebSocket connection closed");
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

function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  return parts.length === 2 ? parts.pop().split(";").shift() : null;
}
