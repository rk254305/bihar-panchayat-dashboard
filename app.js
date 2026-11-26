/**
 * Bihar Panchayat Candidate Identification Dashboard 2026
 * Vento-Inspired Layout & Interactive Analytics App
 */

// Global State
const state = {
  activeMainTab: 'hero', // 'hero', 'zp', 'bp', 'zones'
  activeZpTab: 'zp-district-wise', // 'zp-district-wise', 'zp-progress', 'zp-bifurcation', 'zp-candidates'
  activeBpTab: 'bp-district-wise', // 'bp-district-wise', 'bp-progress', 'bp-bifurcation', 'bp-candidates'
  activeZone: 'All',
  summary: null,
  zpCandidates: null,
  bpCandidates: null,
  charts: {},
  lastSyncedTimestamp: null,
  isSyncing: false,
  // Table filters & pagination
  zpDistrictFilter: { zone: 'All', search: '', sortCol: 'totalIdentified', sortAsc: false, gapOnly: false, page: 1, pageSize: 15 },
  bpDistrictFilter: { zone: 'All', search: '', sortCol: 'blocks', sortAsc: false, page: 1, pageSize: 15 },
  zpCandidateFilter: { zone: 'All', district: 'All', category: 'All', gender: 'All', search: '', missingFilter: 'all', demographicFilter: 'all', page: 1, pageSize: 20 },
  bpCandidateFilter: { zone: 'All', district: 'All', gender: 'All', search: '', missingFilter: 'all', demographicFilter: 'all', page: 1, pageSize: 20 },
  selectedZoneTab: 'Koshi'
};

// Initialize Application
document.addEventListener('DOMContentLoaded', async () => {
  try {
    initTheme();
    initPageZoom();
    initClock();
    setupNavigation();
    await loadSummaryData();
    renderHeroSnapshot();
    startLiveSyncPolling();
    syncLiveSheetData(false);
    lucide.createIcons();
  } catch (err) {
    console.error('Initialization error:', err);
    showToast('Failed to initialize dashboard. Please refresh.', 'error');
  }
});

// ==========================================================================
// PAGE ZOOM & FIT SCREEN CONTROLLER
// ==========================================================================
let currentPageZoom = 100;
let currentMapZoom = 1.0;
const BASE_VIEWBOX = { x: 0, y: 0, w: 720, h: 440 };

function initPageZoom() {
  const saved = localStorage.getItem('dashboard_page_zoom');
  if (saved) {
    const val = parseInt(saved, 10);
    if (!isNaN(val) && val >= 70 && val <= 160) {
      applyPageZoom(val, false);
    } else {
      applyPageZoom(100, false);
    }
  } else {
    applyPageZoom(100, false);
  }

  // Default to Full-Screen Fluid Width unless explicitly set to boxed
  const savedFit = localStorage.getItem('dashboard_fit_width');
  const appContainer = document.getElementById('main-app-container');
  if (appContainer) {
    if (savedFit === 'boxed') {
      appContainer.classList.add('container-boxed');
      const icon = document.getElementById('fit-width-icon');
      if (icon) icon.setAttribute('data-lucide', 'maximize-2');
    } else {
      appContainer.classList.remove('container-boxed');
      const icon = document.getElementById('fit-width-icon');
      if (icon) icon.setAttribute('data-lucide', 'minimize-2');
    }
  }

  // Keyboard shortcut listener: Ctrl + / Ctrl - / Ctrl 0
  window.addEventListener('keydown', (e) => {
    if (e.ctrlKey && (e.key === '=' || e.key === '+')) {
      e.preventDefault();
      changePageZoom(10);
    } else if (e.ctrlKey && (e.key === '-' || e.key === '_')) {
      e.preventDefault();
      changePageZoom(-10);
    } else if (e.ctrlKey && e.key === '0') {
      e.preventDefault();
      resetPageZoom();
    }
  });
}

function applyPageZoom(level, save = true) {
  currentPageZoom = Math.min(Math.max(level, 70), 160);
  
  // Set zoom on document body
  document.body.style.zoom = `${currentPageZoom}%`;
  
  // Update UI indicators
  const label = document.getElementById('page-zoom-level');
  if (label) label.textContent = `${currentPageZoom}%`;
  // floating zoom control removed per UI specs
  
  if (save) {
    localStorage.setItem('dashboard_page_zoom', currentPageZoom.toString());
  }
}

function changePageZoom(delta) {
  applyPageZoom(currentPageZoom + delta);
  if (typeof showToast === 'function') {
    showToast(`Page zoom set to ${currentPageZoom}%`, 'info');
  }
}

function resetPageZoom() {
  applyPageZoom(100);
  if (typeof showToast === 'function') {
    showToast('Page zoom reset to 100%', 'info');
  }
}

function togglePageFitWidth() {
  const appContainer = document.getElementById('main-app-container');
  if (!appContainer) return;
  
  const isBoxed = appContainer.classList.contains('container-boxed');
  if (!isBoxed) {
    appContainer.classList.add('container-boxed');
    localStorage.setItem('dashboard_fit_width', 'boxed');
    if (typeof showToast === 'function') {
      showToast('Page layout: Centered Boxed (1600px)', 'info');
    }
  } else {
    appContainer.classList.remove('container-boxed');
    localStorage.setItem('dashboard_fit_width', 'full');
    if (typeof showToast === 'function') {
      showToast('Page layout: Full Screen Width (100%)', 'info');
    }
  }
  
  const icon = document.getElementById('fit-width-icon');
  if (icon) {
    icon.setAttribute('data-lucide', isBoxed ? 'minimize-2' : 'maximize-2');
    if (window.lucide) lucide.createIcons();
  }
}

function zoomGeoMap(factor) {
  const mapSvg = document.getElementById('bihar-real-svg-map');
  if (!mapSvg) return;
  
  currentMapZoom = Math.min(Math.max(currentMapZoom * factor, 0.8), 2.5);
  const newW = BASE_VIEWBOX.w / currentMapZoom;
  const newH = BASE_VIEWBOX.h / currentMapZoom;
  const newX = BASE_VIEWBOX.x + (BASE_VIEWBOX.w - newW) / 2;
  const newY = BASE_VIEWBOX.y + (BASE_VIEWBOX.h - newH) / 2;
  
  mapSvg.setAttribute('viewBox', `${newX} ${newY} ${newW} ${newH}`);
  const mapZoomEl = document.getElementById('map-zoom-level');
  if (mapZoomEl) mapZoomEl.textContent = `${Math.round(currentMapZoom * 100)}%`;
}

function resetGeoMapZoom() {
  const mapSvg = document.getElementById('bihar-real-svg-map');
  if (!mapSvg) return;
  currentMapZoom = 1.0;
  mapSvg.setAttribute('viewBox', '0 0 720 440');
  const mapZoomEl = document.getElementById('map-zoom-level');
  if (mapZoomEl) mapZoomEl.textContent = '100%';
}

// Attach globally to window for onclick handlers
window.changePageZoom = changePageZoom;
window.resetPageZoom = resetPageZoom;
window.togglePageFitWidth = togglePageFitWidth;
window.zoomGeoMap = zoomGeoMap;
window.resetGeoMapZoom = resetGeoMapZoom;


// ==========================================================================
// PART 2: 10 THEMES SYSTEM & REACTIVE THEME ENGINE
// ==========================================================================
const THEME_NAMES = {
  'kosi-delta': 'Kosi Delta',
  'litti-earth': 'Litti Earth',
  'maroon-saffron': 'Maroon Saffron',
  'slate-lime': 'Slate Lime',
  'midnight-navy': 'Midnight Navy (Dark)',
  'charcoal-copper': 'Charcoal Copper (Dark)',
  'sage-plum': 'Sage Plum',
  'paper-cobalt': 'Paper Cobalt',
  'terracotta-teal': 'Terracotta Teal',
  'monsoon-gold': 'Monsoon Gold'
};

function initTheme() {
  let saved = null;
  try {
    saved = localStorage.getItem('panchayat-theme');
  } catch (e) {}
  if (!saved || !THEME_NAMES[saved]) {
    const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
    saved = prefersDark ? 'midnight-navy' : 'kosi-delta';
  }
  document.documentElement.setAttribute('data-theme', saved);
  updateThemeDropdownUI(saved);
}

function selectTheme(slug) {
  if (!THEME_NAMES[slug]) slug = 'kosi-delta';
  document.documentElement.setAttribute('data-theme', slug);
  try {
    localStorage.setItem('panchayat-theme', slug);
  } catch (e) {}

  updateThemeDropdownUI(slug);
  closeThemeDropdown();

  // Instantly update map and all charts with zero page reload
  renderGeoMapColors();
  if (state.activeMainTab === 'hero') {
    renderHeroComparisonChart();
    renderHeroProgressionChart();
    renderHeroDonuts();
  }
  if (state.summary) {
    if (typeof renderZpProgressReport === 'function') renderZpProgressReport();
    if (typeof renderZpBifurcation === 'function') renderZpBifurcation();
    if (typeof renderBpProgressReport === 'function') renderBpProgressReport();
    if (typeof renderBpBifurcation === 'function') renderBpBifurcation();
  }

  if (typeof showToast === 'function') {
    showToast(`Switched theme to ${THEME_NAMES[slug]}`, 'info');
  }
}

function toggleThemeDropdown() {
  const menu = document.getElementById('theme-dropdown-menu');
  if (!menu) return;
  const isHidden = menu.classList.contains('hidden');
  if (isHidden) {
    menu.classList.remove('hidden');
    updateThemeDropdownUI();
  } else {
    menu.classList.add('hidden');
  }
}

function closeThemeDropdown() {
  const menu = document.getElementById('theme-dropdown-menu');
  if (menu) menu.classList.add('hidden');
}

function toggleTheme() {
  toggleThemeDropdown();
}

function updateThemeDropdownUI(activeSlug) {
  const currentSlug = activeSlug || document.documentElement.getAttribute('data-theme') || 'kosi-delta';
  const label = document.getElementById('theme-toggle-text');
  if (label) label.textContent = THEME_NAMES[currentSlug] || 'Theme';

  document.querySelectorAll('.theme-option-item').forEach(item => {
    const slug = item.getAttribute('data-theme-slug');
    const check = item.querySelector('.theme-check');
    if (check) {
      if (slug === currentSlug) {
        check.classList.remove('hidden');
        item.classList.add('font-bold');
      } else {
        check.classList.add('hidden');
        item.classList.remove('font-bold');
      }
    }
  });
}

// Click outside theme dropdown listener
document.addEventListener('click', (e) => {
  const container = document.getElementById('theme-dropdown-container');
  if (container && !container.contains(e.target)) {
    closeThemeDropdown();
  }
});

function getThemeColors() {
  const cs = getComputedStyle(document.documentElement);
  const primary = cs.getPropertyValue('--primary').trim() || 'var(--primary)';
  const accent = cs.getPropertyValue('--accent').trim() || 'var(--accent)';
  const alert = cs.getPropertyValue('--alert').trim() || 'var(--alert)';
  const ink = cs.getPropertyValue('--ink').trim() || 'var(--ink)';
  const surface = cs.getPropertyValue('--surface').trim() || 'var(--surface)';
  const bg = cs.getPropertyValue('--bg').trim() || 'var(--bg)';
  const line = cs.getPropertyValue('--line').trim() || 'var(--line)';
  const muted = cs.getPropertyValue('--muted').trim() || 'var(--muted)';
  const primarySoft = cs.getPropertyValue('--primary-soft').trim() || 'var(--primary-soft)';
  const accentSoft = cs.getPropertyValue('--accent-soft').trim() || 'var(--accent-soft)';
  const alertSoft = cs.getPropertyValue('--alert-soft').trim() || 'var(--alert-soft)';
  const accentText = cs.getPropertyValue('--accent-text').trim() || 'var(--accent-text)';
  const currentTheme = document.documentElement.getAttribute('data-theme') || 'kosi-delta';
  const isDark = currentTheme === 'midnight-navy' || currentTheme === 'charcoal-copper';

  return {
    isDark,
    zp: primary,
    bp: accent,
    alert: alert,
    positive: primary,
    gapMuted: line,
    textColor: ink,
    mutedText: muted,
    surface: surface,
    bg: bg,
    line: line,
    primarySoft: primarySoft,
    accentSoft: accentSoft,
    alertSoft: alertSoft,
    accentText: accentText,
    gridColor: line
  };
}

function hexToRgba(hex, alpha = 1) {
  if (!hex || typeof hex !== 'string') return hex;
  let clean = hex.trim();
  if (clean.startsWith('#')) {
    if (clean.length === 4) {
      clean = '#' + clean[1] + clean[1] + clean[2] + clean[2] + clean[3] + clean[3];
    }
    const num = parseInt(clean.slice(1), 16);
    const r = (num >> 16) & 255;
    const g = (num >> 8) & 255;
    const b = num & 255;
    return `rgba(${r}, ${g}, ${b}, ${alpha})`;
  }
  return clean;
}

// ==========================================================================
// BIHAR REAL GEOGRAPHIC MAP & DISTRICT INSPECTOR
// ==========================================================================
state.geoDistrictData = null;
state.selectedGeoDistrict = 'Purnia';
state.geoMapMetric = 'zp'; // 'zp', 'bp', 'females', 'gap'

async function loadGeoDistrictData() {
  if (state.geoDistrictData) return state.geoDistrictData;
  try {
    const res = await fetch('data/bihar_district_map_data.json?t=' + Date.now());
    if (res.ok) {
      state.geoDistrictData = await res.json();
    }
  } catch (e) {
    console.error('Error loading geo district map data:', e);
  }
  return state.geoDistrictData;
}

function setGeoMapMetric(metric) {
  state.geoMapMetric = metric;
  
  // Update button active state
  ['zp', 'bp', 'females', 'gap'].forEach(m => {
    const btn = document.getElementById(`map-mode-${m}`);
    if (btn) {
      if (m === metric) btn.classList.add('pill-filter-btn-active');
      else btn.classList.remove('pill-filter-btn-active');
    }
  });

  // Update Legend text
  const legendEl = document.getElementById('geo-map-legend');
  if (legendEl) {
    if (metric === 'zp') {
      legendEl.innerHTML = `
        <span class="font-semibold text-[var(--ink-text)]">Bihar 38 Districts (Atlas View)</span>
        <span class="text-[var(--alert)] font-semibold">● 0-Seat Alerts shown in district text</span>
      `;
    } else if (metric === 'bp') {
      legendEl.innerHTML = `
        <span class="flex items-center gap-1.5"><span class="w-3 h-3 rounded-[2px] border border-[var(--line)]" style="background-color: color-mix(in srgb, var(--accent) 25%, var(--surface));"></span> Low (&lt;30%)</span>
        <span class="flex items-center gap-1.5"><span class="w-3 h-3 rounded-[2px] border border-[var(--line)]" style="background-color: color-mix(in srgb, var(--accent) 55%, var(--surface));"></span> Medium (30-49%)</span>
        <span class="flex items-center gap-1.5"><span class="w-3 h-3 rounded-[2px] border border-[var(--line)]" style="background-color: color-mix(in srgb, var(--accent) 85%, var(--surface));"></span> High (≥50%)</span>
      `;
    } else if (metric === 'females') {
      legendEl.innerHTML = `
        <span class="flex items-center gap-1.5"><span class="w-3 h-3 rounded-[2px] border border-[var(--line)]" style="background-color: color-mix(in srgb, var(--primary) 30%, var(--surface));"></span> Emerging (&lt;10)</span>
        <span class="flex items-center gap-1.5"><span class="w-3 h-3 rounded-[2px] border border-[var(--line)]" style="background-color: color-mix(in srgb, var(--primary) 60%, var(--surface));"></span> Moderate (10-19)</span>
        <span class="flex items-center gap-1.5"><span class="w-3 h-3 rounded-[2px] border border-[var(--line)]" style="background-color: color-mix(in srgb, var(--primary) 90%, var(--surface));"></span> High Density (≥20)</span>
      `;
    } else if (metric === 'gap') {
      legendEl.innerHTML = `
        <span class="flex items-center gap-1.5"><span class="w-3 h-3 rounded-[2px] border border-[var(--alert)]" style="background-color: color-mix(in srgb, var(--alert) 35%, var(--surface));"></span> <strong class="text-[var(--alert)]">● Critical Gaps (Zero-Seat Districts)</strong></span>
      `;
    }
  }

  renderGeoMapColors();
  const labels = { zp: 'Zila Parishad Coverage', bp: 'Block Pramukh Coverage', females: 'Female Candidates', gap: 'GAP 1 Zero-Seat Alerts' };
  showToast(`Map overlay: ${labels[metric] || metric}`, 'info');
}

