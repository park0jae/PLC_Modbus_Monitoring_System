function fetchDataFromElasticsearch(index) {
  // 현재 시간 및 10초 이전 시간 계산
  var currentTime = new Date();
  var startTime = new Date(currentTime.getTime() - 2000).toISOString(); // 10초 이전 시간

  // Elasticsearch 쿼리 설정
  var query = {
    query: {
      bool: {
        must: [
          {
            range: {
              timestamp: {
                gte: startTime,
                lte: currentTime.toISOString() // 현재 시간
              }
            }
          }
        ]
      }
    }
  };

  fetch("호스트 + 포트 지정" + index + "/_search", {
    method: "POST",
    mode: "cors",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(query) // Elasticsearch 쿼리를 요청 body에 포함
  })
  .then(function(response) {
    if (response.ok) {
      return response.json();
    } else {
      throw new Error("데이터를 가져오는데 실패했습니다.");
    }
  })
  .then(function(data) {
    if (data.hits.total.value > 0) {
      var hits = data.hits.hits;
      console.log(hits);
      for (var i = 0; i < hits.length; i++) {
        var hit = hits[i];
        var source = hit._source;

        if (source.suc_or_fail === "Failed") {
          Swal.fire({
            icon: 'warning',
            title: '실패 요청 감지.',
            text : '메일을 확인해주세요!!',
            toast: true,
            position: 'center-center',
            showConfirmButton: false,
            showCloseButton: true,
            customClass: {
              title: 'toast-title',
              closeButton: 'toast-close-button',
              popup: 'toast-popup',
              content: 'toast-content'
            },
            didOpen: (toast) => {
              toast.addEventListener('mouseenter', Swal.stopTimer)
              toast.addEventListener('mouseleave', Swal.resumeTimer)
            }
          });
        } else if (source.match_status === "Mismatch" || source.match_status === "Unknown Hash") {
          Swal.fire({
            icon: 'error',
            title: '!위변조 감지!',
            text : '데이터의 위변조가 감지되었습니다.',
            toast: true,
            position: 'center',
            showConfirmButton: false,
            showCloseButton: true,
            customClass: {
              title: 'toast-title',
              closeButton: 'toast-close-button',
              popup: 'toast-popup',
              content: 'toast-content'
            },
            didOpen: (toast) => {
              toast.addEventListener('mouseenter', Swal.stopTimer)
              toast.addEventListener('mouseleave', Swal.resumeTimer)
            }
          });
        } else {
          console.log("데이터에 위변조 및 이상 요청이 감지되지 않았습니다.");
        }
      }
    } else {
      console.log("아직 데이터가 인덱싱 되지 않았습니다.");
    }
  })
  .catch(function(error) {
    console.error(error);
  });
}

setInterval(function() {
  fetchDataFromElasticsearch("packets-*");
}, 2000);

setInterval(function() {
  fetchDataFromElasticsearch("hash-*");
}, 2000);


