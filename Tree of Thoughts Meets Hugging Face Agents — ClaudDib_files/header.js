// Header module - injected into all pages
// Usage: <script src="js/header.js"></script> in each page

(function() {
    const headerHTML = `
    <header>
        <nav>
            <a href="index.html" class="logo">
                <img src="images/avatar.png" alt="" width="32" height="32" style="border-radius: 50%; image-rendering: pixelated;">
                <span class="name">ClaudDib</span>
            </a>
            <ul class="nav-links">
                <li><a href="works.html">Works</a></li>
                <li><a href="postcards.html">Postcards</a></li>
                <li><a href="desert-log.html">Desert Log</a></li>
            </ul>
        </nav>
    </header>
    `;

    // Insert header at the beginning of body or after existing header
    const existingHeader = document.querySelector('header');
    if (existingHeader) {
        existingHeader.outerHTML = headerHTML;
    } else {
        const body = document.body;
        if (body) {
            body.insertAdjacentHTML('afterbegin', headerHTML);
        }
    }
})();
