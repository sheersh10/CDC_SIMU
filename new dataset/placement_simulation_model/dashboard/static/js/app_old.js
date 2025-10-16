// ===========================
// Global Variables & State
// ===========================

const API_BASE = 'http://localhost:8000/api';
let charts = {};
let currentPage = {
    students: 0,
    companies: 0
};
const PAGE_SIZE = 100;

// ===========================
// Initialization
// ===========================

document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

async function initializeApp() {
    // Setup navigation
    setupNavigation();
    
    // Setup theme toggle
    setupThemeToggle();
    
    // Setup configuration sliders
    setupConfigurationControls();
    
    // Load initial data
    await loadInitialData();
    
    // Setup filter controls
    setupFilters();
    
    // Check for existing simulation results
    checkSimulationStatus();
}

// ===========================
// Navigation
// ===========================

function setupNavigation() {
    const navButtons = document.querySelectorAll('.nav-btn');
    
    navButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const section = btn.dataset.section;
            showSection(section);
            
            // Update active state
            navButtons.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
        });
    });
}

function showSection(sectionName) {
    const sections = document.querySelectorAll('.content-section');
    sections.forEach(section => {
        section.classList.remove('active');
    });
    
    const targetSection = document.getElementById(`${sectionName}-section`);
    if (targetSection) {
        targetSection.classList.add('active');
        
        // Load section-specific data
        if (sectionName === 'students') {
            loadStudentData();
        } else if (sectionName === 'companies') {
            loadCompanyData();
        } else if (sectionName === 'results') {
            loadResultsData();
        }
    }
}

// ===========================
// Theme Toggle
// ===========================

function setupThemeToggle() {
    const themeToggle = document.getElementById('themeToggle');
    const currentTheme = localStorage.getItem('theme') || 'light';
    
    if (currentTheme === 'dark') {
        document.documentElement.setAttribute('data-theme', 'dark');
        themeToggle.innerHTML = '<i class="fas fa-sun"></i>';
    }
    
    themeToggle.addEventListener('click', () => {
        const theme = document.documentElement.getAttribute('data-theme');
        
        if (theme === 'dark') {
            document.documentElement.setAttribute('data-theme', 'light');
            localStorage.setItem('theme', 'light');
            themeToggle.innerHTML = '<i class="fas fa-moon"></i>';
        } else {
            document.documentElement.setAttribute('data-theme', 'dark');
            localStorage.setItem('theme', 'dark');
            themeToggle.innerHTML = '<i class="fas fa-sun"></i>';
        }
    });
}

// ===========================
// Data Loading
// ===========================

async function loadInitialData() {
    showLoading();
    
    try {
        // Load summary stats
        await loadSummaryStats();
        
        // Load overview charts
        await loadOverviewCharts();
        
        // Load departments and domains for filters
        await loadFilterOptions();
        
        hideLoading();
        showToast('Data loaded successfully', 'success');
    } catch (error) {
        console.error('Error loading data:', error);
        hideLoading();
        showToast('Error loading data', 'error');
    }
}

async function loadSummaryStats() {
    try {
        const response = await fetch(`${API_BASE}/stats/summary`);
        const data = await response.json();
        
        document.getElementById('total-students').textContent = data.total_students;
        document.getElementById('total-companies').textContent = data.total_companies;
        document.getElementById('placement-rate').textContent = `${data.placement_rate}%`;
        document.getElementById('placed-students').textContent = data.placed_students;
        document.getElementById('avg-cgpa-all').textContent = data.avg_cgpa_all;
        document.getElementById('avg-cgpa-placed').textContent = data.avg_cgpa_placed;
    } catch (error) {
        console.error('Error loading summary stats:', error);
    }
}

async function loadOverviewCharts() {
    try {
        // Department distribution
        const deptResponse = await fetch(`${API_BASE}/stats/department`);
        const deptData = await deptResponse.json();
        createDepartmentChart(deptData.departments);
        
        // CGPA distribution
        const cgpaResponse = await fetch(`${API_BASE}/stats/cgpa`);
        const cgpaData = await cgpaResponse.json();
        createCGPAChart(cgpaData);
        
        // Domain preferences
        const domainResponse = await fetch(`${API_BASE}/stats/domain`);
        const domainData = await domainResponse.json();
        createDomainChart(domainData);
        
        // Status chart
        createStatusChart();
        
    } catch (error) {
        console.error('Error loading overview charts:', error);
    }
}

