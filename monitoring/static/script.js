const documentBody = document.body;
const viewArea = document.getElementById('table-view');
const spinnerContainer = document.querySelector('.spinner-container');
const summaryReport = document.getElementById('summary-report');

function displayAlert(result, message) {
	var alertMessage = $('#alert-message');
	alertMessage.text(message);
  
	if (result === 'success') {
	  alertMessage.css('background-color', 'green');
	} else if (result === 'failure' || result === 'error') {
	  alertMessage.css('background-color', 'red');
	}
  
	alertMessage.show();
  
	setTimeout(function() {
	  alertMessage.fadeOut();
	}, 3000);
  }

function showSpinner() {
	spinnerContainer.style.display = 'block';
  }
  
  function hideSpinner() {
	spinnerContainer.style.display = 'none';
  }

