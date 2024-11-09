    function showQRCode(authLink) {
        const qrContainer = document.getElementById('qrCode');
        qrContainer.innerHTML = '';
        new QRCode(qrContainer, {
            text: authLink,
            width: 250,
            height: 250
        });
    }

    function removeQRCode() {
        document.getElementById('qrCode').innerHTML = '';
    }

    function setCookie(name, value, days) {
        const date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        const expires = "; expires=" + date.toUTCString();
        document.cookie = name + "=" + (value || "") + expires + "; path=/";
    }

    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        return parts.length === 2 ? parts.pop().split(';').shift() : null;
    }

    function updateConnectButton(address) {
        const connectButton = document.getElementById('connectButton');
        if (address) {
            connectButton.textContent = address.slice(0, 5) +'...'+ address.slice(43, 48);
            connectButton.onclick = function() {
                window.location.href = `/profile/${address}`;
            };
        } else {
            connectButton.textContent = "Подключить кошелек";
            connectButton.onclick = connectWebSocket;
        }
    }

    function connectWebSocket() {
        const socket = new WebSocket("ws://194.87.131.18/ws/auth");

        socket.onopen = () => console.log("Connected to WebSocket");

        socket.onmessage = (event) => {
            const data = JSON.parse(event.data);

            if (data.type === "auth_link") {
                showQRCode(data.payload.auth_link);
            } else if (data.type === "auth_success") {
                const { address, session_id } = data.payload;

                setCookie("session_id", session_id, 7);
                setCookie("address_wallet", address, 7);

                removeQRCode();
                updateConnectButton(address);
            }
        };

        socket.onerror = (error) => console.error("WebSocket Error: ", error);
        socket.onclose = () => console.log("WebSocket connection closed");
    }

    document.addEventListener("DOMContentLoaded", () => {
        const addressWallet = getCookie('address_wallet');
        updateConnectButton(addressWallet);
    });