async function loadFilterOptions() {
    try {
        // Load departments
        const deptResponse = await fetch(`${API_BASE}/departments`);
        const deptData = await deptResponse.json();
        
        const deptFilter = document.getElementById('dept-filter');
        deptFilter.innerHTML = '';
        deptData.departments.forEach(dept => {
            const option = document.createElement('option');
            option.value = dept;
            option.textContent = dept;
            deptFilter.appendChild(option);
        });
        
    } catch (error) {
        console.error('Error loading filter options:', error);
    }
}

// ===========================
// Charts Creation
// ===========================

function createDepartmentChart(departments) {
    const ctx = document.getElementById('deptDistChart');
    if (!ctx) return;
    
    // Destroy existing chart
    if (charts.deptDist) {
        charts.deptDist.destroy();
    }
    
    const labels = departments.map(d => d.department);
    const data = departments.map(d => d.total);
    
    charts.deptDist = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Number of Students',
                data: data,
                backgroundColor: 'rgba(102, 126, 234, 0.8)',
                borderColor: 'rgba(102, 126, 234, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

function createCGPAChart(cgpaData) {
    const ctx = document.getElementById('cgpaDistChart');
    if (!ctx) return;
    
    if (charts.cgpaDist) {
        charts.cgpaDist.destroy();
    }
    
    charts.cgpaDist = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: cgpaData.bins,
            datasets: [
                {
                    label: 'All Students',
                    data: cgpaData.overall,
                    backgroundColor: 'rgba(102, 126, 234, 0.6)',
                    borderColor: 'rgba(102, 126, 234, 1)',
                    borderWidth: 1
                },
                {
                    label: 'Placed',
                    data: cgpaData.placed,
                    backgroundColor: 'rgba(72, 187, 120, 0.6)',
                    borderColor: 'rgba(72, 187, 120, 1)',
                    borderWidth: 1
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top'
                }
            },
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

function createDomainChart(domainData) {
    const ctx = document.getElementById('domainChart');
    if (!ctx) return;
    
    if (charts.domain) {
        charts.domain.destroy();
    }
    
    const domains = Object.keys(domainData.all_domains).slice(0, 10); // Top 10
    const counts = domains.map(d => domainData.all_domains[d]);
    
    charts.domain = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: domains,
            datasets: [{
                data: counts,
                backgroundColor: [
                    'rgba(102, 126, 234, 0.8)',
                    'rgba(247, 147, 251, 0.8)',
                    'rgba(79, 172, 254, 0.8)',
                    'rgba(67, 233, 123, 0.8)',
                    'rgba(250, 112, 154, 0.8)',
                    'rgba(48, 207, 208, 0.8)',
                    'rgba(237, 137, 54, 0.8)',
                    'rgba(245, 101, 101, 0.8)',
                    'rgba(66, 153, 225, 0.8)',
                    'rgba(159, 122, 234, 0.8)'
                ]
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'right'
                }
            }
        }
    });
}

async function createStatusChart() {
    const ctx = document.getElementById('statusChart');
    if (!ctx) return;
    
    if (charts.status) {
        charts.status.destroy();
    }
    
    try {
        const response = await fetch(`${API_BASE}/stats/summary`);
        const data = await response.json();
        
        charts.status = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Placed', 'Unplaced', 'Opted Out'],
                datasets: [{
                    data: [data.placed_students, data.unplaced_students, data.opted_out],
                    backgroundColor: [
                        'rgba(72, 187, 120, 0.8)',
                        'rgba(245, 101, 101, 0.8)',
                        'rgba(237, 137, 54, 0.8)'
                    ]
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });
    } catch (error) {
        console.error('Error creating status chart:', error);
    }
}

// ===========================
// Student Data
// ===========================

