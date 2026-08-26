/**
 * Embeddable Website AI Chatbot Widget
 * One-line integration script for external client websites.
 */
(function () {
  const currentScript = document.currentScript || (function() {
    const scripts = document.getElementsByTagName('script');
    return scripts[scripts.length - 1];
  })();

  const botId = currentScript ? currentScript.getAttribute('data-bot-id') || 'widget_default' : 'widget_default';
  const apiBase = currentScript && currentScript.src ? new URL(currentScript.src).origin : 'http://127.0.0.1:8000';

  // Inject Styles
  const style = document.createElement('style');
  style.innerHTML = `
    .ai-widget-fab {
      position: fixed;
      bottom: 24px;
      right: 24px;
      width: 60px;
      height: 60px;
      border-radius: 50%;
      background: linear-gradient(135deg, #3b82f6, #8b5cf6);
      color: #fff;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      box-shadow: 0 8px 24px rgba(59, 130, 246, 0.4);
      z-index: 999999;
      transition: all 0.3s ease;
    }
    .ai-widget-fab:hover {
      transform: scale(1.08);
      box-shadow: 0 12px 30px rgba(59, 130, 246, 0.6);
    }
    .ai-widget-box {
      position: fixed;
      bottom: 96px;
      right: 24px;
      width: 380px;
      height: 520px;
      background: #0f172a;
      border: 1px solid #1e293b;
      border-radius: 16px;
      box-shadow: 0 20px 40px rgba(0,0,0,0.6);
      display: none;
      flex-direction: column;
      overflow: hidden;
      z-index: 999999;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    .ai-widget-box.open {
      display: flex;
      animation: aiWidgetPop 0.25s ease-out;
    }
    @keyframes aiWidgetPop {
      from { opacity: 0; transform: translateY(12px) scale(0.96); }
      to { opacity: 1; transform: translateY(0) scale(1); }
    }
    .ai-widget-header {
      background: linear-gradient(135deg, #1e293b, #0f172a);
      padding: 16px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      border-bottom: 1px solid #334155;
      color: #f8fafc;
    }
    .ai-widget-title {
      font-weight: 600;
      font-size: 15px;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .ai-widget-status {
      width: 8px;
      height: 8px;
      background: #10b981;
      border-radius: 50%;
      box-shadow: 0 0 8px #10b981;
    }
    .ai-widget-messages {
      flex: 1;
      padding: 16px;
      overflow-y: auto;
      display: flex;
      flex-direction: column;
      gap: 12px;
      background: #090e17;
    }
    .ai-msg {
      max-width: 82%;
      padding: 10px 14px;
      border-radius: 12px;
      font-size: 13.5px;
      line-height: 1.45;
      word-break: break-word;
    }
    .ai-msg-bot {
      background: #1e293b;
      color: #f1f5f9;
      align-self: flex-start;
      border: 1px solid #334155;
    }
    .ai-msg-user {
      background: #3b82f6;
      color: #ffffff;
      align-self: flex-end;
    }
    .ai-widget-footer {
      padding: 12px;
      background: #0f172a;
      border-top: 1px solid #1e293b;
      display: flex;
      gap: 8px;
    }
    .ai-widget-input {
      flex: 1;
      background: #1e293b;
      border: 1px solid #334155;
      border-radius: 8px;
      padding: 10px 12px;
      color: #fff;
      font-size: 13px;
      outline: none;
    }
    .ai-widget-input:focus {
      border-color: #3b82f6;
    }
    .ai-widget-send {
      background: #3b82f6;
      border: none;
      color: #fff;
      padding: 0 16px;
      border-radius: 8px;
      cursor: pointer;
      font-weight: 500;
    }
  `;
  document.head.appendChild(style);

  // Build DOM
  const fab = document.createElement('div');
  fab.className = 'ai-widget-fab';
  fab.innerHTML = `
    <svg width="28" height="28" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"/>
    </svg>
  `;

  const box = document.createElement('div');
  box.className = 'ai-widget-box';
  box.innerHTML = `
    <div class="ai-widget-header">
      <div class="ai-widget-title">
        <span class="ai-widget-status"></span>
        <span>AI SaaS Assistant</span>
      </div>
      <div style="cursor:pointer; color:#94a3b8;" id="ai-widget-close">✕</div>
    </div>
    <div class="ai-widget-messages" id="ai-widget-msg-list">
      <div class="ai-msg ai-msg-bot">👋 Hello! How can I assist you with our AI SaaS platform today?</div>
    </div>
    <div class="ai-widget-footer">
      <input type="text" class="ai-widget-input" id="ai-widget-text" placeholder="Type a message...">
      <button class="ai-widget-send" id="ai-widget-btn">Send</button>
    </div>
  `;

  document.body.appendChild(fab);
  document.body.appendChild(box);

  // Event Listeners
  fab.addEventListener('click', () => box.classList.toggle('open'));
  box.querySelector('#ai-widget-close').addEventListener('click', () => box.classList.remove('open'));

  const msgList = box.querySelector('#ai-widget-msg-list');
  const input = box.querySelector('#ai-widget-text');
  const sendBtn = box.querySelector('#ai-widget-btn');

  async function handleSend() {
    const text = input.value.trim();
    if (!text) return;

    // User Message
    const userDiv = document.createElement('div');
    userDiv.className = 'ai-msg ai-msg-user';
    userDiv.textContent = text;
    msgList.appendChild(userDiv);
    input.value = '';
    msgList.scrollTop = msgList.scrollHeight;

    // Bot Typing Indicator
    const typingDiv = document.createElement('div');
    typingDiv.className = 'ai-msg ai-msg-bot';
    typingDiv.innerHTML = '<em>Thinking...</em>';
    msgList.appendChild(typingDiv);
    msgList.scrollTop = msgList.scrollHeight;

    try {
      const res = await fetch(`${apiBase}/api/widget/message`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ bot_id: botId, message: text })
      });
      const data = await res.json();
      typingDiv.innerHTML = data.reply || 'Thanks for reaching out! A representative will connect with you.';
    } catch (e) {
      typingDiv.innerHTML = '⚡ Our AI assistant is ready to help. You can also contact support directly!';
    }
    msgList.scrollTop = msgList.scrollHeight;
  }

  sendBtn.addEventListener('click', handleSend);
  input.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') handleSend();
  });
})();
