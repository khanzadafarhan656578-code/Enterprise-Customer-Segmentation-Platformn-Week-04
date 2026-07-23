/**
 * Theme Switcher Manager (Dark / Light Mode)
 */

(function () {
  const currentTheme = localStorage.getItem('app-theme') || 'dark';
  document.documentElement.setAttribute('data-theme', currentTheme);

  document.addEventListener('DOMContentLoaded', () => {
    const toggleBtn = document.getElementById('theme-toggle');
    const icon = toggleBtn ? toggleBtn.querySelector('i') : null;

    function updateIcon(theme) {
      if (!icon) return;
      if (theme === 'light') {
        icon.className = 'fas fa-moon';
      } else {
        icon.className = 'fas fa-sun';
      }
    }

    updateIcon(currentTheme);

    if (toggleBtn) {
      toggleBtn.addEventListener('click', () => {
        let activeTheme = document.documentElement.getAttribute('data-theme');
        let newTheme = activeTheme === 'dark' ? 'light' : 'dark';

        document.documentElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('app-theme', newTheme);
        updateIcon(newTheme);
      });
    }
  });
})();
