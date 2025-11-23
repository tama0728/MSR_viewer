# 자동화 시스템 사용 가이드

이 프로젝트는 새로운 이미지를 폴더에 추가하면 자동으로 웹사이트에 반영되도록 설정되었습니다.

## 사용 방법

1. **이미지 추가**:
   - `scenes` 폴더 안에 새로운 폴더를 만들거나 기존 폴더에 이미지를 추가하세요.
   - 예: `scenes/NewDataset/HR/image.png`

2. **변경 사항 업로드 (Push)**:
   - 변경된 사항을 깃허브에 올리세요.
   ```bash
   git add .
   git commit -m "Add new images"
   git push origin master
   ```

3. **자동 업데이트**:
   - 깃허브에 코드가 올라가면, 자동으로 `update_viewer.py` 스크립트가 실행됩니다.
   - 이 스크립트는:
     - 모든 `scenes` 폴더를 스캔합니다.
     - 각 폴더의 `data.js`를 최신 이미지 목록으로 업데이트합니다.
     - 메인 `index.html`에 새로운 데이터셋을 추가합니다.
   - 변경된 내용은 자동으로 저장소에 다시 커밋됩니다.

4. **결과 확인**:
   - 잠시 후 깃허브 저장소를 새로고침하면 `data.js`와 `index.html`이 업데이트된 것을 확인할 수 있습니다.
   - 깃허브 Pages가 설정되어 있다면 웹사이트에서도 곧 확인할 수 있습니다.

## 웹사이트로 보는 법 (GitHub Pages 설정)

깃허브 URL로 접속해서 보려면 **GitHub Pages**를 활성화해야 합니다.

1. 깃허브 저장소 페이지로 이동합니다.
2. 상단 메뉴에서 **Settings** (설정) 탭을 클릭합니다.
3. 왼쪽 사이드바에서 **Pages** 메뉴를 찾아서 클릭합니다.
4. **Build and deployment** 섹션의 **Source** 아래에서 **Deploy from a branch**를 선택합니다.
5. **Branch** 항목에서 `master` (또는 `main`) 브랜치를 선택하고 **Save**를 클릭합니다.
6. 잠시 기다리면(약 1~2분) 페이지 상단에 "Your site is live at..." 메시지와 함께 URL이 나타납니다.
7. 그 URL을 클릭하면 웹사이트를 볼 수 있습니다.

## 로컬에서 실행하기

원한다면 로컬 컴퓨터에서도 수동으로 스크립트를 실행할 수 있습니다:

```bash
python3 update_viewer.py
```
