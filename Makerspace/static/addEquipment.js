//dynamically checks if user has less than 45 characters in equipment name box - MB 
const inputField = document.getElementById('equipment_name');
              const errorMessage = document.getElementById('error-message');
            
              inputField.addEventListener('input', () => {
                if (inputField.value.length > 45) {
                  errorMessage.style.display = 'block';
                } else {
                  errorMessage.style.display = 'none';
                }
              });