document.addEventListener('DOMContentLoaded', function () {

    // Auto-dismiss flash alerts after 5 seconds
    setTimeout(function () {
        document.querySelectorAll('.alert').forEach(function (el) {
            el.style.transition = 'opacity .4s';
            el.style.opacity = '0';
            setTimeout(function () { el.remove(); }, 400);
        });
    }, 5000);

    var userBtn    = document.getElementById('userAvatarBtn');
    var userMenu   = document.getElementById('userDropdownMenu');
    var notifBtn   = document.getElementById('notifBtn');
    var notifPanel = document.getElementById('notifPanel');

    function closeAll() {
        if (userMenu)   userMenu.classList.remove('open');
        if (notifPanel) notifPanel.classList.remove('open');
    }

    // User avatar dropdown
    if (userBtn && userMenu) {
        userBtn.addEventListener('click', function (e) {
            e.stopPropagation();
            var wasOpen = userMenu.classList.contains('open');
            closeAll();
            if (!wasOpen) userMenu.classList.add('open');
        });
        userMenu.addEventListener('click', function (e) { e.stopPropagation(); });
    }

    // Notification bell
    if (notifBtn && notifPanel) {
        notifBtn.addEventListener('click', function (e) {
            e.stopPropagation();
            var wasOpen = notifPanel.classList.contains('open');
            closeAll();
            if (!wasOpen) notifPanel.classList.add('open');
        });
        notifPanel.addEventListener('click', function (e) { e.stopPropagation(); });
    }

    // Click outside closes everything
    document.addEventListener('click', closeAll);

    // Alert dismiss buttons
    document.addEventListener('click', function (e) {
        if (e.target.closest('.alert-close')) {
            e.target.closest('.alert').remove();
        }
    });

    // Confirmation dialogs
    document.querySelectorAll('[data-confirm]').forEach(function (btn) {
        btn.addEventListener('click', function (e) {
            if (!confirm(btn.dataset.confirm)) e.preventDefault();
        });
    });

});
