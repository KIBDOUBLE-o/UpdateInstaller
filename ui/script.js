/**
 * Update installer.
 *
 * Progress is updated ONLY manually via the public API:
 *   Installer.setProgress(45);
 *   Installer.setStatus('Extracting…');
 *   Installer.showProgress();
 *   Installer.complete();
 *   Installer.reset();
 *
 * No setInterval / setTimeout — the bar never moves on its own.
 *
 * Versions can be set via:
 *   Installer.setVersions('1.0.0', '2.0.0');
 *   Installer.setCurrentVersion('1.0.0');
 *   Installer.setNewVersion('2.0.0');
 *
 * Close button is ALWAYS enabled.
 * While installation is running, closing requires two clicks:
 *   1st click  → button enters confirm state ("Click again to close")
 *   2nd click  → actually closes
 * Confirm state auto-resets if the user clicks elsewhere or presses Esc.
 */

const Installer = (() => {
    'use strict';

    // ===== Defaults =====
    const DEFAULT_CURRENT = '<target_version>';
    const DEFAULT_NEW     = '<source_version>';

    // ===== DOM =====
    const installBtn        = document.getElementById('installBtn');
    const closeBtn          = document.getElementById('closeBtn');
    const progressContainer = document.getElementById('progressContainer');
    const progressFill      = document.getElementById('progressFill');
    const progressPercent   = document.getElementById('progressPercent');
    const progressBar       = document.getElementById('progressBar');
    const statusText        = document.getElementById('statusText');
    const currentVersionEl  = document.getElementById('currentVersion');
    const newVersionEl      = document.getElementById('newVersion');

    // ===== State =====
    let isInstalling = false;
    let isConfirming = false;

    let currentVersion = DEFAULT_CURRENT;
    let newVersion     = DEFAULT_NEW;

    // ===== Versions API =====

    /**
     * Applies a value to a version element with a brief flash animation.
     * @param {HTMLElement} el
     * @param {string} value
     */
    function applyVersion(el, value) {
        el.textContent = value;
        el.classList.remove('is-updated');
        // Force reflow so the animation can be re-triggered
        void el.offsetWidth;
        el.classList.add('is-updated');
    }

    /**
     * Sets the "current" version label.
     * @param {string} value
     */
    function setCurrentVersion(value) {
        currentVersion = (value == null || value === '') ? DEFAULT_CURRENT : String(value);
        applyVersion(currentVersionEl, currentVersion);
        currentVersionEl.title = currentVersion;
    }

    /**
     * Sets the "new" version label.
     * @param {string} value
     */
    function setNewVersion(value) {
        newVersion = (value == null || value === '') ? DEFAULT_NEW : String(value);
        applyVersion(newVersionEl, newVersion);
        newVersionEl.title = newVersion;
    }

    /**
     * Sets both versions at once.
     * @param {string} current
     * @param {string} next
     */
    function setVersions(current, next) {
        setCurrentVersion(current);
        setNewVersion(next);
    }

    /** Returns the currently displayed versions. */
    function getVersions() {
        return {
            current: currentVersion,
            new: newVersion
        };
    }

    // ===== Progress API =====

    /**
     * Sets the progress value (0–100).
     * The bar is NOT updated on its own — only by this call.
     * @param {number} percent
     */
    function setProgress(percent) {
        const value = Math.max(0, Math.min(100, Number(percent) || 0));
        progressFill.style.width = value + '%';
        progressPercent.textContent = Math.round(value) + '%';
        progressBar.setAttribute('aria-valuenow', String(Math.round(value)));

        if (value >= 100) {
            progressFill.classList.add('is-complete');
        } else {
            progressFill.classList.remove('is-complete');
        }
    }

    /**
     * Sets the status text.
     * @param {string} text
     */
    function setStatus(text) {
        statusText.textContent = text ?? '';
    }

    /** Shows the progress block. */
    function showProgress() {
        progressContainer.classList.add('is-visible');
        progressContainer.setAttribute('aria-hidden', 'false');
    }

    /** Hides the progress block. */
    function hideProgress() {
        progressContainer.classList.remove('is-visible');
        progressContainer.setAttribute('aria-hidden', 'true');
    }

    /** Full reset of the installer state. */
    function reset() {
        isInstalling = false;
        clearConfirm();

        hideProgress();
        setProgress(0);
        setStatus('Waiting…');

        installBtn.disabled = false;
        // Close button stays enabled at all times
        closeBtn.disabled = false;
    }

    /** Marks the installation as complete. */
    function complete() {
        isInstalling = false;
        clearConfirm();

        setProgress(100);
        setStatus('Installation complete');

        installBtn.disabled = true;
        // Close button stays enabled at all times
        closeBtn.disabled = false;
        closeBtn.focus();
    }

    // ===== Confirm state for Close button =====

    function enterConfirm() {
        isConfirming = true;
        closeBtn.classList.add('is-confirming');
        closeBtn.textContent = 'Click again to close';
    }

    function clearConfirm() {
        if (!isConfirming) return;
        isConfirming = false;
        closeBtn.classList.remove('is-confirming');
        closeBtn.textContent = 'Close';
    }

    // ===== Button stubs =====

    /**
     * STUB: install button click.
     * Only shows progress and switches the UI into installing mode.
     * Further advancement must be driven manually via Installer.setProgress().
     */
    function onInstallClick() {
        console.log('[stub] install clicked', getVersions());

        isInstalling = true;
        installBtn.disabled = true;

        clearConfirm();
        showProgress();
        setProgress(0);
        setStatus('Preparing…');

        // Real app: backend call via IPC/fetch.
        // Progress will arrive from outside via Installer.setProgress().
        window.pywebview?.api?.start_install?.();
    }

    /**
     * STUB: close button click.
     *
     * Rules:
     *   - Not installing → close immediately.
     *   - Installing     → first click enters confirm state,
     *                      second click closes.
     */
    function onCloseClick() {
        console.log('[stub] close clicked', { isInstalling, isConfirming });

        if (isInstalling && !isConfirming) {
            enterConfirm();
            return;
        }

        // Either not installing, or already confirming — proceed to close
        closeWindow();
    }

    /**
     * STUB: actual window close.
     * In a real app: window.close() or IPC "quit".
     */
    function closeWindow() {
        setStatus('Closing…');
        installBtn.disabled = true;
        closeBtn.disabled = true;

        console.log('[stub] window closes now');

        window.pywebview?.api?.quit?.();
    }

    // ===== Events =====

    installBtn.addEventListener('click', onInstallClick);
    closeBtn.addEventListener('click', onCloseClick);

    // Cancel confirm state if the user clicks elsewhere
    document.addEventListener('click', (e) => {
        if (!isConfirming) return;
        if (e.target === closeBtn) return;
        clearConfirm();
    });

    // Or presses Esc
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && isConfirming) {
            clearConfirm();
        }
    });

    // ===== Initialize versions from data-attributes (optional) =====
    // Usage in HTML:
    //   <main class="installer" data-current-version="1.0.0" data-new-version="2.0.0">
    (function initFromDataAttributes() {
        const root = document.querySelector('.installer');
        if (!root) return;

        const cur = root.dataset.currentVersion;
        const nxt = root.dataset.newVersion;

        if (cur) setCurrentVersion(cur);
        if (nxt) setNewVersion(nxt);
    })();

    // ===== Public interface =====
    return {
        // Progress
        setProgress,
        setStatus,
        showProgress,
        hideProgress,
        reset,
        complete,

        // Versions
        setCurrentVersion,
        setNewVersion,
        setVersions,
        getVersions,

        // Internal handlers — in case they're needed from outside
        onClick: {
            install: onInstallClick,
            close: onCloseClick
        }
    };
})();

// Optional: expose to window for manual control from the console
window.Installer = Installer;