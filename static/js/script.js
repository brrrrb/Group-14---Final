document.addEventListener('DOMContentLoaded', function() { // DOMcontent allows javascript to interact with DOM without waiting for external resources to load such as images and stylesheetts
    //listen to specfic event on the document 
    
        var signInBtn = document.getElementById("signInBtn");
        if (signInBtn) {
            signInBtn.addEventListener('click', function() {
                var myModal = new bootstrap.Modal(document.getElementById('myModal'));
                myModal.show();
            });
        }
    
    
    
        var emailBtn = document.getElementById("emailBtn");
        if (emailBtn) {
            emailBtn.addEventListener('click', function() {
                var emailSignInModal = new bootstrap.Modal(document.getElementById('emailSignInModal'));
                emailSignInModal.show();
            });
        }
        
       
       
         var joinNowLink = document.getElementById("joinNow");
    if (joinNowLink) {
        joinNowLink.addEventListener('click', function(event) {
            event.preventDefault();

            var emailSignInModalInstance = bootstrap.Modal.getInstance(document.getElementById('emailSignInModal'));
            if (emailSignInModalInstance) {
                // Listen for the modal to fully hide before showing the joinModal
                var onEmailModalHidden = function() {
                    // Remove the event listener to prevent potential duplication in future invocations
                    emailSignInModalInstance._element.removeEventListener('hidden.bs.modal', onEmailModalHidden);
                    
                    var joinModalInstance = new bootstrap.Modal(document.getElementById('joinModal'));
                    joinModalInstance.show();
                };

                emailSignInModalInstance._element.addEventListener('hidden.bs.modal', onEmailModalHidden);
                emailSignInModalInstance.hide();
            } else {
                // Directly show the joinModal if for some reason the emailSignInModal instance is not available
                var joinModalInstance = new bootstrap.Modal(document.getElementById('joinModal'));
                joinModalInstance.show();
            }
        });
    }
       
    
       
        var businessAccountBtn = document.getElementById("businessAccount");
        businessAccountBtn.addEventListener('click', function() {
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






        var signInLinkFromJoinModal = document.getElementById("signInLinkFromJoinModal");
        if (signInLinkFromJoinModal) {
            signInLinkFromJoinModal.addEventListener('click', function(event) {
                event.preventDefault();
    
                // Hide the joinModal first
                var joinModalInstance = bootstrap.Modal.getInstance(document.getElementById('joinModal'));
                if (joinModalInstance) {
                    joinModalInstance.hide();
                }
    
                // Then, show the myModal
                // Wait for the joinModal to be completely hidden before showing myModal
                var myModalInstance = new bootstrap.Modal(document.getElementById('myModal'));
                myModalInstance.show();
            });
        }


        var signInFromIndividualAccount = document.getElementById('signInFromIndividualAccount');
    if (signInFromIndividualAccount) {
        signInFromIndividualAccount.addEventListener('click', function(event) {
            event.preventDefault(); // Prevent default action of the link

            // Hide the individualAccountModal
            var individualAccountModalInstance = bootstrap.Modal.getInstance(document.getElementById('individualAccountModal'));
            if (individualAccountModalInstance) {
                individualAccountModalInstance.hide();
            }

            // Wait for the individualAccountModal to be hidden before showing myModal
            individualAccountModalInstance._element.addEventListener('hidden.bs.modal', function () {
                var myModalInstance = new bootstrap.Modal(document.getElementById('myModal'));
                myModalInstance.show();
            }, { once: true }); // Use the {once: true} option to automatically remove the event listener after it fires
        });
    }


    var signInFromBusinessAccount = document.getElementById('signInFromBusinessAccount');
    if (signInFromBusinessAccount) {
        signInFromBusinessAccount.addEventListener('click', function(event) {
            event.preventDefault(); // Prevent default action of the link

            // Hide the businessAccountModal first
            var businessAccountModalInstance = bootstrap.Modal.getInstance(document.getElementById('businessAccountModal'));
            if (businessAccountModalInstance) {
                businessAccountModalInstance.hide();
            }

            // Wait for the businessAccountModal to be hidden before showing myModal
            businessAccountModalInstance._element.addEventListener('hidden.bs.modal', function () {
                var myModalInstance = new bootstrap.Modal(document.getElementById('myModal'));
                myModalInstance.show();
            }, { once: true }); // Use the {once: true} option to automatically remove the event listener after it fires
        });
    }


       
       
       });