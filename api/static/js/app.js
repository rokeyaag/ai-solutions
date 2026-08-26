/**
 * NexusAI - SaaS Dashboard Application Frontend Controller
 * Enterprise-grade, bulletproof script with full global bindings and fallbacks.
 */

let serviceChartInstance = null;
let ratioChartInstance = null;
let csvChartInstance = null;
let currentActivePersona = 'software_architect';

const tabTitles = {
  'tab-overview': '<i class="fa-solid fa-chart-pie text-blue-400"></i> Overview & Token Dashboard',
  'tab-chat': '<i class="fa-solid fa-comments text-indigo-400"></i> Multi-Persona AI Chatbot',
  'tab-rag': '<i class="fa-solid fa-file-shield text-cyan-400"></i> Document RAG Studio',
  'tab-copy': '<i class="fa-solid fa-pen-fancy text-pink-400"></i> Copywriting & SEO Suite',
  'tab-vision': '<i class="fa-solid fa-wand-magic-sparkles text-purple-400"></i> AI Vision & OCR Studio',
  'tab-audio': '<i class="fa-solid fa-microphone-lines text-emerald-400"></i> Voice & Audio AI',
  'tab-code': '<i class="fa-solid fa-code text-amber-400"></i> Code Copilot & CSV Visualizer',
  'tab-research': '<i class="fa-solid fa-robot text-teal-400"></i> Autonomous Research Agent',
  'tab-widget': '<i class="fa-solid fa-puzzle-piece text-sky-400"></i> Embeddable Website Widget',
  'tab-settings': '<i class="fa-solid fa-sliders text-slate-400"></i> API Settings & Multi-Model Engine'
};

// ==========================================
// 1. GLOBAL TAB SWITCHING LOGIC
// ==========================================
function switchTab(tabId) {
  try {
    // Hide all tab contents
    document.querySelectorAll('.tab-content').forEach(tab => {
      tab.classList.remove('active');
      tab.style.display = 'none';
    });

    // Reset all navigation button styles
    document.querySelectorAll('.nav-item').forEach(btn => {
      btn.classList.remove('active-tab', 'bg-blue-600/15', 'text-blue-400', 'border', 'border-blue-500/30');
      btn.classList.add('text-slate-300');
    });

    // Activate the targeted tab
    const targetTab = document.getElementById(tabId);
    const navBtn = document.getElementById(`nav-${tabId}`);

    if (targetTab) {
      targetTab.classList.add('active');
      targetTab.style.display = 'block';
    }

    if (navBtn) {
      navBtn.classList.add('active-tab', 'bg-blue-600/15', 'text-blue-400', 'border', 'border-blue-500/30');
      navBtn.classList.remove('text-slate-300');
    }

    // Update Header Title
    const titleElem = document.getElementById('current-tab-title');
    if (titleElem && tabTitles[tabId]) {
      titleElem.innerHTML = tabTitles[tabId];
    }

    if (tabId === 'tab-overview') {
      refreshDashboardMetrics();
    }
  } catch (err) {
    console.error('Error switching tab:', err);
  }
}

