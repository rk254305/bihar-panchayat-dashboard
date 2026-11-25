with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Replace BIHAR INTERACTIVE MAP HANDLERS block with complete GIS map and Inspector functions
old_map_handlers_target = r'// ==========================================================================\n// BIHAR INTERACTIVE MAP HANDLERS\n// ==========================================================================.*?(?=// Realtime Header Clock)'

new_geo_map_code = '''// ==========================================================================
// BIHAR REAL GEOGRAPHIC MAP & DISTRICT INSPECTOR
// ==========================================================================
state.geoDistrictData = null;
state.selectedGeoDistrict = 'Purnia';
state.geoMapMetric = 'zp'; // 'zp', 'bp', 'females', 'gap'

async function loadGeoDistrictData() {
  if (state.geoDistrictData) return state.geoDistrictData;
  try {
    const res = await fetch('public/bihar_district_map_data.json?t=' + Date.now());
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
        <span class="flex items-center gap-1"><span class="w-2.5 h-2.5 rounded-[2px] bg-[var(--color-zp-subtle)] border border-[var(--color-zp)]"></span> On Target (≥60%)</span>
        <span class="flex items-center gap-1"><span class="w-2.5 h-2.5 rounded-[2px] bg-[var(--surface-subtle)] border border-[var(--hairline)]"></span> Moderate</span>
        <span class="flex items-center gap-1"><span class="w-2.5 h-2.5 rounded-[2px] bg-[var(--color-alert-subtle)] border border-[var(--color-alert)]"></span> <strong class="text-[var(--color-alert)]">● GAP 1 (Zero Seats)</strong></span>
      `;
    } else if (metric === 'bp') {
      legendEl.innerHTML = `
        <span class="flex items-center gap-1"><span class="w-2.5 h-2.5 rounded-[2px] bg-[var(--color-bp-subtle)] border border-[var(--color-bp)]"></span> High Pramukh Activity (≥40%)</span>
        <span class="flex items-center gap-1"><span class="w-2.5 h-2.5 rounded-[2px] bg-[var(--surface-subtle)] border border-[var(--hairline)]"></span> In Progress</span>
      `;
    } else if (metric === 'females') {
      legendEl.innerHTML = `
        <span class="flex items-center gap-1"><span class="w-2.5 h-2.5 rounded-[2px] bg-[var(--color-zp-subtle)] border border-[var(--color-zp)]"></span> High Female Density (≥20)</span>
        <span class="flex items-center gap-1"><span class="w-2.5 h-2.5 rounded-[2px] bg-[var(--color-bp-subtle)] border border-[var(--color-bp)]"></span> Moderate Female Inclusion (10-19)</span>
        <span class="flex items-center gap-1"><span class="w-2.5 h-2.5 rounded-[2px] bg-[var(--surface-subtle)] border border-[var(--hairline)]"></span> Emerging (<10)</span>
      `;
    } else if (metric === 'gap') {
      legendEl.innerHTML = `
        <span class="flex items-center gap-1"><span class="w-2.5 h-2.5 rounded-[2px] bg-[var(--color-alert-subtle)] border border-[var(--color-alert)]"></span> <strong class="text-[var(--color-alert)]">● Critical Gaps (40 Zero-Seats across 8 Districts)</strong></span>
      `;
    }
  }

  renderGeoMapColors();
  const labels = { zp: 'Zila Parishad Coverage', bp: 'Block Pramukh Coverage', females: 'Female Candidates', gap: 'GAP 1 Zero-Seat Alerts' };
  showToast(`Map overlay: ${labels[metric] || metric}`, 'info');
}

function renderGeoMapColors() {
  if (!state.geoDistrictData) return;
  const colors = getThemeColors();
  const metric = state.geoMapMetric;

  document.querySelectorAll('.bihar-district-boundary').forEach(path => {
    const distName = path.getAttribute('data-district');
    const d = state.geoDistrictData[distName];
    if (!d) return;

    if (metric === 'zp') {
      if (d.gap1Zp > 0) {
        path.setAttribute('fill', colors.isDark ? '#221211' : 'var(--color-alert-subtle)');
        path.setAttribute('stroke', colors.alert);
        path.setAttribute('opacity', '1');
      } else if (d.pctZp >= 60) {
        path.setAttribute('fill', colors.isDark ? '#0E1D1B' : 'var(--color-zp-subtle)');
        path.setAttribute('stroke', colors.zp);
        path.setAttribute('opacity', '1');
      } else {
        path.setAttribute('fill', colors.isDark ? '#141A23' : 'var(--surface-subtle)');
        path.setAttribute('stroke', colors.gapMuted);
        path.setAttribute('opacity', '1');
      }
    } else if (metric === 'bp') {
      if (d.pctBp >= 40) {
        path.setAttribute('fill', colors.isDark ? '#1C160B' : 'var(--color-bp-subtle)');
        path.setAttribute('stroke', colors.bp);
        path.setAttribute('opacity', '1');
      } else {
        path.setAttribute('fill', colors.isDark ? '#141A23' : 'var(--surface-subtle)');
        path.setAttribute('stroke', colors.gapMuted);
        path.setAttribute('opacity', '1');
      }
    } else if (metric === 'females') {
      const totalFem = (d.femalesZp || 0) + (d.femalesBp || 0);
      if (totalFem >= 20) {
        path.setAttribute('fill', colors.isDark ? '#0E1D1B' : 'var(--color-zp-subtle)');
        path.setAttribute('stroke', colors.zp);
        path.setAttribute('opacity', '1');
      } else if (totalFem >= 10) {
        path.setAttribute('fill', colors.isDark ? '#1C160B' : 'var(--color-bp-subtle)');
        path.setAttribute('stroke', colors.bp);
        path.setAttribute('opacity', '1');
      } else {
        path.setAttribute('fill', colors.isDark ? '#141A23' : 'var(--surface-subtle)');
        path.setAttribute('stroke', colors.gapMuted);
        path.setAttribute('opacity', '1');
      }
    } else if (metric === 'gap') {
      if (d.gap1Zp > 0) {
        path.setAttribute('fill', colors.isDark ? '#2A1312' : 'var(--color-alert-subtle)');
        path.setAttribute('stroke', colors.alert);
        path.setAttribute('stroke-width', '2');
        path.setAttribute('opacity', '1');
      } else {
        path.setAttribute('fill', colors.isDark ? '#0F141B' : 'var(--surface-card)');
        path.setAttribute('stroke', colors.isDark ? '#161D27' : 'var(--hairline-subtle)');
        path.setAttribute('stroke-width', '1');
        path.setAttribute('opacity', '0.45');
      }
    }
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

function hoverDistrictGeo(event, districtName) {
  const tooltip = document.getElementById('bihar-map-tooltip');
  if (!tooltip || !state.geoDistrictData) return;
  const d = state.geoDistrictData[districtName];
  if (!d) return;

  const gapAlert = d.gap1Zp > 0 ? `<div class="mt-1 pt-1 border-t border-[var(--hairline)] text-[var(--color-alert)] font-bold font-mono">● GAP 1: ${d.gap1Zp} Zero-Candidate Seats</div>` : '';

  tooltip.innerHTML = `
    <div class="font-bold text-xs text-[var(--ink-text)]">${d.district}</div>
    <div class="text-[10px] text-[var(--ink-muted)] font-mono">${d.zone} Zone • Code: ${d.code}</div>
    <div class="mt-1 flex items-center justify-between text-xs font-mono">
      <span class="text-[var(--ink-muted)]">ZP Coverage:</span>
      <span class="font-bold text-[var(--color-zp)]">${d.identifiedZp}/${d.target5xZp} (${d.pctZp}%)</span>
    </div>
    <div class="flex items-center justify-between text-xs font-mono">
      <span class="text-[var(--ink-muted)]">BP Coverage:</span>
      <span class="font-bold text-[var(--color-bp)]">${d.identifiedBp}/${d.target3xBp} (${d.pctBp}%)</span>
    </div>
    <div class="flex items-center justify-between text-[10px] font-mono text-[var(--ink-muted)] pt-0.5">
      <span>Females: <strong class="text-[var(--ink-text)]">${d.femalesZp + d.femalesBp}</strong></span>
      <span>Minority: <strong class="text-[var(--ink-text)]">${d.minorityZp + d.minorityBp}</strong></span>
    </div>
    ${gapAlert}
  `;
  tooltip.style.display = 'block';

  const container = tooltip.parentElement;
  if (container) {
    const rect = container.getBoundingClientRect();
    const x = event.clientX - rect.left + 14;
    const y = event.clientY - rect.top + 14;
    tooltip.style.left = `${Math.min(Math.max(x, 10), rect.width - 220)}px`;
    tooltip.style.top = `${Math.min(Math.max(y, 10), rect.height - 110)}px`;
  }
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
    state.zpCandidateFilter.page = 1;
    const searchInput = document.getElementById('zp-cand-search');
    if (searchInput) searchInput.value = dist;
    renderZpCandidates();
    showToast(`Showing ZP Candidates in ${dist}`, 'success');
  } else if (tier === 'bp') {
    switchMainTab('bp');
    switchBpTab('bp-candidates');
    state.bpCandidateFilter.search = dist.toLowerCase();
    state.bpCandidateFilter.page = 1;
    const searchInput = document.getElementById('bp-cand-search');
    if (searchInput) searchInput.value = dist;
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
}
'''

import re
js = re.sub(r'// ==========================================================================\n// BIHAR INTERACTIVE MAP HANDLERS\n// ==========================================================================.*?(?=// Realtime Header Clock)', new_geo_map_code, js, flags=re.DOTALL)

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("app.js updated with complete GIS map, live inspector, and mode switcher!")
