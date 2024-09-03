document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('loginForm');
    const loginButton = document.getElementById('loginButton');
    const loader = document.getElementById('loader');

    form.addEventListener('submit', async (event) => {
        event.preventDefault(); 
        
        loader.style.display = 'block';
        loginButton.disabled = true; 
     

        const formData = new FormData(form);
        const data = {
            phone_number: formData.get('phone_number'),
            password: formData.get('password')
        };

        try {
            const response = await fetch('/login/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                },
                body: JSON.stringify(data),
            });

            const result = await response.json();

            if (response.ok && result.status === 'success') {
               
                window.location.href = '/add-spam/';
            } else {
                
                alert(result.message || 'An error occurred.');
            }
        } catch (error) {
            console.error('Error during login:', error);
        } finally {
          
            loader.style.display = 'none';
            loginButton.disabled = false;
        }
    });
});
