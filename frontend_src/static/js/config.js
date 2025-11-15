/**
 * Frontend Configuration
 * Define API endpoints and global settings
 */

const CONFIG = {
    // API Base URL
    API_BASE_URL: 'http://localhost:5001/api',

    // API Endpoints
    API_ENDPOINTS: {
        // Authentication
        REGISTER: '/auth/register',
        LOGIN: '/auth/login',
        CHANGE_PASSWORD: '/auth/change-password',

        // Watchlist
        WATCHLIST: '/watchlist',

        // Stock Data
        ALL_STOCKS: '/stocks',
        STOCK_DETAIL: '/stock',
        STOCK_HISTORY: '/stock',

        // Alerts
        ALERTS: '/alerts',
        CHECK_ALERTS: '/alerts/check',

        // Dashboard
        DASHBOARD: '/dashboard'
    }
};

/**
 * Send API request helper function
 */
async function apiRequest(endpoint, options = {}) {
    const url = `${CONFIG.API_BASE_URL}${endpoint}`;

    const defaultOptions = {
        headers: {
            'Content-Type': 'application/json'
        }
    };

    const finalOptions = { ...defaultOptions, ...options };

    try {
        const response = await fetch(url, finalOptions);
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Request failed');
        }

        return data;
    } catch (error) {
        console.error('API Request Error:', error);
        throw error;
    }
}

/**
 * Local storage helper
 */
const Storage = {
    // Save user data
    saveUser(user) {
        localStorage.setItem('user', JSON.stringify(user));
    },

    // Get user data
    getUser() {
        const user = localStorage.getItem('user');
        return user ? JSON.parse(user) : null;
    },

    // Clear user data (logout)
    clearUser() {
        localStorage.removeItem('user');
    },

    // Check if logged in
    isLoggedIn() {
        return this.getUser() !== null;
    }
};

/**
 * Navigation helper
 */
const Navigation = {
    toLogin() {
        window.location.href = 'index.html';
    },

    toRegister() {
        window.location.href = 'register.html';
    },

    toDashboard() {
        window.location.href = 'dashboard.html';
    },

    toWatchlist() {
        window.location.href = 'watchlist.html';
    },

    toStockDetail(symbol) {
        window.location.href = `stock-detail.html?symbol=${symbol}`;
    },

    toAlerts() {
        window.location.href = 'alerts.html';
    },

    toSettings() {
        window.location.href = 'settings.html';
    }
};

/**
 * Check authentication status
 */
function checkAuth() {
    if (!Storage.isLoggedIn()) {
        if (typeof Modal !== 'undefined') {
            Modal.warning('Please login first', 'Authentication Required').then(() => {
                Navigation.toLogin();
            });
        } else {
            alert('Please login first');
            Navigation.toLogin();
        }
        return false;
    }
    return true;
}

/**
 * Show error message
 */
function showError(message) {
    if (typeof Modal !== 'undefined') {
        Modal.error(message);
    } else {
        alert(`Error: ${message}`);
    }
}

/**
 * Show success message
 */
function showSuccess(message) {
    if (typeof Modal !== 'undefined') {
        Modal.success(message);
    } else {
        alert(`Success: ${message}`);
    }
}
