//dynamically checks if user has 12 characters in password box
const inputField = document.getElementById('password');
              const errorMessage = document.getElementById('error-message');
            
              inputField.addEventListener('input', () => {
                if (inputField.value.length < 12) {
                  errorMessage.style.display = 'block';
                } else {
                  errorMessage.style.display = 'none';
                }
              });