const BIHAR_ATLAS_COLORS = {
  'West Champaran': '#8fb382',
  'East Champaran': '#d4b46a',
  'Gopalganj': '#d9dcf0',
  'Siwan': '#dff5d8',
  'Saran': '#f3dc4e',
  'Muzaffarpur': '#a4d8f0',
  'Sitamarhi': '#c8825a',
  'Sheohar': '#93b85a',
  'Madhubani': '#b3908d',
  'Darbhanga': '#d6c83a',
  'Vaishali': '#b5eb8c',
  'Samastipur': '#ccf04e',
  'Supaul': '#f08b65',
  'Araria': '#9ca3af',
  'Kishanganj': '#c4d957',
  'Madhepura': '#f5f2e6',
  'Saharsa': '#b3883e',
  'Khagaria': '#e6dfc8',
  'Purnia': '#e6bdb3',
  'Katihar': '#d6bc2b',
  'Begusarai': '#82e673',
  'Munger': '#a4cc5c',
  'Bhagalpur': '#8db37a',
  'Banka': '#ccaa62',
  'Jamui': '#e1f5d8',
  'Lakhisarai': '#cf8b6b',
  'Sheikhpura': '#a8908e',
  'Nalanda': '#f08656',
  'Nawada': '#dcdcf5',
  'Gaya': '#b0dff2',
  'Aurangabad': '#d9c83b',
  'Rohtas': '#ebe9dc',
  'Kaimur': '#d4c028',
  'Buxar': '#e6b3a1',
  'Bhojpur': '#9bbf78',
  'Patna': '#9ca3af',
  'Arwal': '#7eb865',
  'Jehanabad': '#c48539'
};

function renderGeoMapColors() {
  if (!state.geoDistrictData) return;
  const metric = state.geoMapMetric;

  document.querySelectorAll('.bihar-district-boundary').forEach(path => {
    const distName = path.getAttribute('data-district');
    const d = state.geoDistrictData[distName];
    if (!d) return;

    if (metric === 'gap') {
      if (d.gap1Zp > 0) {
        path.setAttribute('fill', 'color-mix(in srgb, var(--alert) 35%, var(--surface))');
        path.setAttribute('stroke', 'var(--alert)');
        path.setAttribute('stroke-width', '1.4');
        path.setAttribute('opacity', '1');
      } else {
        path.setAttribute('fill', BIHAR_ATLAS_COLORS[distName] || '#e2e8f0');
        path.setAttribute('stroke', '#334155');
        path.setAttribute('stroke-width', '1');
        path.setAttribute('opacity', '0.45');
      }
      return;
    }

    path.setAttribute('fill', BIHAR_ATLAS_COLORS[distName] || '#cbd5e1');
    path.setAttribute('stroke', '#1e293b');
    path.setAttribute('stroke-width', '1.15');
    path.setAttribute('opacity', '0.95');
  });
}

function selectDistrictGeo(districtName) {
  state.selectedGeoDistrict = districtName;
  if (!state.geoDistrictData) return;
  const d = state.geoDistrictData[districtName];
  if (!d) return;

  // Highlight active path
  document.querySelectorAll('.bihar-district-boundary').forEach(p => {
    if (p.getAttribute('data-district') === districtName) {
      p.classList.add('active-selected');
    } else {
      p.classList.remove('active-selected');
    }
  });

  // Update District Inspector fields
  const nameEl = document.getElementById('inspect-district-name');
  if (nameEl) nameEl.textContent = districtName;

  const zoneEl = document.getElementById('inspect-zone-name');
  if (zoneEl) zoneEl.textContent = `${d.zone} Zone • Code: ${d.code}`;

  const indicatorEl = document.getElementById('inspect-indicator');
  if (indicatorEl) {
    indicatorEl.style.backgroundColor = d.gap1Zp > 0 ? 'var(--color-alert)' : 'var(--color-zp)';
  }

  const badgeEl = document.getElementById('inspect-status-badge');
  if (badgeEl) {
    if (d.gap1Zp > 0) {
      badgeEl.className = 'font-mono text-[10px] font-bold px-2 py-0.5 rounded-[4px] bg-[var(--color-alert-subtle)] text-[var(--color-alert)] border border-[var(--color-alert)]';
      badgeEl.textContent = `🚨 GAP 1 (${d.gap1Zp} Zero Seats)`;
    } else {
      badgeEl.className = 'font-mono text-[10px] font-bold px-2 py-0.5 rounded-[4px] bg-[var(--color-positive-subtle)] text-[var(--color-positive)] border border-[var(--color-positive)]';
      badgeEl.textContent = `● Active (${d.pctZp}% Coverage)`;
    }
  }

  const unitsEl = document.getElementById('inspect-units-note');
  if (unitsEl) {
    if (d.units && d.units.length > 1) {
      unitsEl.textContent = `Reporting Units: ${d.units.join(' + ')}`;
    } else {
      unitsEl.textContent = `Reporting Unit: ${districtName} (${d.seatsZp} ZP Seats, ${d.blocksBp} Blocks)`;
    }
  }

  // ZP stats
  const zpPctEl = document.getElementById('inspect-zp-pct');
  if (zpPctEl) zpPctEl.textContent = `${d.pctZp}% Covered`;
  const zpIdEl = document.getElementById('inspect-zp-identified');
  if (zpIdEl) zpIdEl.textContent = d.identifiedZp.toLocaleString();
  const zpTargetEl = document.getElementById('inspect-zp-target');
  if (zpTargetEl) zpTargetEl.textContent = d.target5xZp.toLocaleString();
  const zpSeatsEl = document.getElementById('inspect-zp-seats');
  if (zpSeatsEl) zpSeatsEl.textContent = d.seatsZp.toLocaleString();
  const zpGapEl = document.getElementById('inspect-zp-gap1');
  if (zpGapEl) zpGapEl.textContent = d.gap1Zp.toLocaleString();

  // BP stats
  const bpPctEl = document.getElementById('inspect-bp-pct');
  if (bpPctEl) bpPctEl.textContent = `${d.pctBp}% Covered`;
  const bpIdEl = document.getElementById('inspect-bp-identified');
  if (bpIdEl) bpIdEl.textContent = d.identifiedBp.toLocaleString();
  const bpTargetEl = document.getElementById('inspect-bp-target');
  if (bpTargetEl) bpTargetEl.textContent = d.target3xBp.toLocaleString();
  const bpBlocksEl = document.getElementById('inspect-bp-blocks');
  if (bpBlocksEl) bpBlocksEl.textContent = d.blocksBp.toLocaleString();

  // Demographics
  const zpFemEl = document.getElementById('inspect-zp-fem');
  if (zpFemEl) zpFemEl.textContent = d.femalesZp.toLocaleString();
  const bpFemEl = document.getElementById('inspect-bp-fem');
  if (bpFemEl) bpFemEl.textContent = d.femalesBp.toLocaleString();

  const zpMinEl = document.getElementById('inspect-zp-min');
  if (zpMinEl) zpMinEl.textContent = d.minorityZp.toLocaleString();
  const bpMinEl = document.getElementById('inspect-bp-min');
  if (bpMinEl) bpMinEl.textContent = d.minorityBp.toLocaleString();

  // Action buttons
  const distLabelZp = document.getElementById('inspect-btn-dist-label');
  if (distLabelZp) distLabelZp.textContent = districtName;
  const distLabelBp = document.getElementById('inspect-btn-dist-label-bp');
  if (distLabelBp) distLabelBp.textContent = districtName;
}

function positionMapTooltip(event, tooltip) {
  if (!tooltip || !event) return;
  if (tooltip.parentElement !== document.documentElement) {
    document.documentElement.appendChild(tooltip);
  }
  const tooltipWidth = tooltip.offsetWidth || 250;
  const tooltipHeight = tooltip.offsetHeight || 165;
  const margin = 12;

  let posX = event.clientX + 14;
  if (posX + tooltipWidth > window.innerWidth - margin) {
    posX = event.clientX - tooltipWidth - 14;
  }
  posX = Math.max(margin, Math.min(posX, window.innerWidth - tooltipWidth - margin));

  let posY = event.clientY + 14;
  if (posY + tooltipHeight > window.innerHeight - margin) {
    posY = event.clientY - tooltipHeight - 14;
  }
  posY = Math.max(margin, Math.min(posY, window.innerHeight - tooltipHeight - margin));

  tooltip.style.left = `${posX}px`;
  tooltip.style.top = `${posY}px`;
}

function hoverDistrictGeo(event, districtName) {
  const tooltip = document.getElementById('bihar-map-tooltip');
  if (!tooltip || !state.geoDistrictData) return;
  const d = state.geoDistrictData[districtName];
  if (!d) return;

  const zpGap = Math.max(0, (d.target5xZp || 0) - (d.identifiedZp || 0));
  const bpGap = Math.max(0, (d.target3xBp || 0) - (d.identifiedBp || 0));
  const zeroSeats = d.gap1Zp || 0;
  const zeroSeatClass = zeroSeats > 0 ? 'text-[var(--alert)] font-bold' : 'text-[var(--primary)] font-semibold';

  tooltip.innerHTML = `
    <div class="font-bold text-sm text-[var(--ink)] font-sans">${d.district}</div>
    <div class="text-[11px] text-[var(--muted)] font-mono">${d.zone} Zone • Code: ${d.code}</div>
    <div class="mt-1.5 flex items-center justify-between text-xs font-mono">
      <span class="text-[var(--muted)]">ZP Coverage:</span>
      <span class="font-bold text-[var(--primary)]">${d.identifiedZp}/${d.target5xZp} (${d.pctZp}%)</span>
    </div>
    <div class="flex items-center justify-between text-xs font-mono">
      <span class="text-[var(--muted)]">BP Coverage:</span>
      <span class="font-bold text-[var(--accent)]">${d.identifiedBp}/${d.target3xBp} (${d.pctBp}%)</span>
    </div>
    <div class="flex items-center justify-between text-[11px] font-mono text-[var(--muted)] pt-1">
      <span>Females: ZP <strong class="text-[var(--primary)]">${d.femalesZp || 0}</strong> | BP <strong class="text-[var(--accent)]">${d.femalesBp || 0}</strong></span>
      <span>Minority: ZP <strong class="text-[var(--primary)]">${d.minorityZp || 0}</strong> | BP <strong class="text-[var(--accent)]">${d.minorityBp || 0}</strong></span>
    </div>
    <div class="mt-1.5 pt-1.5 border-t border-[var(--line)] space-y-0.5 text-[11px] font-mono">
      <div class="flex items-center justify-between">
        <span class="text-[var(--muted)]">ZP / BP Gap:</span>
        <span class="font-bold text-[var(--ink)]">${zpGap.toLocaleString()} ZP | ${bpGap.toLocaleString()} BP</span>
      </div>
      <div class="flex items-center justify-between">
        <span class="text-[var(--muted)]">Zero-Candidate Seats:</span>
        <span class="${zeroSeatClass}">● ${zeroSeats} Seats</span>
      </div>
    </div>
  `;
  tooltip.style.display = 'block';
  positionMapTooltip(event, tooltip);
}

function leaveDistrictGeo() {
  const tooltip = document.getElementById('bihar-map-tooltip');
  if (tooltip) tooltip.style.display = 'none';
}

function inspectDistrictFilter(tier) {
  const dist = state.selectedGeoDistrict || 'Purnia';
  if (tier === 'zp') {
    switchMainTab('zp');
    switchZpTab('zp-candidates');
    state.zpCandidateFilter.search = dist.toLowerCase();
    state.zpCandidateFilter.demographicFilter = 'all';
    state.zpCandidateFilter.missingFilter = 'all';
    state.zpCandidateFilter.gender = 'All';
    state.zpCandidateFilter.zone = 'All';
    state.zpCandidateFilter.page = 1;
    const searchInput = document.getElementById('zp-cand-search');
    if (searchInput) searchInput.value = dist;
    const zoneSel = document.getElementById('zp-cand-zone-filter');
    if (zoneSel) zoneSel.value = 'All';
    const genderSel = document.getElementById('zp-cand-gender-filter');
    if (genderSel) genderSel.value = 'All';
    updateZpDemographicPills();
    setZpMissingFilter('all');
    renderZpCandidates();
    showToast(`Showing ZP Candidates in ${dist}`, 'success');
  } else if (tier === 'bp') {
    switchMainTab('bp');
    switchBpTab('bp-candidates');
    state.bpCandidateFilter.search = dist.toLowerCase();
    state.bpCandidateFilter.demographicFilter = 'all';
    state.bpCandidateFilter.missingFilter = 'all';
    state.bpCandidateFilter.gender = 'All';
    state.bpCandidateFilter.zone = 'All';
    state.bpCandidateFilter.page = 1;
    const searchInput = document.getElementById('bp-cand-search');
    if (searchInput) searchInput.value = dist;
    const zoneSel = document.getElementById('bp-cand-zone-filter');
    if (zoneSel) zoneSel.value = 'All';
    const genderSel = document.getElementById('bp-cand-gender-filter');
    if (genderSel) genderSel.value = 'All';
    updateBpDemographicPills();
    setBpMissingFilter('all');
    renderBpCandidates();
    showToast(`Showing BP Pramukhs in ${dist}`, 'success');
  }
}

// Fallback & Compatibility wrappers for previously bound onclick functions
function onDistrictMapClick(districtName) {
  selectDistrictGeo(districtName);
}

function onDistrictMapHover(event, districtName) {
  hoverDistrictGeo(event, districtName);
}

function onDistrictMapLeave() {
  leaveDistrictGeo();
}

function switchMapDisplay(view) {
  const mapWrapper = document.getElementById('bihar-map-wrapper');
  const tableView = document.getElementById('bihar-table-view');
  const btnMap = document.getElementById('btn-view-map');
  const btnTable = document.getElementById('btn-view-table');

  if (view === 'map') {
    if (mapWrapper) mapWrapper.classList.remove('hidden');
    if (tableView) tableView.classList.add('hidden');
    if (btnMap) btnMap.classList.add('pill-filter-btn-active');
    if (btnTable) btnTable.classList.remove('pill-filter-btn-active');
  } else {
    if (mapWrapper) mapWrapper.classList.add('hidden');
    if (tableView) tableView.classList.remove('hidden');
    if (btnMap) btnMap.classList.remove('pill-filter-btn-active');
    if (btnTable) btnTable.classList.add('pill-filter-btn-active');
  }
}

