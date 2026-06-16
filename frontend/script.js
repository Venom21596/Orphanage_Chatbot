const BACKEND = "http://127.0.0.1:5000/chat";
let depth = 0;

/* ── UTILITIES ── */
function getTime() {
  return new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

function scroll() {
  const box = document.getElementById('chat-box');
  box.scrollTo({ top: box.scrollHeight, behavior: 'smooth' });
}

function updateProgress() {
  depth = Math.min(depth + 1, 10);
  document.getElementById('progress').style.width = (depth * 10) + '%';
}

function showToast(msg) {
  const t = document.getElementById('toast');
  t.textContent = msg;
  t.style.display = 'block';
  clearTimeout(t._timer);
  t._timer = setTimeout(() => { t.style.display = 'none'; }, 2800);
}

/* ── MESSAGES ── */
function addBotMsg(text) {
  const box = document.getElementById('chat-box');
  const wrap = document.createElement('div');
  wrap.className = 'msg-wrap';
  wrap.innerHTML = `
    <div class="msg-avatar">🤖</div>
    <div>
      <div class="bubble bot">${text}<div class="meta">${getTime()}</div></div>
      <div class="reaction-bar">
        <button class="reaction-btn" onclick="this.textContent='👍✓'; this.style.color='#2563eb'" title="Helpful">👍</button>
        <button class="reaction-btn" onclick="this.textContent='❤️✓'" title="Love">❤️</button>
        <button class="reaction-btn" onclick="showToast('🙏 Thank you for your feedback!')" title="Thanks">🙏</button>
      </div>
    </div>`;
  box.appendChild(wrap);
  scroll();
}

function addUserMsg(text) {
  const box = document.getElementById('chat-box');
  const wrap = document.createElement('div');
  wrap.className = 'msg-wrap user';
  wrap.innerHTML = `<div class="bubble user">${text}<div class="meta">${getTime()}</div></div>`;
  box.appendChild(wrap);
  scroll();
}

/* ── TYPING INDICATOR ── */
function showTyping() {
  const box = document.getElementById('chat-box');
  const wrap = document.createElement('div');
  wrap.id = 'typing';
  wrap.className = 'typing-wrap';
  wrap.innerHTML = `
    <div class="msg-avatar">🤖</div>
    <div class="typing-bubble">
      <div class="dot"></div>
      <div class="dot"></div>
      <div class="dot"></div>
    </div>`;
  box.appendChild(wrap);
  scroll();
}

function removeTyping() {
  const el = document.getElementById('typing');
  if (el) el.remove();
}

/* ── OPTION BUTTONS ── */
function renderOptions(opts) {
  const div = document.getElementById('options');
  div.innerHTML = '';
  if (!opts || !opts.length) return;

  opts.forEach(opt => {
    const btn = document.createElement('button');
    btn.className = 'opt-btn'
      + (opt.toLowerCase().includes('donat')  ? ' donate' : '')
      + (opt.toLowerCase().includes('volunt') ? ' vol'    : '')
      + (opt === 'Back'                        ? ' back'   : '');
    btn.textContent = opt;
    btn.onclick = () => send(opt);
    div.appendChild(btn);
  });
}

/* ── KEYWORD MAPPING ── */
function mapKeyword(text) {
  const m = text.toLowerCase();
  if (/donat|help|support|contribut|fund/i.test(m))      return 'Donate';
  if (/volunte|teach|mentor|work with/i.test(m))          return 'Volunteer';
  if (/about|who are|orphanage|sneha|jyoth/i.test(m))     return 'About Us';
  if (/what do|services|activities|care|provide/i.test(m)) return 'What We Do';
  if (/contact|phone|email|address|reach|location/i.test(m)) return 'Contact Info';
  if (/back|menu/i.test(m))                               return 'Back';
  if (/restart|start again|reset/i.test(m))               return 'Restart Chatbot';
  return text;
}

/* ── SEND MESSAGE ── */
function send(message) {
  if (!message) return;

  if (message === 'Restart Chatbot') {
    document.getElementById('chat-box').innerHTML = '<div class="date-divider">Today</div>';
    document.getElementById('options').innerHTML = '';
    depth = 0;
    document.getElementById('progress').style.width = '0%';
  }

  addUserMsg(message);
  renderOptions([]);
  showTyping();
  updateProgress();

  fetch(BACKEND, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message })
  })
  .then(r => r.json())
  .then(data => {
    const delay = 500 + Math.min((data.message || '').length * 12, 800);
    setTimeout(() => {
      removeTyping();
      if (data.message) addBotMsg(data.message);
      if (data.options)  renderOptions(data.options);
    }, delay);
  })
  .catch(() => {
    removeTyping();
    addBotMsg('⚠️ Backend not running. Please start the Flask server.');
  });
}

/* ── INPUT EVENTS ── */
window.onload = () => {
  const input = document.getElementById('user-input');
  const btn   = document.getElementById('send-btn');

  btn.onclick = () => {
    const text = input.value.trim();
    if (!text) return;
    input.value = '';
    send(mapKeyword(text));
  };

  input.addEventListener('keypress', e => {
    if (e.key === 'Enter') btn.click();
  });
};

/* ── WIDGET OPEN / CLOSE ── */
function openChat() {
  document.getElementById('fab-badge').style.display = 'none';
  document.getElementById('fab').style.display = 'none';

  const w = document.getElementById('widget');
  w.classList.remove('closing');
  w.style.display = 'flex';
  void w.offsetWidth; // force reflow for animation
  w.classList.add('open');

  // Auto-start the bot
  if (!document.querySelector('.bubble')) {
    fetch(BACKEND, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: 'start' })
    })
    .then(r => r.json())
    .then(data => {
      if (data.message) addBotMsg(data.message);
      if (data.options)  renderOptions(data.options);
    })
    .catch(() => {
      addBotMsg("👋 Welcome to Sneha Jyothi Orphan Children's Home 💙\nHow can I help you today?");
      renderOptions(['About Us', 'What We Do', 'Donate', 'Volunteer', 'Contact Info']);
    });
  }
}

function closeChat() {
  const w = document.getElementById('widget');
  w.classList.add('closing');
  setTimeout(() => {
    w.style.display = 'none';
    w.classList.remove('open', 'closing');
    document.getElementById('fab').style.display = 'flex';
  }, 200);
}

function minimizeChat() {
  closeChat();
  showToast('💬 Chat minimized — click the icon to reopen');
}