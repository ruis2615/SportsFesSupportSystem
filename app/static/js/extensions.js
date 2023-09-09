// select要素を取得
const scheduleCategorySelect = document.querySelector('select[name="ScheduleType"]');

// select要素にchangeイベントリスナーを設定
scheduleCategorySelect.addEventListener('change', function() {
  const sportDetailsDiv = document.getElementById('SportDetails');
    while (sportDetailsDiv.lastChild){
      sportDetailsDiv.removeChild(sportDetailsDiv.lastChild)
    }

  // select要素の選択されたoption要素を取得
  const selectedOption = this.options[this.selectedIndex];

  // 選択されたoptionのvalueが「競技(男女)」だった場合
  if (selectedOption.value === '1') {
    // 追加するHTML
    const newHtml = '<p class="text-danger mx-3">※1レースで必要な人数を入力してください。</p>' +
        '                        <div class="col-lg-2">\n' +
        '                            <div class="input-group input-group-static mb-4 mx-3">\n' +
        '                                <label>出場人数</label>\n' +
        '                                <input type="number" class="form-control" name="AppearanceCount" required>\n' +
        '                            </div>\n' +
        '                        </div>\n' +
        '                        <div class="col-lg-2">\n' +
        '                            <div class="input-group input-group-static mb-4 mx-3">\n' +
        '                                <label>補欠人数</label>\n' +
        '                                <input type="number" class="form-control" name="ReserveCount" required>\n' +
        '                            </div>\n' +
        '                        </div>\n' +
        '                        <div class="col-lg-2">\n' +
        '                            <div class="input-group input-group-static mb-4 mx-3">\n' +
        '                                <label>レース数</label>\n' +
        '                                <input type="number" class="form-control" name="RaceNumber" required>\n' +
        '                            </div>\n' +
        '                        </div>';

    // HTMLを追加する要素を取得
    const targetElement = document.getElementById('SportDetails');

    // HTMLを追加する
    targetElement.insertAdjacentHTML('beforeend', newHtml);
  }

  // 選択されたoptionのvalueが「競技(男女別)」だった場合
  if (selectedOption.value === '2') {
    // 追加するHTML
    const newHtml = '<p class="text-danger mx-3">※1レースで必要な人数を入力してください。</p>' +
        '                        <div class="col-lg-2">\n' +
        '                            <div class="input-group input-group-static mb-4 mx-3">\n' +
        '                                <label>出場人数(男子)</label>\n' +
        '                                <input type="number" class="form-control" name="AppearanceCountMale" required>\n' +
        '                            </div>\n' +
        '                        </div>\n' +
        '                        <div class="col-lg-2">\n' +
        '                            <div class="input-group input-group-static mb-4 mx-3">\n' +
        '                                <label>補欠人数(男子)</label>\n' +
        '                                <input type="number" class="form-control" name="ReserveCountMale" required>\n' +
        '                            </div>\n' +
        '                        </div>\n' +
        '                        <div class="col-lg-2">\n' +
        '                            <div class="input-group input-group-static mb-4 mx-3">\n' +
        '                                <label>出場人数(女子)</label>\n' +
        '                                <input type="number" class="form-control" name="AppearanceCountFemale" required>\n' +
        '                            </div>\n' +
        '                        </div>\n' +
        '                        <div class="col-lg-2">\n' +
        '                            <div class="input-group input-group-static mb-4 mx-3">\n' +
        '                                <label>補欠人数(女子)</label>\n' +
        '                                <input type="number" class="form-control" name="ReserveCountFemale" required>\n' +
        '                            </div>\n' +
        '                        </div>\n' +
        '                        <div class="col-lg-2">\n' +
        '                            <div class="input-group input-group-static mb-4 mx-3">\n' +
        '                                <label>レース数</label>\n' +
        '                                <input type="number" class="form-control" name="RaceNumber" required>\n' +
        '                            </div>\n' +
        '                        </div>';

    // HTMLを追加する要素を取得
    const targetElement = document.getElementById('SportDetails');

    // HTMLを追加する
    targetElement.insertAdjacentHTML('beforeend', newHtml);
  }

  // 選択されたoptionのvalueが「その他」だった場合
  if (selectedOption.value === '0') {
    const sportDetailsDiv = document.getElementById('SportDetails');
    while (sportDetailsDiv.lastChild){
      sportDetailsDiv.removeChild(sportDetailsDiv.lastChild)
    }
  }
});