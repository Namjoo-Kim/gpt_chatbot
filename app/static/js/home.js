
$("#searchInput").on("change keyup paste", function(){

    let searchInput = $("#searchInput").val();

	$.ajax({
        type:'get',
        url:'/autoComplete',
        data:{
            "searchText":searchInput
        },
        dataType: 'text',
        success:function (result){
            result = JSON.parse(result);

            let autoDiv = $("#autoDiv")[0];
            if (result.length == 0){
                $("#autoDiv").empty();
                autoDiv.style.display ="none";
                return
            }
            $("#autoDiv").empty();
            autoDiv.style.display ="block"

            for (let i = 0; i < result.length; i++) {
                let row = document.createElement("div");
                row.setAttribute("class","autoRow");
                row.innerHTML=result[i]["_source"]["movieNm"];
                autoDiv.appendChild(row);

            }
        },
        error:function (){
            console.log('fail to auto complte!');
        }
    });

})

function searchBtnClick() {
    let searchInput = $("#searchInput").val();
    $.ajax({
        type: 'get',    //데이터 전송 타입,
        url: '/search',       //데이터를 주고받을 파일 주소 입력,
        data: {
            "searchText": searchInput
        },       //보내는 데이터,
        dataType: 'text', //문자형식으로 받기 ,
        success: function (result) {
            //작업이 성공적으로 발생했을 경우

            result = JSON.parse(result);

            let movieDiv = $("#movieDiv")[0];

            $("#movieTable tr:not(:first)").remove();
            let movieTable = $("#movieTable")[0]

            for (let i = 0; i < result.length; i++) {

                let tr = document.createElement("tr");

                let movieCd = document.createElement("td");
                let movieNm = document.createElement("td");
                let movieNmEn = document.createElement("td");
                let nationAlt = document.createElement("td");
                let typeNm = document.createElement("td");
                let prdtYear = document.createElement("td");

                movieCd.innerHTML = result[i]["_source"]["movieCd"]
                // movieCd.setAttribute('onclick', 'alert(this.innerHTML)')

                movieCd.onclick =  async function () {
                    let response = await fetch('http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json?key=ac8486587997228edc46f9eb6ffa313a&movieCd=' + result[i]["_source"]["movieCd"])
                    if (response) {
                        let json = await response.json()
                        // console.log(json['movieInfoResult']['movieInfo']['directors'])

                        if (json['movieInfoResult']['movieInfo']['directors'].length !== 0) {
                            let director = json['movieInfoResult']['movieInfo']['directors']
                            let directorNm = '감독:';

                            for (let i =0; i <director.length; i++) {
                                let t = director[i]['peopleNm']
                                directorNm = directorNm + ' ' + t
                            }
                            alert(directorNm)
                        } else {
                            alert('감독 정보없음')
                        }
                    } else {
                        alert('error')
                    }
                }

                // movieCd.addEventListener("click",showMovieInfo(), false)ㅋ
                // function showMovieInfo(){
                //     alert("Hello! I am an alert box!!");
                // }

                movieNm.innerHTML = result[i]["_source"]["movieNm"]
                movieNmEn.innerHTML = result[i]["_source"]["movieNmEn"]
                nationAlt.innerHTML = result[i]["_source"]["nationAlt"]
                typeNm.innerHTML = result[i]["_source"]["typeNm"]
                prdtYear.innerHTML = result[i]["_source"]["prdtYear"]

                tr.appendChild(movieCd);
                tr.appendChild(movieNm);
                tr.appendChild(movieNmEn);
                tr.appendChild(nationAlt);
                tr.appendChild(typeNm);
                tr.appendChild(prdtYear);

                movieTable.appendChild(tr);
            }

            movieDiv.appendChild(movieTable);
        },
        error: function () {
            console.log("search fail");
        }
    });

}



