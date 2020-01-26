let result = document.getElementById('disasterAnalysis');
let submit = document.getElementById('dataSubmit');
let disasterName = document.getElementById('disasterSearch');
let cityName = document.getElementById('citySearch');




function fetchApproval() {
  $.ajax({
    url: "/poll/",
    type: "POST",
    cache: false,
    data: {
        disaster: disasterName.value,    //disaster
    },
    success: function(response){
      //alert("test: " + response.match[1]);
      displayResult(response.match);
      displayTweet(response.match[2], response.match[3]);


    }
  });

}
submit.addEventListener('click', fetchApproval);


function displayResult(place){

  var out_string = "Possible " + disasterName.value + " detected in: <br>";
  for(var location in place){
    out_string += place[location];
    out_string += "<br>";
  }
  result.innerHTML = out_string;
}