async function renderHeroMapStats() {
  await loadGeoDistrictData();
  renderGeoMapColors();
  selectDistrictGeo(state.selectedGeoDistrict || 'Purnia');

  const svgMap = document.getElementById('bihar-real-svg-map');
  if (svgMap && !svgMap.dataset.tooltipMoveBound) {
    svgMap.dataset.tooltipMoveBound = '1';
    svgMap.addEventListener('mousemove', (event) => {
      const tooltip = document.getElementById('bihar-map-tooltip');
      if (tooltip && tooltip.style.display === 'block') {
        positionMapTooltip(event, tooltip);
      }
    });
  }
}

// ==========================================================================
// DEMOGRAPHIC RECOGNITION HELPERS
// ==========================================================================
function parseCandidateAge(age) {
  if (age === null || age === undefined) return null;
  const num = parseInt(String(age).trim(), 10);
  return !isNaN(num) && num > 0 ? num : null;
}

function isYouthCandidate(c) {
  const age = parseCandidateAge(c.age);
  return age !== null && age <= 40;
}

function isMinorityCandidate(c) {
  const cat = String(c.category || '').toLowerCase();
  const ccat = String(c.candidateCategory || '').toLowerCase();
  return cat.includes('minority') || ccat.includes('minority');
}

function isFemaleCandidate(c) {
  const g = String(c.gender || '').trim().toLowerCase();
  return g === 'female';
}

// ==========================================================================
// INDIVIDUAL DEMOGRAPHIC REPORT GENERATORS (SEPARATE ZP & BP)
// ==========================================================================
function generateFemaleReport(tier) {
  if (tier === 'zp') {
    switchMainTab('zp');
    switchZpTab('zp-candidates');
    state.zpCandidateFilter.search = '';
    state.zpCandidateFilter.zone = 'All';
    state.zpCandidateFilter.gender = 'Female';
    state.zpCandidateFilter.missingFilter = 'all';
    state.zpCandidateFilter.demographicFilter = 'female';
    state.zpCandidateFilter.page = 1;
    const searchInput = document.getElementById('zp-cand-search');
    if (searchInput) searchInput.value = '';
    const zoneSel = document.getElementById('zp-cand-zone-filter');
    if (zoneSel) zoneSel.value = 'All';
    const genderSel = document.getElementById('zp-cand-gender-filter');
    if (genderSel) genderSel.value = 'Female';
    updateZpDemographicPills();
    setZpMissingFilter('all');
    renderZpCandidates();
    showToast('Generated Individual Report: 607 Female Candidates in Zila Parishad', 'success');
  } else if (tier === 'bp') {
    switchMainTab('bp');
    switchBpTab('bp-candidates');
    state.bpCandidateFilter.search = '';
    state.bpCandidateFilter.zone = 'All';
    state.bpCandidateFilter.gender = 'Female';
    state.bpCandidateFilter.missingFilter = 'all';
    state.bpCandidateFilter.demographicFilter = 'female';
    state.bpCandidateFilter.page = 1;
    const searchInput = document.getElementById('bp-cand-search');
    if (searchInput) searchInput.value = '';
    const zoneSel = document.getElementById('bp-cand-zone-filter');
    if (zoneSel) zoneSel.value = 'All';
    const genderSel = document.getElementById('bp-cand-gender-filter');
    if (genderSel) genderSel.value = 'Female';
    updateBpDemographicPills();
    setBpMissingFilter('all');
    renderBpCandidates();
    showToast('Generated Individual Report: 40 Female Pramukhs in Block Pramukh', 'success');
  }
}

function generateMinorityReport(tier) {
  if (tier === 'zp') {
    switchMainTab('zp');
    switchZpTab('zp-candidates');
    state.zpCandidateFilter.search = '';
    state.zpCandidateFilter.zone = 'All';
    state.zpCandidateFilter.gender = 'All';
    state.zpCandidateFilter.missingFilter = 'all';
    state.zpCandidateFilter.demographicFilter = 'minority';
    state.zpCandidateFilter.page = 1;
    const searchInput = document.getElementById('zp-cand-search');
    if (searchInput) searchInput.value = '';
    const zoneSel = document.getElementById('zp-cand-zone-filter');
    if (zoneSel) zoneSel.value = 'All';
    const genderSel = document.getElementById('zp-cand-gender-filter');
    if (genderSel) genderSel.value = 'All';
    updateZpDemographicPills();
    setZpMissingFilter('all');
    renderZpCandidates();
    showToast('Generated Individual Report: 275 Minority Candidates in Zila Parishad', 'success');
  } else if (tier === 'bp') {
    switchMainTab('bp');
    switchBpTab('bp-candidates');
    state.bpCandidateFilter.search = '';
    state.bpCandidateFilter.zone = 'All';
    state.bpCandidateFilter.gender = 'All';
    state.bpCandidateFilter.missingFilter = 'all';
    state.bpCandidateFilter.demographicFilter = 'minority';
    state.bpCandidateFilter.page = 1;
    const searchInput = document.getElementById('bp-cand-search');
    if (searchInput) searchInput.value = '';
    const zoneSel = document.getElementById('bp-cand-zone-filter');
    if (zoneSel) zoneSel.value = 'All';
    const genderSel = document.getElementById('bp-cand-gender-filter');
    if (genderSel) genderSel.value = 'All';
    updateBpDemographicPills();
    setBpMissingFilter('all');
    renderBpCandidates();
    showToast('Generated Individual Report: 6 Minority Pramukhs in Block Pramukh', 'success');
  }
}

function generateYouthReport(tier) {
  if (tier === 'zp') {
    switchMainTab('zp');
    switchZpTab('zp-candidates');
    state.zpCandidateFilter.search = '';
    state.zpCandidateFilter.zone = 'All';
    state.zpCandidateFilter.gender = 'All';
    state.zpCandidateFilter.missingFilter = 'all';
    state.zpCandidateFilter.demographicFilter = 'youth';
    state.zpCandidateFilter.page = 1;
    const searchInput = document.getElementById('zp-cand-search');
    if (searchInput) searchInput.value = '';
    const zoneSel = document.getElementById('zp-cand-zone-filter');
    if (zoneSel) zoneSel.value = 'All';
    const genderSel = document.getElementById('zp-cand-gender-filter');
    if (genderSel) genderSel.value = 'All';
    updateZpDemographicPills();
    setZpMissingFilter('all');
    renderZpCandidates();
    showToast('Generated Individual Report: 1,050 Youth Candidates (Age ≤ 40) in Zila Parishad', 'success');
  } else if (tier === 'bp') {
    switchMainTab('bp');
    switchBpTab('bp-candidates');
    state.bpCandidateFilter.search = '';
    state.bpCandidateFilter.zone = 'All';
    state.bpCandidateFilter.gender = 'All';
    state.bpCandidateFilter.missingFilter = 'all';
    state.bpCandidateFilter.demographicFilter = 'youth';
    state.bpCandidateFilter.page = 1;
    const searchInput = document.getElementById('bp-cand-search');
    if (searchInput) searchInput.value = '';
    const zoneSel = document.getElementById('bp-cand-zone-filter');
    if (zoneSel) zoneSel.value = 'All';
    const genderSel = document.getElementById('bp-cand-gender-filter');
    if (genderSel) genderSel.value = 'All';
    updateBpDemographicPills();
    setBpMissingFilter('all');
    renderBpCandidates();
    showToast('Generated Individual Report: 144 Youth Pramukhs (Age ≤ 40) in Block Pramukh', 'success');
  }
}

// Demographic Pill & Clear Filter Helpers (ZP & BP)
function updateZpDemographicPills() {
  const cur = state.zpCandidateFilter.demographicFilter || 'all';
  ['all', 'youth', 'female', 'minority'].forEach(d => {
    const btn = document.getElementById(`zp-filter-demo-${d}`);
    if (btn) {
      if (d === cur) {
        btn.classList.add('pill-filter-btn-active');
      } else {
        btn.classList.remove('pill-filter-btn-active');
      }
    }
  });
}

function setZpDemographicFilter(demo) {
  state.zpCandidateFilter.demographicFilter = demo;
  state.zpCandidateFilter.page = 1;
  updateZpDemographicPills();
  renderZpCandidates();
}

function clearZpFilters() {
  state.zpCandidateFilter.zone = 'All';
  state.zpCandidateFilter.gender = 'All';
  state.zpCandidateFilter.search = '';
  state.zpCandidateFilter.missingFilter = 'all';
  state.zpCandidateFilter.demographicFilter = 'all';
  state.zpCandidateFilter.page = 1;
  const searchInput = document.getElementById('zp-cand-search');
  if (searchInput) searchInput.value = '';
  const zoneSel = document.getElementById('zp-cand-zone-filter');
  if (zoneSel) zoneSel.value = 'All';
  const genderSel = document.getElementById('zp-cand-gender-filter');
  if (genderSel) genderSel.value = 'All';
  updateZpDemographicPills();
  setZpMissingFilter('all');
}

function updateBpDemographicPills() {
  const cur = state.bpCandidateFilter.demographicFilter || 'all';
  ['all', 'youth', 'female', 'minority'].forEach(d => {
    const btn = document.getElementById(`bp-filter-demo-${d}`);
    if (btn) {
      if (d === cur) {
        btn.classList.add('pill-filter-btn-active');
      } else {
        btn.classList.remove('pill-filter-btn-active');
      }
    }
  });
}

function setBpDemographicFilter(demo) {
  state.bpCandidateFilter.demographicFilter = demo;
  state.bpCandidateFilter.page = 1;
  updateBpDemographicPills();
  renderBpCandidates();
}

function clearBpFilters() {
  state.bpCandidateFilter.zone = 'All';
  state.bpCandidateFilter.gender = 'All';
  state.bpCandidateFilter.search = '';
  state.bpCandidateFilter.missingFilter = 'all';
  state.bpCandidateFilter.demographicFilter = 'all';
  state.bpCandidateFilter.page = 1;
  const searchInput = document.getElementById('bp-cand-search');
  if (searchInput) searchInput.value = '';
  const zoneSel = document.getElementById('bp-cand-zone-filter');
  if (zoneSel) zoneSel.value = 'All';
  const genderSel = document.getElementById('bp-cand-gender-filter');
  if (genderSel) genderSel.value = 'All';
  updateBpDemographicPills();
  setBpMissingFilter('all');
}

// Realtime Header Clock
function initClock() {
  const clockEl = document.getElementById('live-clock');
  const update = () => {
    const now = new Date();
    if (clockEl) {
      clockEl.textContent = now.toLocaleTimeString('en-IN', { hour12: true, hour: '2-digit', minute: '2-digit' }) + ' IST';
    }
  };
  update();
  setInterval(update, 1000);
}

// Toast Notifications
function showToast(message, type = 'info') {
  const container = document.getElementById('toast-container');
  if (!container) return;
  const toast = document.createElement('div');
  const colors = {
    info: 'border-blue-200 text-blue-900 bg-white shadow-lg',
    success: 'border-emerald-200 text-emerald-900 bg-white shadow-lg',
    error: 'border-rose-200 text-rose-900 bg-white shadow-lg'
  };
  toast.className = `p-3 px-4 rounded-2xl border flex items-center gap-3 text-xs transition-all duration-300 transform translate-y-2 opacity-0 ${colors[type] || colors.info}`;
  toast.innerHTML = `<i data-lucide="${type === 'success' ? 'check-circle' : type === 'error' ? 'alert-triangle' : 'info'}" class="w-4 h-4 ${type === 'success' ? 'text-emerald-600' : type === 'error' ? 'text-rose-600' : 'text-blue-600'}"></i><span class="font-bold">${message}</span>`;
  container.appendChild(toast);
  lucide.createIcons({ root: toast });
  setTimeout(() => toast.classList.remove('translate-y-2', 'opacity-0'), 10);
  setTimeout(() => {
    toast.classList.add('opacity-0', 'translate-y-2');
    setTimeout(() => toast.remove(), 300);
  }, 3500);
}

// Data Fetching & Dynamic Syncing
async function loadSummaryData() {
  const resp = await fetch('data/dashboard_summary.json?t=' + Date.now());
  if (!resp.ok) throw new Error('Could not load summary');
  state.summary = await resp.json();
  state.lastSyncedTimestamp = new Date(state.summary.meta.lastSynced || Date.now());
  updateSyncTimeDisplay();
  populateDropdowns();
}

async function syncLiveSheetData(isManual = false) {
  if (state.isSyncing) return;
  state.isSyncing = true;

  const syncIcon = document.getElementById('sync-icon');
  const syncBtn = document.getElementById('btn-sync-now');
  if (syncIcon) syncIcon.classList.add('animate-spin');
  if (syncBtn) syncBtn.classList.add('opacity-75');

  if (isManual) {
    showToast('Connecting live to Google Sheet... fetching fresh nominations', 'info');
  }

  try {
    const res = await fetch('/api/sync?t=' + Date.now());
    if (!res.ok) throw new Error('Live sync endpoint returned ' + res.status);
    const data = await res.json();
    
    if (data.status === 'success' && data.summary) {
      state.summary = data.summary;
      state.zpCandidates = Array.isArray(data.zpCandidates) ? data.zpCandidates : null;
      state.bpCandidates = Array.isArray(data.bpCandidates) ? data.bpCandidates : null;
      state.lastSyncedTimestamp = new Date(data.lastSynced || Date.now());
      updateSyncTimeDisplay();
      populateDropdowns();

      if (state.activeMainTab === 'hero') {
        renderHeroSnapshot();
      } else if (state.activeMainTab === 'zp') {
        switchZpTab(state.activeZpTab);
      } else if (state.activeMainTab === 'bp') {
        switchBpTab(state.activeBpTab);
      } else if (state.activeMainTab === 'zones') {
        renderZoneDeepDive(state.selectedZoneTab);
      }

      showToast(`Google Sheet synced! (${data.zpCandidateCount} ZP & ${data.bpCandidateCount} BP updated)`, 'success');
    }
  } catch (err) {
    console.error('Live sync error:', err);
    if (isManual) {
      showToast('Live sync error: Using local cached sheet data', 'error');
    }
  } finally {
    state.isSyncing = false;
    if (syncIcon) syncIcon.classList.remove('animate-spin');
    if (syncBtn) syncBtn.classList.remove('opacity-75');
  }
}

function updateSyncTimeDisplay() {
  const el = document.getElementById('sync-status-time');
  if (!el || !state.lastSyncedTimestamp) return;

  const diffSec = Math.floor((Date.now() - state.lastSyncedTimestamp.getTime()) / 1000);
  if (diffSec < 10) {
    el.textContent = 'Synced just now';
  } else if (diffSec < 60) {
    el.textContent = `Synced ${diffSec}s ago`;
  } else if (diffSec < 3600) {
    const mins = Math.floor(diffSec / 60);
    el.textContent = `Synced ${mins}m ago`;
  } else {
    el.textContent = state.lastSyncedTimestamp.toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit' });
  }
}

function startLiveSyncPolling() {
  setInterval(updateSyncTimeDisplay, 10000);
  setInterval(() => {
    syncLiveSheetData(false);
  }, 60000);
}

async function loadZpCandidates() {
  if (state.zpCandidates) return state.zpCandidates;
  const loader = document.getElementById('zp-candidate-loader');
  if (loader) loader.classList.remove('hidden');
  try {
    const resp = await fetch('data/zp_candidates.json?t=' + Date.now());
    state.zpCandidates = await resp.json();
  } catch (e) {
    console.error('Error loading ZP candidates:', e);
    showToast('Failed to load candidate directory', 'error');
    state.zpCandidates = [];
  } finally {
    if (loader) loader.classList.add('hidden');
  }
  return state.zpCandidates;
}