// ==========================================
// 2. DASHBOARD CHARTS (SAFE INITIALIZER)
// ==========================================
function initDashboardCharts() {
  try {
    if (typeof Chart === 'undefined') {
      console.warn('Chart.js not yet loaded, retrying in 500ms...');
      setTimeout(initDashboardCharts, 500);
      return;
    }

    const ctxService = document.getElementById('chart-service-usage');
    if (ctxService && !serviceChartInstance) {
      serviceChartInstance = new Chart(ctxService, {
        type: 'bar',
        data: {
          labels: ['Multi-Persona Chat', 'Document RAG', 'Copywriting & SEO', 'Code Copilot', 'Research Agent', 'Vision & OCR'],
          datasets: [{
            label: 'Tokens Consumed',
            data: [12450, 8320, 4120, 3280, 2100, 800],
            backgroundColor: ['#6366f1', '#06b6d4', '#ec4899', '#f59e0b', '#14b8a6', '#a855f7'],
            borderRadius: 6
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { display: false } },
          scales: {
            x: { grid: { color: '#1e293b' }, ticks: { color: '#94a3b8', font: { size: 11 } } },
            y: { grid: { color: '#1e293b' }, ticks: { color: '#94a3b8', font: { size: 11 } } }
          }
        }
      });
    }

    const ctxRatio = document.getElementById('chart-token-ratio');
    if (ctxRatio && !ratioChartInstance) {
      ratioChartInstance = new Chart(ctxRatio, {
        type: 'doughnut',
        data: {
          labels: ['Prompt Tokens', 'Output Tokens'],
          datasets: [{
            data: [18450, 12620],
            backgroundColor: ['#3b82f6', '#10b981'],
            borderWidth: 0
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { position: 'bottom', labels: { color: '#cbd5e1', font: { size: 11 } } }
          },
          cutout: '70%'
        }
      });
    }
  } catch (e) {
    console.warn('Dashboard chart initialization notice:', e);
  }
}

async function refreshDashboardMetrics() {
  try {
    const res = await fetch('/api/dashboard/metrics');
    if (!res.ok) return;
    const data = await res.json();

    const elTokens = document.getElementById('header-total-tokens');
    const elCost = document.getElementById('header-total-cost');
    const elReq = document.getElementById('card-requests');
    const elCardTokens = document.getElementById('card-tokens');
    const elCardCost = document.getElementById('card-cost');

    if (elTokens) elTokens.textContent = Number(data.total_tokens || 31070).toLocaleString();
    if (elCost) elCost.textContent = `$${data.estimated_cost_usd || 0.0482}`;
    if (elReq) elReq.textContent = data.total_requests || 42;
    if (elCardTokens) elCardTokens.textContent = Number(data.total_tokens || 31070).toLocaleString();
    if (elCardCost) elCardCost.textContent = `$${data.estimated_cost_usd || 0.0482}`;

    // Render Activity Stream
    const listElem = document.getElementById('activity-stream-list');
    if (listElem && data.recent_activities) {
      listElem.innerHTML = data.recent_activities.map(act => `
        <div class="p-3.5 flex items-center justify-between hover:bg-slate-800/30 transition text-xs">
          <div class="flex items-center gap-3">
            <span class="w-2 h-2 rounded-full bg-emerald-400"></span>
            <div>
              <span class="font-semibold text-white">[${act.service}]</span>
              <span class="text-slate-300 ml-1">${act.action}</span>
            </div>
          </div>
          <div class="flex items-center gap-4 text-slate-400 font-mono text-[11px]">
            <span>${act.tokens} tokens</span>
            <span class="text-indigo-400">${act.latency_ms}ms</span>
            <span class="text-slate-500">${act.timestamp}</span>
          </div>
        </div>
      `).join('');
    }
  } catch (err) {
    console.warn('Metrics refresh failed:', err);
  }
}

// ==========================================
// 3. MULTI-PERSONA CHATBOT
// ==========================================
function initPersonas() {
  const container = document.getElementById('persona-buttons-container');
  if (!container) return;

  const personas = [
    { id: 'software_architect', name: 'Software Architect', icon: 'fa-sitemap' },
    { id: 'business_consultant', name: 'Business Consultant', icon: 'fa-chart-line' },
    { id: 'seo_copywriter', name: 'SEO & Copywriter', icon: 'fa-pen-nib' },
    { id: 'legal_advisor', name: 'Legal & Compliance', icon: 'fa-scale-balanced' },
    { id: 'ai_engineer', name: 'Senior AI Engineer', icon: 'fa-brain' }
  ];

  container.innerHTML = personas.map((p, idx) => `
    <button type="button" onclick="selectPersona('${p.id}')" id="btn-persona-${p.id}" class="px-3 py-1.5 rounded-lg text-xs font-medium border flex items-center gap-1.5 transition ${idx === 0 ? 'bg-indigo-600/20 text-indigo-400 border-indigo-500/40' : 'bg-slate-800/60 text-slate-400 border-slate-700 hover:text-white'}">
      <i class="fa-solid ${p.icon}"></i> ${p.name}
    </button>
  `).join('');
}

function selectPersona(personaId) {
  currentActivePersona = personaId;
  document.querySelectorAll('[id^="btn-persona-"]').forEach(btn => {
    btn.className = 'px-3 py-1.5 rounded-lg text-xs font-medium border flex items-center gap-1.5 transition bg-slate-800/60 text-slate-400 border-slate-700 hover:text-white';
  });
  const activeBtn = document.getElementById(`btn-persona-${personaId}`);
  if (activeBtn) {
    activeBtn.className = 'px-3 py-1.5 rounded-lg text-xs font-medium border flex items-center gap-1.5 transition bg-indigo-600/20 text-indigo-400 border-indigo-500/40';
  }
  showToast(`Active Persona: ${personaId.replace(/_/g, ' ').toUpperCase()}`);
}

async function sendChatMessage() {
  const input = document.getElementById('chat-input');
  if (!input) return;
  const text = input.value.trim();
  if (!text) return;

  const container = document.getElementById('chat-messages-container');
  if (!container) return;

  // Add User Message
  container.innerHTML += `
    <div class="flex gap-3 max-w-2xl ml-auto justify-end">
      <div class="bg-blue-600 text-white rounded-xl p-4 text-sm leading-relaxed shadow-lg">
        ${escapeHtml(text)}
      </div>
      <div class="w-8 h-8 rounded-lg bg-blue-600/40 text-blue-300 flex items-center justify-center shrink-0 border border-blue-500/30">
        <i class="fa-solid fa-user"></i>
      </div>
    </div>
  `;
  input.value = '';
  container.scrollTop = container.scrollHeight;

  // Loading Indicator
  const loadingId = 'loading-' + Date.now();
  container.innerHTML += `
    <div id="${loadingId}" class="flex gap-3 max-w-2xl">
      <div class="w-8 h-8 rounded-lg bg-indigo-600/30 text-indigo-400 flex items-center justify-center shrink-0 border border-indigo-500/30">
        <i class="fa-solid fa-brain fa-spin"></i>
      </div>
      <div class="bg-slate-800/80 border border-slate-700/60 rounded-xl p-4 text-sm text-slate-400 italic">
        Generating response...
      </div>
    </div>
  `;
  container.scrollTop = container.scrollHeight;

  try {
    const temp = parseFloat(document.getElementById('chat-temp')?.value || '0.7');
    const res = await fetch('/api/chat/send', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ persona: currentActivePersona, message: text, temperature: temp })
    });
    const data = await res.json();
    const loader = document.getElementById(loadingId);
    if (loader) loader.remove();

    container.innerHTML += `
      <div class="flex gap-3 max-w-3xl">
        <div class="w-8 h-8 rounded-lg bg-indigo-600/30 text-indigo-400 flex items-center justify-center shrink-0 border border-indigo-500/30">
          <i class="fa-solid fa-robot"></i>
        </div>
        <div class="bg-slate-800/80 border border-slate-700/60 rounded-xl p-4 text-xs leading-relaxed text-slate-200 whitespace-pre-wrap">
          ${data.reply}
          <div class="mt-3 pt-2 border-t border-slate-700/50 flex items-center gap-3 text-[10px] text-slate-400 font-mono">
            <span>Model: ${data.model}</span>
            <span>Latency: ${data.latency_ms}ms</span>
            <span>Tokens: ${data.tokens}</span>
          </div>
        </div>
      </div>
    `;
    container.scrollTop = container.scrollHeight;
  } catch (e) {
    const loader = document.getElementById(loadingId);
    if (loader) loader.remove();
    showToast('Failed to reach AI engine', 'error');
  }
}

