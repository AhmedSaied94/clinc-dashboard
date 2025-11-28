/**
 * Dashboard JavaScript
 * GSAP animations and general dashboard functionality
 */

(function () {
  "use strict";

  // Initialize GSAP
  gsap.registerPlugin(ScrollTrigger);

  // Animate stat cards on load
  function animateStatCards() {
    const cards = document.querySelectorAll(".stat-card");

    if (cards.length > 0) {
      // Set initial state for all cards
      gsap.set(cards, {
        y: 30,
        opacity: 0,
      });

      // Animate to final state with stagger
      gsap.to(cards, {
        duration: 0.8,
        y: 0,
        opacity: 1,
        stagger: {
          amount: 0.4,
          from: "start",
        },
        ease: "power3.out",
        onComplete: function() {
          // Ensure all cards are at final state
          gsap.set(cards, {
            clearProps: "all",
          });
        },
      });
    }
  }

  // Animate chart cards
  function animateChartCards() {
    const chartCards = document.querySelectorAll(".chart-card");

    chartCards.forEach((card, index) => {
      gsap.from(card, {
        scrollTrigger: {
          trigger: card,
          start: "top 80%",
          toggleActions: "play none none none",
        },
        duration: 0.6,
        y: 50,
        opacity: 0,
        delay: index * 0.1,
        ease: "power2.out",
      });
    });
  }

  // Animate filter card
  function animateFilterCard() {
    const filterCard = document.querySelector(".filter-card");

    if (filterCard) {
      gsap.from(filterCard, {
        duration: 0.6,
        y: -20,
        opacity: 0,
        ease: "power2.out",
      });
    }
  }

  // Animate sidebar navigation
  function animateSidebar() {
    const navItems = document.querySelectorAll(".sidebar .nav-item");

    gsap.from(navItems, {
      duration: 0.5,
      x: -30,
      opacity: 0,
      stagger: 0.05,
      ease: "power2.out",
    });
  }

  // Highlight active navigation
  function highlightActiveNav() {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll(".sidebar .nav-link");

    navLinks.forEach((link) => {
      const href = link.getAttribute("href");
      if (href && currentPath.includes(href) && href !== "/") {
        link.classList.add("active");
      }
    });
  }

  // Initialize delete confirmation
  function initDeleteConfirmation() {
    const deleteButtons = document.querySelectorAll(
      '[data-bs-toggle="modal"][data-bs-target="#deleteModal"]'
    );

    deleteButtons.forEach((button) => {
      button.addEventListener("click", function () {
        const placementId = this.dataset.placementId;
        const placementName = this.dataset.placementName;

        // Update modal content
        const modal = document.getElementById("deleteModal");
        if (modal) {
          const deleteForm = modal.querySelector("form");
          if (deleteForm) {
            deleteForm.action = `/dashboard/placements/${placementId}/delete/`;
          }

          const placementInfo = modal.querySelector(".placement-info");
          if (placementInfo) {
            placementInfo.textContent = placementName;
          }
        }
      });
    });
  }

  // Initialize search functionality
  function initSearch() {
    const searchInput = document.querySelector('input[name="search"]');

    if (searchInput) {
      // Add debounce for search
      let searchTimeout;
      searchInput.addEventListener("input", function () {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(() => {
          // Could add AJAX search here
        }, 500);
      });
    }
  }

  // Animate page transitions
  function animatePageLoad() {
    gsap.from(".main-content", {
      duration: 0.5,
      opacity: 0,
      ease: "power2.out",
    });
  }

  // Initialize everything when DOM is ready
  function init() {
    animatePageLoad();
    animateFilterCard();
    animateStatCards();
    animateChartCards();
    animateSidebar();
    highlightActiveNav();
    initDeleteConfirmation();
    initSearch();
  }

  // Wait for DOM to be ready
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