async function loadBpCandidates() {
  if (state.bpCandidates) return state.bpCandidates;
  const loader = document.getElementById('bp-candidate-loader');
  if (loader) loader.classList.remove('hidden');
  try {
    const resp = await fetch('data/bp_candidates.json?t=' + Date.now());
    state.bpCandidates = await resp.json();
  } catch (e) {
    console.error('Error loading BP candidates:', e);
    showToast('Failed to load Block Pramukh directory', 'error');
    state.bpCandidates = [];
  } finally {
    if (loader) loader.classList.add('hidden');
  }
  return state.bpCandidates;
}

// Setup Navigation & Listeners
function setupNavigation() {
  // Main Top Nav Tabs (Sidebar buttons)
  document.querySelectorAll('[data-main-tab]').forEach(btn => {
    btn.addEventListener('click', () => {
      const target = btn.getAttribute('data-main-tab');
      switchMainTab(target);
    });
  });

  // ZP Sub-tabs
  document.querySelectorAll('[data-zp-tab]').forEach(btn => {
    btn.addEventListener('click', () => {
      const target = btn.getAttribute('data-zp-tab');
      switchZpTab(target);
    });
  });

  // BP Sub-tabs
  document.querySelectorAll('[data-bp-tab]').forEach(btn => {
    btn.addEventListener('click', () => {
      const target = btn.getAttribute('data-bp-tab');
      switchBpTab(target);
    });
  });

  // Modal Close
  const modalClose = document.getElementById('candidate-modal-close');
  const modalOverlay = document.getElementById('candidate-modal');
  if (modalClose && modalOverlay) {
    modalClose.addEventListener('click', () => modalOverlay.classList.add('hidden'));
    modalOverlay.addEventListener('click', (e) => {
      if (e.target === modalOverlay) modalOverlay.classList.add('hidden');
    });
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && !modalOverlay.classList.contains('hidden')) {
        modalOverlay.classList.add('hidden');
      }
    });
  }

  // Quick Intel Search Input
  const intelSearch = document.getElementById('quick-intel-search');
  if (intelSearch) {
    intelSearch.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') {
        const val = intelSearch.value.trim();
        if (val) {
          switchMainTab('zp');
          switchZpTab('zp-candidates');
          const candInput = document.getElementById('zp-cand-search');
          if (candInput) {
            candInput.value = val;
            state.zpCandidateFilter.search = val.toLowerCase();
            renderZpCandidates();
          }
        }
      }
    });
  }

  setupFilterListeners();
}

// Drawer Navigation & Mobile Handlers
function navigateFromDrawer(mainTab, subTab = null) {
  switchMainTab(mainTab);
  if (subTab) {
    if (mainTab === 'zp') {
      switchZpTab(subTab);
    } else if (mainTab === 'bp') {
      switchBpTab(subTab);
    }
  }
  closeMobileDrawer();
}

function toggleMobileDrawer() {
  const drawer = document.getElementById('app-drawer');
  const backdrop = document.getElementById('drawer-backdrop');
  if (drawer && backdrop) {
    const isClosed = drawer.classList.contains('-translate-x-full');
    if (isClosed) {
      drawer.classList.remove('-translate-x-full');
      backdrop.classList.remove('hidden');
    } else {
      drawer.classList.add('-translate-x-full');
      backdrop.classList.add('hidden');
    }
  }
}

function closeMobileDrawer() {
  const drawer = document.getElementById('app-drawer');
  const backdrop = document.getElementById('drawer-backdrop');
  if (drawer && backdrop) {
    drawer.classList.add('-translate-x-full');
    backdrop.classList.add('hidden');
  }
}

// Close drawer on Escape key
window.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    closeMobileDrawer();
  }
});

function updateDrawerActiveState(mainTab, subTab = null) {
  // Update main tab items in drawer
  document.querySelectorAll('[data-drawer-tab]').forEach(btn => {
    const isAct = btn.getAttribute('data-drawer-tab') === mainTab;
    if (isAct) {
      btn.classList.add('sidebar-link-active');
      const icon = btn.querySelector('i');
      if (icon) icon.className = icon.className.replace('text-slate-500', 'text-slate-700');
    } else {
      btn.classList.remove('sidebar-link-active');
      const icon = btn.querySelector('i');
      if (icon) icon.className = icon.className.replace('text-slate-700', 'text-slate-500');
    }
  });

  // Update sub-tab items in drawer
  const curSub = subTab || (mainTab === 'zp' ? state.activeZpTab : mainTab === 'bp' ? state.activeBpTab : null);
  document.querySelectorAll('[data-drawer-subtab]').forEach(btn => {
    const target = btn.getAttribute('data-drawer-subtab');
    if (target === curSub && (mainTab === 'zp' || mainTab === 'bp')) {
      btn.classList.add('drawer-sublink-active');
    } else {
      btn.classList.remove('drawer-sublink-active');
    }
  });
}

// Switch Main Section
function switchMainTab(tabName) {
  state.activeMainTab = tabName;

  // Sidebar styling
  document.querySelectorAll('[data-main-tab]').forEach(btn => {
    btn.classList.remove('sidebar-link-active');
    const icon = btn.querySelector('i');
    if (icon) icon.className = icon.className.replace('text-slate-700', 'text-slate-500');
    
    if (btn.getAttribute('data-main-tab') === tabName) {
      btn.classList.add('sidebar-link-active');
      if (icon) icon.classList.add('text-slate-700');
    }
  });

  updateDrawerActiveState(tabName);

  // Top Bar Title & Filter Pills
  const titleEl = document.getElementById('page-main-title');
  const pillAll = document.getElementById('pill-all-zones');
  const pillZp = document.getElementById('pill-zp-filter');
  const pillBp = document.getElementById('pill-bp-filter');

  if (pillAll && pillZp && pillBp) {
    pillAll.classList.remove('pill-filter-btn-active');
    pillZp.classList.remove('pill-filter-btn-active');
    pillBp.classList.remove('pill-filter-btn-active');

    if (tabName === 'hero') {
      if (titleEl) titleEl.textContent = 'Overview';
      pillAll.classList.add('pill-filter-btn-active');
    } else if (tabName === 'zp') {
      if (titleEl) titleEl.textContent = 'Zila Parishad (ZP)';
      pillZp.classList.add('pill-filter-btn-active');
    } else if (tabName === 'bp') {
      if (titleEl) titleEl.textContent = 'Block Pramukh (BP)';
      pillBp.classList.add('pill-filter-btn-active');
    } else if (tabName === 'zones') {
      if (titleEl) titleEl.textContent = '12 Administrative Zones';
    }
  }

  // Show/Hide Main Sections
  document.querySelectorAll('.main-section').forEach(sec => sec.classList.add('hidden'));
  const activeSec = document.getElementById(`section-${tabName}`);
  if (activeSec) {
    activeSec.classList.remove('hidden');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  if (tabName === 'hero') {
    renderHeroSnapshot();
  } else if (tabName === 'zp') {
    switchZpTab(state.activeZpTab);
  } else if (tabName === 'bp') {
    switchBpTab(state.activeBpTab);
  } else if (tabName === 'zones') {
    renderZoneDeepDive(state.selectedZoneTab);
  }

  lucide.createIcons();
}

// Switch ZP Sub-Tab
function switchZpTab(tabName) {
  state.activeZpTab = tabName;
  document.querySelectorAll('[data-zp-tab]').forEach(btn => {
    const isAct = btn.getAttribute('data-zp-tab') === tabName;
    if (isAct) {
      btn.classList.add('subtab-bar-btn-active');
      btn.classList.add('pill-filter-btn-active');
    } else {
      btn.classList.remove('subtab-bar-btn-active');
      btn.classList.remove('pill-filter-btn-active');
    }
  });

  document.querySelectorAll('.zp-sub-panel').forEach(p => p.classList.add('hidden'));
  const panel = document.getElementById(`panel-${tabName}`);
  if (panel) panel.classList.remove('hidden');

  if (tabName === 'zp-district-wise') renderZpDistrictWise();
  else if (tabName === 'zp-progress') renderZpProgressReport();
  else if (tabName === 'zp-bifurcation') renderZpBifurcation();
  else if (tabName === 'zp-candidates') renderZpCandidates();

  updateDrawerActiveState('zp', tabName);
  lucide.createIcons();
}

// Switch BP Sub-Tab
function switchBpTab(tabName) {
  state.activeBpTab = tabName;
  document.querySelectorAll('[data-bp-tab]').forEach(btn => {
    const isAct = btn.getAttribute('data-bp-tab') === tabName;
    if (isAct) {
      btn.classList.add('subtab-bar-btn-active');
      btn.classList.add('pill-filter-btn-active');
    } else {
      btn.classList.remove('subtab-bar-btn-active');
      btn.classList.remove('pill-filter-btn-active');
    }
  });

  document.querySelectorAll('.bp-sub-panel').forEach(p => p.classList.add('hidden'));
  const panel = document.getElementById(`panel-${tabName}`);
  if (panel) panel.classList.remove('hidden');

  if (tabName === 'bp-district-wise') renderBpDistrictWise();
  else if (tabName === 'bp-progress') renderBpProgressReport();
  else if (tabName === 'bp-bifurcation') renderBpBifurcation();
  else if (tabName === 'bp-candidates') renderBpCandidates();

  updateDrawerActiveState('bp', tabName);
  lucide.createIcons();
}

// Populate Filter Dropdowns
function populateDropdowns() {
  if (!state.summary) return;
  const zones = state.summary.meta.zonesList;

  const zpZoneSelect = document.getElementById('zp-district-zone-filter');
  if (zpZoneSelect) {
    zpZoneSelect.innerHTML = '<option value="All">All 12 Zones</option>' + zones.map(z => `<option value="${z}">${z} Zone</option>`).join('');
  }

  const bpZoneSelect = document.getElementById('bp-district-zone-filter');
  if (bpZoneSelect) {
    bpZoneSelect.innerHTML = '<option value="All">All 12 Zones</option>' + zones.map(z => `<option value="${z}">${z} Zone</option>`).join('');
  }

  const zpCandZone = document.getElementById('zp-cand-zone-filter');
  if (zpCandZone) {
    zpCandZone.innerHTML = '<option value="All">All Zones</option>' + zones.map(z => `<option value="${z}">${z}</option>`).join('');
  }

  const bpCandZone = document.getElementById('bp-cand-zone-filter');
  if (bpCandZone) {
    bpCandZone.innerHTML = '<option value="All">All Zones</option>' + zones.map(z => `<option value="${z}">${z}</option>`).join('');
  }

  const zoneTabContainer = document.getElementById('zone-tab-buttons');
  if (zoneTabContainer) {
    zoneTabContainer.innerHTML = zones.map(z => `
      <button onclick="switchZoneDeepDive('${z}')" class="zone-tab-btn ${z === state.selectedZoneTab ? 'zone-tab-active pill-filter-btn-active' : ''}">
        ${z}
      </button>
    `).join('');
  }
}

// Setup Event Listeners for Filters
function setupFilterListeners() {
  const zpZoneFilter = document.getElementById('zp-district-zone-filter');
  const zpSearch = document.getElementById('zp-district-search');
  if (zpZoneFilter) {
    zpZoneFilter.addEventListener('change', (e) => {
      state.zpDistrictFilter.zone = e.target.value;
      state.zpDistrictFilter.page = 1;
      renderZpDistrictWise();
    });
  }
  if (zpSearch) {
    zpSearch.addEventListener('input', (e) => {
      state.zpDistrictFilter.search = e.target.value.toLowerCase().trim();
      state.zpDistrictFilter.page = 1;
      renderZpDistrictWise();
    });
  }

  const bpZoneFilter = document.getElementById('bp-district-zone-filter');
  const bpSearch = document.getElementById('bp-district-search');
  if (bpZoneFilter) {
    bpZoneFilter.addEventListener('change', (e) => {
      state.bpDistrictFilter.zone = e.target.value;
      state.bpDistrictFilter.page = 1;
      renderBpDistrictWise();
    });
  }
  if (bpSearch) {
    bpSearch.addEventListener('input', (e) => {
      state.bpDistrictFilter.search = e.target.value.toLowerCase().trim();
      state.bpDistrictFilter.page = 1;
      renderBpDistrictWise();
    });
  }

  const zpCandZone = document.getElementById('zp-cand-zone-filter');
  const zpCandGender = document.getElementById('zp-cand-gender-filter');
  const zpCandSearch = document.getElementById('zp-cand-search');
  if (zpCandZone) zpCandZone.addEventListener('change', (e) => { state.zpCandidateFilter.zone = e.target.value; state.zpCandidateFilter.page = 1; renderZpCandidates(); });
  if (zpCandGender) zpCandGender.addEventListener('change', (e) => { state.zpCandidateFilter.gender = e.target.value; state.zpCandidateFilter.page = 1; renderZpCandidates(); });
  if (zpCandSearch) zpCandSearch.addEventListener('input', (e) => { state.zpCandidateFilter.search = e.target.value.toLowerCase().trim(); state.zpCandidateFilter.page = 1; renderZpCandidates(); });

  const bpCandZone = document.getElementById('bp-cand-zone-filter');
  const bpCandGender = document.getElementById('bp-cand-gender-filter');
  const bpCandSearch = document.getElementById('bp-cand-search');
  if (bpCandGender) bpCandGender.addEventListener('change', (e) => { state.bpCandidateFilter.gender = e.target.value; state.bpCandidateFilter.page = 1; renderBpCandidates(); });
  if (bpCandZone) bpCandZone.addEventListener('change', (e) => { state.bpCandidateFilter.zone = e.target.value; state.bpCandidateFilter.page = 1; renderBpCandidates(); });
  if (bpCandSearch) bpCandSearch.addEventListener('input', (e) => { state.bpCandidateFilter.search = e.target.value.toLowerCase().trim(); state.bpCandidateFilter.page = 1; renderBpCandidates(); });
}

/* ==========================================================================
   1. HERO PAGE / OVERVIEW
   ========================================================================== */

function renderHeroSnapshot() {
  if (!state.summary) return;
  const { snapshot } = state.summary;

  // Track 1: Zila Parishad (ZP Only)
  const zpIdEl = document.getElementById('hero-zp-identified');
  if (zpIdEl) zpIdEl.textContent = snapshot.zp.totalIdentified.toLocaleString();
  const zpCovEl = document.getElementById('hero-zp-coverage-pct');
  if (zpCovEl) zpCovEl.textContent = `${snapshot.zp.overallCoveragePct}% Done`;
  const zpSeat1El = document.getElementById('hero-zp-seat1');
  if (zpSeat1El) zpSeat1El.textContent = snapshot.zp.seatsWithAtLeast1.toLocaleString();
  const zpSeat1PctEl = document.getElementById('hero-zp-seat1-pct');
  if (zpSeat1PctEl) zpSeat1PctEl.textContent = `(${snapshot.zp.seatsWith1Pct}%)`;
  const zpGapEl = document.getElementById('hero-zp-gap');
  if (zpGapEl) zpGapEl.textContent = snapshot.zp.remainingCandidates.toLocaleString();

  // ZP Demographics (ZP Only)
  const zpMin = snapshot.zp.demographics?.minority || 0;
  const zpFem = snapshot.zp.demographics?.female || 0;
  const zpYuv = snapshot.zp.demographics?.yuva || 0;
  const zpMinEl = document.getElementById('hero-zp-minority');
  if (zpMinEl) zpMinEl.textContent = zpMin.toLocaleString();
  const zpMinPctEl = document.getElementById('hero-zp-minority-pct');
  if (zpMinPctEl && snapshot.zp.totalIdentified) zpMinPctEl.textContent = `(${round(zpMin / snapshot.zp.totalIdentified * 100)}% of ZP)`;
  
  const mahilaEl = document.getElementById('hero-mahila-total');
  if (mahilaEl) mahilaEl.textContent = zpFem.toLocaleString();
  const mahilaPctEl = document.getElementById('hero-mahila-pct');
  if (mahilaPctEl && snapshot.zp.totalIdentified) mahilaPctEl.textContent = `(${round(zpFem / snapshot.zp.totalIdentified * 100)}% of ZP)`;

  const yuvaEl = document.getElementById('hero-yuva-total');
  if (yuvaEl) yuvaEl.textContent = zpYuv.toLocaleString();
  const yuvaPctEl = document.getElementById('hero-yuva-pct');
  if (yuvaPctEl && snapshot.zp.totalIdentified) yuvaPctEl.textContent = `(${round(zpYuv / snapshot.zp.totalIdentified * 100)}% of ZP)`;

  // Track 2: Block Pramukh (BP Only)
  const bpIdEl = document.getElementById('hero-bp-identified');
  if (bpIdEl) bpIdEl.textContent = snapshot.bp.totalIdentified.toLocaleString();
  const bpBlocksEl = document.getElementById('hero-bp-blocks');
  if (bpBlocksEl) bpBlocksEl.textContent = snapshot.bp.totalBlocks.toLocaleString();
  const bpCovEl = document.getElementById('hero-bp-coverage-pct');
  if (bpCovEl) bpCovEl.textContent = `${snapshot.bp.overallCoveragePct}% Done`;
  const bpGapEl = document.getElementById('hero-bp-gap');
  if (bpGapEl) bpGapEl.textContent = snapshot.bp.remainingBlocks.toLocaleString();

  // BP Demographics (BP Only)
  const bpMin = snapshot.bp.demographics?.minority || 0;
  const bpFem = snapshot.bp.demographics?.female || 0;
  const bpYuv = snapshot.bp.demographics?.yuva || 0;
  const bpMinEl = document.getElementById('hero-bp-minority');
  if (bpMinEl) bpMinEl.textContent = bpMin.toLocaleString();
  const bpMinPctEl = document.getElementById('hero-bp-minority-pct');
  if (bpMinPctEl && snapshot.bp.totalIdentified) bpMinPctEl.textContent = `(${round(bpMin / snapshot.bp.totalIdentified * 100)}% of BP)`;

  const bpFemEl = document.getElementById('hero-bp-female');
  if (bpFemEl) bpFemEl.textContent = bpFem.toLocaleString();
  const bpFemPctEl = document.getElementById('hero-bp-female-pct');
  if (bpFemPctEl && snapshot.bp.totalIdentified) bpFemPctEl.textContent = `(${round(bpFem / snapshot.bp.totalIdentified * 100)}% of BP)`;

  const bpYuvEl = document.getElementById('hero-bp-yuva');
  if (bpYuvEl) bpYuvEl.textContent = bpYuv.toLocaleString();
  const bpYuvPctEl = document.getElementById('hero-bp-yuva-pct');
  if (bpYuvPctEl && snapshot.bp.totalIdentified) bpYuvPctEl.textContent = `(${round(bpYuv / snapshot.bp.totalIdentified * 100)}% of BP)`;

  const bpFemSub = document.getElementById('hero-bp-female-sub');
  if (bpFemSub) bpFemSub.textContent = bpFem.toLocaleString();
  const bpYuvSub = document.getElementById('hero-bp-yuva-sub');
  if (bpYuvSub) bpYuvSub.textContent = bpYuv.toLocaleString();

  // Progression subtitles
  const seat1Sub = document.getElementById('hero-zp-seat1-sub');
  if (seat1Sub) seat1Sub.textContent = snapshot.zp.seatsWithAtLeast1.toLocaleString();
  const seat2El = document.getElementById('hero-zp-seat2');
  if (seat2El) seat2El.textContent = snapshot.zp.seatsWith2.toLocaleString();
  const seat3El = document.getElementById('hero-zp-seat3');
  if (seat3El) seat3El.textContent = snapshot.zp.seatsWith3.toLocaleString();
  const seat4El = document.getElementById('hero-zp-seat4');
  if (seat4El) seat4El.textContent = snapshot.zp.seatsWith4.toLocaleString();
  const seat5El = document.getElementById('hero-zp-seat5');
  if (seat5El) seat5El.textContent = snapshot.zp.seatsWith5Plus.toLocaleString();
  const zpYuvaEl = document.getElementById('hero-zp-yuva');
  if (zpYuvaEl) zpYuvaEl.textContent = zpYuv.toLocaleString();
  const zpFemaleEl = document.getElementById('hero-zp-female');
  if (zpFemaleEl) zpFemaleEl.textContent = zpFem.toLocaleString();

  // Hidden compatibility tags
  const heroCombinedEl = document.getElementById('hero-combined-total');
  if (heroCombinedEl) heroCombinedEl.textContent = snapshot.zp.totalIdentified.toLocaleString();
  const diverseTotalEl = document.getElementById('hero-diverse-total');
  if (diverseTotalEl) diverseTotalEl.textContent = (zpFem + zpYuv).toLocaleString();
  const diverseShareEl = document.getElementById('hero-diverse-share');
  if (diverseShareEl) diverseShareEl.textContent = `${round((zpFem + zpYuv) / snapshot.zp.totalIdentified * 100)}%`;
  const minorityTotalEl = document.getElementById('hero-minority-total');
  if (minorityTotalEl) minorityTotalEl.textContent = zpMin.toLocaleString();
  const minShareEl = document.getElementById('hero-minority-share');
  if (minShareEl) minShareEl.textContent = `${round(zpMin / snapshot.zp.totalIdentified * 100)}%`;

  renderHeroComparisonChart();
  renderHeroDonuts();
  renderHeroProgressionChart();
  renderHeroKeyDistricts();
  renderHeroMapStats();
}

// 5 Key Districts Comparison Table (Top 5 Districts compared by 5x members formula)
function renderHeroKeyDistricts() {
  const tbody = document.getElementById('hero-key-districts-body');
  if (!tbody || !state.summary) return;
  const districts = state.summary.zp.districtWise;

  // 5 key districts: East Champaran, Muzaffarpur, Saran, Gaya, and Purnia (gap district)
  const sorted = [...districts].sort((a, b) => b.seats - a.seats);
  const top4 = sorted.slice(0, 4);
  const gapDistrict = districts.find(d => d.gap1 >= 10) || sorted[4];
  const list = [...top4, gapDistrict];

  tbody.innerHTML = list.map(d => {
    const target5x = d.seats * 5;
    let statusBadge = '<span class="text-[10px] font-bold text-emerald-600">● 100% Active</span>';
    if (d.gap1 > 0) {
      statusBadge = `<span class="text-[10px] font-bold text-rose-600">● Gap 1 (${d.gap1})</span>`;
    } else if (d.progressPct && parseInt(d.progressPct) >= 10) {
      statusBadge = `<span class="text-[10px] font-bold text-blue-600">● On Target</span>`;
    }
    return `
      <tr class="hover:bg-slate-50 transition-colors">
        <td class="font-bold text-slate-800">${d.district}</td>
        <td class="text-center text-slate-600 font-semibold">${d.seats} <span class="text-[10px] text-slate-400 font-normal">(${target5x})</span></td>
        <td class="text-right">${statusBadge}</td>
      </tr>
    `;
  }).join('');
}

// Zone Performance Comparison (Bar Chart matching "Performance" in Vento reference)
function renderHeroComparisonChart() {
  const ctx = document.getElementById('chart-hero-comparison');
  if (!ctx || !state.summary) return;

  const zpZones = state.summary.zp.progressByZone;
  const bpZones = state.summary.bp.progressByZone;
  const colors = getThemeColors();

  const labels = zpZones.map(z => z.zone.slice(0, 3).toUpperCase());
  const zpPercentages = zpZones.map(z => parseFloat(z.coveragePct));
  const bpPercentages = zpZones.map(z => {
    const found = bpZones.find(b => b.zone === z.zone);
    return found ? parseFloat(found.coveragePct) : 0;
  });

  if (state.charts.heroComparison) state.charts.heroComparison.destroy();

  state.charts.heroComparison = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [
        {
          label: 'ZP Coverage',
          data: zpPercentages,
          backgroundColor: colors.zp,
          borderRadius: 2,
          barPercentage: 0.65
        },
        {
          label: 'BP Coverage',
          data: bpPercentages,
          backgroundColor: colors.bp,
          borderRadius: 2,
          barPercentage: 0.65
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      layout: {
        padding: { top: 4, bottom: 2, left: 6, right: 6 }
      },
      plugins: {
        legend: {
          display: true,
          position: 'top',
          align: 'center',
          labels: {
            color: colors.textColor,
            font: { family: 'IBM Plex Sans', size: 11, weight: 600 },
            boxWidth: 10,
            boxHeight: 10,
            padding: 14
          }
        },
        tooltip: {
          backgroundColor: colors.surface,
          titleColor: colors.textColor,
          bodyColor: colors.textColor,
          borderColor: colors.gapMuted,
          borderWidth: 1,
          padding: 8,
          titleFont: { family: 'IBM Plex Sans', size: 11, weight: 'bold' },
          bodyFont: { family: 'IBM Plex Mono', size: 10 }
        }
      },
      scales: {
        x: {
          grid: { display: false },
          ticks: { color: colors.mutedText, font: { family: 'IBM Plex Sans', size: 11, weight: 600 } }
        },
        y: {
          min: 0,
          max: 100,
          grid: { color: colors.gridColor },
          ticks: { color: colors.mutedText, font: { family: 'IBM Plex Mono', size: 10 }, callback: v => v + '%' }
        }
      }
    }
  });
}

