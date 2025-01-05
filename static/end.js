const buttons = document.querySelectorAll('.categorys-btn');
const divs = document.querySelectorAll('.categorys-btn-div');
let isClicked = null;

buttons.forEach(button => {
    const targetId = button.getAttribute('data-target');

    button.addEventListener('mouseover', () => {
        if (isClicked !== targetId) {
            hideAllDivs();
            deactivateAllButtons();
            document.getElementById(targetId).style.display = 'flex';
        }
    });

    button.addEventListener('mouseout', () => {
        if (isClicked !== targetId) {
            hideAllDivs();
            deactivateAllButtons();
        }
    });

    button.addEventListener('click', () => {
        if (isClicked === targetId) {
            hideAllDivs();
            deactivateAllButtons();
            isClicked = null;
        } else {
            hideAllDivs();
            deactivateAllButtons();
            document.getElementById(targetId).style.display = 'flex';
            button.classList.add('active');
            isClicked = targetId;
        }
    });
});

function hideAllDivs() {
    divs.forEach(div => {
        div.style.display = 'none';
    });
}

function deactivateAllButtons() {
    buttons.forEach(button => {
        button.classList.remove('active');
    });
}



const scrollableDiv = document.getElementById("product-section");
const sections = document.querySelectorAll("section");
const navLinks = document.querySelectorAll("#categoryMenu a");
let lastActiveSection = ""; // Variable to store the last active section ID

// Scroll event listener on the scrollable div
scrollableDiv.addEventListener("scroll", () => {
    let currentSection = null; // Default to null if no section is in the viewport

    // Loop through sections to determine which is active
    sections.forEach((section) => {
        const sectionTop = section.offsetTop - scrollableDiv.scrollTop - 125; // Top position relative to scroll
        const sectionBottom = sectionTop + section.clientHeight; // Bottom position relative to scroll

        // Check if the section is currently in view
        if (sectionTop <= 0 && sectionBottom > 0) {
            currentSection = section.getAttribute("id");
        }
    });

    // If no section is active, retain the last active one
    if (!currentSection) {
        currentSection = lastActiveSection;
    } else {
        lastActiveSection = currentSection; // Update the last active section
    }

    // Update active class on navigation links
    navLinks.forEach((link) => {
        link.classList.remove("active");
        if (link.getAttribute("href").substring(1) === currentSection) {
            link.classList.add("active");

            // Scroll leftDiv to keep the active link in view
            link.scrollIntoView({ behavior: "auto", block: "center" });
        }
    });
});

// const tabs = document.getElementById("mynavbar");
// const tabs_li = tabs.querySelectorAll('li a');

// tabs_li.forEach((li) => {
//     li.addEventListener('click', () => {
//         tabs_li.forEach((p) => p.classList.remove('active'));
//         li.classList.add('active');
//     })
// })