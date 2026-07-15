// 模拟 “完成预测” 事件：实际应在预测逻辑结束后调用
function finishPrediction(record) {
  const historyBody = document.getElementById('predict-history-body');
  const totalEl = document.getElementById('predict-total');
  
  // 构造一行记录
  const row = `
    <tr>
      <td class="px-2 py-2">${record.idx}</td>
      <td class="px-2 py-2">
        <span class="flex items-center">
          <svg class="w-5 h-5 text-blue-500 mr-2" fill="currentColor" viewBox="0 0 24 24">
            <path d="M12 2L2 7l10 5 10-5-10-5zm0 18.5c-3.04 0-5.5-2.46-5.5-5.5s2.46-5.5 5.5-5.5 5.5 2.46 5.5 5.5-2.46 5.5-5.5 5.5z"/>
          </svg>
          ${record.taskName}
        </span>
        <span class="block text-xs text-gray-500">${record.batch}</span>
      </td>
      <td class="px-2 py-2">${record.createTime}</td>
      <td class="px-2 py-2">${record.imageCount}</td>
      <td class="px-2 py-2 text-blue-600">${record.averageGrade}</td>
      <td class="px-2 py-2">${record.modelVersion}</td>
      <td class="px-2 py-2">
        <span class="px-2 py-1 bg-green-100 text-green-600 rounded-md">${record.status}</span>
      </td>
      <td class="px-2 py-2">
        <button class="text-blue-500 hover:underline mr-2">查看</button>
        <button class="text-blue-500 hover:underline mr-2">下载</button>
        <button class="text-red-500 hover:underline">删除</button>
      </td>
    </tr>
  `;
  
  historyBody.insertAdjacentHTML('beforeend', row);
  // 更新总数（简单示例，实际可维护数组或从后端取）
  totalEl.textContent = historyBody.querySelectorAll('tr').length;
}

// 模拟 “完成训练” 事件：实际应在训练逻辑结束后调用
function finishTraining(record) {
  const historyBody = document.getElementById('train-history-body');
  const totalEl = document.getElementById('train-total');
  
  // 构造一行记录
  const row = `
    <tr>
      <td class="px-2 py-2">${record.idx}</td>
      <td class="px-2 py-2">
        <span class="flex items-center">
          <svg class="w-5 h-5 text-orange-500 mr-2" fill="currentColor" viewBox="0 0 24 24">
            <path d="M12 2L2 7l10 5 10-5-10-5zm0 18.5c-3.04 0-5.5-2.46-5.5-5.5s2.46-5.5 5.5-5.5 5.5 2.46 5.5 5.5-2.46 5.5-5.5 5.5z"/>
          </svg>
          ${record.taskName}
        </span>
        <span class="block text-xs text-gray-500">${record.batch}</span>
      </td>
      <td class="px-2 py-2">${record.createTime}</td>
      <td class="px-2 py-2">${record.epochs}</td>
      <td class="px-2 py-2">${record.batchSize}</td>
      <td class="px-2 py-2">${record.modelVersion}</td>
      <td class="px-2 py-2">
        <span class="px-2 py-1 bg-green-100 text-green-600 rounded-md">${record.status}</span>
      </td>
      <td class="px-2 py-2">
        <button class="text-blue-500 hover:underline mr-2">查看</button>
        <button class="text-blue-500 hover:underline mr-2">下载</button>
        <button class="text-red-500 hover:underline">删除</button>
      </td>
    </tr>
  `;
  
  historyBody.insertAdjacentHTML('beforeend', row);
  // 更新总数（简单示例，实际可维护数组或从后端取）
  totalEl.textContent = historyBody.querySelectorAll('tr').length;
}

// 模拟调用：实际在预测/训练完成后触发
// 预测完成示例
const predictRecord = {
  idx: 1,
  taskName: '浮选泡沫品位分析#001',
  batch: 'Batch_20250601',
  createTime: '2025-06-01 14:30',
  imageCount: 24,
  averageGrade: '47.1%',
  modelVersion: 'n',
  status: '已完成'
};
finishPrediction(predictRecord);

// 训练完成示例
const trainRecord = {
  idx: 1,
  taskName: '模型训练任务#001',
  batch: 'Train_20250601',
  createTime: '2025-06-01 15:00',
  epochs: 10,
  batchSize: 8,
  modelVersion: 'n',
  status: '已完成'
};
finishTraining(trainRecord);