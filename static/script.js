// AI Meme Generator Frontend Logic

document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const memeForm = document.getElementById('memeForm');
    const generateBtn = document.getElementById('generateBtn');
    const loading = document.getElementById('loading');
    const error = document.getElementById('error');
    const result = document.getElementById('result');
    const memeImage = document.getElementById('memeImage');
    const templateName = document.getElementById('templateName');
    const topText = document.getElementById('topText');
    const bottomText = document.getElementById('bottomText');
    const downloadLink = document.getElementById('downloadLink');
    const generateAnother = document.getElementById('generateAnother');
    const templateCount = document.getElementById('templateCount');

    // Load template suggestions
    loadTemplateSuggestions();

    // Load stats
    loadStats();

    // Form submission
    memeForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        await generateMeme();
    });

    // Generate another button
    generateAnother.addEventListener('click', function() {
        result.style.display = 'none';
        memeForm.reset();
        document.getElementById('topic').focus();
    });

    /**
     * Generate meme from form data
     */
    async function generateMeme() {
        // Get form data
        const topic = document.getElementById('topic').value.trim();
        const template = document.getElementById('template').value.trim();
        const style = document.getElementById('style').value;

        if (!topic) {
            showError('Please enter a topic for your meme');
            return;
        }

        // Show loading state
        showLoading();

        try {
            // Make API request
            const response = await fetch('/api/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    topic: topic,
                    template_name: template || null,
                    style: style,
                    use_imgflip: false
                })
            });

            const data = await response.json();

            if (data.success) {
                // Display the generated meme
                displayMeme(data);
            } else {
                showError(data.error || 'Failed to generate meme');
            }

        } catch (err) {
            console.error('Error generating meme:', err);
            showError('Network error. Please check your connection and try again.');
        }
    }

    /**
     * Display generated meme
     */
    function displayMeme(data) {
        loading.style.display = 'none';
        error.style.display = 'none';

        // Update meme image
        memeImage.src = data.meme_url;
        memeImage.alt = `${data.template.name} meme`;

        // Update meme info
        templateName.textContent = data.template.name;
        topText.textContent = data.caption.top_text || '(none)';
        bottomText.textContent = data.caption.bottom_text || '(none)';

        // Update download link
        downloadLink.href = data.meme_url;
        downloadLink.download = `meme_${Date.now()}.jpg`;

        // Show result with animation
        result.style.display = 'block';
        result.classList.add('fade-in');
    }

    /**
     * Show loading state
     */
    function showLoading() {
        error.style.display = 'none';
        result.style.display = 'none';
        loading.style.display = 'block';
        generateBtn.disabled = true;
    }

    /**
     * Show error message
     */
    function showError(message) {
        loading.style.display = 'none';
        result.style.display = 'none';
        error.style.display = 'block';
        error.textContent = message;
        generateBtn.disabled = false;
    }

    /**
     * Load template suggestions for autocomplete
     */
    async function loadTemplateSuggestions() {
        try {
            const response = await fetch('/api/templates?limit=100');
            const data = await response.json();

            if (data.success) {
                const datalist = document.getElementById('templateSuggestions');
                data.templates.forEach(template => {
                    const option = document.createElement('option');
                    option.value = template.name;
                    datalist.appendChild(option);
                });
            }
        } catch (err) {
            console.error('Error loading template suggestions:', err);
        }
    }

    /**
     * Load application stats
     */
    async function loadStats() {
        try {
            const response = await fetch('/api/health');
            const data = await response.json();

            if (data.status === 'healthy') {
                templateCount.textContent = data.templates_loaded;
            } else {
                templateCount.textContent = 'N/A';
            }
        } catch (err) {
            console.error('Error loading stats:', err);
            templateCount.textContent = 'N/A';
        }
    }

    // Re-enable button after loading completes
    memeImage.addEventListener('load', function() {
        generateBtn.disabled = false;
    });

    memeImage.addEventListener('error', function() {
        generateBtn.disabled = false;
        showError('Failed to load meme image');
    });
});
