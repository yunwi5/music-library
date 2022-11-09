// JS logic to close the flash message if the user clicks the "X" button
function closeFlashMessage(closeBtn) {
    const flashContainer = closeBtn.parentElement;
    if (flashContainer) {
        flashContainer.style.display = 'none';
    }
}
