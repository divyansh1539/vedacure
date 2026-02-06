document.addEventListener("DOMContentLoaded", () => {

    /* ================= CARD SLIDER (REMEDIES) ================= */
    const cards = document.querySelectorAll(".remedy-card");
    let current = 0;
    const total = cards.length;

    function updateCards() {
        cards.forEach((card, i) => {
            card.classList.remove("active", "prev", "next");

            if (i === current) {
                card.classList.add("active");
            } 
            else if (i === (current - 1 + total) % total) {
                card.classList.add("prev");
            } 
            else if (i === (current + 1) % total) {
                card.classList.add("next");
            }
        });
    }

    window.slideRight = () => {
        current = (current + 1) % total;
        updateCards();
    };

    window.slideLeft = () => {
        current = (current - 1 + total) % total;
        updateCards();
    };

    if (cards.length > 0) {
        updateCards();
    }

    /* ================= FULL PAGE SCROLL ================= */
    const pages = [
        "/",          // home
        "/remedies/",
        "/ai/",
        "/about/",
        "/blog/",
        "/contact/"
    ];

    let isScrolling = false;

    function go(next) {
        if (isScrolling) return;
        isScrolling = true;

        let path = window.location.pathname;
        if (!path.endsWith("/")) path += "/";

        const index = pages.indexOf(path);
        if (index === -1) {
            isScrolling = false;
            return;
        }

        if (next && index < pages.length - 1) {
            window.location.href = pages[index + 1];
        }

        if (!next && index > 0) {
            window.location.href = pages[index - 1];
        }

        setTimeout(() => isScrolling = false, 1200);
    }

    /* ===== MOUSE / TRACKPAD SCROLL ===== */
    window.addEventListener("wheel", (e) => {
        if (Math.abs(e.deltaY) < 60) return;

        if (e.deltaY > 0) go(true);   // scroll down
        else go(false);              // scroll up
    }, { passive: true });

    /* ===== MOBILE SWIPE ===== */
    let startY = 0;

    window.addEventListener("touchstart", (e) => {
        startY = e.touches[0].clientY;
    }, { passive: true });

    window.addEventListener("touchend", (e) => {
        const endY = e.changedTouches[0].clientY;
        const diff = startY - endY;

        if (Math.abs(diff) < 80) return;

        if (diff > 0) go(true);   // swipe up
        else go(false);           // swipe down
    });

});