async function loadStudentData(filters = {}) {
    try {
        const params = new URLSearchParams({
            limit: PAGE_SIZE,
            offset: currentPage.students * PAGE_SIZE,
            ...filters
        });
        
        const response = await fetch(`${API_BASE}/students?${params}`);
        const data = await response.json();
        
        displayStudentsTable(data.data);
        updateStudentPagination(data.total, data.offset);
        
        // Load department charts
        await loadDepartmentCharts();
        
    } catch (error) {
        console.error('Error loading student data:', error);
        showToast('Error loading student data', 'error');
    }
}

function displayStudentsTable(students) {
    const tbody = document.getElementById('students-tbody');
    tbody.innerHTML = '';
    
    if (students.length === 0) {
        tbody.innerHTML = '<tr><td colspan="8" style="text-align: center;">No students found</td></tr>';
        return;
    }
    
    students.forEach(student => {
        const row = document.createElement('tr');
        
        let statusClass = 'status-unplaced';
        if (student.status === 'Placed') statusClass = 'status-placed';
        if (student.status === 'Opted_Out') statusClass = 'status-opted';
        
        row.innerHTML = `
            <td>${student.roll_no}</td>
            <td>${student.name}</td>
            <td>${student.department}</td>
            <td>${student.cgpa}</td>
            <td>${student.domain_1 || '-'}</td>
            <td>${student.domain_2 || '-'}</td>
            <td><span class="status-badge ${statusClass}">${student.status}</span></td>
            <td>${student.placed_company || '-'}</td>
        `;
        
        tbody.appendChild(row);
    });
}

function updateStudentPagination(total, offset) {
    const currentPageNum = Math.floor(offset / PAGE_SIZE) + 1;
    const totalPages = Math.ceil(total / PAGE_SIZE);
    
    document.getElementById('students-page-info').textContent = `Page ${currentPageNum} of ${totalPages}`;
    
    document.getElementById('prev-students').disabled = currentPageNum === 1;
    document.getElementById('next-students').disabled = currentPageNum === totalPages;
}

async function loadDepartmentCharts() {
    try {
        const response = await fetch(`${API_BASE}/stats/department`);
        const data = await response.json();
        
        // Department placement chart
        const ctx1 = document.getElementById('deptPlacementChart');
        if (ctx1) {
            if (charts.deptPlacement) {
                charts.deptPlacement.destroy();
            }
            
            const labels = data.departments.map(d => d.department);
            const placedData = data.departments.map(d => d.placed);
            const unplacedData = data.departments.map(d => d.unplaced);
            
            charts.deptPlacement = new Chart(ctx1, {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [
                        {
                            label: 'Placed',
                            data: placedData,
                            backgroundColor: 'rgba(72, 187, 120, 0.8)'
                        },
                        {
                            label: 'Unplaced',
                            data: unplacedData,
                            backgroundColor: 'rgba(245, 101, 101, 0.8)'
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        x: {
                            stacked: true
                        },
                        y: {
                            stacked: true,
                            beginAtZero: true
                        }
                    }
                }
            });
        }
        
        // CGPA by department
        const ctx2 = document.getElementById('cgpaByDeptChart');
        if (ctx2) {
            if (charts.cgpaByDept) {
                charts.cgpaByDept.destroy();
            }
            
            const labels = data.departments.map(d => d.department);
            const avgCgpa = data.departments.map(d => d.avg_cgpa);
            
            charts.cgpaByDept = new Chart(ctx2, {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Average CGPA',
                        data: avgCgpa,
                        backgroundColor: 'rgba(79, 172, 254, 0.8)',
                        borderColor: 'rgba(79, 172, 254, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            beginAtZero: true,
                            max: 10
                        }
                    }
                }
            });
        }
        
    } catch (error) {
        console.error('Error loading department charts:', error);
    }
}

// ===========================
// Company Data
// ===========================

async function loadCompanyData() {
    try {
        const params = new URLSearchParams({
            limit: PAGE_SIZE,
            offset: currentPage.companies * PAGE_SIZE
        });
        
        const response = await fetch(`${API_BASE}/companies?${params}`);
        const data = await response.json();
        
        displayCompaniesTable(data.data);
        updateCompanyPagination(data.total, data.offset);
        
        // Load company charts
        await loadCompanyCharts();
        
    } catch (error) {
        console.error('Error loading company data:', error);
        showToast('Error loading company data', 'error');
    }
}

