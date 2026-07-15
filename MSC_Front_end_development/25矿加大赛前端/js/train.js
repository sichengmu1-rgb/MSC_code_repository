document.addEventListener('DOMContentLoaded', function () {
  const modelParamsSelect = document.getElementById('model-params');
  const customParamsDiv = document.getElementById('custom-params');
  const trainImagesInput = document.getElementById('train-images');
  const trainImagesPreview = document.getElementById('train-images-preview');
  const gradeDataInput = document.getElementById('grade-data');
  const gradeDataInfo = document.getElementById('grade-data-info');
  const gradeFilename = document.getElementById('grade-filename');
  const gradeFilesize = document.getElementById('grade-filesize');
  const trainButton = document.getElementById('train-button');
  const trainingResults = document.getElementById('training-results');

  modelParamsSelect.addEventListener('change', function () {
    if (this.value === 'custom') {
      customParamsDiv.classList.remove('hidden');
    } else {
      customParamsDiv.classList.add('hidden');
    }
  });

  trainImagesInput.addEventListener('change', function () {
    const files = this.files;
    trainImagesPreview.innerHTML = '';
    for (let i = 0; i < files.length; i++) {
      const file = files[i];
      const reader = new FileReader();
      reader.onload = function (e) {
        const img = document.createElement('img');
        img.src = e.target.result;
        img.classList.add('w-full', 'h-auto', 'rounded-md');
        trainImagesPreview.appendChild(img);
      };
      reader.readAsDataURL(file);
    }
  });

  gradeDataInput.addEventListener('change', function () {
    const file = this.files[0];
    if (file) {
      gradeFilename.textContent = file.name;
      gradeFilesize.textContent = (file.size / 1024).toFixed(1) + ' KB';
      gradeDataInfo.classList.remove('hidden');
    } else {
      gradeDataInfo.classList.add('hidden');
    }
  });

  trainButton.addEventListener('click', function () {
    const trainImages = trainImagesInput.files;
    const gradeData = gradeDataInput.files[0];
    if (trainImages.length === 0 || !gradeData) {
      alert('请上传泡沫图像和品位数据');
      return;
    }
    const modelParams = modelParamsSelect.value;
    let epochs, batchSize;
    if (modelParams === 'custom') {
      epochs = document.getElementById('epochs').value;
      batchSize = document.getElementById('batch-size').value;
    }

    // 处理训练逻辑
    console.log('开始训练模型');

    // 模拟训练完成
    setTimeout(function () {
      trainingResults.classList.remove('hidden');

      // 保存数据到历史记录
      const historyData = {
        idx: document.getElementById('train-history-body').querySelectorAll('tr').length + 1,
        taskName: '模型训练任务#' + (document.getElementById('train-history-body').querySelectorAll('tr').length + 1),
        batch: 'Train_' + new Date().toISOString().replace(/[-T:.Z]/g, ''),
        createTime: new Date().toLocaleString(),
        epochs: epochs,
        batchSize: batchSize,
        modelVersion: 's',
        status: '已完成'
      };
      finishTraining(historyData);
    }, 3000);
  });
});