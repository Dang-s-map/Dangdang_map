//home.html부분

const requestHomeLeft = new XMLHttpRequest(); //어디로 떠날까요? 부분
const onClickHome = (direction) => {
  requestHomeLeft.open("POST", "/btn_main/", true);
  requestHomeLeft.setRequestHeader(
    "Content-Type",
    "application/x-www-form-urlencoded"
  );
  requestHomeLeft.send(JSON.stringify({ direction: direction }));
};

requestHomeLeft.onreadystatechange = () => {
  if (requestHomeLeft.readyState === XMLHttpRequest.DONE) {
    if (requestHomeLeft.status <= 400) {
      const { direction } = JSON.parse(requestHomeLeft.response);
      let element = document.querySelector("#num");
      let count = Number(element.innerHTML);
      if (direction == "left") {
        count -= 1;
        if (count == -1) {
          count = 2;
        } else {
          count %= 2;
        }
      } else {
        count += 1;
        count %= 3;
      }

      element.innerHTML = `${count}`;

      if (count == 0) {
        const locationSet = document.querySelector(".shift-locations");
        locationSet.innerHTML = `<div class="home_location"><a href="/list/cafe/서울/애견동반">
        <img src="/static/img/main_loc/Tag-14.png" alt=""></a></div>
        <div class="home_location"><a href="/list/cafe/경기/애견동반">
        <img src="/static/img/main_loc/Tag-12.png" alt=""></a></div>
        <div class="home_location"><a href="/list/cafe/인천/애견동반">
        <img src="/static/img/main_loc/Tag-13.png" alt=""></a></div>
        <div class="home_location"><a href="/list/cafe/강원/애견동반">
        <img src="/static/img/main_loc/Tag-11.png" alt=""></a></div>
        <div class="home_location"><a href="/list/cafe/충북/애견동반">
        <img src="/static/img/main_loc/Tag-15.png" alt=""></a></div>
        <div class="home_location"><a href="/list/cafe/충남/애견동반">
        <img src="/static/img/main_loc/Tag-16.png" alt=""></a></div>`;
        const page = document.querySelector(".page_dot");
        page.innerHTML = '<img src="/static/img/page_1.svg" alt="">';
      } else if (count == 1) {
        const locationSet = document.querySelector(".shift-locations");
        locationSet.innerHTML = `<div class="home_location"><a href="/list/cafe/대전/애견동반">
        <img src="/static/img/main_loc/Tag-5.png" alt=""></a></div>
        <div class="home_location"><a href="/list/cafe/세종/애견동반">
        <img src="/static/img/main_loc/Tag-6.png" alt=""></a></div>
        <div class="home_location"><a href="/list/cafe/경북/애견동반">
        <img src="/static/img/main_loc/Tag-7.png" alt=""></a></div>
        <div class="home_location"><a href="/list/cafe/경남/애견동반">
        <img src="/static/img/main_loc/Tag-8.png" alt=""></a></div>
        <div class="home_location"><a href="/list/cafe/대구/애견동반">
        <img src="/static/img/main_loc/Tag-9.png" alt=""></a></div>
        <div class="home_location"><a href="/list/cafe/울산/애견동반">
        <img src="/static/img/main_loc/Tag-10.png" alt=""></a></div>`;
        const page = document.querySelector(".page_dot");
        page.innerHTML = '<img src="/static/img/page_2.svg" alt="">';
      } else {
        const locationSet = document.querySelector(".shift-locations");
        locationSet.innerHTML = `<div class="home_location"><a href="/list/cafe/부산/애견동반">
        <img src="/static/img/main_loc/Tag.png" alt=""></a></div>
        <div class="home_location"><a href="/list/cafe/광주/애견동반">
        <img src="/static/img/main_loc/Tag-1.png" alt=""></a></div>
        <div class="home_location"><a href="/list/cafe/전북/애견동반">
        <img src="/static/img/main_loc/Tag-2.png" alt=""></a></div>
        <div class="home_location"><a href="/list/cafe/전남/애견동반">
        <img src="/static/img/main_loc/Tag-3.png" alt=""></a></div>
        <div class="home_location"><a href="/list/cafe/제주/애견동반">
        <img src="/static/img/main_loc/Tag-4.png" alt=""></a></div>`;
        const page = document.querySelector(".page_dot");
        page.innerHTML = '<img src="/static/img/page_3.svg" alt="">';
      }
    }
  }
};

// mainList.html 부분

// 멍카페, 멍숙소, 멍놀자 세부선택 ajax 처리
const requestCate = new XMLHttpRequest();
const onClickCate = (cate) => {
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
      const locName = document.querySelector(".selected-category");
      locName.innerHTML = `${cate} 세부옵션`;
      const detailBox = document.querySelector(".option-box");
      if (cate == "카페") {
        detailBox.innerHTML = `<div class="option-col">
    <label class="type-menu">
      <input type="radio" name="type" value="애견전용" />
      <span></span>애견전용 카페
    </label>
    <label class="type-menu">
      <input type="radio" name="type" value="애견동반" checked/>
      <span></span>애견동반 카페
    </label>
  </div>`;
      } else if (cate == "숙소") {
        detailBox.innerHTML = `<div class="option-col">
        <label class="type-menu">
          <input type="radio" name="type" value="호텔" />
          <span></span>호텔
        </label>
        <label class="type-menu">
          <input type="radio" name="type" value="모텔" />
          <span></span>모텔
        </label>
        </div>
        <div class="option-col">
        <label class="type-menu">
          <input type="radio" name="type" value="리조트" />
          <span></span>리조트
        </label>
        <label class="type-menu">
          <input type="radio" name="type" value="펜션" checked/>
          <span></span>펜션
        </label>
      </div>`;
      } else if (cate == "장소") {
        detailBox.innerHTML = `<div class="option-col">
        <label class="type-menu">
          <input type="radio" name="type" value="공원"/>
          <span></span>공원
        </label>
        <label class="type-menu">
          <input type="radio" name="type" value="수영장" />
          <span></span>수영장
        </label>  
      </div>
      <div class="option-col">
      <label class="type-menu">
        <input type="radio" name="type" value="해변" />
        <span></span>해변
      </label>
      <label class="type-menu">
      <input type="radio" name="type" value="명소" checked/>
      <span></span>명소
      </label></div>`;
      }
    }
  }
};
// 새로 고침시 타입 체크박스 체크상태 변경
const selectedType = document.querySelector(".selected-type").innerHTML;
const changeType = document.getElementsByName("type");
changeType.forEach((type) => {
  if (type.value == selectedType) {
    type.checked = true;
  }
});

//찜하기 기능
const requestLike = new XMLHttpRequest();
const onClickLike = (category, place_id, favorite) => {
  const url = "/like/";
  requestLike.open("POST", url, true);
  requestLike.setRequestHeader(
    "content-Type",
    "application/x-www-form-urlencoded"
  );
  console.log(category, place_id, favorite); // test코드
  requestLike.send(
    JSON.stringify({
      category: category,
      place_id: place_id,
    })
  );
};

requestLike.onreadystatechange = () => {
  if (requestLike.readyState === XMLHttpRequest.DONE) {
    //서버가 응답할 준비를 마침
    const { place_id, isLogin } = JSON.parse(requestLike.response);
    console.log(place_id);
    const element = document.querySelector(`#favorite-${place_id}`);
    const i = element.querySelector(".like button i");
    const btn = element.querySelector(".like button").innerHTML;
    if (isLogin) {
      i.classList.toggle("far");
      i.classList.toggle("fas");
    } else {
      alert("로그인 하세요!");
    }
  }
};
