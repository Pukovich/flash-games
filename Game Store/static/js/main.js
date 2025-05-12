// DOM Elements
const authSection = document.getElementById('authSection');
const userProfile = document.getElementById('userProfile');
const authModal = document.getElementById('authModal');
const loginTitle = document.getElementById('loginTitle');
const registerTitle = document.getElementById('registerTitle');
const loginBtn = document.getElementById('loginBtn');
const registerBtn = document.getElementById('registerBtn');
const loginSwitch = document.getElementById('loginSwitch');
const registerSwitch = document.getElementById('registerSwitch');

// Toggle auth modal
function toggleAuthModal(show = true) {
    authModal.style.display = show ? 'flex' : 'none';
}

// Switch between login and register forms
function switchAuthForm(isLogin = true) {
    loginTitle.style.display = isLogin ? 'block' : 'none';
    registerTitle.style.display = isLogin ? 'none' : 'block';
    loginBtn.style.display = isLogin ? 'block' : 'none';
    registerBtn.style.display = isLogin ? 'none' : 'block';
    loginSwitch.style.display = isLogin ? 'block' : 'none';
    registerSwitch.style.display = isLogin ? 'none' : 'block';
}

// Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    // Auth modal close button
    const closeBtn = document.querySelector('.auth-modal-close');
    if (closeBtn) {
        closeBtn.addEventListener('click', () => toggleAuthModal(false));
    }

    // Login/Register switch buttons
    const switchButtons = document.querySelectorAll('.auth-switch-btn');
    switchButtons.forEach(button => {
        button.addEventListener('click', () => {
            const isCurrentlyLogin = loginTitle.style.display !== 'none';
            switchAuthForm(!isCurrentlyLogin);
        });
    });

    // Close modal when clicking outside
    window.addEventListener('click', (e) => {
        if (e.target === authModal) {
            toggleAuthModal(false);
        }
    });

    // Catalog dropdown
    const catalogBtn = document.querySelector('.catalog-btn');
    const catalogMenu = document.querySelector('.catalog-menu');
    
    if (catalogBtn && catalogMenu) {
        catalogBtn.addEventListener('click', () => {
            const isExpanded = catalogBtn.getAttribute('aria-expanded') === 'true';
            catalogBtn.setAttribute('aria-expanded', !isExpanded);
            catalogMenu.style.display = isExpanded ? 'none' : 'block';
        });

        // Close catalog menu when clicking outside
        document.addEventListener('click', (e) => {
            if (!catalogBtn.contains(e.target) && !catalogMenu.contains(e.target)) {
                catalogBtn.setAttribute('aria-expanded', 'false');
                catalogMenu.style.display = 'none';
            }
        });
    }

    // User profile dropdown
    const userAvatarBtn = document.querySelector('.user-avatar-btn');
    const profileDropdown = document.querySelector('.profile-dropdown');
    
    if (userAvatarBtn && profileDropdown) {
        userAvatarBtn.addEventListener('click', () => {
            const isExpanded = userAvatarBtn.getAttribute('aria-expanded') === 'true';
            userAvatarBtn.setAttribute('aria-expanded', !isExpanded);
            profileDropdown.style.display = isExpanded ? 'none' : 'block';
        });

        // Close profile dropdown when clicking outside
        document.addEventListener('click', (e) => {
            if (!userAvatarBtn.contains(e.target) && !profileDropdown.contains(e.target)) {
                userAvatarBtn.setAttribute('aria-expanded', 'false');
                profileDropdown.style.display = 'none';
            }
        });
    }
});

// Autocomplete for search
(function() {
    const searchInput = document.querySelector('.search-input');
    if (!searchInput) return;
    let acList = null;
    let acResults = [];
    let acIndex = -1;
    let acTimeout = null;

    function closeList() {
        if (acList) {
            acList.remove();
            acList = null;
            acResults = [];
            acIndex = -1;
        }
    }

    function renderList(results) {
        closeList();
        if (!results.length) return;
        acList = document.createElement('div');
        acList.className = 'autocomplete-list';
        results.forEach((item, idx) => {
            const el = document.createElement('div');
            el.className = 'autocomplete-item';
            el.textContent = item.name;
            el.addEventListener('mousedown', function(e) {
                e.preventDefault();
                searchInput.value = item.name;
                closeList();
                searchInput.form && searchInput.form.submit();
            });
            acList.appendChild(el);
        });
        searchInput.parentNode.appendChild(acList);
        acResults = results;
        acIndex = -1;
    }

    searchInput.addEventListener('input', function() {
        const val = this.value.trim();
        if (acTimeout) clearTimeout(acTimeout);
        if (!val) return closeList();
        acTimeout = setTimeout(() => {
            fetch(`/autocomplete/?q=${encodeURIComponent(val)}`)
                .then(r => r.json())
                .then(data => {
                    renderList(data.results || []);
                });
        }, 200);
    });

    searchInput.addEventListener('keydown', function(e) {
        if (!acList) return;
        const items = acList.querySelectorAll('.autocomplete-item');
        if (e.key === 'ArrowDown') {
            acIndex = (acIndex + 1) % items.length;
            items.forEach((el, i) => el.classList.toggle('active', i === acIndex));
            e.preventDefault();
        } else if (e.key === 'ArrowUp') {
            acIndex = (acIndex - 1 + items.length) % items.length;
            items.forEach((el, i) => el.classList.toggle('active', i === acIndex));
            e.preventDefault();
        } else if (e.key === 'Enter') {
            if (acIndex >= 0 && acResults[acIndex]) {
                searchInput.value = acResults[acIndex].name;
                closeList();
                searchInput.form && searchInput.form.submit();
                e.preventDefault();
            }
        } else if (e.key === 'Escape') {
            closeList();
        }
    });

    document.addEventListener('click', function(e) {
        if (!acList) return;
        if (e.target !== searchInput && !acList.contains(e.target)) {
            closeList();
        }
    });
})(); 