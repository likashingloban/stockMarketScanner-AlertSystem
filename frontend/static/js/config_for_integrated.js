/**
 * Frontend Config - For Integrated Deployment
 * Use this when frontend is served by Flask
 */

const CONFIG = {
    // API Base URL - Same origin (no CORS needed)
    API_BASE_URL: '/api',

    API_ENDPOINTS: {
        // Authentication
        REGISTER: '/auth/register',
        LOGIN: '/auth/login',

        // Watchlist
        WATCHLIST: '/watchlist',

        // Stock Data
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
 * API request helper
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
        console.error('API Error:', error);
        throw error;
    }
}

/**
 * Local storage helper
 */
const Storage = {
    saveUser(user) {
        localStorage.setItem('user', JSON.stringify(user));
    },

    getUser() {
        const user = localStorage.getItem('user');
        return user ? JSON.parse(user) : null;
    },

    clearUser() {
        localStorage.removeItem('user');
    },

    isLoggedIn() {
        return this.getUser() !== null;
    }
};

/**
 * Navigation helper
 */
const Navigation = {
    toLogin() {
        window.location.href = '/';
    },

    toRegister() {
        window.location.href = '/register';
    },

    toDashboard() {
        window.location.href = '/dashboard';
    },

    toWatchlist() {
        window.location.href = '/watchlist';
    },

    toStockDetail(symbol) {
        window.location.href = `/stock-detail?symbol=${symbol}`;
    },

    toAlerts() {
        window.location.href = '/alerts';
    }
};

/**
 * Auth check
 */
function checkAuth() {
    if (!Storage.isLoggedIn()) {
        alert('Please login first');
        Navigation.toLogin();
        return false;
    }
    return true;
}

/**
 * Message helpers
 */
function showError(message) {
    alert(`Error: ${message}`);
}

function showSuccess(message) {
    alert(`Success: ${message}`);
}
