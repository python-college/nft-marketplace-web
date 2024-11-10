document.getElementById("createNFTButton").addEventListener("click", createNFT);

function createNFT() {
  const name = document.getElementById("nftName").value;
  const description = document.getElementById("nftDescription").value;
  const imageInput = document.getElementById("nftImage").files[0];

  if (!name || !description || !imageInput) {
    alert("Заполните все поля.");
    return;
  }

  const sessionId = getCookie("session_id"); // Получаем session_id из куки
  const addressWallet = getCookie('address_wallet')

  const reader = new FileReader();
  reader.onload = () => {
    const base64Image = reader.result.split(",")[1];

    const data = {
      session_id: sessionId,
      name: name,
      description: description,
      collection_address: collectionAddress,
      base64_image: base64Image
    };

    const socket = new WebSocket("ws://194.87.131.18/ws/create/nft");

    socket.onopen = () => {
      console.log("WebSocket connection opened for creating NFT");
      socket.send(JSON.stringify(data));
    };

    socket.onmessage = (event) => {
      const response = JSON.parse(event.data);
      if (response.type === "mint_nft_data_processed" && response.message === "Data successfully received and processed") {
        alert("Минт успешно завершен!");
        window.location.href = `/profile/${addressWallet}/`;
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

function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  return parts.length === 2 ? parts.pop().split(";").shift() : null;
}
