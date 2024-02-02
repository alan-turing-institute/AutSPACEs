
document.addEventListener('DOMContentLoaded', (event) => {
    // Check if the user has set a theme before
    let storedTheme = localStorage.getItem('theme');

    if (storedTheme !== null) {
        console.log("The user has set a theme before - it is " + storedTheme);
        document.body.setAttribute('data-bs-theme', storedTheme);
        footer.setAttribute('data-bs-theme', storedTheme);
        console.log("The theme has been set to " + storedTheme);
    } else {
        console.log("The user has not set a theme before");
        // Get the system theme
        let systemTheme = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
        document.body.setAttribute('data-bs-theme', systemTheme);
        footer.setAttribute('data-bs-theme', systemTheme);
        console.log("The theme has been set to the system theme: " + systemTheme);
    }
});


document.getElementById('theme-toggle').addEventListener('click', function() {
    let currentTheme = document.body.getAttribute('data-bs-theme');
    console.log("Before clicking the current theme is " + currentTheme + " mode");
    console.log('Theme toggle clicked')
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
