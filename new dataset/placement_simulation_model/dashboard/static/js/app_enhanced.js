"""
Enhanced Placement Dashboard JavaScript
Includes all required visualizations from DASHBOARD_PLAN
"""

// API Base URL
const API_BASE = '';

// Global state
let dashboardData = {
    students: [],
    companies: [],
    departments: [],
    domains: [],
    stats: {},
    results: null
};

// Chart instances
let charts = {};

// Color schemes
const COLORS = {
    primary: '#667eea',
    secondary: '#764ba2',
    success: '#43e97b',
    danger: '#f5576c',
    warning: '#fee140',
    info: '#4facfe',
    departments: [
        '#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe', '#00f2fe',
        '#43e97b', '#38f9d7', '#fa709a', '#fee140', '#30cfd0', '#330867',
        '#a8edea', '#fed6e3', '#ffecd2', '#fcb69f', '#ff9a9e', '#fecfef',
        '#ffeaa7', '#dfe6e9', '#74b9ff', '#a29bfe'
    ],
    gradient: (ctx, color1, color2) => {
        const gradient = ctx.createLinearGradient(0, 0, 0, 400);
        gradient.addColorStop(0, color1);
        gradient.addColorStop(1, color2);
        return gradient;
    }
};

// Initialize dashboard
async function initDashboard() {
    console.log('Initializing dashboard...');
    
    // Load initial data
    await loadData();
    
    // Load statistics
    await loadStatistics();
    
    // Render all visualizations
    renderAllCharts();
    
    // Setup event listeners
    setupEventListeners();
    
    console.log('Dashboard initialized!');
}

// Load data from API
async function loadData() {
    try {
        // Force data reload for clean data
        await fetch(`${API_BASE}/api/data/load`);
        
        // Load departments and domains
        const [deptsRes, domainsRes] = await Promise.all([
            fetch(`${API_BASE}/api/departments`),
            fetch(`${API_BASE}/api/domains`)
        ]);
        
        dashboardData.departments = (await deptsRes.json()).departments;
        dashboardData.domains = (await domainsRes.json()).domains;
        
        console.log('Data loaded successfully');
    } catch (error) {
        console.error('Error loading data:', error);
    }
}

// Load statistics
async function loadStatistics() {
    try {
        const [summary, department, cgpa, companies, domain] = await Promise.all([
            fetch(`${API_BASE}/api/stats/summary`).then(r => r.json()),
            fetch(`${API_BASE}/api/stats/department`).then(r => r.json()),
            fetch(`${API_BASE}/api/stats/cgpa`).then(r => r.json()),
            fetch(`${API_BASE}/api/stats/companies`).then(r => r.json()),
            fetch(`${API_BASE}/api/stats/domain`).then(r => r.json())
        ]);
        
        dashboardData.stats = {
            summary,
            department,
            cgpa,
            companies,
            domain
        };
        
        // Update summary cards
        updateSummaryCards(summary);
        
        console.log('Statistics loaded successfully');
    } catch (error) {
        console.error('Error loading statistics:', error);
    }
}

// Update summary cards
function updateSummaryCards(summary) {
    document.getElementById('total-students').textContent = summary.total_students.toLocaleString();
    document.getElementById('total-companies').textContent = summary.total_companies;
    document.getElementById('placement-rate').textContent = `${summary.placement_rate}%`;
    document.getElementById('placed-students').textContent = summary.placed_students.toLocaleString();
    document.getElementById('avg-cgpa-all').textContent = summary.avg_cgpa_all.toFixed(2);
    document.getElementById('avg-cgpa-placed').textContent = summary.avg_cgpa_placed.toFixed(2);
}

// Render all charts
function renderAllCharts() {
    // Section B: Student Analytics
    renderDepartmentDistribution();
    renderCGPADistribution();
    renderDomainPreferences();
    renderPlacementStatus();
    renderDepartmentHitRate();
    renderCGPABoxPlot();
    renderDepartmentDomainHeatmap();
    
    // Section C: Company Analytics
    renderCompanyDistribution();
    renderRoleTypeAnalysis();
    renderDayWiseCompanies();
    renderCompanyCapacityUtilization();
}

// 1. Department Distribution (Pie + Bar)
function renderDepartmentDistribution() {
    const data = dashboardData.stats.department.departments;
    const labels = data.map(d => d.department);
    const values = data.map(d => d.total);
    
    const ctx = document.getElementById('deptDistChart');
    if (charts.deptDist) charts.deptDist.destroy();
    
    charts.deptDist = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Total Students',
                data: values,
                backgroundColor: COLORS.departments.slice(0, labels.length),
                borderColor: COLORS.departments.slice(0, labels.length).map(c => c + 'dd'),
                borderWidth: 2,
                borderRadius: 8
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const total = values.reduce((a, b) => a + b, 0);
                            const percent = ((context.parsed.y / total) * 100).toFixed(1);
                            return `Students: ${context.parsed.y} (${percent}%)`;
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)'
                    }
                },
                x: {
                    grid: {
                        display: false
                    }
                }
            }
        }
    });
}

