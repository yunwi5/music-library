// JS logic for responsive header search form toggling functionality
const MOBILE_BP = 690; // Mobile screen break point

const header = document.querySelector('#header');
const searchForm = document.querySelector('.search-form');
const headerHeading = document.querySelector('.header__heading');

const searchIcon = document.querySelector('#search-icon');
searchIcon.addEventListener('click', () => {
    if (window.innerWidth >= MOBILE_BP) return;
    searchForm.style.display = 'flex';
    headerHeading.style.display = 'none';
    searchIcon.style.display = 'none';
});

function turnOffSearchMode() {
    headerHeading.style.display = 'block';
    searchForm.style.display = 'none';
    searchIcon.style.display = 'block';
}

window.addEventListener('resize', () => {
    if (window.innerWidth >= MOBILE_BP) {
        headerHeading.style.display = 'block';
        searchForm.style.display = 'flex';
        searchIcon.style.display = 'none';
    } else {
        turnOffSearchMode();
    }
});

window.addEventListener('click', function (e) {
    if (!header.contains(e.target) && window.innerWidth < MOBILE_BP) {
        turnOffSearchMode();
    }
});

// JS logic to close the flash message if the user clicks the "X" button
function closeFlashMessage(closeBtn) {
    const flashContainer = closeBtn.parentElement;
    if (flashContainer) {
        flashContainer.style.display = 'none';
    }
}