// ZP Depth Progression (Matching "Total Balance" blue vertical bars)
function renderHeroProgressionChart() {
  const ctx = document.getElementById('chart-hero-progression');
  if (!ctx || !state.summary) return;

  const { snapshot } = state.summary;
  const colors = getThemeColors();
  const labels = ['≥1 Cand', '≥2 Cands', '≥3 Cands', '≥4 Cands', '5+ Cands'];
  const values = [
    snapshot.zp.seatsWithAtLeast1,
    snapshot.zp.seatsWith2,
    snapshot.zp.seatsWith3,
    snapshot.zp.seatsWith4,
    snapshot.zp.seatsWith5Plus
  ];

  if (state.charts.progression) state.charts.progression.destroy();

  state.charts.progression = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        label: 'Seats Covered',
        data: values,
        backgroundColor: colors.zp,
        borderRadius: 2,
        barPercentage: 0.55
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      layout: {
        padding: { top: 4, bottom: 2, left: 10, right: 8 }
      },
      plugins: {
        legend: {
          display: true,
          position: 'top',
          align: 'center',
          labels: {
            color: colors.textColor,
            font: { family: 'IBM Plex Sans', size: 11, weight: 600 },
            boxWidth: 10,
            boxHeight: 10,
            padding: 14
          }
        },
        tooltip: {
          backgroundColor: colors.surface,
          titleColor: colors.textColor,
          bodyColor: colors.textColor,
          borderColor: colors.gapMuted,
          borderWidth: 1,
          padding: 8,
          titleFont: { family: 'IBM Plex Sans', size: 11 },
          bodyFont: { family: 'IBM Plex Mono', size: 10 }
        }
      },
      scales: {
        x: {
          grid: { display: false },
          ticks: { color: colors.mutedText, font: { family: 'IBM Plex Sans', size: 11, weight: 600 } }
        },
        y: {
          min: 0,
          max: 1200,
          grid: { color: colors.gridColor },
          ticks: { color: colors.mutedText, font: { family: 'IBM Plex Mono', size: 10 } }
        }
      }
    }
  });
}

// Gauge / Donut Meters (Matching "Spent Amount" & "Revenue" meters)
function renderHeroDonuts() {
  const { snapshot } = state.summary;
  const colors = getThemeColors();

  // ZP Donut (56.4% identified, 43.6% remaining gap - ZP ONLY)
  const ctxZp = document.getElementById('chart-hero-zp-donut');
  if (ctxZp) {
    if (state.charts.zpDonut) state.charts.zpDonut.destroy();
    const zpIdentified = snapshot.zp.totalIdentified;
    const zpRemaining = Math.max(0, 5800 - zpIdentified);
    state.charts.zpDonut = new Chart(ctxZp, {
      type: 'doughnut',
      data: {
        datasets: [{
          data: [zpIdentified, zpRemaining],
          backgroundColor: [colors.zp, colors.gapMuted],
          borderWidth: 0
        }]
      },
      options: {
        cutout: '76%',
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false }, tooltip: { enabled: false } }
      }
    });
  }

  // BP Donut (32.9% identified, 67.1% remaining gap - BP ONLY, NO COMBINATION)
  const ctxBp = document.getElementById('chart-hero-bp-donut');
  if (ctxBp) {
    if (state.charts.bpDonut) state.charts.bpDonut.destroy();
    const bpIdentified = snapshot.bp.totalIdentified;
    const bpRemaining = Math.max(0, 1602 - bpIdentified);
    state.charts.bpDonut = new Chart(ctxBp, {
      type: 'doughnut',
      data: {
        datasets: [{
          data: [bpIdentified, bpRemaining],
          backgroundColor: [colors.bp, colors.gapMuted],
          borderWidth: 0
        }]
      },
      options: {
        cutout: '76%',
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false }, tooltip: { enabled: false } }
      }
    });
  }
}

/* ==========================================================================
   2. ZILA PARISHAD (ZP) SECTION & SUB-TABS
   ========================================================================== */