// 2. Department Hit Rate (Grouped Bar: Total vs Placed)
function renderDepartmentHitRate() {
    const data = dashboardData.stats.department.departments;
    const labels = data.map(d => d.department);
    const totalStudents = data.map(d => d.total);
    const placedStudents = data.map(d => d.placed);
    
    const ctx = document.getElementById('deptHitRateChart');
    if (!ctx) return;
    if (charts.deptHitRate) charts.deptHitRate.destroy();
    
    charts.deptHitRate = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Total Students',
                    data: totalStudents,
                    backgroundColor: 'rgba(102, 126, 234, 0.8)',
                    borderColor: 'rgba(102, 126, 234, 1)',
                    borderWidth: 2,
                    borderRadius: 6
                },
                {
                    label: 'Placed Students',
                    data: placedStudents,
                    backgroundColor: 'rgba(67, 233, 123, 0.8)',
                    borderColor: 'rgba(67, 233, 123, 1)',
                    borderWidth: 2,
                    borderRadius: 6
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: 'Department Hit Rate: Total vs Placed Students',
                    font: {
                        size: 16,
                        weight: 'bold'
                    }
                },
                legend: {
                    position: 'top'
                },
                tooltip: {
                    callbacks: {
                        afterLabel: function(context) {
                            const dept = data[context.dataIndex];
                            return `Placement Rate: ${dept.placement_rate}%`;
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Number of Students'
                    },
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)'
                    }
                },
                x: {
                    grid: {
                        display: false
                    }
                }
            }
        }
    });
}

// 3. Horizontal Bar Chart: Placement Rate % by Department
function renderPlacementRateByDepartment() {
    const data = dashboardData.stats.department.departments;
    const labels = data.map(d => d.department);
    const rates = data.map(d => d.placement_rate);
    
    const ctx = document.getElementById('placementRateChart');
    if (!ctx) return;
    if (charts.placementRate) charts.placementRate.destroy();
    
    // Sort by placement rate
    const sorted = data.map((d, i) => ({label: labels[i], rate: rates[i]}))
                      .sort((a, b) => b.rate - a.rate);
    
    charts.placementRate = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: sorted.map(d => d.label),
            datasets: [{
                label: 'Placement Rate (%)',
                data: sorted.map(d => d.rate),
                backgroundColor: sorted.map(d => {
                    if (d.rate >= 80) return 'rgba(67, 233, 123, 0.8)'; // Green
                    if (d.rate >= 50) return 'rgba(254, 225, 64, 0.8)';  // Yellow
                    return 'rgba(245, 87, 108, 0.8)';  // Red
                }),
                borderWidth: 2,
                borderRadius: 6
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: 'Placement Rate by Department (%)',
                    font: {
                        size: 16,
                        weight: 'bold'
                    }
                },
                legend: {
                    display: false
                }
            },
            scales: {
                x: {
                    beginAtZero: true,
                    max: 100,
                    title: {
                        display: true,
                        text: 'Placement Rate (%)'
                    }
                }
            }
        }
    });
}

// 4. CGPA Distribution (Histogram)
function renderCGPADistribution() {
    const data = dashboardData.stats.cgpa;
    
    const ctx = document.getElementById('cgpaDistChart');
    if (charts.cgpaDist) charts.cgpaDist.destroy();
    
    charts.cgpaDist = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.bins,
            datasets: [
                {
                    label: 'Overall',
                    data: data.overall,
                    backgroundColor: 'rgba(102, 126, 234, 0.6)',
                    borderColor: 'rgba(102, 126, 234, 1)',
                    borderWidth: 2,
                    borderRadius: 6
                },
                {
                    label: 'Placed',
                    data: data.placed,
                    backgroundColor: 'rgba(67, 233, 123, 0.6)',
                    borderColor: 'rgba(67, 233, 123, 1)',
                    borderWidth: 2,
                    borderRadius: 6
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: 'CGPA Distribution',
                    font: {
                        size: 16
                    }
                },
                legend: {
                    position: 'top'
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Number of Students'
                    },
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'CGPA Range'
                    },
                    grid: {
                        display: false
                    }
                }
            }
        }
    });
}

