class MedRAGClient {
    static async handleResponse(response) {
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.message || 'Request failed');
        }
        return await response.json();
    }

    static async uploadFile(projectId, file) {
        const formData = new FormData();
        formData.append('file', file);
        
        const response = await fetch(`/base/data/upload/${projectId}`, {
            method: 'POST',
            body: formData
        });
        return this.handleResponse(response);
    }

    static async processFiles(projectId, config) {
        const response = await fetch(`/base/data/process/${projectId}`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(config)
        });
        return this.handleResponse(response);
    }

    static async searchIndex(projectId, query) {
        const response = await fetch(`/api/nlp/index/search/${projectId}`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({text: query, limit: 5})
        });
        return this.handleResponse(response);
    }
}

// DOM Ready
document.addEventListener('DOMContentLoaded', () => {
    // Initialize mobile menu
    const menuToggle = document.querySelector('.menu-toggle');
    const navLinks = document.querySelector('.nav-links');
    
    if (menuToggle && navLinks) {
        menuToggle.addEventListener('click', () => {
            navLinks.classList.toggle('active');
        });
        
        // Close menu when clicking outside
        document.addEventListener('click', (e) => {
            if (!navLinks.contains(e.target) && !menuToggle.contains(e.target)) {
                navLinks.classList.remove('active');
            }
        });
    }
    
    // Initialize any UI components
    console.log('MED-RAG Frontend Initialized');
    
    // Add form submit handlers dynamically
    document.getElementById('uploadForm')?.addEventListener('submit', async (e) => {
        e.preventDefault();
        const form = e.target;
        const statusDiv = document.getElementById('uploadStatus');
        
        try {
            statusDiv.innerHTML = '<div class="alert info">Uploading...</div>';
            const result = await MedRAGClient.uploadFile(
                form.project_id.value,
                form.file.files[0]
            );
            
            statusDiv.innerHTML = `
                <div class="alert success">
                    ${result['File uploaded successfully']}<br>
                    File ID: ${result.file_id}<br>
                    Project ID: ${result.project_id}
                </div>
            `;
            form.reset();
        } catch (error) {
            statusDiv.innerHTML = `<div class="alert error">Error: ${error.message}</div>`;
        }
    });
});