function renderZpDistrictWise() {
  if (!state.summary) return;
  const list = state.summary.zp.districtWise;
  const { zone, search, sortCol, sortAsc, page, pageSize } = state.zpDistrictFilter;

  let filtered = list.filter(d => {
    const matchZone = zone === 'All' || d.zone.toLowerCase() === zone.toLowerCase();
    const matchSearch = !search || d.district.toLowerCase().includes(search) || d.zone.toLowerCase().includes(search);
    const matchGap = !state.zpDistrictFilter.gapOnly || d.gap1 > 0;
    return matchZone && matchSearch && matchGap;
  });

  filtered.sort((a, b) => {
    let vA = a[sortCol];
    let vB = b[sortCol];
    if (typeof vA === 'string') {
      vA = vA.replace('%', '');
      vB = vB.replace('%', '');
      const numA = parseFloat(vA);
      const numB = parseFloat(vB);
      if (!isNaN(numA) && !isNaN(numB)) {
        return sortAsc ? numA - numB : numB - numA;
      }
      return sortAsc ? vA.localeCompare(vB) : vB.localeCompare(vA);
    }
    return sortAsc ? vA - vB : vB - vA;
  });

  const total = filtered.length;
  const totalPages = Math.ceil(total / pageSize) || 1;
  const curPage = Math.min(page, totalPages);
  const start = (curPage - 1) * pageSize;
  const pageItems = filtered.slice(start, start + pageSize);

  const tbody = document.getElementById('zp-district-table-body');
  if (tbody) {
    if (pageItems.length === 0) {
      tbody.innerHTML = `<tr><td colspan="12" class="text-center py-8 text-slate-400">No districts match your filter.</td></tr>`;
    } else {
      tbody.innerHTML = pageItems.map((d, idx) => {
        const cov1 = d.coverage1Pct;
        const progressNum = parseFloat(d.progressPct.replace('%', '')) || 0;
        return `
          <tr class="hover:bg-slate-50 transition-colors ${d.gap1 > 0 ? 'bg-rose-50/20' : ''}">
            <td class="font-mono text-xs text-slate-400">${start + idx + 1}</td>
            <td class="font-bold text-slate-900">
              ${d.district}
              <span class="block text-xs font-normal text-slate-400">${d.zone}</span>
            </td>
            <td class="text-center font-bold text-blue-700">${d.seats}</td>
            <td class="text-center">
              <span class="px-2 py-0.5 rounded-full text-xs font-semibold ${cov1 >= 95 ? 'bg-emerald-50 text-emerald-700' : cov1 >= 80 ? 'bg-blue-50 text-blue-700' : 'bg-amber-50 text-amber-700'}">
                ${d.seatsWith1} (${cov1}%)
              </span>
            </td>
            <td class="text-center text-slate-600 font-medium">${d.seatsWith2}</td>
            <td class="text-center text-slate-600 font-medium">${d.seatsWith3}</td>
            <td class="text-center text-slate-600 font-medium">${d.seatsWith4}</td>
            <td class="text-center text-slate-600 font-medium">${d.seatsWith5}</td>
            <td class="text-center font-black text-emerald-700">${d.totalIdentified}</td>
            <td class="text-center font-bold text-rose-600">
              ${d.gap1 > 0 
                ? `<span class="badge-warning-gap"><i data-lucide="alert-triangle" class="w-3 h-3"></i> ${d.gap1} Zero-Seats</span>` 
                : '<span class="text-slate-400 font-medium">0</span>'}
            </td>
            <td class="text-center text-amber-700 font-medium">${d.gap2}</td>
            <td class="text-center">
              <div class="flex items-center justify-center gap-2">
                <div class="w-14 bg-slate-100 rounded-full h-1.5 overflow-hidden">
                  <div class="bg-blue-600 h-1.5 rounded-full" style="width: ${Math.min(100, progressNum * 5)}%"></div>
                </div>
                <span class="text-xs font-bold text-slate-700">${d.progressPct}</span>
              </div>
            </td>
          </tr>
        `;
      }).join('');
    }
  }

  const infoEl = document.getElementById('zp-district-pagination-info');
  if (infoEl) infoEl.textContent = `Showing ${total === 0 ? 0 : start + 1} to ${Math.min(start + pageSize, total)} of ${total} districts`;

  const prevBtn = document.getElementById('zp-district-prev-btn');
  const nextBtn = document.getElementById('zp-district-next-btn');
  if (prevBtn) prevBtn.disabled = curPage <= 1;
  if (nextBtn) nextBtn.disabled = curPage >= totalPages;
}

function sortZpDistrict(colName) {
  if (state.zpDistrictFilter.sortCol === colName) {
    state.zpDistrictFilter.sortAsc = !state.zpDistrictFilter.sortAsc;
  } else {
    state.zpDistrictFilter.sortCol = colName;
    state.zpDistrictFilter.sortAsc = false;
  }
  renderZpDistrictWise();
}

function setZpDistrictGapFilter(onlyGap) {
  state.zpDistrictFilter.gapOnly = onlyGap;
  state.zpDistrictFilter.page = 1;

  const btnAll = document.getElementById('zp-dist-filter-all');
  const btnGap = document.getElementById('zp-dist-filter-gap');
  if (btnAll && btnGap) {
    if (onlyGap) {
      btnAll.classList.remove('pill-filter-btn-active');
      btnGap.classList.add('pill-filter-btn-active');
    } else {
      btnAll.classList.add('pill-filter-btn-active');
      btnGap.classList.remove('pill-filter-btn-active');
    }
  }

  renderZpDistrictWise();
  lucide.createIcons();
}

function prevZpDistrictPage() {
  if (state.zpDistrictFilter.page > 1) {
    state.zpDistrictFilter.page--;
    renderZpDistrictWise();
  }
}

function nextZpDistrictPage() {
  state.zpDistrictFilter.page++;
  renderZpDistrictWise();
}

function renderZpProgressReport() {
  if (!state.summary) return;
  const zones = state.summary.zp.progressByZone;

  const cardsContainer = document.getElementById('zp-progress-zone-cards');
  if (cardsContainer) {
    cardsContainer.innerHTML = zones.map(z => {
      const pct = parseFloat(z.coveragePct) || 0;
      return `
        <div class="vento-card p-4 flex flex-col justify-between hover:shadow-md transition-all">
          <div class="flex items-center justify-between mb-2">
            <h4 class="font-extrabold text-[var(--ink)] font-sans text-sm">${z.zone}</h4>
            <span class="text-[10px] font-bold px-2 py-0.5 rounded-full ${pct >= 70 ? 'bg-[var(--primary-soft)] text-[var(--primary)]' : 'bg-[var(--surface)] border border-[var(--line)] text-[var(--muted)]'}">
              ${z.coveragePct}
            </span>
          </div>
          <div class="space-y-1 mb-2 text-xs">
            <div class="flex justify-between text-[var(--muted)] font-sans">
              <span>Seats: <strong class="text-[var(--ink)] font-mono">${z.seats}</strong></span>
              <span>Target: <strong class="text-[var(--ink)] font-mono">${z.target5x}</strong></span>
            </div>
            <div class="flex justify-between text-[var(--muted)] font-sans">
              <span>Identified: <strong class="text-[var(--primary)] font-mono">${z.identified}</strong></span>
              <span>Deficit: <strong class="text-[var(--alert)] font-mono">${z.remaining}</strong></span>
            </div>
          </div>
          <button onclick="switchMainTab('zones'); switchZoneDeepDive('${z.zone}')" class="vento-btn-secondary text-[10px] py-1 w-full justify-center">
            Zone Details →
          </button>
        </div>
      `;
    }).join('');
    lucide.createIcons({ root: cardsContainer });
  }

  const tbody = document.getElementById('zp-progress-table-body');
  if (tbody) {
    tbody.innerHTML = zones.map((z, idx) => `
      <tr class="hover:bg-[var(--primary-soft)] transition-colors">
        <td class="font-mono text-xs text-[var(--muted)]">${idx + 1}</td>
        <td class="font-bold text-[var(--ink)] font-sans">${z.zone}</td>
        <td class="text-center font-bold text-[var(--ink)] font-mono">${z.seats}</td>
        <td class="text-center font-medium text-[var(--muted)] font-mono">${z.target5x}</td>
        <td class="text-center font-black text-[var(--primary)] font-mono">${z.identified}</td>
        <td class="text-center font-bold text-[var(--alert)] font-mono">${z.remaining}</td>
        <td class="text-center font-bold text-[var(--primary)] font-mono">${z.coveragePct}</td>
        <td class="text-center">
          <div class="w-20 mx-auto bg-[var(--line)] rounded-full h-1.5 overflow-hidden">
            <div class="bg-[var(--primary)] h-1.5 rounded-full" style="width: ${z.coveragePct}"></div>
          </div>
        </td>
      </tr>
    `).join('');
  }

  const ctx = document.getElementById('chart-zp-zone-progress');
  if (ctx) {
    if (state.charts.zpZoneProgress) state.charts.zpZoneProgress.destroy();
    const colors = getThemeColors();
    state.charts.zpZoneProgress = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: zones.map(z => z.zone),
        datasets: [
          { label: 'Identified', data: zones.map(z => z.identified), backgroundColor: colors.zp, borderRadius: 3 },
          { label: 'Remaining Deficit', data: zones.map(z => z.remaining), backgroundColor: colors.alert, borderRadius: 3 }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: true,
            position: 'top',
            align: 'end',
            labels: {
              color: colors.textColor,
              font: { family: 'IBM Plex Sans', size: 12, weight: 600 },
              boxWidth: 12,
              boxHeight: 12,
              padding: 14
            }
          }
        },
        scales: {
          x: { stacked: true, grid: { display: false }, ticks: { color: colors.textColor, font: { family: 'IBM Plex Mono', size: 10 } } },
          y: { stacked: true, grid: { color: colors.gridColor }, ticks: { color: colors.mutedText, font: { family: 'IBM Plex Mono', size: 10 } } }
        }
      }
    });
  }
}

function renderZpBifurcation() {
  if (!state.summary) return;
  const totals = state.summary.zp.bifurcationTotals;

  document.getElementById('zp-bif-total').textContent = totals.total.toLocaleString();
  document.getElementById('zp-bif-male').textContent = totals.male.toLocaleString();
  document.getElementById('zp-bif-male-pct').textContent = `${round(totals.male / totals.total * 100)}%`;
  document.getElementById('zp-bif-female').textContent = totals.female.toLocaleString();
  document.getElementById('zp-bif-female-pct').textContent = `${round(totals.female / totals.total * 100)}%`;
  document.getElementById('zp-bif-yuva').textContent = totals.yuva.toLocaleString();
  document.getElementById('zp-bif-yuva-pct').textContent = `${round(totals.yuva / totals.total * 100)}%`;
  document.getElementById('zp-bif-minority').textContent = totals.minority.toLocaleString();
  document.getElementById('zp-bif-minority-pct').textContent = `${round(totals.minority / totals.total * 100)}%`;

  const ctx = document.getElementById('chart-zp-bifurcation');
  if (ctx) {
    if (state.charts.zpBifurcation) state.charts.zpBifurcation.destroy();
    const colors = getThemeColors();
    state.charts.zpBifurcation = new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: ['Male', 'Female', 'Youth', 'Minority'],
        datasets: [{
          data: [totals.male, totals.female, totals.yuva, totals.minority],
          backgroundColor: [
            colors.zp,
            colors.bp,
            hexToRgba(colors.zp, 0.45),
            hexToRgba(colors.textColor, 0.4)
          ],
          borderWidth: 1,
          borderColor: colors.surface
        }]
      },
      options: {
        cutout: '70%',
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: true,
            position: 'bottom',
            labels: {
              color: colors.textColor,
              font: { family: 'IBM Plex Sans', size: 12, weight: 600 },
              boxWidth: 12,
              boxHeight: 12,
              padding: 14
            }
          }
        }
      }
    });
  }
}

async function renderZpCandidates() {
  const candidates = await loadZpCandidates();
  if (!candidates) return;

  const { zone, gender, search, missingFilter, demographicFilter, page, pageSize } = state.zpCandidateFilter;

  const filtered = candidates.filter(c => {
    const matchZone = zone === 'All' || c.zone.toLowerCase() === zone.toLowerCase();
    const matchGender = gender === 'All' ||
      c.gender.toLowerCase() === gender.toLowerCase() ||
      (gender.toLowerCase() === 'female' && isFemaleCandidate(c));

    let matchDemo = true;
    if (demographicFilter === 'youth') {
      matchDemo = isYouthCandidate(c);
    } else if (demographicFilter === 'female') {
      matchDemo = isFemaleCandidate(c);
    } else if (demographicFilter === 'minority') {
      matchDemo = isMinorityCandidate(c);
    }

    const hasMissingPhone = !c.contact || !c.contact.trim();
    const hasMissingGender = !c.gender || !c.gender.trim();
    const hasMissingCat = !c.category || !c.category.trim();

    let matchMissing = true;
    if (missingFilter === 'phone') {
      matchMissing = hasMissingPhone;
    } else if (missingFilter === 'gender') {
      matchMissing = hasMissingGender;
    } else if (missingFilter === 'category') {
      matchMissing = hasMissingCat;
    } else if (missingFilter === 'any') {
      matchMissing = hasMissingPhone || hasMissingGender || hasMissingCat;
    }

    let matchSearch = true;
    if (search) {
      const words = search.toLowerCase().split(/\s+/).filter(Boolean);
      matchSearch = words.every(word => {
        if (word === 'yuva' || word === 'youth') {
          return isYouthCandidate(c);
        } else if (word === 'minority' || word === 'alpashankhyak') {
          return isMinorityCandidate(c);
        } else if (word === 'female' || word === 'mahila' || word === 'women') {
          return isFemaleCandidate(c);
        } else {
          return (
            (c.name && c.name.toLowerCase().includes(word)) ||
            (c.district && c.district.toLowerCase().includes(word)) ||
            (c.block && c.block.toLowerCase().includes(word)) ||
            (c.zpSeat && c.zpSeat.toLowerCase().includes(word)) ||
            (c.category && c.category.toLowerCase().includes(word)) ||
            (c.caste && c.caste.toLowerCase().includes(word)) ||
            (c.seatReservation && c.seatReservation.toLowerCase().includes(word)) ||
            (c.contact && c.contact.includes(word)) ||
            (c.age && String(c.age).trim() === word)
          );
        }
      });
    }

    return matchZone && matchGender && matchDemo && matchMissing && matchSearch;
  });

  const banner = document.getElementById('zp-cand-active-filter-banner');
  const bannerText = document.getElementById('zp-active-filter-text');
  const activeTags = [];
  if (demographicFilter === 'youth') activeTags.push('🌱 Yuva / Youth (Age ≤ 40)');
  if (demographicFilter === 'female') activeTags.push('👩 Mahila / Women');
  if (demographicFilter === 'minority') activeTags.push('✨ Minority');
  if (missingFilter && missingFilter !== 'all') activeTags.push(`⚠️ Missing ${missingFilter}`);
  if (gender !== 'All' && demographicFilter !== 'female') activeTags.push(`Gender: ${gender}`);
  if (zone !== 'All') activeTags.push(`Zone: ${zone}`);
  if (search) activeTags.push(`Search: "${search}"`);

  if (banner && bannerText) {
    if (activeTags.length > 0) {
      bannerText.textContent = `Filtered: ${activeTags.join(' • ')} (${filtered.length} candidates)`;
      banner.classList.remove('hidden');
    } else {
      banner.classList.add('hidden');
    }
  }

  const total = filtered.length;
  const totalPages = Math.ceil(total / pageSize) || 1;
  const curPage = Math.min(page, totalPages);
  const start = (curPage - 1) * pageSize;
  const pageItems = filtered.slice(start, start + pageSize);

  const tbody = document.getElementById('zp-candidate-table-body');
  if (tbody) {
    if (pageItems.length === 0) {
      tbody.innerHTML = `<tr><td colspan="8" class="text-center py-10 text-slate-400">No candidates found matching criteria.</td></tr>`;
    } else {
      tbody.innerHTML = pageItems.map((c) => {
        const hasMissingPhone = !c.contact || !c.contact.trim();
        const hasMissingGender = !c.gender || !c.gender.trim();
        const hasMissingCat = !c.category || !c.category.trim();
        const isMissingAny = hasMissingPhone || hasMissingGender || hasMissingCat;

        const youth = isYouthCandidate(c);
        const minority = isMinorityCandidate(c);
        const demoBadge = youth
          ? `<span class="text-[10px] px-1.5 py-0.5 rounded font-bold bg-amber-50 text-amber-800 border border-amber-200">🌱 Yuva (${c.age || '≤40'})</span>`
          : (c.age ? `<span class="text-[10px] text-slate-400 font-mono">Age ${c.age}</span>` : '');

        const minorityBadge = minority
          ? `<span class="text-[10px] px-1.5 py-0.5 rounded font-bold bg-purple-50 text-purple-800 border border-purple-200">✨ Minority</span>`
          : '';

        return `
        <tr class="hover:bg-slate-50 transition-colors cursor-pointer ${isMissingAny ? 'row-has-missing' : ''}" onclick="openCandidateModal('${c.id}', 'zp')">
          <td class="font-mono text-xs text-slate-400 font-bold">${c.id}</td>
          <td>
            <div class="font-bold text-slate-900 hover:text-blue-600 transition-colors flex items-center gap-1.5 flex-wrap">
              <span>${c.name}</span>
              ${demoBadge}
              ${minorityBadge}
              ${isMissingAny ? '<span class="w-1.5 h-1.5 rounded-full bg-rose-500 inline-block" title="Incomplete Record"></span>' : ''}
            </div>
            <div class="text-xs mt-0.5">
              ${hasMissingPhone 
                ? '<span class="badge-missing"><i data-lucide="phone-off" class="w-3 h-3"></i> Missing Phone</span>' 
                : `<span class="text-slate-500 font-mono">${c.contact}</span>`}
            </div>
          </td>
          <td>
            <div class="font-semibold text-slate-800">${c.district}</div>
            <div class="text-xs text-slate-400">${c.zone}</div>
          </td>
          <td>
            <div class="text-slate-800 font-medium">${c.block}</div>
            <div class="text-xs text-blue-600 font-bold">${c.zpSeat}</div>
          </td>
          <td>
            <span class="text-xs px-2 py-0.5 rounded-full bg-slate-100 text-slate-600 font-medium">
              ${c.seatReservation || 'Unreserved'}
            </span>
          </td>
          <td>
            ${hasMissingGender 
              ? '<span class="badge-incomplete"><i data-lucide="help-circle" class="w-3 h-3"></i> Missing</span>' 
              : `<span class="text-xs px-2 py-0.5 rounded font-bold ${c.gender?.toLowerCase() === 'female' ? 'bg-pink-50 text-pink-600' : 'bg-blue-50 text-blue-600'}">${c.gender || 'Male'}</span>`}
          </td>
          <td>
            ${hasMissingCat 
              ? '<span class="badge-incomplete"><i data-lucide="help-circle" class="w-3 h-3"></i> Missing</span>' 
              : `<span class="text-xs px-2 py-0.5 rounded font-bold bg-slate-100 text-slate-600">${c.category || 'GEN'}</span>`}
          </td>
          <td class="text-right">
            <button onclick="event.stopPropagation(); openCandidateModal('${c.id}', 'zp')" class="vento-btn-secondary text-[11px] py-1">
              View Profile
            </button>
          </td>
        </tr>
      `}).join('');
    }
  }

  const infoEl = document.getElementById('zp-cand-pagination-info');
  if (infoEl) infoEl.textContent = `Showing ${total === 0 ? 0 : start + 1} to ${Math.min(start + pageSize, total)} of ${total} candidates`;

  const prevBtn = document.getElementById('zp-cand-prev-btn');
  const nextBtn = document.getElementById('zp-cand-next-btn');
  if (prevBtn) prevBtn.disabled = curPage <= 1;
  if (nextBtn) nextBtn.disabled = curPage >= totalPages;
  lucide.createIcons();
}

