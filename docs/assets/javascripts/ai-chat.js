document.addEventListener('DOMContentLoaded', () => {
    // Inject HTML Structure
    const chatHTML = `
    <div id="ai-chat-container">
        <div id="ai-chat-window">
            <div id="ai-chat-header">
                <span>Page AI Assistant</span>
                <div id="ai-chat-header-actions">
                    <button class="ai-chat-icon-btn" id="ai-chat-settings-btn" title="Settings">
                        <svg viewBox="0 0 24 24"><path d="M19.14,12.94c0.04-0.3,0.06-0.61,0.06-0.94c0-0.32-0.02-0.64-0.06-0.94l2.03-1.58c0.18-0.14,0.23-0.41,0.12-0.61 l-1.92-3.32c-0.12-0.22-0.37-0.29-0.59-0.22l-2.39,0.96c-0.5-0.38-1.03-0.7-1.62-0.94L14.4,2.81c-0.04-0.24-0.24-0.41-0.48-0.41 h-3.84c-0.24,0-0.43,0.17-0.47,0.41L9.25,5.35C8.66,5.59,8.12,5.92,7.63,6.29L5.24,5.33c-0.22-0.08-0.47,0-0.59,0.22L2.73,8.87 C2.62,9.08,2.66,9.34,2.86,9.48l2.03,1.58C4.84,11.36,4.8,11.69,4.8,12s0.02,0.64,0.06,0.94l-2.03,1.58 c-0.18,0.14-0.23,0.41-0.12,0.61l1.92,3.32c0.12,0.22,0.37,0.29,0.59,0.22l2.39-0.96c0.5,0.38,1.03,0.7,1.62,0.94l0.36,2.54 c0.05,0.24,0.24,0.41,0.48,0.41h3.84c0.24,0,0.43-0.17,0.47-0.41l0.36-2.54c0.59-0.24,1.13-0.56,1.62-0.94l2.39,0.96 c0.22,0.08,0.47,0,0.59-0.22l1.92-3.32c0.12-0.22,0.07-0.49-0.12-0.61L19.14,12.94z M12,15.6c-1.98,0-3.6-1.62-3.6-3.6 s1.62-3.6,3.6-3.6s3.6,1.62,3.6,3.6S13.98,15.6,12,15.6z"/></svg>
                    </button>
                    <button class="ai-chat-icon-btn" id="ai-chat-close-btn" title="Close">
                        <svg viewBox="0 0 24 24"><path d="M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41z"/></svg>
                    </button>
                </div>
            </div>
            <div id="ai-chat-settings">
                <h3>Settings</h3>
                <label for="ai-chat-apikey-input">Kimi API Key (Stored in your browser)</label>
                <input type="password" id="ai-chat-apikey-input" placeholder="sk-..." />
                <button id="ai-chat-settings-save">Save Key</button>
                <p style="font-size:0.8rem; margin-top: 10px; color: #666;">This key is never sent to our servers. It is used directly from your browser to communicate with the Moonshot AI API.</p>
            </div>
            <div id="ai-chat-body">
                <div class="ai-chat-message system">Welcome! I can answer questions about the contents of this specific page.</div>
            </div>
            <div id="ai-chat-input-area">
                <input type="text" id="ai-chat-input" placeholder="Ask a question..." autocomplete="off"/>
                <button id="ai-chat-send">
                    <svg viewBox="0 0 24 24"><path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/></svg>
                </button>
            </div>
        </div>
        <div id="ai-chat-toggle" title="Ask AI">
            <svg viewBox="0 0 24 24"><path d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm-2 12H6v-2h12v2zm0-3H6V9h12v2zm0-3H6V6h12v2z"/></svg>
        </div>
    </div>`;

    document.body.insertAdjacentHTML('beforeend', chatHTML);

    const toggleBtn = document.getElementById('ai-chat-toggle');
    const closeBtn = document.getElementById('ai-chat-close-btn');
    const settingsBtn = document.getElementById('ai-chat-settings-btn');
    const chatWindow = document.getElementById('ai-chat-window');
    const settingsView = document.getElementById('ai-chat-settings');
    const apikeyInput = document.getElementById('ai-chat-apikey-input');
    const saveKeyBtn = document.getElementById('ai-chat-settings-save');
    const chatBody = document.getElementById('ai-chat-body');
    const inputField = document.getElementById('ai-chat-input');
    const sendBtn = document.getElementById('ai-chat-send');

    let conversationHistory = [];

    // Load API Key
    let apiKey = localStorage.getItem('kimi_api_key') || '';
    if (apiKey) {
        apikeyInput.value = apiKey;
    } else {
        // Show settings if no key
        settingsView.classList.add('active');
    }

    toggleBtn.addEventListener('click', () => {
        chatWindow.classList.toggle('open');
        if (chatWindow.classList.contains('open')) {
            inputField.focus();
        }
    });

    closeBtn.addEventListener('click', () => {
        chatWindow.classList.remove('open');
    });

    settingsBtn.addEventListener('click', () => {
        settingsView.classList.toggle('active');
    });

    saveKeyBtn.addEventListener('click', () => {
        apiKey = apikeyInput.value.trim();
        localStorage.setItem('kimi_api_key', apiKey);
        settingsView.classList.remove('active');
        if(conversationHistory.length === 0) {
           addMessage("system", "API Key saved. How can I help you?");
        }
    });

    function getPageContext() {
        const article = document.querySelector('article') || document.querySelector('.md-content__inner') || document.body;
        return article.innerText.substring(0, 30000); // Limit context to avoid token limits
    }

    function addMessage(role, text) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `ai-chat-message ${role}`;
        msgDiv.textContent = text;
        chatBody.appendChild(msgDiv);
        chatBody.scrollTop = chatBody.scrollHeight;
    }

    function showTyping() {
        const msgDiv = document.createElement('div');
        msgDiv.className = `ai-chat-message assistant ai-typing-wrapper`;
        msgDiv.id = "ai-typing-indicator";
        msgDiv.innerHTML = `
            <div class="ai-typing-indicator">
                <div class="ai-typing-dot"></div>
                <div class="ai-typing-dot"></div>
                <div class="ai-typing-dot"></div>
            </div>
        `;
        chatBody.appendChild(msgDiv);
        chatBody.scrollTop = chatBody.scrollHeight;
    }

    function removeTyping() {
        const ind = document.getElementById('ai-typing-indicator');
        if(ind) ind.remove();
    }

    async function handleSend() {
        const text = inputField.value.trim();
        if (!text) return;

        if (!apiKey) {
            settingsView.classList.add('active');
            addMessage("system", "Please provide your Kimi API key first.");
            return;
        }

        inputField.value = '';
        addMessage('user', text);
        showTyping();

        // Prepare context on first message
        if (conversationHistory.length === 0) {
            conversationHistory.push({
                role: 'system',
                content: `You are an AI assistant integrated into a documentation page. Use the following page content to accurately answer user queries. Do not make up information if it is not in the text. \n\n--- PAGE CONTENT ---\n${getPageContext()}`
            });
        }

        conversationHistory.push({ role: 'user', content: text });

        try {
            const response = await fetch('https://corsproxy.io/?https://api.kimi.com/coding/v1/chat/completions', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${apiKey}`
                },
                body: JSON.stringify({
                    model: 'moonshot-v1-8k',
                    messages: conversationHistory,
                    temperature: 0.3
                })
            });

            removeTyping();

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                console.error("API Error:", errorData);
                throw new Error(errorData.error?.message || `HTTP ${response.status}`);
            }

            const data = await response.json();
            const reply = data.choices[0].message.content;
            
            conversationHistory.push({ role: 'assistant', content: reply });
            addMessage('assistant', reply);

        } catch (error) {
            removeTyping();
            addMessage('system', `Error: ${error.message}`);
            conversationHistory.pop(); // Remove the user message that failed
        }
    }

    sendBtn.addEventListener('click', handleSend);
    inputField.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') handleSend();
    });
});