// ==========================================
// 4. DOCUMENT RAG STUDIO
// ==========================================
async function loadRAGDocuments() {
  try {
    const res = await fetch('/api/rag/documents');
    if (!res.ok) return;
    const data = await res.json();
    const listElem = document.getElementById('rag-document-list');
    if (listElem && data.documents) {
      listElem.innerHTML = data.documents.map(d => `
        <div class="p-2.5 rounded-lg bg-slate-800/60 border border-slate-700 flex items-center justify-between text-xs">
          <div class="flex items-center gap-2 overflow-hidden">
            <i class="fa-solid fa-file-pdf text-red-400 shrink-0"></i>
            <span class="truncate text-slate-200 font-medium">${d.filename}</span>
          </div>
          <span class="text-[10px] text-cyan-400 font-mono shrink-0">${d.chunks_count} chunks</span>
        </div>
      `).join('');
    }
  } catch (err) {
    console.warn('RAG document load failed:', err);
  }
}

async function indexNewDocument() {
  const title = document.getElementById('rag-doc-title')?.value.trim() || 'Custom_Document.txt';
  const content = document.getElementById('rag-doc-content')?.value.trim();
  if (!content) {
    showToast('Please enter document content to index', 'error');
    return;
  }

  const formData = new FormData();
  formData.append('filename', title);
  formData.append('content_text', content);

  try {
    const res = await fetch('/api/rag/upload', { method: 'POST', body: formData });
    const data = await res.json();
    showToast(`Indexed '${data.document.filename}' (${data.document.chunks_count} chunks)!`);
    document.getElementById('rag-doc-content').value = '';
    loadRAGDocuments();
  } catch (e) {
    showToast('Failed to index document', 'error');
  }
}

