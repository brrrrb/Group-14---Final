document.addEventListener('DOMContentLoaded', function() {
    // Sign In button interaction for username modal
    var signInBtn = document.getElementById("signInBtn");
    if (signInBtn) {
        signInBtn.addEventListener('click', function() {
            var usernameSignInModal = new bootstrap.Modal(document.getElementById('usernameSignInModal'));
            usernameSignInModal.show();
        });
    }

    // Email Sign In button interaction
    var emailBtn = document.getElementById("emailBtn");
    if (emailBtn) {
        emailBtn.addEventListener('click', function() {
            var emailSignInModal = new bootstrap.Modal(document.getElementById('emailSignInModal'));
            emailSignInModal.show();
        });
    }
    
    // Join Now link interaction to trigger join modal
    var joinNowLink = document.getElementById("joinNow");
    if (joinNowLink) {
        joinNowLink.addEventListener('click', function(event) {
            event.preventDefault();
            var emailSignInModalInstance = bootstrap.Modal.getInstance(document.getElementById('emailSignInModal'));
            if (emailSignInModalInstance) {
                emailSignInModalInstance._element.addEventListener('hidden.bs.modal', function() {
                    emailSignInModalInstance._element.removeEventListener('hidden.bs.modal', arguments.callee);
                    var joinModalInstance = new bootstrap.Modal(document.getElementById('joinModal'));
                    joinModalInstance.show();
                });
                emailSignInModalInstance.hide();
            } else {
                var joinModalInstance = new bootstrap.Modal(document.getElementById('joinModal'));
                joinModalInstance.show();
            }
        });
    }

    // Business account button interaction to show business modal
    var businessAccountBtn = document.getElementById("businessAccount");
    if (businessAccountBtn) {
        businessAccountBtn.addEventListener('click', function() {
            var joinModalInstance = bootstrap.Modal.getInstance(document.getElementById('joinModal'));
            joinModalInstance.hide();
            var businessAccountModal = new bootstrap.Modal(document.getElementById('businessAccountModal'));
            businessAccountModal.show();
        });
    }

    // Individual account button interaction to show individual modal
    var individualAccountBtn = document.getElementById("individualAccount");
    if (individualAccountBtn) {
        individualAccountBtn.addEventListener('click', function() {
            var joinModalInstance = bootstrap.Modal.getInstance(document.getElementById('joinModal'));
            joinModalInstance.hide();
            var individualAccountModal = new bootstrap.Modal(document.getElementById('individualAccountModal'));
            individualAccountModal.show();
        });
    }

    // Handling sign-in from Join modal
    var signInLinkFromJoinModal = document.getElementById("signInLinkFromJoinModal");
    if (signInLinkFromJoinModal) {
        signInLinkFromJoinModal.addEventListener('click', function(event) {
            event.preventDefault();
            var joinModalInstance = bootstrap.Modal.getInstance(document.getElementById('joinModal'));
            if (joinModalInstance) {
                joinModalInstance.hide();
                var myModalInstance = new bootstrap.Modal(document.getElementById('myModal'));
                myModalInstance.show();
            }
        });
    }

    // Sign in from individual account interaction
    var signInFromIndividualAccount = document.getElementById('signInFromIndividualAccount');
    if (signInFromIndividualAccount) {
        signInFromIndividualAccount.addEventListener('click', function(event) {
            event.preventDefault();
            var individualAccountModalInstance = bootstrap.Modal.getInstance(document.getElementById('individualAccountModal'));
            if (individualAccountModalInstance) {
                individualAccountModalInstance.hide();
                individualAccountModalInstance._element.addEventListener('hidden.bs.modal', function () {
                    var myModalInstance = new bootstrap.Modal(document.getElementById('myModal'));
                    myModalInstance.show();
                }, { once: true });
            }
        });
    }

    // Sign in from business account interaction
    var signInFromBusinessAccount = document.getElementById('signInFromBusinessAccount');
    if (signInFromBusinessAccount) {
        signInFromBusinessAccount.addEventListener('click', function(event) {
            event.preventDefault();
            var businessAccountModalInstance = bootstrap.Modal.getInstance(document.getElementById('businessAccountModal'));
            if (businessAccountModalInstance) {
                businessAccountModalInstance.hide();
                businessAccountModalInstance._element.addEventListener('hidden.bs.modal', function () {
                    var myModalInstance = new bootstrap.Modal(document.getElementById('myModal'));
                    myModalInstance.show();
                }, { once: true });
            }
        });
    }
});



function validateBusinessForm() {
    var einNumber = document.getElementById('einNumber').value;
    if (!/^[0-9]{9}$/.test(einNumber)) {
        alert("EIN must be exactly 9 digits");
        return false;
    }
    return true;
}