function displayCompaniesTable(companies) {
    const tbody = document.getElementById('companies-tbody');
    tbody.innerHTML = '';
    
    if (companies.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" style="text-align: center;">No companies found</td></tr>';
        return;
    }
    
    companies.forEach(company => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${company.company_name}</td>
            <td>${company.job_role}</td>
            <td>${company.arrival_day}</td>
            <td>${company.min_offers}</td>
            <td>${company.max_offers}</td>
            <td>${company.min_cgpa}</td>
            <td>${company.allowed_departments}</td>
        `;
        tbody.appendChild(row);
    });
}

function updateCompanyPagination(total, offset) {
    const currentPageNum = Math.floor(offset / PAGE_SIZE) + 1;
    const totalPages = Math.ceil(total / PAGE_SIZE);
    
    document.getElementById('companies-page-info').textContent = `Page ${currentPageNum} of ${totalPages}`;
    
    document.getElementById('prev-companies').disabled = currentPageNum === 1;
    document.getElementById('next-companies').disabled = currentPageNum === totalPages;
}

async function loadCompanyCharts() {
    try {
        const response = await fetch(`${API_BASE}/stats/companies`);
        const data = await response.json();
        
        // Role type chart
        const ctx1 = document.getElementById('roleTypeChart');
        if (ctx1) {
            if (charts.roleType) {
                charts.roleType.destroy();
            }
            
            const roles = Object.keys(data.role_types);
            const counts = Object.values(data.role_types);
            
            charts.roleType = new Chart(ctx1, {
                type: 'pie',
                data: {
                    labels: roles,
                    datasets: [{
                        data: counts,
                        backgroundColor: [
                            'rgba(102, 126, 234, 0.8)',
                            'rgba(247, 147, 251, 0.8)',
                            'rgba(79, 172, 254, 0.8)',
                            'rgba(67, 233, 123, 0.8)',
                            'rgba(250, 112, 154, 0.8)',
                            'rgba(48, 207, 208, 0.8)',
                            'rgba(237, 137, 54, 0.8)',
                            'rgba(245, 101, 101, 0.8)'
                        ]
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'right'
                        }
                    }
                }
            });
        }
        
        // Company by day chart
        const ctx2 = document.getElementById('companyDayChart');
        if (ctx2) {
            if (charts.companyDay) {
                charts.companyDay.destroy();
            }
            
            const days = Object.keys(data.day_distribution);
            const counts = Object.values(data.day_distribution);
            
            charts.companyDay = new Chart(ctx2, {
                type: 'bar',
                data: {
                    labels: days.map(d => `Day ${d}`),
                    datasets: [{
                        label: 'Number of Companies',
                        data: counts,
                        backgroundColor: 'rgba(67, 233, 123, 0.8)',
                        borderColor: 'rgba(67, 233, 123, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        }
        
        // Capacity chart
        const ctx3 = document.getElementById('capacityChart');
        if (ctx3) {
            if (charts.capacity) {
                charts.capacity.destroy();
            }
            
            charts.capacity = new Chart(ctx3, {
                type: 'bar',
                data: {
                    labels: ['Total Capacity'],
                    datasets: [
                        {
                            label: 'Minimum',
                            data: [data.total_min_capacity],
                            backgroundColor: 'rgba(237, 137, 54, 0.8)'
                        },
                        {
                            label: 'Maximum',
                            data: [data.total_max_capacity],
                            backgroundColor: 'rgba(67, 233, 123, 0.8)'
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        }
        
    } catch (error) {
        console.error('Error loading company charts:', error);
    }
}

// ===========================
// Results
// ===========================

async function loadResultsData() {
    try {
        const response = await fetch(`${API_BASE}/simulation/results`);
        const data = await response.json();
        
        // Show results content
        document.getElementById('no-results').style.display = 'none';
        document.getElementById('results-content').style.display = 'block';
        
        // Display results
        displayResults(data);
        
    } catch (error) {
        console.error('No results available:', error);
        document.getElementById('no-results').style.display = 'flex';
        document.getElementById('results-content').style.display = 'none';
    }
}

function displayResults(data) {
    // Calculate statistics
    const totalPlaced = data.students.filter(s => s.status === 'Placed').length;
    const placementRate = (totalPlaced / data.students.length * 100).toFixed(2);
    const companiesHired = data.companies.filter(c => c.hired > 0).length;
    const avgHires = (totalPlaced / companiesHired).toFixed(2);
    
    // Update summary cards
    document.getElementById('result-placed').textContent = totalPlaced;
    document.getElementById('result-rate').textContent = `${placementRate}%`;
    document.getElementById('result-companies').textContent = companiesHired;
    document.getElementById('result-avg').textContent = avgHires;
    
    // Department-wise results
    const deptStats = {};
    data.students.forEach(student => {
        if (!deptStats[student.department]) {
            deptStats[student.department] = { total: 0, placed: 0 };
        }
        deptStats[student.department].total++;
        if (student.status === 'Placed') {
            deptStats[student.department].placed++;
        }
    });
    
    const deptLabels = Object.keys(deptStats);
    const deptPlaced = deptLabels.map(d => deptStats[d].placed);
    
    // Department chart
    const ctx1 = document.getElementById('resultDeptChart');
    if (ctx1) {
        if (charts.resultDept) {
            charts.resultDept.destroy();
        }
        
        charts.resultDept = new Chart(ctx1, {
            type: 'bar',
            data: {
                labels: deptLabels,
                datasets: [{
                    label: 'Placed Students',
                    data: deptPlaced,
                    backgroundColor: 'rgba(72, 187, 120, 0.8)'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }
    
    // Company hiring chart (top 15)
    const sortedCompanies = data.companies
        .filter(c => c.hired > 0)
        .sort((a, b) => b.hired - a.hired)
        .slice(0, 15);
    
    const ctx2 = document.getElementById('resultCompanyChart');
    if (ctx2) {
        if (charts.resultCompany) {
            charts.resultCompany.destroy();
        }
        
        charts.resultCompany = new Chart(ctx2, {
            type: 'bar',
            data: {
                labels: sortedCompanies.map(c => c.company_name),
                datasets: [{
                    label: 'Students Hired',
                    data: sortedCompanies.map(c => c.hired),
                    backgroundColor: 'rgba(102, 126, 234, 0.8)'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                indexAxis: 'y',
                scales: {
                    x: {
                        beginAtZero: true
                    }
                }
            }
        });
    }
    
    // Top companies table
    displayTopCompaniesTable(sortedCompanies);
}

function displayTopCompaniesTable(companies) {
    const tbody = document.getElementById('top-companies-tbody');
    tbody.innerHTML = '';
    
    companies.forEach((company, index) => {
        const row = document.createElement('tr');
        const utilization = ((company.hired / company.max_hires) * 100).toFixed(1);
        const meetsMin = company.hired >= company.min_hires;
        
        row.innerHTML = `
            <td>${index + 1}</td>
            <td>${company.company_name}</td>
            <td>${company.job_role}</td>
            <td><strong>${company.hired}</strong></td>
            <td>${company.min_hires}</td>
            <td>${company.max_hires}</td>
            <td>
                <span style="color: ${utilization > 70 ? 'var(--success)' : utilization > 50 ? 'var(--warning)' : 'var(--danger)'}">
                    ${utilization}%
                </span>
            </td>
        `;
        tbody.appendChild(row);
    });
}

// ===========================
// Configuration
// ===========================

function setupConfigurationControls() {
    // Setup sliders
    const sliders = [
        { id: 'w1-cgpa', value: 'w1-value' },
        { id: 'w2-skill', value: 'w2-value' },
        { id: 'w3-random', value: 'w3-value' },
        { id: 'w4-dep', value: 'w4-value' },
        { id: 'w5-profile', value: 'w5-value' },
        { id: 'w6-cgpa', value: 'w6-value' },
        { id: 'w7-random', value: 'w7-value' },
        { id: 'p-opt-out', value: 'opt-value' },
        { id: 'over-offer', value: 'multiplier-value' }
    ];
    
    sliders.forEach(slider => {
        const element = document.getElementById(slider.id);
        const valueDisplay = document.getElementById(slider.value);
        
        element.addEventListener('input', (e) => {
            valueDisplay.textContent = e.target.value;
        });
    });
    
    // Reset configuration
    document.getElementById('reset-config').addEventListener('click', resetConfiguration);
    
    // Run simulation
    document.getElementById('run-simulation').addEventListener('click', runSimulation);
}

function resetConfiguration() {
    document.getElementById('w1-cgpa').value = 0.3;
    document.getElementById('w1-value').textContent = '0.3';
    
    document.getElementById('w2-skill').value = 0.2;
    document.getElementById('w2-value').textContent = '0.2';
    
    document.getElementById('w3-random').value = 0.2;
    document.getElementById('w3-value').textContent = '0.2';
    
    document.getElementById('w4-dep').value = 0.3;
    document.getElementById('w4-value').textContent = '0.3';
    
    document.getElementById('w5-profile').value = 0.3;
    document.getElementById('w5-value').textContent = '0.3';
    
    document.getElementById('w6-cgpa').value = 0.5;
    document.getElementById('w6-value').textContent = '0.5';
    
    document.getElementById('w7-random').value = 0.2;
    document.getElementById('w7-value').textContent = '0.2';
    
    document.getElementById('p-opt-out').value = 0.05;
    document.getElementById('opt-value').textContent = '0.05';
    
    document.getElementById('over-offer').value = 1.5;
    document.getElementById('multiplier-value').textContent = '1.5';
    
    document.getElementById('random-seed').value = 42;
    
    document.getElementById('use-dep-score').checked = true;
    document.getElementById('enforce-min').checked = true;
    
    showToast('Configuration reset to defaults', 'info');
}

async function runSimulation() {
    // Get configuration
    const config = {
        w1_cgpa: parseFloat(document.getElementById('w1-cgpa').value),
        w2_skill: parseFloat(document.getElementById('w2-skill').value),
        w3_random: parseFloat(document.getElementById('w3-random').value),
        w4_dep_score: parseFloat(document.getElementById('w4-dep').value),
        w5_profile: parseFloat(document.getElementById('w5-profile').value),
        w6_cgpa_interview: parseFloat(document.getElementById('w6-cgpa').value),
        w7_random_interview: parseFloat(document.getElementById('w7-random').value),
        p_opt_out: parseFloat(document.getElementById('p-opt-out').value),
        random_seed: parseInt(document.getElementById('random-seed').value),
        over_offer_multiplier: parseFloat(document.getElementById('over-offer').value),
        use_dep_score: document.getElementById('use-dep-score').checked,
        enforce_min_hires: document.getElementById('enforce-min').checked
    };
    
    // Disable button
    const runBtn = document.getElementById('run-simulation');
    runBtn.disabled = true;
    runBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Running...';
    
    // Show progress
    const progressDiv = document.getElementById('simulation-progress');
    progressDiv.style.display = 'block';
    
    try {
        // Start simulation
        const response = await fetch(`${API_BASE}/simulation/run`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(config)
        });
        
        if (!response.ok) {
            throw new Error('Failed to start simulation');
        }
        
        showToast('Simulation started', 'success');
        
        // Poll for status
        pollSimulationStatus();
        
    } catch (error) {
        console.error('Error running simulation:', error);
        showToast('Error starting simulation', 'error');
        runBtn.disabled = false;
        runBtn.innerHTML = '<i class="fas fa-rocket"></i> Run Simulation';
        progressDiv.style.display = 'none';
    }
}

async function pollSimulationStatus() {
    const interval = setInterval(async () => {
        try {
            const response = await fetch(`${API_BASE}/simulation/status`);
            const data = await response.json();
            
            // Update progress
            document.getElementById('progress-message').textContent = data.message;
            document.getElementById('progress-percent').textContent = `${data.progress}%`;
            document.getElementById('progress-fill').style.width = `${data.progress}%`;
            
            if (data.status === 'completed') {
                clearInterval(interval);
                showToast('Simulation completed successfully!', 'success');
                
                // Re-enable button
                const runBtn = document.getElementById('run-simulation');
                runBtn.disabled = false;
                runBtn.innerHTML = '<i class="fas fa-rocket"></i> Run Simulation';
                
                // Hide progress after delay
                setTimeout(() => {
                    document.getElementById('simulation-progress').style.display = 'none';
                }, 2000);
                
                // Reload data
                await loadInitialData();
                
                // Switch to results
                showSection('results');
                document.querySelectorAll('.nav-btn').forEach(btn => {
                    btn.classList.remove('active');
                    if (btn.dataset.section === 'results') {
                        btn.classList.add('active');
                    }
                });
                
            } else if (data.status === 'error') {
                clearInterval(interval);
                showToast(`Simulation error: ${data.message}`, 'error');
                
                const runBtn = document.getElementById('run-simulation');
                runBtn.disabled = false;
                runBtn.innerHTML = '<i class="fas fa-rocket"></i> Run Simulation';
                document.getElementById('simulation-progress').style.display = 'none';
            }
            
        } catch (error) {
            console.error('Error polling status:', error);
            clearInterval(interval);
        }
    }, 1000);
}

async function checkSimulationStatus() {
    try {
        const response = await fetch(`${API_BASE}/simulation/status`);
        const data = await response.json();
        
        if (data.status === 'completed') {
            // Load results if available
            await loadResultsData();
        }
    } catch (error) {
        // No results available
    }
}

// ===========================
// Filters
// ===========================

function setupFilters() {
    // Student filters
    document.getElementById('apply-student-filter').addEventListener('click', applyStudentFilters);
    document.getElementById('reset-student-filter').addEventListener('click', resetStudentFilters);
    
    // Pagination
    document.getElementById('prev-students').addEventListener('click', () => {
        if (currentPage.students > 0) {
            currentPage.students--;
            loadStudentData();
        }
    });
    
    document.getElementById('next-students').addEventListener('click', () => {
        currentPage.students++;
        loadStudentData();
    });
    
    document.getElementById('prev-companies').addEventListener('click', () => {
        if (currentPage.companies > 0) {
            currentPage.companies--;
            loadCompanyData();
        }
    });
    
    document.getElementById('next-companies').addEventListener('click', () => {
        currentPage.companies++;
        loadCompanyData();
    });
    
    // Export
    document.getElementById('export-students').addEventListener('click', exportStudents);
}

function applyStudentFilters() {
    const filters = {};
    
    const dept = document.getElementById('dept-filter').value;
    if (dept) filters.department = dept;
    
    const cgpaMin = document.getElementById('cgpa-min').value;
    if (cgpaMin) filters.cgpa_min = parseFloat(cgpaMin);
    
    const cgpaMax = document.getElementById('cgpa-max').value;
    if (cgpaMax) filters.cgpa_max = parseFloat(cgpaMax);
    
    const status = document.getElementById('status-filter').value;
    if (status) filters.status = status;
    
    currentPage.students = 0;
    loadStudentData(filters);
}

function resetStudentFilters() {
    document.getElementById('dept-filter').selectedIndex = 0;
    document.getElementById('cgpa-min').value = '';
    document.getElementById('cgpa-max').value = '';
    document.getElementById('status-filter').selectedIndex = 0;
    
    currentPage.students = 0;
    loadStudentData();
}

async function exportStudents() {
    try {
        window.open(`${API_BASE}/export/csv`, '_blank');
        showToast('Export started', 'success');
    } catch (error) {
        console.error('Error exporting:', error);
        showToast('Error exporting data', 'error');
    }
}

// ===========================
// Utility Functions
// ===========================

function showLoading() {
    document.getElementById('loading-overlay').style.display = 'flex';
}

function hideLoading() {
    document.getElementById('loading-overlay').style.display = 'none';
}

function showToast(message, type = 'info') {
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    
    let icon = 'fa-info-circle';
    if (type === 'success') icon = 'fa-check-circle';
    if (type === 'error') icon = 'fa-exclamation-circle';
    
    toast.innerHTML = `
        <i class="fas ${icon}"></i>
        <span>${message}</span>
    `;
    
    container.appendChild(toast);
    
    // Auto remove after 3 seconds
    setTimeout(() => {
        toast.remove();
    }, 3000);
}
