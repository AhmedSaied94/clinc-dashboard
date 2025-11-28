/**
 * Theme Toggle JavaScript
 * Handles dark/light theme switching with localStorage persistence
 */

(function () {
  "use strict";

  const THEME_KEY = "clinic-dashboard-theme";
  const themeToggleBtn = document.getElementById("themeToggle");
  const themeIcon = document.getElementById("themeIcon");
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
    if (!themeIcon) return;

    if (theme === "dark") {
      themeIcon.classList.remove("bi-moon-fill");
      themeIcon.classList.add("bi-sun-fill");
    } else {
      themeIcon.classList.remove("bi-sun-fill");
      themeIcon.classList.add("bi-moon-fill");
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

    // Animate button with GSAP
    if (typeof gsap !== "undefined") {
      gsap.to(themeToggleBtn, {
        rotation: "+=360",
        duration: 0.5,
        ease: "back.out(1.7)",
      });
    }
  }

  // Initialize theme on page load
  function initTheme() {
    const savedTheme = getSavedTheme();
    applyTheme(savedTheme);

    // Add event listener to toggle button
    if (themeToggleBtn) {
      themeToggleBtn.addEventListener("click", toggleTheme);
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
