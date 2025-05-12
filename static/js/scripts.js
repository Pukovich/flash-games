const state = {
    isCatalogOpen: false,
    selectedCategory: "popular",
    selectedNavItem: "home",
    isLoggedIn: false,
    isAuthModalOpen: false,
    isProfileMenuOpen: false,
    authMode: "login",
    userProfile: {
      username: "",
      email: "",
      avatar: "https://placehold.co/48x48",
    },
    selectedFilters: {
      platforms: {},
      categories: {},
      genres: {},
    },
    games: {
      catalog: [
        {
          id: 1,
          name: "Red Dead Redemption 2",
          price: "2999₽",
          image: "https://placehold.co/300x160",
          discount: "20",
        },
        {
          id: 2,
          name: "Cyberpunk 2077",
          price: "1999₽",
          image: "https://placehold.co/300x160",
          discount: "35",
        },
        {
          id: 3,
          name: "Elden Ring",
          price: "3999₽",
          image: "https://placehold.co/300x160",
          discount: "15",
        },
      ],
      new: [
        {
          id: 4,
          name: "Starfield",
          price: "4999₽",
          image: "https://placehold.co/300x160",
          discount: "10",
        },
        {
          id: 5,
          name: "Baldurs Gate 3",
          price: "3999₽",
          image: "https://placehold.co/300x160",
          discount: "25",
        },
      ],
      popular: [
        {
          id: 6,
          name: "GTA V",
          price: "999₽",
          image: "https://placehold.co/300x160",
          discount: "50",
        },
        {
          id: 7,
          name: "The Witcher 3",
          price: "1499₽",
          image: "https://placehold.co/300x160",
          discount: "40",
        },
      ],
      expected: [
        {
          id: 8,
          name: "GTA VI",
          price: "4999₽",
          image: "https://placehold.co/300x160",
          discount: "0",
        },
        {
          id: 9,
          name: "Dragon Age 4",
          price: "3999₽",
          image: "https://placehold.co/300x160",
          discount: "0",
        },
      ],
    },
  };

  // DOM Elements
  const authSection = document.getElementById("authSection");
  const userProfile = document.getElementById("userProfile");
  const authModal = document.getElementById("authModal");
  const loginTitle = document.getElementById("loginTitle");
  const registerTitle = document.getElementById("registerTitle");
  const loginBtn = document.getElementById("loginBtn");
  const registerBtn = document.getElementById("registerBtn");
  const loginSwitch = document.getElementById("loginSwitch");
  const registerSwitch = document.getElementById("registerSwitch");
  const catalogBtn = document.querySelector(".catalog-btn");
  const catalogMenu = document.querySelector(".catalog-menu");
  const userAvatarBtn = document.querySelector(".user-avatar-btn");
  const profileDropdown = document.querySelector(".profile-dropdown");
  const logoutBtn = document.querySelector(".logout-btn");
  const gamesTabs = document.querySelectorAll(".games-tab");
  const gamesGrid = document.getElementById("gamesGrid");
  const platformFilters = document.getElementById("platformFilters");
  const categoryFilters = document.getElementById("categoryFilters");
  const genreFilters = document.getElementById("genreFilters");

  // Event Listeners
  document.querySelector(".login-link").addEventListener("click", () => {
    state.authMode = "login";
    state.isAuthModalOpen = true;
    updateUI();
  });

  document.querySelector(".register-link").addEventListener("click", () => {
    state.authMode = "register";
    state.isAuthModalOpen = true;
    updateUI();
  });

  document
    .querySelector(".auth-modal-close")
    .addEventListener("click", () => {
      state.isAuthModalOpen = false;
      updateUI();
    });

  loginBtn.addEventListener("click", () => {
    state.isLoggedIn = true;
    state.userProfile = {
      username: "John Doe",
      email: "john@example.com",
      avatar: "https://placehold.co/48x48",
    };
    state.isAuthModalOpen = false;
    updateUI();
  });

  registerBtn.addEventListener("click", () => {
    state.isLoggedIn = true;
    state.userProfile = {
      username: "New User",
      email: "user@example.com",
      avatar: "https://placehold.co/48x48",
    };
    state.isAuthModalOpen = false;
    updateUI();
  });

  document.querySelectorAll(".auth-switch-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      state.authMode = state.authMode === "login" ? "register" : "login";
      updateUI();
    });
  });

  catalogBtn.addEventListener("click", () => {
    state.isCatalogOpen = !state.isCatalogOpen;
    updateUI();
  });

  userAvatarBtn?.addEventListener("click", () => {
    state.isProfileMenuOpen = !state.isProfileMenuOpen;
    updateUI();
  });

  logoutBtn?.addEventListener("click", () => {
    state.isLoggedIn = false;
    state.isProfileMenuOpen = false;
    state.userProfile = {
      username: "",
      email: "",
      avatar: "",
    };
    updateUI();
  });

  gamesTabs.forEach((tab) => {
    tab.addEventListener("click", () => {
      state.selectedCategory = tab.dataset.category;
      updateUI();
    });
  });

  // Functions
  function updateUI() {
    // Auth state
    if (state.isLoggedIn) {
      authSection.style.display = "none";
      userProfile.style.display = "block";
      document.querySelector(".profile-username").textContent =
        state.userProfile.username;
      document.querySelector(".profile-email").textContent =
        state.userProfile.email;
      document.querySelector(".avatar-img").src = state.userProfile.avatar;
    } else {
      authSection.style.display = "block";
      userProfile.style.display = "none";
    }

    // Auth modal
    authModal.style.display = state.isAuthModalOpen ? "flex" : "none";
    if (state.authMode === "login") {
      loginTitle.style.display = "block";
      registerTitle.style.display = "none";
      loginBtn.style.display = "block";
      registerBtn.style.display = "none";
      loginSwitch.style.display = "block";
      registerSwitch.style.display = "none";
    } else {
      loginTitle.style.display = "none";
      registerTitle.style.display = "block";
      loginBtn.style.display = "none";
      registerBtn.style.display = "block";
      loginSwitch.style.display = "none";
      registerSwitch.style.display = "block";
    }

    // Catalog menu
    catalogMenu.style.display = state.isCatalogOpen ? "block" : "none";
    catalogBtn.setAttribute("aria-expanded", state.isCatalogOpen);

    // Profile dropdown
    profileDropdown.style.display = state.isProfileMenuOpen
      ? "block"
      : "none";
    userAvatarBtn?.setAttribute("aria-expanded", state.isProfileMenuOpen);

    // Game tabs
    gamesTabs.forEach((tab) => {
      if (tab.dataset.category === state.selectedCategory) {
        tab.classList.add("active");
      } else {
        tab.classList.remove("active");
      }
    });

    // Render games
    renderGames();

    // Render filters
    renderFilters();
  }

  function renderGames() {
    gamesGrid.innerHTML = "";

    const games = state.games[state.selectedCategory] || [];

    games.forEach((game) => {
      const hasDiscount = game.discount !== "0";
      const discountedPrice = Math.round(
        parseInt(game.price) * (1 - parseInt(game.discount) / 100),
      );

      const gameCard = document.createElement("article");
      gameCard.className = "game-card";

      gameCard.innerHTML = `
      <img src="${game.image}" alt="${game.name}" class="game-card-img">
      <div class="game-card-info">
        <h3 class="game-card-title">${game.name}</h3>
        <div class="game-card-price-container">
          ${
            hasDiscount
              ? `
            <div class="game-card-discount">-${game.discount}%</div>
            <div class="game-card-original-price">${game.price}</div>
            <div class="game-card-discounted-price">${discountedPrice}₽</div>
          `
              : `
            <div class="game-card-regular-price">${game.price}</div>
          `
          }
        </div>
      </div>
    `;

      gamesGrid.appendChild(gameCard);
    });
  }

  function renderFilters() {
    // Platform filters
    const platforms = [
      "Игры для MAC",
      "Игры для PC",
      "Игры для Linux",
      "Игры для Xbox",
      "Игры для Playstation",
    ];
    renderFilterOptions(platformFilters, platforms, "platforms");

    // Category filters
    const categories = [
      "Steam",
      "SteamOS",
      "Origin",
      "Uplay",
      "Xbox",
      "Playstation",
      "Mac OS X",
      "Linux",
    ];
    renderFilterOptions(categoryFilters, categories, "categories");

    // Genre filters
    const genres = [
      "Экшен",
      "Инди",
      "Приключения",
      "Стратегия",
      "RPG",
      "Гонки",
      "Симуляторы",
      "Спортивные",
      "Головоломки",
      "Хоррор",
      "Казуальные",
    ];
    renderFilterOptions(genreFilters, genres, "genres");
  }

  function renderFilterOptions(container, options, filterType) {
    container.innerHTML = "";

    options.forEach((option) => {
      const filterItem = document.createElement("div");
      filterItem.className = "filter-item";

      const isChecked = state.selectedFilters[filterType][option];

      filterItem.innerHTML = `
      <label class="filter-label">
        <input type="checkbox" class="filter-checkbox" ${isChecked ? "checked" : ""}>
        <span>${option}</span>
      </label>
    `;

      const checkbox = filterItem.querySelector("input");
      checkbox.addEventListener("change", () => {
        state.selectedFilters[filterType][option] = checkbox.checked;
      });

      container.appendChild(filterItem);
    });
  }

  // Initialize UI
  updateUI();

  // Social icons
  function createSocialLinks() {
    const socialLinks = [
        {
            icon: '/static/svg/socials/facebook.svg',
            url: 'https://facebook.com'
        },
        {
            icon: '/static/svg/socials/twitter.svg',
            url: 'https://twitter.com'
        },
        {
            icon: '/static/svg/socials/instagram.svg',
            url: 'https://instagram.com'
        }
    ];

    const socialLinksContainer = document.querySelector('.social-links');
    if (socialLinksContainer) {
        socialLinks.forEach(link => {
            const a = document.createElement('a');
            a.href = link.url;
            a.className = 'social-link';
            a.target = '_blank';
            a.rel = 'noopener noreferrer';
            
            const img = document.createElement('img');
            img.src = link.icon;
            img.alt = 'Social Media Icon';
            img.className = 'social-icon';
            
            a.appendChild(img);
            socialLinksContainer.appendChild(a);
        });
    }
  }

  // Close dropdowns when clicking outside
  document.addEventListener("click", (event) => {
    // Close profile dropdown when clicking outside
    if (state.isProfileMenuOpen && !event.target.closest(".user-profile")) {
      state.isProfileMenuOpen = false;
      updateUI();
    }

    // Close catalog menu when clicking outside
    if (state.isCatalogOpen && !event.target.closest(".catalog-dropdown")) {
      state.isCatalogOpen = false;
      updateUI();
    }
  });

  // Keyboard accessibility
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
      // Close modal on ESC
      if (state.isAuthModalOpen) {
        state.isAuthModalOpen = false;
        updateUI();
      }

      // Close dropdowns on ESC
      if (state.isProfileMenuOpen) {
        state.isProfileMenuOpen = false;
        updateUI();
      }

      if (state.isCatalogOpen) {
        state.isCatalogOpen = false;
        updateUI();
      }
    }
  });