async function runRAGQuery() {
  const query = document.getElementById('rag-query-input')?.value.trim();
  if (!query) return;

  const answerBox = document.getElementById('rag-answer-display');
  if (answerBox) answerBox.innerHTML = '<span class="text-cyan-400 italic">Searching semantic vector index & calculating similarity scores...</span>';

  try {
    const res = await fetch('/api/rag/query', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query: query, top_k: 3 })
    });
    const data = await res.json();
    if (answerBox) answerBox.innerHTML = `<div class="whitespace-pre-wrap">${data.answer}</div>`;

    const citationsContainer = document.getElementById('rag-citations-container');
    const citationsList = document.getElementById('rag-citations-list');
    
    if (citationsContainer && citationsList && data.citations && data.citations.length > 0) {
      citationsContainer.classList.remove('hidden');
      citationsList.innerHTML = data.citations.map(c => `
        <div class="p-3 rounded-lg bg-slate-800/80 border border-slate-700 text-xs space-y-1">
          <div class="flex justify-between items-center text-[10px] text-cyan-400 font-mono font-semibold">
            <span>${c.filename} (Page ${c.page})</span>
            <span class="px-1.5 py-0.5 rounded bg-cyan-500/20 text-cyan-300">Confidence: ${Math.round(c.score*100)}%</span>
          </div>
          <div class="text-slate-300 text-[11px]">"${c.text}"</div>
        </div>
      `).join('');
    }
  } catch (e) {
    if (answerBox) answerBox.innerHTML = '<span class="text-red-400">RAG query failed</span>';
  }
}

// ==========================================
// 5. COPYWRITING & SEO SUITE
// ==========================================
async function generateCopyContent() {
  const type = document.getElementById('copy-type')?.value || 'blog_post';
  const topic = document.getElementById('copy-topic')?.value || 'AI SaaS Innovation';
  const audience = document.getElementById('copy-audience')?.value || 'B2B Founders';
  const keywords = document.getElementById('copy-keywords')?.value || 'AI, SaaS';

  const outputBox = document.getElementById('copy-output-content');
  if (outputBox) outputBox.textContent = 'Generating SEO-optimized marketing asset...';

  try {
    const res = await fetch('/api/copywriting/generate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ content_type: type, topic, target_audience: audience, keywords })
    });
    const data = await res.json();
    if (outputBox) outputBox.textContent = data.generated_content;
    showToast('Content generated successfully!');
  } catch (e) {
    if (outputBox) outputBox.textContent = 'Generation failed.';
  }
}

// ==========================================
// 6. AI VISION & OCR STUDIO
// ==========================================
async function generateVisionImage() {
  const prompt = document.getElementById('vision-prompt')?.value || 'Futuristic glowing cyber AI dashboard';
  const style = document.getElementById('vision-style')?.value || 'Photorealistic';
  const aspect = document.getElementById('vision-aspect')?.value || '1:1';

  showToast('Generating AI image...');
  try {
    const res = await fetch('/api/vision/generate-image', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ prompt, style, aspect_ratio: aspect })
    });
    const data = await res.json();
    const previewBox = document.getElementById('vision-image-preview');
    if (previewBox) {
      previewBox.innerHTML = `<img src="${data.image_url}" alt="AI Generated" class="w-full h-full object-cover rounded-xl shadow-lg">`;
    }
    showToast('Image generated successfully!');
  } catch (e) {
    showToast('Image generation failed', 'error');
  }
}

