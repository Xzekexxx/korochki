
class NotificationSystem {
    constructor() {
        this.container = null;
        this.init();
    }

    init() {

        this.container = document.createElement('div');
        this.container.id = 'notification-container';
        this.container.style.cssText = `
            position: fixed;
            top: 100px;
            right: 20px;
            z-index: 9999;
        `;
        document.body.appendChild(this.container);

        this.checkForMessages();
    }

    show(message, type = 'info', duration = 5000) {
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.style.cssText = `
            padding: 15px 25px;
            border-radius: 10px;
            color: white;
            font-weight: 500;
            margin-bottom: 10px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.3);
            animation: slideIn 0.5s ease;
            display: flex;
            align-items: center;
            gap: 10px;
        `;

        let icon = '';
        switch(type) {
            case 'success':
                icon = '<i class="fas fa-check-circle"></i>';
                break;
            case 'error':
                icon = '<i class="fas fa-exclamation-circle"></i>';
                break;
            case 'info':
                icon = '<i class="fas fa-info-circle"></i>';
                break;
        }

        notification.innerHTML = `${icon} ${message}`;
        this.container.appendChild(notification);

        setTimeout(() => {
            notification.style.animation = 'fadeOut 0.5s ease';
            setTimeout(() => {
                notification.remove();
            }, 500);
        }, duration);
    }

    success(message, duration = 5000) {
        this.show(message, 'success', duration);
    }

    error(message, duration = 5000) {
        this.show(message, 'error', duration);
    }

    info(message, duration = 5000) {
        this.show(message, 'info', duration);
    }

    checkForMessages() {

        const successMsg = document.querySelector('[data-success-message]');
        const errorMsg = document.querySelector('[data-error-message]');

        if (successMsg) {
            this.success(successMsg.dataset.successMessage);
        }
        if (errorMsg) {
            this.error(errorMsg.dataset.errorMessage);
        }
    }
}

function filterByStatus(status) {
    const url = new URL(window.location.href);
    if (status && status !== 'all') {
        url.searchParams.set('status', status);
    } else {
        url.searchParams.delete('status');
    }
    window.location.href = url.toString();
}

function searchApplications() {
    const searchText = document.getElementById('search-input')?.value;
    const url = new URL(window.location.href);
    if (searchText) {
        url.searchParams.set('search', searchText);
    } else {
        url.searchParams.delete('search');
    }
    window.location.href = url.toString();
}

function goToPage(page) {
    const url = new URL(window.location.href);
    url.searchParams.set('page', page);
    window.location.href = url.toString();
}

document.addEventListener('DOMContentLoaded', () => {
    window.notifications = new NotificationSystem();
});
