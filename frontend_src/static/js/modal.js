/**
 * Custom Modal Helper
 * Replace browser default alert() and confirm() with Bootstrap modals
 */

const Modal = {
    /**
     * Show alert modal (replaces alert())
     */
    alert(message, title = 'Alert', type = 'info') {
        return new Promise((resolve) => {
            // Remove existing modal if any
            const existingModal = document.getElementById('customAlertModal');
            if (existingModal) {
                existingModal.remove();
            }

            // Icon and color based on type
            const icons = {
                success: '✓',
                error: '✗',
                warning: '⚠',
                info: 'ℹ'
            };

            const colors = {
                success: 'text-success',
                error: 'text-danger',
                warning: 'text-warning',
                info: 'text-primary'
            };

            const icon = icons[type] || icons.info;
            const color = colors[type] || colors.info;

            // Create modal HTML
            const modalHTML = `
                <div class="modal fade" id="customAlertModal" tabindex="-1">
                    <div class="modal-dialog modal-dialog-centered">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title">
                                    <span class="${color} fs-4 me-2">${icon}</span>
                                    ${title}
                                </h5>
                                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                            </div>
                            <div class="modal-body">
                                ${message}
                            </div>
                            <div class="modal-footer">
                                <button type="button" class="btn btn-primary" data-bs-dismiss="modal">OK</button>
                            </div>
                        </div>
                    </div>
                </div>
            `;

            // Add to body
            document.body.insertAdjacentHTML('beforeend', modalHTML);

            // Show modal
            const modalElement = document.getElementById('customAlertModal');
            const modal = new bootstrap.Modal(modalElement);
            modal.show();

            // Cleanup and resolve when closed
            modalElement.addEventListener('hidden.bs.modal', () => {
                modalElement.remove();
                resolve();
            });
        });
    },

    /**
     * Show confirm modal (replaces confirm())
     */
    confirm(message, title = 'Confirm', options = {}) {
        return new Promise((resolve) => {
            // Remove existing modal if any
            const existingModal = document.getElementById('customConfirmModal');
            if (existingModal) {
                existingModal.remove();
            }

            const confirmText = options.confirmText || 'Confirm';
            const cancelText = options.cancelText || 'Cancel';
            const confirmClass = options.confirmClass || 'btn-primary';
            const icon = options.icon || '?';

            // Create modal HTML
            const modalHTML = `
                <div class="modal fade" id="customConfirmModal" tabindex="-1">
                    <div class="modal-dialog modal-dialog-centered">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title">
                                    <span class="fs-4 me-2">${icon}</span>
                                    ${title}
                                </h5>
                                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                            </div>
                            <div class="modal-body">
                                ${message}
                            </div>
                            <div class="modal-footer">
                                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal" id="cancelBtn">
                                    ${cancelText}
                                </button>
                                <button type="button" class="btn ${confirmClass}" id="confirmBtn">
                                    ${confirmText}
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            `;

            // Add to body
            document.body.insertAdjacentHTML('beforeend', modalHTML);

            // Show modal
            const modalElement = document.getElementById('customConfirmModal');
            const modal = new bootstrap.Modal(modalElement);
            modal.show();

            // Handle confirm button
            document.getElementById('confirmBtn').addEventListener('click', () => {
                modal.hide();
                resolve(true);
            });

            // Handle cancel or close
            modalElement.addEventListener('hidden.bs.modal', (e) => {
                if (e.target.id === 'customConfirmModal') {
                    modalElement.remove();
                    // Only resolve false if not already resolved true
                    resolve(false);
                }
            });
        });
    },

    /**
     * Show success message
     */
    success(message, title = 'Success') {
        return this.alert(message, title, 'success');
    },

    /**
     * Show error message
     */
    error(message, title = 'Error') {
        return this.alert(message, title, 'error');
    },

    /**
     * Show warning message
     */
    warning(message, title = 'Warning') {
        return this.alert(message, title, 'warning');
    },

    /**
     * Show info message
     */
    info(message, title = 'Information') {
        return this.alert(message, title, 'info');
    }
};