async function runOCRScan() {
  const out = document.getElementById('ocr-output-container');
  if (out) out.innerHTML = '<span class="text-purple-400 italic">Processing document OCR & parsing structured entities...</span>';

  try {
    const res = await fetch('/api/vision/ocr-scan', { method: 'POST' });
    const data = await res.json();

    if (out) {
      out.innerHTML = `
        <div class="space-y-3">
          <div class="flex justify-between items-center bg-purple-500/10 p-2.5 rounded-lg border border-purple-500/30">
            <span class="font-semibold text-purple-300">${data.document_type}</span>
            <span class="text-emerald-400 font-mono">Invoice #: ${data.extracted_fields.invoice_number}</span>
          </div>
          <div class="grid grid-cols-2 gap-2 text-[11px]">
            <div><span class="text-slate-500">Vendor:</span> <span class="text-white">${data.extracted_fields.vendor_name}</span></div>
            <div><span class="text-slate-500">Date:</span> <span class="text-white">${data.extracted_fields.issue_date}</span></div>
            <div><span class="text-slate-500">Total:</span> <span class="text-emerald-400 font-bold">$${data.extracted_fields.grand_total.toLocaleString()}</span></div>
            <div><span class="text-slate-500">Status:</span> <span class="text-emerald-400">${data.extracted_fields.payment_status}</span></div>
          </div>
          <div class="pt-2 border-t border-slate-800 font-mono text-[10px] text-slate-400 whitespace-pre-wrap">${data.raw_text_preview}</div>
        </div>
      `;
    }
    showToast('OCR extracted fields successfully!');
  } catch (e) {
    if (out) out.innerHTML = '<span class="text-red-400">OCR Scan failed</span>';
  }
}

// ==========================================
// 7. VOICE & AUDIO AI
// ==========================================
async function runAudioTranscription() {
  const out = document.getElementById('audio-transcription-output');
  if (out) out.innerHTML = '<span class="text-emerald-400 italic">Whisper AI processing speech stream...</span>';

  try {
    const res = await fetch('/api/audio/transcribe', { method: 'POST' });
    const data = await res.json();

    if (out) {
      out.innerHTML = `
        <div class="space-y-3">
          <div class="text-xs font-semibold text-emerald-400 flex justify-between">
            <span>Transcript (${data.duration_sec}s audio)</span>
            <span class="text-slate-400 font-mono">${Math.round(data.confidence * 100)}% Confidence</span>
          </div>
          <p class="text-xs text-slate-200 leading-relaxed bg-slate-950 p-3 rounded-lg border border-slate-800">
            "${data.full_transcript}"
          </p>
          <div class="space-y-1.5 pt-2">
            ${data.segments.map(s => `
              <div class="text-[11px] flex gap-2 text-slate-400">
                <span class="text-emerald-400 font-mono">[${s.start}]</span>
                <span class="text-slate-300 font-semibold">${s.speaker}:</span>
                <span>${s.text}</span>
              </div>
            `).join('')}
          </div>
        </div>
      `;
    }
    showToast('Whisper transcription complete!');
  } catch (e) {
    if (out) out.innerHTML = '<span class="text-red-400">Transcription failed</span>';
  }
}

function playTTSVoice() {
  const text = document.getElementById('tts-input-text')?.value;
  if (!text) return;

  if ('speechSynthesis' in window) {
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    const speed = parseFloat(document.getElementById('tts-speed')?.value || '1.0');
    utterance.rate = speed;
    window.speechSynthesis.speak(utterance);
    showToast('Synthesizing speech playback...');
  } else {
    showToast('Speech synthesis not supported in this browser', 'error');
  }
}

