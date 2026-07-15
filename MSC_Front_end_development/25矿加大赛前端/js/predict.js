document.addEventListener('DOMContentLoaded', function () {
  const predictButton = document.getElementById('predict-button');
  const predictingStatus = document.getElementById('predicting-status');
  const predictionResults = document.getElementById('prediction-results');
  const predictInitialState = document.getElementById('predict-initial-state');
  const predictImagesInput = document.getElementById('predict-images');
  const predictImagesPreview = document.getElementById('predict-images-preview');
  const modelVersionSelect = document.getElementById('model-version');
  const predictionTableBody = document.getElementById('prediction-table-body');

  predictImagesInput.addEventListener('change', function () {
    const files = this.files;
    predictImagesPreview.innerHTML = '';
    for (let i = 0; i < files.length; i++) {
      const file = files[i];
      const reader = new FileReader();
      reader.onload = function (e) {
        const img = document.createElement('img');
        img.src = e.target.result;
        img.classList.add('w-full', 'h-auto', 'rounded-md');
        predictImagesPreview.appendChild(img);
      };
      reader.readAsDataURL(file);
    }
  });

  predictButton.addEventListener('click', function () {
    const files = predictImagesInput.files;
    if (files.length === 0) {
      alert('请上传待预测的泡沫图像');
      return;
    }
    const modelVersion = modelVersionSelect.value;

    predictInitialState.classList.add('hidden');
    predictingStatus.classList.remove('hidden');

    // 模拟预测过程
    setTimeout(function () {
      predictingStatus.classList.add('hidden');
      predictionResults.classList.remove('hidden');

      // 模拟生成预测结果并添加到历史记录
      const historyData = {
        idx: document.getElementById('predict-history-body').querySelectorAll('tr').length + 1,
        taskName: '浮选泡沫品位分析#' + (document.getElementById('predict-history-body').querySelectorAll('tr').length + 1),
        batch: 'Batch_' + new Date().toISOString().replace(/[-T:.Z]/g, ''),
        createTime: new Date().toLocaleString(),
        imageCount: files.length,
        averageGrade: '53.4%',
        modelVersion: modelVersion,
        status: '已完成'
      };
      finishPrediction(historyData);

      for (let i = 0; i < files.length; i++) {
        const file = files[i];
        const row = document.createElement('tr');
        row.innerHTML = `
          <td class="px-4 py-3">${file.name}</td>
          <td class="px-4 py-3">53.4%</td>
          <td class="px-4 py-3">92.7%</td>
          <td class="px-4 py-3">2.4</td>
          <td class="px-4 py-3">
            <button class="text-primary hover:underline">查看详情</button>
          </td>
        `;
        predictionTableBody.appendChild(row);
      }
    }, 3000);
  });
});