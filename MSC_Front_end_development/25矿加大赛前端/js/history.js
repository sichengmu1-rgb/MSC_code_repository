document.addEventListener('DOMContentLoaded', function () {
  // 预测历史搜索
  const predictSearchInput = document.getElementById('predict-history-search');
  const predictTableBody = document.getElementById('predict-history-body');
  const predictRows = predictTableBody.getElementsByTagName('tr');

  predictSearchInput.addEventListener('input', function () {
    const searchTerm = this.value.toLowerCase();
    for (let i = 0; i < predictRows.length; i++) {
      const row = predictRows[i];
      const taskName = row.cells[1].textContent.toLowerCase();
      if (taskName.includes(searchTerm)) {
        row.style.display = '';
      } else {
        row.style.display = 'none';
      }
    }
  });

  // 训练历史搜索
  const trainSearchInput = document.getElementById('train-history-search');
  const trainTableBody = document.getElementById('train-history-body');
  const trainRows = trainTableBody.getElementsByTagName('tr');

  trainSearchInput.addEventListener('input', function () {
    const searchTerm = this.value.toLowerCase();
    for (let i = 0; i < trainRows.length; i++) {
      const row = trainRows[i];
      const taskName = row.cells[1].textContent.toLowerCase();
      if (taskName.includes(searchTerm)) {
        row.style.display = '';
      } else {
        row.style.display = 'none';
      }
    }
  });
});