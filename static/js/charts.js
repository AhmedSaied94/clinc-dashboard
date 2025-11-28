/**
 * Chart.js Configuration and Initialization
 * Handles all analytics charts with dynamic data loading
 */

(function () {
  "use strict";

  let charts = {};

  // Get theme colors
  function getThemeColors() {
    const theme = document.body.getAttribute("data-theme");
    const isDark = theme === "dark";

    return {
      textColor: isDark ? "#e9ecef" : "#212529",
      gridColor: isDark ? "rgba(255, 255, 255, 0.1)" : "rgba(0, 0, 0, 0.1)",
      tooltipBg: isDark ? "#2a2d3a" : "#ffffff",
      chartColors: [
        "#0d6efd",
        "#dc3545",
        "#ffc107",
        "#198754",
        "#0dcaf0",
        "#6610f2",
        "#fd7e14",
        "#d63384",
        "#20c997",
        "#6f42c1",
      ],
    };
  }

  // Fetch analytics data from API
  async function fetchAnalyticsData(filterParams = "") {
    try {
      const response = await fetch(`/dashboard/api/analytics/?${filterParams}`);
      if (!response.ok) {
        throw new Error("Failed to fetch analytics data");
      }
      return await response.json();
    } catch (error) {
      console.error("Error fetching analytics:", error);
      return null;
    }
  }

  // Create or update department chart
  function createDepartmentChart(data, colors) {
    const ctx = document.getElementById("departmentChart");
    if (!ctx) return;

    const labels = data.department_stats.map(
      (item) => item.department || "Unknown"
    );
    const values = data.department_stats.map((item) => item.count);

    if (charts.department) {
      charts.department.destroy();
    }

    charts.department = new Chart(ctx, {
      type: "doughnut",
      data: {
        labels: labels,
        datasets: [
          {
            data: values,
            backgroundColor: colors.chartColors,
            borderWidth: 2,
            borderColor: colors.tooltipBg,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: true,
        plugins: {
          legend: {
            position: "bottom",
            labels: {
              color: colors.textColor,
              padding: 15,
            },
          },
          tooltip: {
            backgroundColor: colors.tooltipBg,
            titleColor: colors.textColor,
            bodyColor: colors.textColor,
            borderColor: colors.gridColor,
            borderWidth: 1,
          },
        },
      },
    });

    // Animate with GSAP
    if (typeof gsap !== "undefined") {
      gsap.from(ctx, {
        scale: 0.8,
        opacity: 0,
        duration: 0.8,
        ease: "back.out(1.7)",
      });
    }
  }

  // Create or update specialty chart
  function createSpecialtyChart(data, colors) {
    const ctx = document.getElementById("specialtyChart");
    if (!ctx) return;

    const labels = data.specialty_stats.map(
      (item) => item.specialty || "Unknown"
    );
    const values = data.specialty_stats.map((item) => item.count);

    if (charts.specialty) {
      charts.specialty.destroy();
    }

    charts.specialty = new Chart(ctx, {
      type: "pie",
      data: {
        labels: labels,
        datasets: [
          {
            data: values,
            backgroundColor: colors.chartColors,
            borderWidth: 2,
            borderColor: colors.tooltipBg,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: true,
        plugins: {
          legend: {
            position: "bottom",
            labels: {
              color: colors.textColor,
              padding: 15,
            },
          },
          tooltip: {
            backgroundColor: colors.tooltipBg,
            titleColor: colors.textColor,
            bodyColor: colors.textColor,
            borderColor: colors.gridColor,
            borderWidth: 1,
          },
        },
      },
    });

    if (typeof gsap !== "undefined") {
      gsap.from(ctx, {
        scale: 0.8,
        opacity: 0,
        duration: 0.8,
        delay: 0.1,
        ease: "back.out(1.7)",
      });
    }
  }

  // Create or update shift chart
  function createShiftChart(data, colors) {
    const ctx = document.getElementById("shiftChart");
    if (!ctx) return;

    const labels = data.shift_stats.map((item) => item.shift || "Unknown");
    const values = data.shift_stats.map((item) => item.count);

    if (charts.shift) {
      charts.shift.destroy();
    }

    charts.shift = new Chart(ctx, {
      type: "bar",
      data: {
        labels: labels,
        datasets: [
          {
            label: "Placements",
            data: values,
            backgroundColor: colors.chartColors[2],
            borderColor: colors.chartColors[2],
            borderWidth: 1,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: true,
        scales: {
          y: {
            beginAtZero: true,
            ticks: {
              color: colors.textColor,
              stepSize: 1,
            },
            grid: {
              color: colors.gridColor,
            },
          },
          x: {
            ticks: {
              color: colors.textColor,
            },
            grid: {
              color: colors.gridColor,
            },
          },
        },
        plugins: {
          legend: {
            display: false,
          },
          tooltip: {
            backgroundColor: colors.tooltipBg,
            titleColor: colors.textColor,
            bodyColor: colors.textColor,
            borderColor: colors.gridColor,
            borderWidth: 1,
          },
        },
      },
    });

    if (typeof gsap !== "undefined") {
      gsap.from(ctx, {
        scaleY: 0,
        opacity: 0,
        duration: 0.8,
        delay: 0.2,
        ease: "power2.out",
      });
    }
  }

  // Create or update status chart
  function createStatusChart(data, colors) {
    const ctx = document.getElementById("statusChart");
    if (!ctx) return;

    const labels = data.status_stats.map((item) => item.status || "Unknown");
    const values = data.status_stats.map((item) => item.count);

    if (charts.status) {
      charts.status.destroy();
    }

    charts.status = new Chart(ctx, {
      type: "doughnut",
      data: {
        labels: labels,
        datasets: [
          {
            data: values,
            backgroundColor: ["#198754", "#ffc107", "#dc3545", "#6c757d"],
            borderWidth: 2,
            borderColor: colors.tooltipBg,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: true,
        plugins: {
          legend: {
            position: "bottom",
            labels: {
              color: colors.textColor,
              padding: 15,
            },
          },
          tooltip: {
            backgroundColor: colors.tooltipBg,
            titleColor: colors.textColor,
            bodyColor: colors.textColor,
            borderColor: colors.gridColor,
            borderWidth: 1,
          },
        },
      },
    });

    if (typeof gsap !== "undefined") {
      gsap.from(ctx, {
        scale: 0.8,
        opacity: 0,
        duration: 0.8,
        delay: 0.3,
        ease: "back.out(1.7)",
      });
    }
  }

  // Create or update time series chart
  function createTimeSeriesChart(data, colors) {
    const ctx = document.getElementById("timeSeriesChart");
    if (!ctx) return;

    const labels = data.time_series.map((item) => item.date);
    const values = data.time_series.map((item) => item.count);

    if (charts.timeSeries) {
      charts.timeSeries.destroy();
    }

    charts.timeSeries = new Chart(ctx, {
      type: "line",
      data: {
        labels: labels,
        datasets: [
          {
            label: "Placements",
            data: values,
            borderColor: colors.chartColors[4],
            backgroundColor: colors.chartColors[4] + "33",
            borderWidth: 2,
            fill: true,
            tension: 0.4,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: true,
        scales: {
          y: {
            beginAtZero: true,
            ticks: {
              color: colors.textColor,
              stepSize: 1,
            },
            grid: {
              color: colors.gridColor,
            },
          },
          x: {
            ticks: {
              color: colors.textColor,
              maxRotation: 45,
              minRotation: 45,
            },
            grid: {
              color: colors.gridColor,
            },
          },
        },
        plugins: {
          legend: {
            display: false,
          },
          tooltip: {
            backgroundColor: colors.tooltipBg,
            titleColor: colors.textColor,
            bodyColor: colors.textColor,
            borderColor: colors.gridColor,
            borderWidth: 1,
          },
        },
      },
    });

    if (typeof gsap !== "undefined") {
      gsap.from(ctx, {
        scaleY: 0,
        opacity: 0,
        duration: 0.8,
        delay: 0.4,
        ease: "power2.out",
      });
    }
  }

  // Initialize all charts
  async function initializeCharts(filterParams = "") {
    const data = await fetchAnalyticsData(filterParams);
    if (!data) return;

    const colors = getThemeColors();

    createDepartmentChart(data, colors);
    createSpecialtyChart(data, colors);
    createShiftChart(data, colors);
    createStatusChart(data, colors);
    createTimeSeriesChart(data, colors);
  }

  // Update charts when theme changes
  function updateChartsTheme(theme) {
    if (Object.keys(charts).length > 0) {
      const currentUrl = new URL(window.location.href);
      const filterParams = currentUrl.search.substring(1);
      initializeCharts(filterParams);
    }
  }

  // Expose functions globally
  window.initializeCharts = initializeCharts;
  window.updateChartsTheme = updateChartsTheme;
})();
