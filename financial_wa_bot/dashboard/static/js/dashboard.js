// Dashboard JavaScript

// Format number as Indonesian Rupiah
function formatCurrency(amount) {
    return new Intl.NumberFormat('id-ID', {
        style: 'currency',
        currency: 'IDR',
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
    }).format(amount);
}

// Format date to Indonesian format
function formatDate(dateString) {
    return new Date(dateString).toLocaleDateString('id-ID', {
        day: '2-digit',
        month: 'short',
        year: 'numeric'
    });
}

// Initialize Charts
function initializeCharts(expenseData, trendData) {
    // Expense Categories Chart
    const expenseCtx = document.getElementById('expenseChart').getContext('2d');
    const expenseChart = new Chart(expenseCtx, {
        type: 'doughnut',
        data: {
            labels: expenseData.labels,
            datasets: [{
                data: expenseData.values,
                backgroundColor: [
                    '#4F46E5', '#7C3AED', '#EC4899', '#EF4444',
                    '#F59E0B', '#10B981', '#3B82F6', '#6366F1'
                ]
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'right',
                    labels: {
                        font: {
                            family: "'Inter', sans-serif"
                        }
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return `${context.label}: ${formatCurrency(context.raw)}`;
                        }
                    }
                }
            }
        }
    });

    // Income vs Expense Trend Chart
    const trendCtx = document.getElementById('trendChart').getContext('2d');
    const trendChart = new Chart(trendCtx, {
        type: 'line',
        data: {
            labels: trendData.dates,
            datasets: [{
                label: 'Pemasukan',
                data: trendData.income,
                borderColor: '#10B981',
                backgroundColor: '#10B98120',
                fill: true,
                tension: 0.4
            }, {
                label: 'Pengeluaran',
                data: trendData.expense,
                borderColor: '#EF4444',
                backgroundColor: '#EF444420',
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                    labels: {
                        font: {
                            family: "'Inter', sans-serif"
                        }
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return `${context.dataset.label}: ${formatCurrency(context.raw)}`;
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value) {
                            return formatCurrency(value);
                        }
                    }
                }
            }
        }
    });

    return { expenseChart, trendChart };
}

// Update dashboard data via WebSocket
function updateDashboardData(data) {
    switch (data.type) {
        case 'balance':
            updateBalance(data.data);
            break;
        case 'transaction':
            updateTransactions(data.data);
            break;
        case 'budget':
            updateBudget(data.data);
            break;
        case 'notification':
            showNotification(data.data);
            break;
    }
}

// Update balance display
function updateBalance(balance) {
    document.getElementById('current-balance').textContent = formatCurrency(balance.current_balance);
    document.getElementById('total-income').textContent = formatCurrency(balance.total_income);
    document.getElementById('total-expenses').textContent = formatCurrency(balance.total_expenses);
}

// Update recent transactions
function updateTransactions(transactions) {
    const container = document.getElementById('recent-transactions');
    container.innerHTML = transactions.map(transaction => `
        <tr>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                ${formatDate(transaction.date)}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                ${transaction.category}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                ${transaction.description || '-'}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm ${transaction.type === 'expense' ? 'text-red-500' : 'text-green-500'}">
                ${transaction.type === 'expense' ? '-' : ''}${formatCurrency(transaction.amount)}
            </td>
        </tr>
    `).join('');
}

// Update budget progress
function updateBudget(budgetStatus) {
    const container = document.getElementById('budget-progress');
    container.innerHTML = budgetStatus.budget_status.map(status => `
        <div class="mb-4">
            <div class="flex justify-between text-sm mb-1">
                <span>${status.category}</span>
                <span>${status.percentage_used.toFixed(1)}%</span>
            </div>
            <div class="w-full bg-gray-200 rounded-full h-2">
                <div class="bg-purple-500 h-2 rounded-full" 
                     style="width: ${status.percentage_used}%">
                </div>
            </div>
        </div>
    `).join('');
}

// Show notification toast
function showNotification(notification) {
    const toast = document.createElement('div');
    toast.className = `fixed bottom-4 right-4 bg-white shadow-lg rounded-lg p-4 
                      transform transition-transform duration-300 translate-y-0
                      flex items-center space-x-2`;
    
    const icon = notification.type === 'success' ? 'check-circle' : 
                 notification.type === 'warning' ? 'exclamation-triangle' : 
                 'info-circle';
    
    const color = notification.type === 'success' ? 'text-green-500' : 
                  notification.type === 'warning' ? 'text-yellow-500' : 
                  'text-blue-500';

    toast.innerHTML = `
        <i class="fas fa-${icon} ${color} text-lg"></i>
        <p class="text-gray-800">${notification.message}</p>
    `;

    document.body.appendChild(toast);

    // Remove toast after 3 seconds
    setTimeout(() => {
        toast.classList.add('translate-y-full');
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// Export functions
window.dashboardFunctions = {
    initializeCharts,
    updateDashboardData,
    formatCurrency,
    formatDate
};
