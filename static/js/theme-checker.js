
document.addEventListener('DOMContentLoaded', (event) => {
    // Check if the user has set a theme before
    let storedTheme = localStorage.getItem('theme');

    if (storedTheme !== null) {
        document.body.setAttribute('data-bs-theme', storedTheme);
        footer.setAttribute('data-bs-theme', storedTheme);
    } else {
        // Get the system theme
        let systemTheme = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
        document.body.setAttribute('data-bs-theme', systemTheme);
        footer.setAttribute('data-bs-theme', systemTheme);
    }
});


document.getElementById('theme-toggle').addEventListener('click', function() {
    let currentTheme = document.body.getAttribute('data-bs-theme');
    if (currentTheme === 'dark') {
        document.body.setAttribute('data-bs-theme', 'light');
        footer.setAttribute('data-bs-theme', 'light');
        localStorage.setItem('theme', 'light');
    } else {
        document.body.setAttribute('data-bs-theme', 'dark');
        footer.setAttribute('data-bs-theme', 'dark');
        localStorage.setItem('theme', 'dark');
    }
});