// 5. CGPA Box Plot by Department
function renderCGPABoxPlot() {
    const ctx = document.getElementById('cgpaBoxPlotChart');
    if (!ctx) return;
    
    // For now, use department stats to show average CGPA
    const data = dashboardData.stats.department.departments;
    const labels = data.map(d => d.department);
    const avgCGPA = data.map(d => d.avg_cgpa);
    
    if (charts.cgpaBox) charts.cgpaBox.destroy();
    
    charts.cgpaBox = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Average CGPA',
                data: avgCGPA,
                backgroundColor: COLORS.departments.slice(0, labels.length).map(c => c + '99'),
                borderColor: COLORS.departments.slice(0, labels.length),
                borderWidth: 2,
                borderRadius: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: 'CGPA Distribution by Department',
                    font: {
                        size: 16,
                        weight: 'bold'
                    }
                },
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 10,
                    title: {
                        display: true,
                        text: 'Average CGPA'
                    }
                }
            }
        }
    });
}

// 6. Department × Domain Heatmap (Simplified as Stacked Bar)
function renderDepartmentDomainHeatmap() {
    const ctx = document.getElementById('deptDomainHeatmap');
    if (!ctx) return;
    
    const data = dashboardData.stats.domain.dept_domain_matrix;
    if (!data || data.length === 0) return;
    
    // Get all unique domains
    const allDomains = new Set();
    data.forEach(d => {
        Object.keys(d.domains).forEach(domain => allDomains.add(domain));
    });
    const domains = Array.from(allDomains).slice(0, 10); // Top 10 domains
    
    const datasets = domains.map((domain, index) => ({
        label: domain,
        data: data.map(d => d.domains[domain] || 0),
        backgroundColor: COLORS.departments[index % COLORS.departments.length],
        borderWidth: 1
    }));
    
    if (charts.deptDomainHeatmap) charts.deptDomainHeatmap.destroy();
    
    charts.deptDomainHeatmap = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.map(d => d.department),
            datasets: datasets
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: 'Department × Domain Matrix',
                    font: {
                        size: 16,
                        weight: 'bold'
                    }
                },
                legend: {
                    position: 'right',
                    labels: {
                        boxWidth: 12,
                        font: {
                            size: 10
                        }
                    }
                }
            },
            scales: {
                x: {
                    stacked: true,
                    grid: {
                        display: false
                    }
                },
                y: {
                    stacked: true,
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Number of Students'
                    }
                }
            }
        }
    });
}

// 7. Domain Preferences (Pie Chart)
function renderDomainPreferences() {
    const data = dashboardData.stats.domain;
    const domainCounts = data.all_domains;
    const labels = Object.keys(domainCounts).slice(0, 10); // Top 10
    const values = labels.map(l => domainCounts[l]);
    
    const ctx = document.getElementById('domainChart');
    if (charts.domain) charts.domain.destroy();
    
    charts.domain = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: values,
                backgroundColor: COLORS.departments.slice(0, labels.length),
                borderWidth: 2,
                borderColor: '#fff'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: 'Top Domain Preferences',
                    font: {
                        size: 16
                    }
                },
                legend: {
                    position: 'right',
                    labels: {
                        boxWidth: 12,
                        font: {
                            size: 11
                        }
                    }
                }
            }
        }
    });
}

// 8. Placement Status (Donut Chart)
function renderPlacementStatus() {
    const summary = dashboardData.stats.summary;
    
    const ctx = document.getElementById('statusChart');
    if (charts.status) charts.status.destroy();
    
    charts.status = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Placed', 'Unplaced', 'Opted Out'],
            datasets: [{
                data: [
                    summary.placed_students,
                    summary.unplaced_students,
                    summary.opted_out
                ],
                backgroundColor: [
                    'rgba(67, 233, 123, 0.8)',   // Green
                    'rgba(245, 87, 108, 0.8)',   // Red
                    'rgba(254, 225, 64, 0.8)'    // Yellow
                ],
                borderWidth: 3,
                borderColor: '#fff'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: 'Placement Status Overview',
                    font: {
                        size: 16
                    }
                },
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
}

// 9. Company Distribution by Role Type
function renderCompanyDistribution() {
    const ctx = document.getElementById('companyRoleChart');
    if (!ctx) return;
    
    const data = dashboardData.stats.companies;
    const labels = Object.keys(data.role_types).slice(0, 10);
    const values = labels.map(l => data.role_types[l]);
    
    if (charts.companyRole) charts.companyRole.destroy();
    
    charts.companyRole = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: labels,
            datasets: [{
                data: values,
                backgroundColor: COLORS.departments.slice(0, labels.length),
                borderWidth: 2,
                borderColor: '#fff'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: 'Companies by Role Type',
                    font: {
                        size: 16,
                        weight: 'bold'
                    }
                },
                legend: {
                    position: 'right',
                    labels: {
                        boxWidth: 12,
                        font: {
                            size: 11
                        }
                    }
                }
            }
        }
    });
}