// ==========================================
// 8. CODE COPILOT & CSV DATA VISUALIZER
// ==========================================
async function runCodeConvert() {
  const code = document.getElementById('code-source-input')?.value || '';
  const fromL = document.getElementById('code-from-lang')?.value || 'JavaScript';
  const toL = document.getElementById('code-to-lang')?.value || 'Python';

  try {
    const res = await fetch('/api/code/convert', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ source_code: code, from_lang: fromL, to_lang: toL })
    });
    const data = await res.json();
    const out = document.getElementById('code-converted-output');
    if (out) out.textContent = data.converted_code;
    showToast(`Code converted to ${toL}!`);
  } catch (e) {
    showToast('Code conversion failed', 'error');
  }
}

async function runSQLGenerate() {
  const prompt = document.getElementById('sql-prompt')?.value || '';
  const dialect = document.getElementById('sql-dialect')?.value || 'PostgreSQL';

  try {
    const res = await fetch('/api/code/sql-generator', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ prompt, dialect })
    });
    const data = await res.json();
    const out = document.getElementById('sql-output-display');
    if (out) out.textContent = data.sql_query;
    showToast(`Generated ${dialect} query!`);
  } catch (e) {
    showToast('SQL generation failed', 'error');
  }
}

function initCSVChart() {
  try {
    if (typeof Chart === 'undefined') {
      setTimeout(initCSVChart, 500);
      return;
    }
    const ctx = document.getElementById('chart-csv-visualizer');
    if (ctx && !csvChartInstance) {
      csvChartInstance = new Chart(ctx, {
        type: 'line',
        data: {
          labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug'],
          datasets: [
            { label: 'Active Users', data: [1200, 1850, 2400, 3100, 4200, 5600, 7100, 8900], borderColor: '#3b82f6', tension: 0.3 },
            { label: 'Revenue ($)', data: [14500, 19200, 26800, 34500, 46000, 62500, 78000, 98400], borderColor: '#10b981', tension: 0.3 }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            x: { grid: { color: '#1e293b' }, ticks: { color: '#94a3b8' } },
            y: { grid: { color: '#1e293b' }, ticks: { color: '#94a3b8' } }
          }
        }
      });
    }
  } catch (e) {
    console.warn('CSV chart notice:', e);
  }
}

async function runCSVVisualization() {
  try {
    const res = await fetch('/api/code/csv-visualize', { method: 'POST' });
    const data = await res.json();
    if (csvChartInstance && data.chart_data) {
      csvChartInstance.data.labels = data.chart_data.labels;
      csvChartInstance.data.datasets = data.chart_data.datasets;
      csvChartInstance.update();
      showToast(`Dataset rendered (${data.total_rows} rows)!`);
    }
  } catch (e) {
    showToast('CSV visualization failed', 'error');
  }
}

// ==========================================
// 9. AUTONOMOUS RESEARCH AGENT
// ==========================================
async function startAutonomousResearch() {
  const topic = document.getElementById('research-topic-input')?.value.trim() || 'AI SaaS Architecture';
  const btn = document.getElementById('research-start-btn');
  if (btn) {
    btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Researching...';
    btn.disabled = true;
  }

  const reportElem = document.getElementById('research-report-content');
  if (reportElem) reportElem.textContent = 'Agent active: Analyzing sources and synthesizing executive report...';

  try {
    const res = await fetch('/api/research/execute', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ topic, focus_area: 'Market & Technology Landscape' })
    });
    const data = await res.json();
    if (reportElem) reportElem.textContent = data.executive_report;
    showToast('Autonomous research report completed!');
  } catch (e) {
    if (reportElem) reportElem.textContent = 'Research agent encountered an error.';
  } finally {
    if (btn) {
      btn.innerHTML = '<i class="fa-solid fa-play"></i> Execute Agent';
      btn.disabled = false;
    }
  }
}

// ==========================================
// 10. API SETTINGS & ENGINE CONFIG
// ==========================================
async function saveActiveProvider(provider) {
  try {
    await fetch('/api/settings/update', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ active_provider: provider, demo_mode: provider === 'demo' })
    });
    const lbl = document.getElementById('sidebar-provider-label');
    if (lbl) lbl.textContent = `${provider.toUpperCase()} Engine`;
    showToast(`Engine set to ${provider.toUpperCase()}`);
  } catch (e) {
    showToast('Failed to update provider', 'error');
  }
}

