document.addEventListener('DOMContentLoaded', function() {

    var signInBtn = document.getElementById("signInBtn");
    if (signInBtn) {
        signInBtn.addEventListener('click', function() {
            var myModal = new bootstrap.Modal(document.getElementById('myModal'));
            myModal.show();
        });
    }
  
    var emailBtn = document.getElementById("emailSignIn");
    if (emailBtn) {
        emailBtn.addEventListener('click', function() {
            var mainModalEl = document.getElementById('myModal');
            var mainModalInstance = bootstrap.Modal.getInstance(mainModalEl);
            if (mainModalInstance) {
                mainModalInstance.hide();
            }
            var emailModal = new bootstrap.Modal(document.getElementById('emailSignInModal'));
            emailModal.show();
        });
    }
  
    var joinNowLink = document.getElementById("joinNow");
    if (joinNowLink) {
        joinNowLink.addEventListener('click', function(event) {
            event.preventDefault(); 
  
            var emailSignInModalInstance = bootstrap.Modal.getInstance(document.getElementById('emailSignInModal'));
            if (emailSignInModalInstance) {
                emailSignInModalInstance.hide();
            }
  
            var joinModalInstance = new bootstrap.Modal(document.getElementById('joinModal'));
            joinModalInstance.show();
        });
    }
  
  
    var businessAccountBtn = document.getElementById("businessAccount");
    businessAccountBtn.addEventListener('click', function() {
        // Hide the current join modal
        var joinModalInstance = bootstrap.Modal.getInstance(document.getElementById('joinModal'));
        joinModalInstance.hide();
  
        var businessAccountModal = new bootstrap.Modal(document.getElementById('businessAccountModal'));
        businessAccountModal.show();
    });
  
  
    var individualAccountBtn = document.getElementById("individualAccount");
    individualAccountBtn.addEventListener('click', function() {
        var joinModalInstance = bootstrap.Modal.getInstance(document.getElementById('joinModal'));
        joinModalInstance.hide();
  
        var individualAccountModal = new bootstrap.Modal(document.getElementById('individualAccountModal'));
        individualAccountModal.show();
    });
  
  });