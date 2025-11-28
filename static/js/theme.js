/**
 * Theme Toggle JavaScript
 * Handles dark/light theme switching with localStorage persistence
 */

(function () {
  "use strict";

  const THEME_KEY = "clinic-dashboard-theme";
  const themeToggleBtn = document.getElementById("themeToggle"); // Desktop
  const themeToggleBtnMobile = document.getElementById("themeToggleMobile"); // Mobile
  const themeIcon = document.getElementById("themeIcon"); // Desktop
  const themeIconMobile = document.getElementById("themeIconMobile"); // Mobile
  const body = document.body;

  // Get saved theme or default to light
  function getSavedTheme() {
    return localStorage.getItem(THEME_KEY) || "light";
  }

  // Save theme to localStorage
  function saveTheme(theme) {
    localStorage.setItem(THEME_KEY, theme);
  }

  // Apply theme to document
  function applyTheme(theme) {
    body.setAttribute("data-theme", theme);
    updateThemeIcon(theme);

    // Update Chart.js theme if charts exist
    if (typeof updateChartsTheme === "function") {
      updateChartsTheme(theme);
    }
  }

  // Update theme toggle icon
  function updateThemeIcon(theme) {
    // Update desktop icon
    if (themeIcon) {
      if (theme === "dark") {
        themeIcon.classList.remove("bi-moon-fill");
        themeIcon.classList.add("bi-sun-fill");
      } else {
        themeIcon.classList.remove("bi-sun-fill");
        themeIcon.classList.add("bi-moon-fill");
      }
    }

    // Update mobile icon
    if (themeIconMobile) {
      if (theme === "dark") {
        themeIconMobile.classList.remove("bi-moon-fill");
        themeIconMobile.classList.add("bi-sun-fill");
      } else {
        themeIconMobile.classList.remove("bi-sun-fill");
        themeIconMobile.classList.add("bi-moon-fill");
      }
    }
  }

  // Toggle theme
  function toggleTheme() {
    const currentTheme = body.getAttribute("data-theme");
    const newTheme = currentTheme === "light" ? "dark" : "light";

    // Animate the transition
    body.style.transition = "background-color 0.3s ease, color 0.3s ease";

    applyTheme(newTheme);
    saveTheme(newTheme);

    // Animate buttons with GSAP
    if (typeof gsap !== "undefined") {
      if (themeToggleBtn) {
        gsap.to(themeToggleBtn, {
          rotation: "+=360",
          duration: 0.5,
          ease: "back.out(1.7)",
        });
      }
      if (themeToggleBtnMobile) {
        gsap.to(themeToggleBtnMobile, {
          rotation: "+=360",
          duration: 0.5,
          ease: "back.out(1.7)",
        });
      }
    }
  }

  // Initialize theme on page load
  function initTheme() {
    const savedTheme = getSavedTheme();
    applyTheme(savedTheme);

    // Add event listener to toggle buttons (desktop and mobile)
    if (themeToggleBtn) {
      themeToggleBtn.addEventListener("click", toggleTheme);
    }
    if (themeToggleBtnMobile) {
      themeToggleBtnMobile.addEventListener("click", toggleTheme);
    }
  }

  // Wait for DOM to be ready
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initTheme);
  } else {
    initTheme();
  }

  // Expose function globally for charts
  window.getCurrentTheme = getSavedTheme;
})();