async function saveApiKeys() {
  const groq = document.getElementById('key-groq')?.value;
  const gemini = document.getElementById('key-gemini')?.value;
  const openai = document.getElementById('key-openai')?.value;

  try {
    await fetch('/api/settings/update', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        groq_key: groq || undefined,
        gemini_key: gemini || undefined,
        openai_key: openai || undefined
      })
    });
    showToast('API Keys saved successfully!');
  } catch (e) {
    showToast('Failed to save keys', 'error');
  }
}

async function testApiHealth() {
  try {
    const res = await fetch('/api/settings/test-connection', { method: 'POST' });
    const data = await res.json();
    showToast(`Status: ${data.status.toUpperCase()} (${data.latency_ms}ms)`);
  } catch (e) {
    showToast('Connection test failed', 'error');
  }
}

// ==========================================
// UTILITIES (CLIPBOARD, TOAST, ESCAPE)
// ==========================================
function copyToClipboard(elementId) {
  const elem = document.getElementById(elementId);
  if (!elem) return;
  const text = elem.innerText || elem.textContent;
  navigator.clipboard.writeText(text).then(() => {
    showToast('Copied to clipboard!');
  });
}

function showToast(msg, type = 'success') {
  const toast = document.getElementById('toast');
  const toastMsg = document.getElementById('toast-message');
  const toastIcon = document.getElementById('toast-icon');

  if (!toast || !toastMsg) return;

  toastMsg.textContent = msg;
  if (type === 'error') {
    if (toastIcon) toastIcon.className = 'fa-solid fa-triangle-exclamation text-rose-400';
  } else {
    if (toastIcon) toastIcon.className = 'fa-solid fa-circle-check text-emerald-400';
  }

  toast.classList.remove('translate-y-20', 'opacity-0');
  setTimeout(() => {
    toast.classList.add('translate-y-20', 'opacity-0');
  }, 3000);
}

function escapeHtml(text) {
  const map = { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;' };
  return text.replace(/[&<>"']/g, m => map[m]);
}

// ==========================================
// BIND ALL GLOBALS TO WINDOW
// ==========================================
window.switchTab = switchTab;
window.refreshDashboardMetrics = refreshDashboardMetrics;
window.selectPersona = selectPersona;
window.sendChatMessage = sendChatMessage;
window.indexNewDocument = indexNewDocument;
window.runRAGQuery = runRAGQuery;
window.generateCopyContent = generateCopyContent;
window.generateVisionImage = generateVisionImage;
window.runOCRScan = runOCRScan;
window.runAudioTranscription = runAudioTranscription;
window.playTTSVoice = playTTSVoice;
window.runCodeConvert = runCodeConvert;
window.runSQLGenerate = runSQLGenerate;
window.runCSVVisualization = runCSVVisualization;
window.startAutonomousResearch = startAutonomousResearch;
window.saveActiveProvider = saveActiveProvider;
window.saveApiKeys = saveApiKeys;
window.testApiHealth = testApiHealth;
window.copyToClipboard = copyToClipboard;
window.showToast = showToast;

// Auto-run on DOM Ready
document.addEventListener('DOMContentLoaded', () => {
  initPersonas();
  initDashboardCharts();
  refreshDashboardMetrics();
  loadRAGDocuments();
  initCSVChart();

  // Attach dynamic click events to sidebar buttons as safety layer
  document.querySelectorAll('.nav-item').forEach(btn => {
    btn.addEventListener('click', function () {
      const tabId = this.id.replace('nav-', '');
      switchTab(tabId);
    });
  });

  const chatInput = document.getElementById('chat-input');
  if (chatInput) {
    chatInput.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') sendChatMessage();
    });
  }

  const tempSlider = document.getElementById('chat-temp');
  if (tempSlider) {
    tempSlider.addEventListener('input', (e) => {
      const valElem = document.getElementById('chat-temp-val');
      if (valElem) valElem.textContent = e.target.value;
    });
  }
});