function filterZpByMissing(filterType = 'phone') {
  switchMainTab('zp');
  switchZpTab('zp-candidates');
  setZpMissingFilter(filterType);
}

function setZpMissingFilter(filterType) {
  state.zpCandidateFilter.missingFilter = filterType;
  state.zpCandidateFilter.page = 1;

  ['all', 'phone', 'gender', 'category', 'any'].forEach(f => {
    const btn = document.getElementById(`zp-filter-missing-${f}`);
    if (btn) {
      if (f === filterType) {
        btn.classList.add('pill-filter-btn-active');
      } else {
        btn.classList.remove('pill-filter-btn-active');
      }
    }
  });

  renderZpCandidates();
}

function prevZpCandidatePage() {
  if (state.zpCandidateFilter.page > 1) {
    state.zpCandidateFilter.page--;
    renderZpCandidates();
  }
}

function nextZpCandidatePage() {
  state.zpCandidateFilter.page++;
  renderZpCandidates();
}

/* ==========================================================================
   3. BLOCK PRAMUKH (BP) SECTION & SUB-TABS
   ========================================================================== */

function renderBpDistrictWise() {
  if (!state.summary) return;
  const list = state.summary.bp.districtWise;
  const { zone, search, sortCol, sortAsc, page, pageSize } = state.bpDistrictFilter;

  let filtered = list.filter(d => {
    const matchZone = zone === 'All' || d.zone.toLowerCase() === zone.toLowerCase();
    const matchSearch = !search || d.district.toLowerCase().includes(search) || d.zone.toLowerCase().includes(search);
    const matchGap = !state.zpDistrictFilter.gapOnly || d.gap1 > 0;
    return matchZone && matchSearch && matchGap;
  });

  filtered.sort((a, b) => {
    let vA = a[sortCol];
    let vB = b[sortCol];
    return sortAsc ? vA - vB : vB - vA;
  });

  const total = filtered.length;
  const totalPages = Math.ceil(total / pageSize) || 1;
  const curPage = Math.min(page, totalPages);
  const start = (curPage - 1) * pageSize;
  const pageItems = filtered.slice(start, start + pageSize);

  const tbody = document.getElementById('bp-district-table-body');
  if (tbody) {
    if (pageItems.length === 0) {
      tbody.innerHTML = `<tr><td colspan="9" class="text-center py-8 text-slate-400">No districts match criteria.</td></tr>`;
    } else {
      tbody.innerHTML = pageItems.map((d, idx) => `
        <tr class="hover:bg-slate-50 transition-colors">
          <td class="font-mono text-xs text-slate-400">${start + idx + 1}</td>
          <td class="font-bold text-slate-900">
            ${d.district}
            <span class="block text-xs font-normal text-slate-400">${d.zone}</span>
          </td>
          <td class="text-center font-bold text-amber-700">${d.blocks}</td>
          <td class="text-center text-slate-600 font-medium">${d.blocksWith1}</td>
          <td class="text-center text-slate-600 font-medium">${d.blocksWith2}</td>
          <td class="text-center text-slate-600 font-medium">${d.blocksWith3}</td>
          <td class="text-center font-black text-amber-700">${d.totalIdentified}</td>
          <td class="text-center font-bold text-rose-600">${d.gap1}</td>
          <td class="text-center text-slate-500 font-medium">${d.gap2}</td>
        </tr>
      `).join('');
    }
  }

  const infoEl = document.getElementById('bp-district-pagination-info');
  if (infoEl) infoEl.textContent = `Showing ${total === 0 ? 0 : start + 1} to ${Math.min(start + pageSize, total)} of ${total} districts`;

  const prevBtn = document.getElementById('bp-district-prev-btn');
  const nextBtn = document.getElementById('bp-district-next-btn');
  if (prevBtn) prevBtn.disabled = curPage <= 1;
  if (nextBtn) nextBtn.disabled = curPage >= totalPages;
}

function prevBpDistrictPage() {
  if (state.bpDistrictFilter.page > 1) {
    state.bpDistrictFilter.page--;
    renderBpDistrictWise();
  }
}

function nextBpDistrictPage() {
  state.bpDistrictFilter.page++;
  renderBpDistrictWise();
}

function renderBpProgressReport() {
  if (!state.summary) return;
  const zones = state.summary.bp.progressByZone;

  const cardsContainer = document.getElementById('bp-progress-zone-cards');
  if (cardsContainer) {
    cardsContainer.innerHTML = zones.map(z => {
      const pct = parseFloat(z.coveragePct) || 0;
      return `
        <div class="vento-card p-4 flex flex-col justify-between hover:shadow-md transition-all">
          <div class="flex items-center justify-between mb-2">
            <h4 class="font-extrabold text-[var(--ink)] font-sans text-sm">${z.zone}</h4>
            <span class="text-[10px] font-bold px-2 py-0.5 rounded-full ${pct >= 40 ? 'bg-[var(--primary-soft)] text-[var(--primary)]' : 'bg-[var(--surface)] border border-[var(--line)] text-[var(--muted)]'}">
              ${z.coveragePct}
            </span>
          </div>
          <div class="space-y-1 mb-2 text-xs">
            <div class="flex justify-between text-[var(--muted)] font-sans">
              <span>Blocks: <strong class="text-[var(--ink)] font-mono">${z.blocks}</strong></span>
              <span>Target: <strong class="text-[var(--ink)] font-mono">${z.target3x}</strong></span>
            </div>
            <div class="flex justify-between text-[var(--muted)] font-sans">
              <span>Identified: <strong class="text-[var(--accent)] font-mono">${z.identified}</strong></span>
              <span>Deficit: <strong class="text-[var(--alert)] font-mono">${z.remaining}</strong></span>
            </div>
          </div>
        </div>
      `;
    }).join('');
    lucide.createIcons({ root: cardsContainer });
  }

  const ctx = document.getElementById('chart-bp-zone-progress');
  if (ctx) {
    if (state.charts.bpZoneProgress) state.charts.bpZoneProgress.destroy();
    const colors = getThemeColors();
    state.charts.bpZoneProgress = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: zones.map(z => z.zone),
        datasets: [
          { label: 'Identified', data: zones.map(z => z.identified), backgroundColor: colors.bp, borderRadius: 3 },
          { label: 'Remaining Deficit', data: zones.map(z => z.remaining), backgroundColor: colors.alert, borderRadius: 3 }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: true,
            position: 'top',
            align: 'end',
            labels: {
              color: colors.textColor,
              font: { family: 'IBM Plex Sans', size: 12, weight: 600 },
              boxWidth: 12,
              boxHeight: 12,
              padding: 14
            }
          }
        },
        scales: {
          x: { stacked: true, grid: { display: false }, ticks: { color: colors.textColor, font: { family: 'IBM Plex Mono', size: 10 } } },
          y: { stacked: true, grid: { color: colors.gridColor }, ticks: { color: colors.mutedText, font: { family: 'IBM Plex Mono', size: 10 } } }
        }
      }
    });
  }
}

function renderBpBifurcation() {
  if (!state.summary) return;
  const totals = state.summary.bp.bifurcationTotals;
  const totalBp = totals.total || 1;

  const totalEl = document.getElementById('bp-bif-total');
  if (totalEl) totalEl.textContent = totals.total.toLocaleString();

  const maleEl = document.getElementById('bp-bif-male');
  if (maleEl) maleEl.textContent = totals.male.toLocaleString();
  const malePctEl = document.getElementById('bp-bif-male-pct');
  if (malePctEl) malePctEl.textContent = `${round(totals.male / totalBp * 100)}%`;

  const femaleEl = document.getElementById('bp-bif-female');
  if (femaleEl) femaleEl.textContent = totals.female.toLocaleString();
  const femalePctEl = document.getElementById('bp-bif-female-pct');
  if (femalePctEl) femalePctEl.textContent = `${round(totals.female / totalBp * 100)}%`;

  const yuvaEl = document.getElementById('bp-bif-yuva');
  if (yuvaEl) yuvaEl.textContent = totals.yuva.toLocaleString();
  const yuvaPctEl = document.getElementById('bp-bif-yuva-pct');
  if (yuvaPctEl) yuvaPctEl.textContent = `${round(totals.yuva / totalBp * 100)}%`;

  const minEl = document.getElementById('bp-bif-minority');
  if (minEl && totals.minority !== undefined) minEl.textContent = totals.minority.toLocaleString();
  const minPctEl = document.getElementById('bp-bif-minority-pct');
  if (minPctEl && totals.minority !== undefined) minPctEl.textContent = `${round(totals.minority / totalBp * 100)}%`;
}

