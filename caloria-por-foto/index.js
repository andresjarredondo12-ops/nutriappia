// Archivo: admin.js

document.addEventListener('DOMContentLoaded', () => {
    const emailInput = document.getElementById('email-input');
    const grantButton = document.getElementById('grant-button');
    const statusMessage = document.getElementById('status-message');

    grantButton.addEventListener('click', async () => {
        const email = emailInput.value;

        // Validamos que el email no esté vacío y sea un formato válido
        if (!email || !email.includes('@')) {
            statusMessage.textContent = 'Por favor, ingresa un correo válido.';
            statusMessage.style.color = 'red';
            return;
        }

        // Mostramos un mensaje de "cargando"
        statusMessage.textContent = 'Procesando...';
        statusMessage.style.color = 'black';

        try {
            // Esta es la parte clave: llamamos a nuestra API en Vercel
            const response = await fetch('/api/grant-premium', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email: email }),
            });

            const result = await response.json();

            if (!response.ok) {
                // Si la API devuelve un error (ej: usuario no encontrado)
                throw new Error(result.error || 'Ocurrió un error en el servidor.');
            }

            // Mostramos el mensaje de éxito
            statusMessage.textContent = result.message;
            statusMessage.style.color = 'green';
            emailInput.value = ''; // Limpiamos el campo

        } catch (error) {
            // Mostramos el mensaje de error
            statusMessage.textContent = error.message;
            statusMessage.style.color = 'red';
        }
    });
});
