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
      test.innerHTML = "";
      const { list } = JSON.parse(requestGo.response);
      console.log(list);
      for (var i = 0; i < list.length; i++) {
        const add = document.createElement("div");
        add.classList.add("list-box");
        add.innerHTML = `${list[i]["name"]} ${list[i]["address"]} ${list[i]["phone"]}`;
        test.append(add);
      }
      const { list } = JSON.parse(requestGo.response);

      lists = JSON.parse(list);

      // 사용할 때는 lists[a]["fields"][b]로 사용하면 됩니다.
      // a 는 index 번호, b는 속성
      // ex) list[0]["fields"]["name"] --> 0번째 장소의 이름
    }
  }
};
// const { list } = JSON.parse(requestGo.response);
//       test = document.querySelector(".right");

//       test.appned('p')
//       list.forEach((place) => {
//         const add = document.createElement('p');
//         test.append(add)
//       });
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
    <input type="radio" name="detail" value="애견전용" />애견전용
  </div>
  <div>
    <input type="radio" name="detail" value="애견동반" />애견동반
  </div>
</form>`;
      } else if (cate == "숙소") {
        detailBox.innerHTML = `<div class="cate-selected">${cate} 세부사항을 선택하세요!</div><form action="">
  <div>
    <input type="radio" name="detail" value="호텔" />호텔
  </div>
  <div>
    <input type="radio" name="detail" value="모텔" />모텔
  </div>
  <div>
    <input type="radio" name="detail" value="리조트" />리조트
  </div>
  <div>
    <input type="radio" name="detail" value="펜션" />펜션
  </div>
</form>`;
      } else if (cate == "장소") {
        detailBox.innerHTML = `<div class="cate-selected">${cate} 세부사항을 선택하세요!</div><form action="">
  <div>
    <input type="radio" name="detail" value="공원" />공원
  </div>
  <div>
    <input type="radio" name="detail" value="수영장" />수영장
  </div>
  <div>
    <input type="radio" name="detail" value="해변" />해변
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
      <div><input type="radio" name="location" value="경기" />경기</div>
      <div><input type="radio" name="location" value="인천" />인천</div>
      <div><input type="radio" name="location" value="강원" />강원</div>
      <div><input type="radio" name="location" value="충북" />충북</div>
      <div><input type="radio" name="location" value="충남" />충남</div>
      <div><input type="radio" name="location" value="대전" />대전</div>
      <div><input type="radio" name="location" value="세종" />세종</div>
      <div><input type="radio" name="location" value="전북" />전북</div>`;
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
      <div><input type="radio" name="location" value="광주" />광주</div>
      <div><input type="radio" name="location" value="경북" />경북</div>
      <div><input type="radio" name="location" value="경남" />경남</div>
      <div><input type="radio" name="location" value="대구" />대구</div>
      <div><input type="radio" name="location" value="울산" />울산</div>
      <div><input type="radio" name="location" value="부산" />부산</div>
      <div><input type="radio" name="location" value="대전" />대전</div>
      <div><input type="radio" name="location" value="제주" />제주</div>`;
    }
  }
};


//찜하기 기능
const requestLike = new XMLHttpRequest();
const onClickLike = (id) => {
  const url = "/like/";
  requestLike.open("POST", url, true);
  requestLike.setRequestHeader(
    "content-Type",
    "application/x-www-form-urlencoded"
  );
  requestLike.send(JSON.stringify({ id: id }))
}

requestLike.onreadystatechange = () => {
  if (requestLike.readyState === XMLHttpRequest.DONE) { //서버가 응답할 준비를 마침
    const { id, type } = JSON.parse(requestLike.response);
    const element = document.querySelector(`#favorite-${id}`);
    const i = element.querySelector(".like button i");
    i.classList.toggle("fas");
    i.classList.toggle("far");
  }
}
