document.addEventListener("DOMContentLoaded", () => {

    /* ================= CARD SLIDER (REMEDIES) ================= */
    const cards = document.querySelectorAll(".remedy-card");
    let current = 0;
    const total = cards.length;

    function updateCards() {
        cards.forEach((card, i) => {
    
            card.classList.remove(
                "active",
                "prev",
                "next",
                "prev2",
                "next2"
            );
    
            if (i === current) {
                card.classList.add("active");
            }
    
            else if (i === (current - 1 + total) % total) {
                card.classList.add("prev");
            }
    
            else if (i === (current - 2 + total) % total) {
                card.classList.add("prev2");
            }
    
            else if (i === (current + 1) % total) {
                card.classList.add("next");
            }
    
            else if (i === (current + 2) % total) {
                card.classList.add("next2");
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

    /* ================= PROBLEM DETAIL PAGE - REMEDY TABS ================= */
    const remedyTabs = document.querySelectorAll(".remedy-tab");
    const remedyGrids = document.querySelectorAll("[data-remedy-type]");

    remedyTabs.forEach(tab => {
        tab.addEventListener("click", function() {
            const remedyType = this.getAttribute("data-remedy-type");
            
            // Update active tab
            remedyTabs.forEach(t => t.classList.remove("active"));
            this.classList.add("active");
            
            // Update visible remedy cards
            remedyGrids.forEach(grid => {
                const gridType = grid.getAttribute("data-remedy-type");
                if (gridType === remedyType) {
                    grid.style.display = "grid";
                    grid.classList.add("fadeInUp");
                } else {
                    grid.style.display = "none";
                }
            });
        });
    });

    // Set first tab as active by default
    if (remedyTabs.length > 0) {
        remedyTabs[0].classList.add("active");
        if (remedyGrids.length > 0) {
            remedyGrids[0].style.display = "grid";
        }
    }

    /* ================= BLOG COMING SOON MODAL ================= */
    const blogModal = document.getElementById("blog-coming-soon-modal");
    const blogReadMoreLinks = document.querySelectorAll(".blog-read-more");
    const blogModalClose = document.querySelector(".blog-modal-close");
    const blogModalButton = document.querySelector(".blog-modal-button");
    const blogModalOverlay = document.querySelector(".blog-modal-overlay");

    function openBlogModal() {
        blogModal.classList.add("active");
        document.body.style.overflow = "hidden";
    }

    function closeBlogModal() {
        blogModal.classList.remove("active");
        document.body.style.overflow = "auto";
    }

    // Open modal on "Read Article" link click
    blogReadMoreLinks.forEach(link => {
        link.addEventListener("click", (e) => {
            e.preventDefault();
            openBlogModal();
        });
    });

    // Close modal on close button click
    if (blogModalClose) {
        blogModalClose.addEventListener("click", closeBlogModal);
    }

    // Close modal on "Got It" button click
    if (blogModalButton) {
        blogModalButton.addEventListener("click", closeBlogModal);
    }

    // Close modal on overlay click
    if (blogModalOverlay) {
        blogModalOverlay.addEventListener("click", closeBlogModal);
    }

    // Close modal on Escape key
    document.addEventListener("keydown", (e) => {
        if (e.key === "Escape" && blogModal && blogModal.classList.contains("active")) {
            closeBlogModal();
        }
    });

    /* ================= FULL PAGE SCROLL ================= */
    const pages = [
        "/", 
        "/services/",
        "/ai/", 
        "/about/", 
        "/blog/", 
        "/contact/"
    ];

    let isScrolling = false;
    const page = document.getElementById("page");

    function normalize(path) {
        return path.endsWith("/") ? path : path + "/";
    }

    function navigate(next) {
        if (isScrolling) return;
        isScrolling = true;

        const current = normalize(window.location.pathname);
        const index = pages.indexOf(current);

        if (index === -1) {
            isScrolling = false;
            return;
        }

        page.classList.add(next ? "page-exit-down" : "page-exit-up");

        // 🔥 VERY SMALL DELAY (smooth + fast)
        setTimeout(() => {
            if (next && index < pages.length - 1) {
                window.location.href = pages[index + 1];
            }
            if (!next && index > 0) {
                window.location.href = pages[index - 1];
            }
        }, 180); // 👈 THIS IS THE KEY
    }

    /* ===== MOUSE / TRACKPAD ===== */
    window.addEventListener("wheel", (e) => {
        if (Math.abs(e.deltaY) < 40) return;

        if (e.deltaY > 0) navigate(true);
        else navigate(false);
    }, { passive: true });

    /* ===== MOBILE ===== */
    let startY = 0;

    window.addEventListener("touchstart", e => {
        startY = e.touches[0].clientY;
    }, { passive: true });

    window.addEventListener("touchend", e => {
        const diff = startY - e.changedTouches[0].clientY;
        if (Math.abs(diff) < 70) return;

        if (diff > 0) navigate(true);
        else navigate(false);
    });
});

const reveal = document.getElementById("pageReveal");

document.querySelectorAll(".card-link").forEach(link => {

    link.addEventListener("click", function(e) {

        e.preventDefault();

        const url = this.href;

        // start animation
        reveal.classList.add("active");

        // navigate fast
        setTimeout(() => {
            window.location.href = url;
        }, 420);

    });

});