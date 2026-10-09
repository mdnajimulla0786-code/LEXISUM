// Toast Notification System
function showToast(message, type = 'info') {
  const container = document.getElementById('toast-container');
  if (!container) return;

  const toast = document.createElement('div');
  toast.className = `toast ${type}`;

  let iconSvg = '';
  if (type === 'success') {
    iconSvg = `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24" width="18" height="18"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg>`;
  } else if (type === 'error') {
    iconSvg = `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24" width="18" height="18"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>`;
  } else {
    iconSvg = `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24" width="18" height="18"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>`;
  }

  toast.innerHTML = `${iconSvg}<span>${message}</span>`;
  container.appendChild(toast);

  setTimeout(() => {
    toast.style.transition = 'all 0.3s ease';
    toast.style.opacity = '0';
    toast.style.transform = 'translateX(100%)';
    setTimeout(() => toast.remove(), 300);
  }, 4000);
}

// Live Hash Formula Calculator (sum(ord(c)) % 10)
function calculateHashDetails(key, tableSize = 10) {
  if (!key || key.length === 0) {
    return { asciiSum: 0, index: 0, breakdown: "empty", charList: [] };
  }
  let sum = 0;
  const charList = [];
  for (let i = 0; i < key.length; i++) {
    const code = key.charCodeAt(i);
    sum += code;
    charList.push(`'${key[i]}'(${code})`);
  }
  const index = sum % tableSize;
  const breakdown = `${charList.join(' + ')} = ${sum} % ${tableSize} = [Index ${index}]`;
  return { asciiSum: sum, index, breakdown, charList };
}

// Global Stats Fetcher
async function updateNavStats() {
  try {
    const res = await fetch('/api/stats');
    if (res.ok) {
      const data = await res.json();
      const countEl = document.getElementById('nav-symbol-count');
      if (countEl) countEl.innerText = `${data.total} Symbols`;
      return data;
    }
  } catch (err) {
    console.warn("Could not fetch stats:", err);
  }
  return null;
}

// Quick Sample Seeder for Demonstration
async function loadSampleSymbols() {
  const sampleCode = `int global_counter = 0;
float pi = 3.14159;
char status = 'A';
double max_threshold = 99.95;

void process_data() {
    int local_temp = 42;
    float ratio = 0.75;
}

int main() {
    int exit_code = 0;
    char flag = 'Y';
}`;

  try {
    const res = await fetch('/analyze', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ code: sampleCode })
    });
    const result = await res.json();
    showToast(result.message || 'Sample symbols seeded successfully!', 'success');
    setTimeout(() => {
      window.location.reload();
    }, 900);
  } catch (err) {
    showToast('Failed to seed sample symbols: ' + err.message, 'error');
  }
}

// Global initialization
document.addEventListener('DOMContentLoaded', () => {
  updateNavStats();
});