// 10. Day-wise Company Distribution
function renderDayWiseCompanies() {
    const ctx = document.getElementById('dayWiseCompaniesChart');
    if (!ctx) return;
    
    const data = dashboardData.stats.companies;
    const days = Object.keys(data.day_distribution).sort();
    const counts = days.map(d => data.day_distribution[d]);
    
    if (charts.dayWise) charts.dayWise.destroy();
    
    charts.dayWise = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: days.map(d => `Day ${d}`),
            datasets: [{
                label: 'Number of Companies',
                data: counts,
                backgroundColor: ['rgba(102, 126, 234, 0.8)', 'rgba(245, 87, 108, 0.8)', 'rgba(67, 233, 123, 0.8)', 'rgba(254, 225, 64, 0.8)'],
                borderColor: ['rgba(102, 126, 234, 1)', 'rgba(245, 87, 108, 1)', 'rgba(67, 233, 123, 1)', 'rgba(254, 225, 64, 1)'],
                borderWidth: 2,
                borderRadius: 8
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: 'Companies Visiting Per Day',
                    font: {
                        size: 16,
                        weight: 'bold'
                    }
                },
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Number of Companies'
                    }
                }
            }
        }
    });
}

// 11. Role Type Analysis (Min vs Max Hires)
function renderRoleTypeAnalysis() {
    const ctx = document.getElementById('roleTypeAnalysisChart');
    if (!ctx) return;
    
    const summary = dashboardData.stats.companies;
    
    if (charts.roleAnalysis) charts.roleAnalysis.destroy();
    
    charts.roleAnalysis = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Total Capacity'],
            datasets: [
                {
                    label: 'Min Capacity',
                    data: [summary.total_min_capacity],
                    backgroundColor: 'rgba(245, 87, 108, 0.8)',
                    borderColor: 'rgba(245, 87, 108, 1)',
                    borderWidth: 2,
                    borderRadius: 6
                },
                {
                    label: 'Max Capacity',
                    data: [summary.total_max_capacity],
                    backgroundColor: 'rgba(67, 233, 123, 0.8)',
                    borderColor: 'rgba(67, 233, 123, 1)',
                    borderWidth: 2,
                    borderRadius: 6
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: 'Total Hiring Capacity: Min vs Max',
                    font: {
                        size: 16,
                        weight: 'bold'
                    }
                },
                legend: {
                    position: 'top'
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Number of Positions'
                    }
                }
            }
        }
    });
}

// 12. Company Capacity Utilization
function renderCompanyCapacityUtilization() {
    const ctx = document.getElementById('capacityUtilizationChart');
    if (!ctx) return;
    
    const summary = dashboardData.stats.companies;
    const utilization = (summary.total_min_capacity / summary.total_max_capacity * 100).toFixed(1);
    
    if (charts.capacity) charts.capacity.destroy();
    
    charts.capacity = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Min Required', 'Additional Capacity'],
            datasets: [{
                data: [
                    summary.total_min_capacity,
                    summary.total_max_capacity - summary.total_min_capacity
                ],
                backgroundColor: [
                    'rgba(102, 126, 234, 0.8)',
                    'rgba(200, 200, 200, 0.3)'
                ],
                borderWidth: 2,
                borderColor: '#fff'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: `Hiring Capacity Overview (${utilization}% Minimum)`,
                    font: {
                        size: 16,
                        weight: 'bold'
                    }
                },
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
}

// Setup event listeners
function setupEventListeners() {
    // Navigation
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const section = e.target.closest('.nav-btn').dataset.section;
            switchSection(section);
        });
    });
    
    // Theme toggle
    const themeToggle = document.getElementById('themeToggle');
    if (themeToggle) {
        themeToggle.addEventListener('click', toggleTheme);
    }
    
    // Refresh button
    const refreshBtn = document.getElementById('refreshBtn');
    if (refreshBtn) {
        refreshBtn.addEventListener('click', async () => {
            await loadData();
            await loadStatistics();
            renderAllCharts();
        });
    }
}

// Switch sections
function switchSection(section) {
    // Update nav buttons
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    document.querySelector(`[data-section="${section}"]`).classList.add('active');
    
    // Update sections
    document.querySelectorAll('.content-section').forEach(sec => {
        sec.classList.remove('active');
    });
    document.getElementById(`${section}-section`).classList.add('active');
}

// Toggle theme
function toggleTheme() {
    document.body.classList.toggle('dark-mode');
    const icon = document.querySelector('#themeToggle i');
    if (document.body.classList.contains('dark-mode')) {
        icon.classList.remove('fa-moon');
        icon.classList.add('fa-sun');
    } else {
        icon.classList.remove('fa-sun');
        icon.classList.add('fa-moon');
    }
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initDashboard);
} else {
    initDashboard();
}
