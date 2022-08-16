// medicalList에서 검색 눌렀을 때

const requestMedical = new XMLHttpRequest();
const onclickMedical = () => {
  requestMedical.open("POST", "/medicals/", true);
  requestMedical.setRequestHeader(
    "Content-Type",
    "application/x-www-form-urlencoded"
  );
  location = document.getElementById("location");
  loc = location.options[location.selectedIndex].text;
  query = document.getElementById("query-loc").value;
  console.log(loc, query);
  requestMedical.send(JSON.stringify({ loc: loc, query: query }));
};

requestMedical.onreadystatechange = () => {
  if (requestMedical.readyState === XMLHttpRequest.DONE) {
    if (requestMedical.status <= 400) {
      const { medicals, query, loc } = JSON.parse(requestMedical.response);
      console.log(query, loc);
    }
  }
};
