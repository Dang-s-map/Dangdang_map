// mainList.html 부분
const requestGo = new XMLHttpRequest();
const onClickGo = () => {
  requestGo.open("POST", "/listGo/", true);
  requestGo.setRequestHeader(
    "Content-Type",
    "application/x-www-form-urlencoded"
  );
  var location, category, detail;
  const locList = document.getElementsByName("location");
  locList.forEach((loc) => {
    if (loc.checked) {
      location = loc.value;
    }
  });

  const cateSelected = document.querySelector(".cate-selected").innerHTML;
  if (cateSelected.includes("카페")) {
    category = "cafe";
  } else if (cateSelected.includes("숙소")) {
    category = "accomodation";
  } else if (cateSelected.includes("장소")) {
    category = "place";
  }

  const detailList = document.getElementsByName("detail");
  detailList.forEach((d) => {
    if (d.checked) {
      detail = d.value;
    }
  });
  requestGo.send(
    JSON.stringify({ location: location, category: category, detail: detail })
  );
};

requestGo.onreadystatechange = () => {
  if (requestGo.readyState === XMLHttpRequest.DONE) {
    if (requestGo.status < 400) {
      const { location, category, detail } = JSON.parse(requestGo.response);
      test = document.querySelector(".right");
      test.innerHTML += `${location} ${category} ${detail}`;
    }
  }
};

//
const requestLoc = new XMLHttpRequest();

const onClickLocation = (location) => {
  requestLoc.open("POST", "/locations/", true);
  requestLoc.setRequestHeader(
    "Content-Type",
    "application/x-www-form-urlencoded"
  );
  requestLoc.send(JSON.stringify({ location: location }));
};

requestLoc.onreadystatechange = () => {
  if (requestLoc.readyState === XMLHttpRequest.DONE) {
    if (requestLoc.status < 400) {
      //  views.py/locations 에서 보내준 data 화면에 뿌리기
    }
  }
};

// 멍카페, 멍숙소, 멍놀자 세부선택 ajax 처리
const requestCate = new XMLHttpRequest();
const onClickCate = (cate) => {
  // 질문!! -> 눌렀을 때 서버로 데이터 가져와서 뿌려주는 게 아닌데 이 부분 필요? 간소화?
  requestCate.open("POST", "/cates/", true);
  requestCate.setRequestHeader(
    "Content-Type",
    "application/x-www-form-urlencoded"
  );
  requestCate.send(JSON.stringify({ cate: cate }));
};

requestCate.onreadystatechange = () => {
  if (requestCate.readyState === XMLHttpRequest.DONE) {
    if (requestCate.status < 400) {
      const { cate } = JSON.parse(requestCate.response);
      const detailBox = document.querySelector("#left-detail");

      if (cate == "카페") {
        detailBox.innerHTML = `<div class="cate-selected">${cate} 세부사항을 선택하세요!</div><form action="">
  <div>
    <input type="radio" name="detail" value="dogs-only" />애견 전용
  </div>
  <div>
    <input type="radio" name="detail" value="dogs-can" />애견 동반
  </div>
</form>`;
      } else if (cate == "숙소") {
        detailBox.innerHTML = `<div class="cate-selected">${cate} 세부사항을 선택하세요!</div><form action="">
  <div>
    <input type="radio" name="detail" value="hotel" />호텔
  </div>
  <div>
    <input type="radio" name="detail" value="motel" />모텔
  </div>
  <div>
    <input type="radio" name="detail" value="resort" />리조트
  </div>
  <div>
    <input type="radio" name="detail" value="pension" />펜션
  </div>
</form>`;
      } else if (cate == "장소") {
        detailBox.innerHTML = `<div class="cate-selected">${cate} 세부사항을 선택하세요!</div><form action="">
  <div>
    <input type="radio" name="detail" value="park" />공원
  </div>
  <div>
    <input type="radio" name="detail" value="pool" />수영장
  </div>
  <div>
    <input type="radio" name="detail" value="beach" />해변
  </div>
</form>`;
      }
    }
  }
};

// 지역 고르기 부분 ajax
// <
const requestLeft = new XMLHttpRequest();
const onClickLeft = () => {
  requestLeft.open("POST", "/locationBtn/", true);
  requestLeft.setRequestHeader(
    "Content-Type",
    "application/x-www-form-urlencoded"
  );
  requestLeft.send(JSON.stringify({})); // 뭐 넘겨줘야 하니 생각해보기
};

requestLeft.onreadystatechange = () => {
  if (requestLeft.readyState === XMLHttpRequest.DONE) {
    if (requestLeft.status < 400) {
      const locationBox = document.querySelector("#location-select");
      locationBox.innerHTML = `<div><input type="radio" name="location" value="seoul" />서울</div>
      <div><input type="radio" name="location" value="gyeonggi" />경기</div>
      <div><input type="radio" name="location" value="incheon" />인천</div>
      <div><input type="radio" name="location" value="gangwon" />강원</div>
      <div><input type="radio" name="location" value="chungbuk" />충북</div>
      <div><input type="radio" name="location" value="chungnam" />충남</div>
      <div><input type="radio" name="location" value="deajeon" />대전</div>
      <div><input type="radio" name="location" value="sejong" />세종</div>
      <div><input type="radio" name="location" value="jeonbuk" />전북</div>`;
    }
  }
};
// >
const requestRight = new XMLHttpRequest();
const onClickRight = () => {
  requestRight.open("POST", "/locationBtn/", true);
  requestRight.setRequestHeader(
    "Content-Type",
    "application/x-www-form-urlencoded"
  );
  requestRight.send(JSON.stringify({})); // 뭐 넘겨줘야 하니 생각해보기
};

requestRight.onreadystatechange = () => {
  if (requestRight.readyState === XMLHttpRequest.DONE) {
    if (requestRight.status < 400) {
      const locationBox = document.querySelector("#location-select");
      locationBox.innerHTML = `<div><input type="radio" name="location" value="jeonnam" />전남</div>
      <div><input type="radio" name="location" value="gwangju" />광주</div>
      <div><input type="radio" name="location" value="gyeongbuk" />경북</div>
      <div><input type="radio" name="location" value="gyeongnam" />경남</div>
      <div><input type="radio" name="location" value="daegu" />대구</div>
      <div><input type="radio" name="location" value="ulsan" />울산</div>
      <div><input type="radio" name="location" value="busan" />부산</div>
      <div><input type="radio" name="location" value="daejeon" />대전</div>
      <div><input type="radio" name="location" value="jeju" />제주</div>`;
    }
  }
};


//목록에서 장소이름 클릭하면 상세페이지 뜨는 부분
