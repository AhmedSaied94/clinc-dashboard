/* Enhanced Sidebar & Navbar JavaScript */

// Sidebar Collapse/Expand Functionality
document.addEventListener("DOMContentLoaded", function () {
  const sidebar = document.getElementById("sidebar");
  const sidebarCollapseBtn = document.getElementById("sidebarCollapseBtn");
  const sidebarToggle = document.getElementById("sidebarToggle");
  const sidebarOverlay = document.getElementById("sidebarOverlay");
  const globalSearch = document.getElementById("globalSearch");

  // Toggle sidebar collapse (desktop)
  if (sidebarCollapseBtn) {
    sidebarCollapseBtn.addEventListener("click", function () {
      sidebar.classList.toggle("collapsed");

      // Save state to localStorage
      const isCollapsed = sidebar.classList.contains("collapsed");
      localStorage.setItem("sidebarCollapsed", isCollapsed);
    });
  }

  // Toggle sidebar visibility (mobile)
  if (sidebarToggle) {
    sidebarToggle.addEventListener("click", function () {
      sidebar.classList.toggle("show");
      sidebarOverlay.classList.toggle("active");
    });
  }

  // Close sidebar when clicking overlay
  if (sidebarOverlay) {
    sidebarOverlay.addEventListener("click", function () {
      sidebar.classList.remove("show");
      sidebarOverlay.classList.remove("active");
    });
  }

  // Restore sidebar state from localStorage
  const savedState = localStorage.getItem("sidebarCollapsed");
  if (savedState === "true" && window.innerWidth > 992) {
    sidebar.classList.add("collapsed");
  }

  // Global search functionality
  if (globalSearch) {
    globalSearch.addEventListener("input", function (e) {
      const searchTerm = e.target.value.toLowerCase();
      if (searchTerm.length > 2) {
        // Implement search logic here
        console.log("Searching for:", searchTerm);
        // You can make AJAX call to search endpoint
      }
    });

    globalSearch.addEventListener("keypress", function (e) {
      if (e.key === "Enter") {
        e.preventDefault();
        const searchTerm = e.target.value;
        if (searchTerm) {
          window.location.href = `/dashboard/placements/?search=${encodeURIComponent(
            searchTerm
          )}`;
        }
      }
    });
  }

  // Highlight active nav link based on current URL
  const currentPath = window.location.pathname;
  document.querySelectorAll(".sidebar-nav .nav-link").forEach((link) => {
    if (link.getAttribute("href") === currentPath) {
      link.classList.add("active");
    } else if (
      currentPath.includes("placement") &&
      link.href.includes("placement")
    ) {
      link.classList.add("active");
    }
  });

  // Smooth scroll for anchor links
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener("click", function (e) {
      const href = this.getAttribute("href");
      if (href !== "#" && href.length > 1) {
        e.preventDefault();
        const target = document.querySelector(href);
        if (target) {
          target.scrollIntoView({
            behavior: "smooth",
            block: "start",
          });
        }
      }
    });
  });

  // Auto-hide notifications after delay
  setTimeout(() => {
    document.querySelectorAll(".alert-dismissible").forEach((alert) => {
      if (!alert.classList.contains("permanent")) {
        setTimeout(() => {
          const bsAlert = new bootstrap.Alert(alert);
          bsAlert.close();
        }, 5000);
      }
    });
  }, 100);

  // Add ripple effect to buttons
  document.querySelectorAll(".btn, .nav-link").forEach((element) => {
    element.addEventListener("click", function (e) {
      const ripple = document.createElement("span");
      ripple.classList.add("ripple");
      this.appendChild(ripple);

      const rect = this.getBoundingClientRect();
      const size = Math.max(rect.width, rect.height);
      const x = e.clientX - rect.left - size / 2;
      const y = e.clientY - rect.top - size / 2;

      ripple.style.width = ripple.style.height = size + "px";
      ripple.style.left = x + "px";
      ripple.style.top = y + "px";

      setTimeout(() => ripple.remove(), 600);
    });
  });
});

// Add ripple CSS dynamically
const rippleStyles = document.createElement("style");
rippleStyles.textContent = `
    .ripple {
        position: absolute;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.5);
        transform: scale(0);
        animation: rippleEffect 0.6s ease-out;
        pointer-events: none;
    }
    
    @keyframes rippleEffect {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }
    
    .btn, .nav-link {
        position: relative;
        overflow: hidden;
    }
`;
document.head.appendChild(rippleStyles);
