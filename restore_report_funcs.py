with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

funcs = '''
// ==========================================================================
// INDIVIDUAL DEMOGRAPHIC REPORT GENERATORS (SEPARATE ZP & BP)
// ==========================================================================
function generateFemaleReport(tier) {
  if (tier === 'zp') {
    switchMainTab('zp');
    switchZpTab('zp-candidates');
    state.zpCandidateFilter.gender = 'Female';
    state.zpCandidateFilter.page = 1;
    const genderSel = document.getElementById('zp-cand-gender-filter');
    if (genderSel) genderSel.value = 'Female';
    renderZpCandidates();
    showToast('Generated Individual Report: 607 Female Candidates in Zila Parishad', 'success');
  } else if (tier === 'bp') {
    switchMainTab('bp');
    switchBpTab('bp-candidates');
    state.bpCandidateFilter.gender = 'Female';
    state.bpCandidateFilter.page = 1;
    const genderSel = document.getElementById('bp-cand-gender-filter');
    if (genderSel) genderSel.value = 'Female';
    renderBpCandidates();
    showToast('Generated Individual Report: 40 Female Pramukhs in Block Pramukh', 'success');
  }
}

function generateMinorityReport(tier) {
  if (tier === 'zp') {
    switchMainTab('zp');
    switchZpTab('zp-candidates');
    state.zpCandidateFilter.search = 'minority';
    state.zpCandidateFilter.page = 1;
    const searchInput = document.getElementById('zp-cand-search');
    if (searchInput) searchInput.value = 'minority';
    renderZpCandidates();
    showToast('Generated Individual Report: 275 Minority Candidates in Zila Parishad', 'success');
  } else if (tier === 'bp') {
    switchMainTab('bp');
    switchBpTab('bp-candidates');
    state.bpCandidateFilter.search = 'minority';
    state.bpCandidateFilter.page = 1;
    const searchInput = document.getElementById('bp-cand-search');
    if (searchInput) searchInput.value = 'minority';
    renderBpCandidates();
    showToast('Generated Individual Report: 6 Minority Pramukhs in Block Pramukh', 'success');
  }
}

function generateYouthReport(tier) {
  if (tier === 'zp') {
    switchMainTab('zp');
    switchZpTab('zp-candidates');
    state.zpCandidateFilter.search = 'yuva';
    state.zpCandidateFilter.page = 1;
    const searchInput = document.getElementById('zp-cand-search');
    if (searchInput) searchInput.value = 'yuva';
    renderZpCandidates();
    showToast('Generated Individual Report: 1,050 Youth Candidates in Zila Parishad', 'success');
  } else if (tier === 'bp') {
    switchMainTab('bp');
    switchBpTab('bp-candidates');
    state.bpCandidateFilter.search = 'yuva';
    state.bpCandidateFilter.page = 1;
    const searchInput = document.getElementById('bp-cand-search');
    if (searchInput) searchInput.value = 'yuva';
    renderBpCandidates();
    showToast('Generated Individual Report: 144 Youth Pramukhs in Block Pramukh', 'success');
  }
}
'''

js = js.replace("// Realtime Header Clock", funcs + "\n// Realtime Header Clock")

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Restored report generator functions in app.js!")