async function renderBpCandidates() {
  const candidates = await loadBpCandidates();
  if (!candidates) return;

  const { zone, gender, search, missingFilter, demographicFilter, page, pageSize } = state.bpCandidateFilter;

  const filtered = candidates.filter(c => {
    const matchZone = zone === 'All' || c.zone.toLowerCase() === zone.toLowerCase();
    const matchGender = !gender || gender === 'All' ||
      (c.gender && c.gender.toLowerCase() === gender.toLowerCase()) ||
      (gender.toLowerCase() === 'female' && isFemaleCandidate(c)) ||
      (gender.toLowerCase() === 'male' && c.gender && c.gender.toLowerCase() === 'male');

    let matchDemo = true;
    if (demographicFilter === 'youth') {
      matchDemo = isYouthCandidate(c);
    } else if (demographicFilter === 'female') {
      matchDemo = isFemaleCandidate(c);
    } else if (demographicFilter === 'minority') {
      matchDemo = isMinorityCandidate(c);
    }

    const hasMissingPhone = !c.contact || !c.contact.trim();
    const hasMissingGender = !c.gender || !c.gender.trim();
    const hasMissingCat = !c.category && !c.candidateCategory;

    let matchMissing = true;
    if (missingFilter === 'phone') {
      matchMissing = hasMissingPhone;
    } else if (missingFilter === 'gender') {
      matchMissing = hasMissingGender;
    } else if (missingFilter === 'any') {
      matchMissing = hasMissingPhone || hasMissingGender || hasMissingCat;
    }

    let matchSearch = true;
    if (search) {
      const words = search.toLowerCase().split(/\s+/).filter(Boolean);
      matchSearch = words.every(word => {
        if (word === 'yuva' || word === 'youth') {
          return isYouthCandidate(c);
        } else if (word === 'minority' || word === 'alpashankhyak') {
          return isMinorityCandidate(c);
        } else if (word === 'female' || word === 'mahila' || word === 'women') {
          return isFemaleCandidate(c);
        } else {
          return (
            (c.name && c.name.toLowerCase().includes(word)) ||
            (c.district && c.district.toLowerCase().includes(word)) ||
            (c.block && c.block.toLowerCase().includes(word)) ||
            (c.contact && c.contact.includes(word)) ||
            (c.category && c.category.toLowerCase().includes(word)) ||
            (c.candidateCategory && c.candidateCategory.toLowerCase().includes(word)) ||
            (c.caste && c.caste.toLowerCase().includes(word)) ||
            (c.pkMeetingStatus && c.pkMeetingStatus.toLowerCase().includes(word)) ||
            (c.age && String(c.age).trim() === word)
          );
        }
      });
    }

    return matchZone && matchGender && matchDemo && matchMissing && matchSearch;
  });

  const banner = document.getElementById('bp-cand-active-filter-banner');
  const bannerText = document.getElementById('bp-active-filter-text');
  const activeTags = [];
  if (demographicFilter === 'youth') activeTags.push('🌱 Yuva / Youth (Age ≤ 40)');
  if (demographicFilter === 'female') activeTags.push('👩 Mahila / Women');
  if (demographicFilter === 'minority') activeTags.push('✨ Minority');
  if (missingFilter && missingFilter !== 'all') activeTags.push(`⚠️ Missing ${missingFilter}`);
  if (gender !== 'All' && demographicFilter !== 'female') activeTags.push(`Gender: ${gender}`);
  if (zone !== 'All') activeTags.push(`Zone: ${zone}`);
  if (search) activeTags.push(`Search: "${search}"`);

  if (banner && bannerText) {
    if (activeTags.length > 0) {
      bannerText.textContent = `Filtered: ${activeTags.join(' • ')} (${filtered.length} pramukhs)`;
      banner.classList.remove('hidden');
    } else {
      banner.classList.add('hidden');
    }
  }

  const total = filtered.length;
  const totalPages = Math.ceil(total / pageSize) || 1;
  const curPage = Math.min(page, totalPages);
  const start = (curPage - 1) * pageSize;
  const pageItems = filtered.slice(start, start + pageSize);

  const tbody = document.getElementById('bp-candidate-table-body');
  if (tbody) {
    if (pageItems.length === 0) {
      tbody.innerHTML = `<tr><td colspan="8" class="text-center py-10 text-slate-400">No Block Pramukh candidates match criteria.</td></tr>`;
    } else {
      tbody.innerHTML = pageItems.map((c) => {
        const hasMissingPhone = !c.contact || !c.contact.trim();
        const hasMissingGender = !c.gender || !c.gender.trim();
        const hasMissingCat = !c.category && !c.candidateCategory;
        const isMissingAny = hasMissingPhone || hasMissingGender || hasMissingCat;

        const youth = isYouthCandidate(c);
        const minority = isMinorityCandidate(c);
        const demoBadge = youth
          ? `<span class="text-[10px] px-1.5 py-0.5 rounded font-bold bg-amber-50 text-amber-800 border border-amber-200">🌱 Yuva (${c.age || '≤40'})</span>`
          : (c.age ? `<span class="text-[10px] text-slate-400 font-mono">Age ${c.age}</span>` : '');

        const minorityBadge = minority
          ? `<span class="text-[10px] px-1.5 py-0.5 rounded font-bold bg-purple-50 text-purple-800 border border-purple-200">✨ Minority</span>`
          : '';

        return `
        <tr class="hover:bg-slate-50 transition-colors cursor-pointer ${isMissingAny ? 'row-has-missing' : ''}" onclick="openCandidateModal('${c.id}', 'bp')">
          <td class="font-mono text-xs text-slate-400 font-bold">${c.id}</td>
          <td>
            <div class="font-bold text-slate-900 hover:text-amber-700 transition-colors flex items-center gap-1.5 flex-wrap">
              <span>${c.name}</span>
              ${demoBadge}
              ${minorityBadge}
              ${isMissingAny ? '<span class="w-1.5 h-1.5 rounded-full bg-rose-500 inline-block" title="Incomplete Record"></span>' : ''}
            </div>
            <div class="text-xs mt-0.5">
              ${hasMissingPhone 
                ? '<span class="badge-missing"><i data-lucide="phone-off" class="w-3 h-3"></i> Missing Phone</span>' 
                : `<span class="text-slate-500 font-mono">${c.contact}</span>`}
            </div>
          </td>
          <td>
            <div class="font-semibold text-slate-800">${c.district}</div>
            <div class="text-xs text-slate-400">${c.zone}</div>
          </td>
          <td>
            <div class="font-bold text-amber-700">${c.block}</div>
          </td>
          <td>
            ${hasMissingGender 
              ? '<span class="badge-incomplete"><i data-lucide="help-circle" class="w-3 h-3"></i> Missing</span>' 
              : `<span class="text-xs px-2 py-0.5 rounded font-bold ${c.gender?.toLowerCase() === 'female' ? 'bg-pink-50 text-pink-600' : 'bg-blue-50 text-blue-600'}">${c.gender || 'Male'}</span>`}
          </td>
          <td>
            ${hasMissingCat 
              ? '<span class="badge-incomplete"><i data-lucide="help-circle" class="w-3 h-3"></i> Missing</span>' 
              : `<span class="text-xs px-2 py-0.5 rounded font-bold bg-slate-100 text-slate-600">${c.category || c.candidateCategory || 'GEN'}</span>`}
          </td>
          <td>
            <span class="text-xs px-2 py-0.5 rounded-full font-bold ${c.pkMeetingStatus ? 'bg-emerald-50 text-emerald-700' : 'text-slate-400'}">
              ${c.pkMeetingStatus || 'Pending'}
            </span>
          </td>
          <td class="text-right">
            <button onclick="event.stopPropagation(); openCandidateModal('${c.id}', 'bp')" class="vento-btn-secondary text-[11px] py-1">
              View Profile
            </button>
          </td>
        </tr>
      `}).join('');
    }
  }

  const infoEl = document.getElementById('bp-cand-pagination-info');
  if (infoEl) infoEl.textContent = `Showing ${total === 0 ? 0 : start + 1} to ${Math.min(start + pageSize, total)} of ${total} candidates`;

  const prevBtn = document.getElementById('bp-cand-prev-btn');
  const nextBtn = document.getElementById('bp-cand-next-btn');
  if (prevBtn) prevBtn.disabled = curPage <= 1;
  if (nextBtn) nextBtn.disabled = curPage >= totalPages;
  lucide.createIcons();
}

function setBpMissingFilter(filterType) {
  state.bpCandidateFilter.missingFilter = filterType;
  state.bpCandidateFilter.page = 1;

  ['all', 'phone', 'gender', 'any'].forEach(f => {
    const btn = document.getElementById(`bp-filter-missing-${f}`);
    if (btn) {
      if (f === filterType) {
        btn.classList.add('pill-filter-btn-active');
      } else {
        btn.classList.remove('pill-filter-btn-active');
      }
    }
  });

  renderBpCandidates();
}

function prevBpCandidatePage() {
  if (state.bpCandidateFilter.page > 1) {
    state.bpCandidateFilter.page--;
    renderBpCandidates();
  }
}

function nextBpCandidatePage() {
  state.bpCandidateFilter.page++;
  renderBpCandidates();
}

/* ==========================================================================
   4. 12 ZONE DEEP DIVES
   ========================================================================== */

async function switchZoneDeepDive(zoneName) {
  state.selectedZoneTab = zoneName;

  document.querySelectorAll('#zone-tab-buttons button').forEach(btn => {
    const isAct = btn.textContent.trim() === zoneName;
    if (isAct) {
      btn.classList.add('zone-tab-active');
      btn.classList.add('pill-filter-btn-active');
    } else {
      btn.classList.remove('zone-tab-active');
      btn.classList.remove('pill-filter-btn-active');
    }
  });

  renderZoneDeepDive(zoneName);
}

async function renderZoneDeepDive(zoneName) {
  if (!state.summary) return;

  const zpProgress = state.summary.zp.progressByZone.find(z => z.zone.toLowerCase() === zoneName.toLowerCase());
  const bpProgress = state.summary.bp.progressByZone.find(b => b.zone.toLowerCase() === zoneName.toLowerCase());
  const districts = state.summary.zp.districtWise.filter(d => d.zone.toLowerCase() === zoneName.toLowerCase());

  document.getElementById('zone-title').textContent = `${zoneName} Zone Profile`;

  if (zpProgress) {
    document.getElementById('zone-zp-seats').textContent = zpProgress.seats;
    document.getElementById('zone-zp-target').textContent = zpProgress.target5x;
    document.getElementById('zone-zp-identified').textContent = zpProgress.identified;
    document.getElementById('zone-zp-remaining').textContent = zpProgress.remaining;
    document.getElementById('zone-zp-coverage').textContent = zpProgress.coveragePct;
  }

  if (bpProgress) {
    document.getElementById('zone-bp-blocks').textContent = bpProgress.blocks;
    document.getElementById('zone-bp-target').textContent = bpProgress.target3x;
    document.getElementById('zone-bp-identified').textContent = bpProgress.identified;
    document.getElementById('zone-bp-remaining').textContent = bpProgress.remaining;
    document.getElementById('zone-bp-coverage').textContent = bpProgress.coveragePct;
  }

  const distContainer = document.getElementById('zone-districts-list');
  if (distContainer) {
    distContainer.innerHTML = districts.map(d => `
      <div class="vento-card p-4 hover:shadow-md transition-all">
        <div class="flex items-center justify-between mb-2">
          <h5 class="font-extrabold text-slate-900 text-base">${d.district}</h5>
          <span class="text-xs px-2.5 py-0.5 rounded-full font-bold bg-blue-50 text-blue-700">
            ${d.seats} Seats
          </span>
        </div>
        <div class="grid grid-cols-2 gap-1.5 text-sm text-slate-500">
          <div>Identified: <strong class="text-emerald-700">${d.totalIdentified}</strong></div>
          <div>Gap 1: <strong class="text-rose-600">${d.gap1}</strong></div>
          <div>Progress: <strong class="text-slate-700">${d.progressPct}</strong></div>
          <div>≥1: <strong class="text-slate-700">${d.seatsWith1}</strong></div>
        </div>
      </div>
    `).join('');
  }

  const candidates = await loadZpCandidates();
  const zoneCands = candidates ? candidates.filter(c => c.zone.toLowerCase() === zoneName.toLowerCase()) : [];

  const rosterBody = document.getElementById('zone-roster-body');
  if (rosterBody) {
    rosterBody.innerHTML = zoneCands.slice(0, 15).map((c, i) => `
      <tr class="hover:bg-slate-50 cursor-pointer text-sm" onclick="openCandidateModal('${c.id}', 'zp')">
        <td class="font-mono text-sm text-slate-400">${i + 1}</td>
        <td class="font-bold text-slate-900">${c.name}</td>
        <td class="text-slate-600">${c.district}</td>
        <td class="text-blue-600 font-bold">${c.zpSeat}</td>
        <td><span class="text-xs px-2 py-0.5 rounded-full bg-slate-100 text-slate-600">${c.seatReservation || 'Unreserved'}</span></td>
        <td class="text-slate-500 text-sm">${c.contact || '—'}</td>
      </tr>
    `).join('');
  }

  lucide.createIcons();
}

/* ==========================================================================
   5. CANDIDATE PROFILE MODAL
   ========================================================================== */

async function openCandidateModal(candidateId, type = 'zp') {
  let candidate = null;
  if (type === 'zp') {
    const list = await loadZpCandidates();
    candidate = list.find(c => c.id === candidateId);
  } else {
    const list = await loadBpCandidates();
    candidate = list.find(c => c.id === candidateId);
  }

  if (!candidate) {
    showToast('Candidate dossier not found', 'error');
    return;
  }

  const modal = document.getElementById('candidate-modal');
  if (!modal) return;

  document.getElementById('modal-title').textContent = candidate.name;
  document.getElementById('modal-subtitle').textContent = `${type === 'zp' ? 'Zila Parishad Candidate' : 'Block Pramukh Candidate'} • ID: ${candidate.id}`;
  document.getElementById('modal-zone').textContent = candidate.zone || '—';
  document.getElementById('modal-district').textContent = candidate.district || '—';
  document.getElementById('modal-block').textContent = candidate.block || '—';
  document.getElementById('modal-seat').textContent = candidate.zpSeat || '—';
  document.getElementById('modal-reservation').textContent = candidate.seatReservation || 'Unreserved';
  const alertBox = document.getElementById('modal-missing-alert');
  const alertText = document.getElementById('modal-missing-alert-text');
  const hasMissingPhone = !candidate.contact || !candidate.contact.trim();
  const hasMissingGender = !candidate.gender || !candidate.gender.trim();
  const hasMissingCat = !candidate.category && !candidate.candidateCategory;

  let missingItems = [];
  if (hasMissingPhone) missingItems.push('Phone Number');
  if (hasMissingGender) missingItems.push('Gender');
  if (hasMissingCat) missingItems.push('Category');

  if (alertBox && alertText) {
    if (missingItems.length > 0) {
      alertBox.classList.remove('hidden');
      alertText.textContent = `Incomplete Candidate Profile: Missing ${missingItems.join(', ')} — Field verification required`;
    } else {
      alertBox.classList.add('hidden');
    }
  }

  const phoneEl = document.getElementById('modal-phone');
  if (phoneEl) {
    if (hasMissingPhone) {
      phoneEl.innerHTML = '<span class="badge-missing"><i data-lucide="phone-off" class="w-3.5 h-3.5"></i> Not Provided</span>';
    } else {
      phoneEl.textContent = candidate.contact;
    }
  }

  const genderEl = document.getElementById('modal-gender');
  if (genderEl) {
    if (hasMissingGender) {
      genderEl.innerHTML = '<span class="badge-incomplete"><i data-lucide="help-circle" class="w-3 h-3"></i> Not Recorded</span>';
    } else {
      genderEl.textContent = candidate.gender;
    }
  }

  const catEl = document.getElementById('modal-category');
  if (catEl) {
    if (hasMissingCat) {
      catEl.innerHTML = '<span class="badge-incomplete"><i data-lucide="help-circle" class="w-3 h-3"></i> Not Recorded</span>';
    } else {
      catEl.textContent = candidate.category || candidate.candidateCategory;
    }
  }

  document.getElementById('modal-age').textContent = candidate.age ? `${candidate.age} Years` : '—';
  document.getElementById('modal-caste').textContent = candidate.caste || '—';
  document.getElementById('modal-poc').textContent = candidate.jsptPoc || '—';
  document.getElementById('modal-designation').textContent = candidate.jsDesignation || '—';
  document.getElementById('modal-profile').textContent = candidate.briefProfile || 'No biographical profile available in current registry.';
  document.getElementById('modal-remarks').textContent = candidate.remarks || 'No remarks recorded.';

  const bpMeetingBox = document.getElementById('modal-bp-meeting-box');
  if (bpMeetingBox) {
    if (type === 'bp' && candidate.pkMeetingStatus) {
      bpMeetingBox.classList.remove('hidden');
      document.getElementById('modal-meeting-status').textContent = candidate.pkMeetingStatus;
      document.getElementById('modal-meeting-date').textContent = candidate.meetingDate || '—';
    } else {
      bpMeetingBox.classList.add('hidden');
    }
  }

  modal.classList.remove('hidden');
  lucide.createIcons({ root: modal });
}

function copyCandidatePhone() {
  const phone = document.getElementById('modal-phone').textContent;
  if (phone && phone !== 'Not Provided') {
    navigator.clipboard.writeText(phone);
    showToast(`Copied phone: ${phone}`, 'success');
  } else {
    showToast('No phone number available to copy', 'info');
  }
}

/* ==========================================================================
   6. CSV EXPORT UTILITY
   ========================================================================== */

function exportTableToCsv(type) {
  let filename = 'export.csv';
  let rows = [];

  if (type === 'zp-districts') {
    filename = 'Bihar_ZP_District_Wise_Report_2026.csv';
    rows.push(['Zone', 'District', 'ZP Seats', 'Seats with 1', 'Seats with 2', 'Seats with 3', 'Seats with 4', 'Seats with 5+', 'Total Identified', 'GAP 1', 'GAP 2', 'Progress %']);
    state.summary.zp.districtWise.forEach(d => {
      rows.push([d.zone, d.district, d.seats, d.seatsWith1, d.seatsWith2, d.seatsWith3, d.seatsWith4, d.seatsWith5, d.totalIdentified, d.gap1, d.gap2, d.progressPct]);
    });
  } else if (type === 'bp-districts') {
    filename = 'Bihar_BP_District_Wise_Report_2026.csv';
    rows.push(['Zone', 'District', 'Blocks', 'Blocks with 1', 'Blocks with 2', 'Blocks with 3', 'Total Identified', 'GAP 1', 'GAP 2']);
    state.summary.bp.districtWise.forEach(d => {
      rows.push([d.zone, d.district, d.blocks, d.blocksWith1, d.blocksWith2, d.blocksWith3, d.totalIdentified, d.gap1, d.gap2]);
    });
  }

  const csvContent = "data:text/csv;charset=utf-8," + rows.map(e => e.join(",")).join("\n");
  const encodedUri = encodeURI(csvContent);
  const link = document.createElement("a");
  link.setAttribute("href", encodedUri);
  link.setAttribute("download", filename);
  document.body.appendChild(link);
  link.click();
  link.remove();
  showToast(`Exported ${filename}`, 'success');
}

function round(num) {
  return Math.round(num * 10) / 10;
}

window.selectTheme = selectTheme;
window.toggleThemeDropdown = toggleThemeDropdown;
window.closeThemeDropdown = closeThemeDropdown;
