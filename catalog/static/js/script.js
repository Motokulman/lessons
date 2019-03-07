//
  /***** START BOILERPLATE CODE: Load client library, authorize user. *****/

  // Global variables for GoogleAuth object, auth status.
  var GoogleAuth;

  /**
   * Load the API's client and auth2 modules.
   * Call the initClient function after the modules load.
   */
  function handleClientLoad() {
    gapi.load('client:auth2', initClient);
  }

  function initClient() {
    // Initialize the gapi.client object, which app uses to make API requests.
    // Get API key and client ID from API Console.
    // 'scope' field specifies space-delimited list of access scopes

    gapi.client.init({
        'clientId': '806025746763-mqj886g6hus4jscvuneufgosinvgl7o6.apps.googleusercontent.com',
        'discoveryDocs': ['https://www.googleapis.com/discovery/v1/apis/youtube/v3/rest'],
        'scope': 'https://www.googleapis.com/auth/youtube.force-ssl https://www.googleapis.com/auth/youtubepartner'
    }).then(function () {
      GoogleAuth = gapi.auth2.getAuthInstance();

      // Listen for sign-in state changes.
      GoogleAuth.isSignedIn.listen(updateSigninStatus);

      // Handle initial sign-in state. (Determine if user is already signed in.)
      setSigninStatus();

      // Call handleAuthClick function when user clicks on "Authorize" button.
      $('#execute-request-button').click(function() {
        handleAuthClick(event);
      }); 
    });
  }

  function handleAuthClick(event) {
    // Sign user in after click on auth button.
    GoogleAuth.signIn();

  }

  function setSigninStatus() {
     // console.log("setSigninStatus")
    var user = GoogleAuth.currentUser.get();
    isAuthorized = user.hasGrantedScopes('https://www.googleapis.com/auth/youtube.force-ssl https://www.googleapis.com/auth/youtubepartner');
    // Toggle button text and displayed statement based on current auth status.
    if (!isAuthorized) {
        console.log("!isAuthorized");
      GoogleAuth.signIn();
    }
  }

  function updateSigninStatus(isSignedIn) {
    setSigninStatus();
  }

  function createResource(properties) {
    var resource = {};
    var normalizedProps = properties;
    for (var p in properties) {
      var value = properties[p];
      if (p && p.substr(-2, 2) == '[]') {
        var adjustedName = p.replace('[]', '');
        if (value) {
          normalizedProps[adjustedName] = value.split(',');
        }
        delete normalizedProps[p];
      }
    }
    for (var p in normalizedProps) {
      // Leave properties that don't have values out of inserted resource.
      if (normalizedProps.hasOwnProperty(p) && normalizedProps[p]) {
        var propArray = p.split('.');
        var ref = resource;
        for (var pa = 0; pa < propArray.length; pa++) {
          var key = propArray[pa];
          if (pa == propArray.length - 1) {
            ref[key] = normalizedProps[p];
          } else {
            ref = ref[key] = ref[key] || {};
          }
        }
      };
    }
    return resource;
  }

  function removeEmptyParams(params) {
    for (var p in params) {
      if (!params[p] || params[p] == 'undefined') {
        delete params[p];
      }
    }
    return params;
  }
  
  
  //window.onload = setSigninStatus; 

  

  var lessonsIdArr = ["wVgerXQI8RY", "EAUbz6K5vdg", "oFB0FYiB5M8", "qRA1SQH7g8w", "QLeAb0f3mO8", "fRQGeyLXPug", "KHF6CRuprPo", "PKaKYDdR9zY", "y7zzd33lVwQ", "A2krIs8uGeI", "WYNP4hyiSRg", "N8ePFANgVsM", "uO5vSCqJscc", "L715_6P1U0c", "g1HpawZ2aRg", "mmUN7O9WAcs", "oRxE71NfJUo", "Ow_UjTIpsCM"];
  var lessonIdNum = localStorage.getItem("lessonIdNum");
  
  
  if (!lessonIdNum) {
      localStorage.setItem("lessonIdNum", 0);
      lessonIdNum = localStorage.getItem("lessonIdNum"); 
  }
console.log('lessonIdNum = ' + lessonIdNum);
  
  if (window.matchMedia('(display-mode: standalone)').matches) {
  console.log('display-mode is standalone');
}
  

  function executeRequest(request) {
    request.execute(function(response) {
        console.log(response);
        showSearchRes(response);
    });
  }
  
    function showSearchRes(response) {
      var res = response;
      var searchResListDiv = document.getElementById("search-result");

      for(var i = 0; i<response.pageInfo.resultsPerPage; i++){
          if (response.items[i].id.videoId == undefined) continue;
      var imgDiv = document.createElement("div");
      var iVideoId =  response.items[i].id.videoId;
      imgDiv.id = iVideoId;
   //   console.log('imgDiv.id = ' + imgDiv.id);
      imgDiv.name = "iSearchResult";
      imgDiv.className = "col-lg-4";
      imgDiv.innerHTML = '<img  src=\"' + response.items[i].snippet.thumbnails.medium.url + '\" alt=\"' + response.items[i].snippet.title + '\"><br><p></p>';
    //  var imgDivText = document.createTextNode('<a href=""><img src=\"' + response.items[0].snippet.thumbnails.high.url + '\" alt=\"' + response.items[0].snippet.title + '\"></a>');
     // imgDiv.appendChild(imgDivText);


      searchResListDiv.appendChild(imgDiv);
      
      var descriptDiv = document.createElement("div");
      descriptDiv.className = "col-lg-8";
      descriptDiv.innerHTML = '<strong>' + response.items[i].snippet.title + '</strong> <br> Канал: ' + response.items[i].snippet.channelTitle + '<br>' + response.items[i].snippet.description;
      searchResListDiv.appendChild(descriptDiv);
      
  //    var separatorDiv = document.createElement("div");
    //  separatorDiv.className = "col-12";
    //  imgDiv.innerHTML = '<p></p>';
   //   searchResListDiv.appendChild(separatorDiv);
  
      }

      $(function() {
 //        var x = true;
        $(document).on('click touchstart', 'div', function(){ 
            if (this.name ==  "iSearchResult") {
                console.log(this.id);
                playVideo(this.id);
                
  //              x = !x;
            }

        });
    });
  }

  function buildApiRequest(requestMethod, path, params, properties) {
    params = removeEmptyParams(params);
    var request;
    if (properties) {
      var resource = createResource(properties);
      request = gapi.client.request({
          'body': resource,
          'method': requestMethod,
          'path': path,
          'params': params
      });
    } else {
      request = gapi.client.request({
          'method': requestMethod,
          'path': path,
          'params': params
      });
    }
    executeRequest(request);
  }

    // 2. This code loads the IFrame Player API code asynchronously.
    
      var tag = document.createElement('script');

      tag.src = "https://www.youtube.com/iframe_api";
      var firstScriptTag = document.getElementsByTagName('script')[0];
      firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

      // 3. This function creates an <iframe> (and YouTube player)
      //    after the API code downloads.
    var player;
    var playerLesson;

          var playerTag;
          var playerLessonTag;//  = document.getElementById("playerLesson");

    function playVideo(vidId) {
  //      console.log('vidId = ' + vidId);
var s =  vidId;// + '?rel=0';
        // console.log('s = ' + s);
         player = new YT.Player('player', {
          height: 1080, //'360',
          width: 1920,//'640',
          playerVars: { 'rel': 0, 'fs': 0, 'showinfo': 0, 'autohide': 1 },
          videoId: s,
          events: {
            'onReady': onPlayerReady,
          //  'onStateChange': onPlayerStateChange
          }
        });
        
            mixpanel.track("Play Video Clicked",
                {
               //     "youtube_video_id": youtubeVideoId
                });
        
        

        
      }
  var videoDiv = document.getElementById('myvideo');
      // 4. The API will call this function when the video player is ready.
      function onPlayerReady(event) {
          playerTag = document.getElementById(player.getIframe().id);
          videoDiv.hidden = false;
         // playerLessonTag = document.getElementById(playerLesson.getIframe().id);
       //  playerTag.hidden = false;
       //  playerLessonTag.hidden = true;
        //  alert('onPlayerReady');
        event.target.playVideo();

        
    //    console.log('onPlayerReady');
        //setInterval(prepareLessonPlayer, 10000);
        setInterval(prepareLessonPlayer, 300000);
       // setTimeout(playLesson, 10000);
      }
      

      

      
      function prepareLessonPlayer() {
          
          console.log('prepareLessonPlayer');
          
          playerLesson = new YT.Player('playerLesson', {
          height: 1080, //'360',
          width: 1920,//'640',
          playerVars: { 'rel': 0, 'fs': 0, 'showinfo': 0, 'autohide': 1, 'autoplay': 1},
          videoId:   lessonsIdArr[lessonIdNum],
          events: {
            'onReady': onPlayerLessonReady,
            'onStateChange': onPlayerLessonStateChange
          }
        });
      }
      
      var timerId;
      function onPlayerLessonReady(event) {
          console.log('onPlayerLessonReady');
          playerLessonTag = document.getElementById(playerLesson.getIframe().id);
          playerLessonTag.hidden = true;
          
       //   playerLessonTag = document.getElementById(playerLesson.getIframe().id);
          
        //  console.log('onPlayerLessonReady');
        event.target.playVideo();
      //  event.target.pauseVideo();
        
        timerId = setInterval(timerFunction, 100);
      }
      
      
     function timerFunction() {
         console.log('timerFunction');
 //console.log('playerLesson.getVideoLoadedFraction() == ' + playerLesson.getVideoLoadedFraction());
          if (playerLesson.getVideoLoadedFraction() > 0 ) {
              clearTimeout(timerId);
              playerLesson.pauseVideo();
              playLesson();
             
          }
      }
         
      function playLesson() {
          

          

          console.log('playLesson');
         // console.log(document.getElementById(player.getIframe().id).width);
          player.pauseVideo();
          playerTag.hidden = true;
          
          playerLessonTag.hidden = false;
          
          playerLesson.setSize(player.getIframe().width, player.getIframe().height);
       // console.log(player.getIframe());
          playerLesson.playVideo();
          
      }
      
      function onPlayerLessonStateChange(event) {
        if (event.data == YT.PlayerState.ENDED) {
          playerLessonTag.hidden = true;
          playerTag.hidden = false;
          player.setSize(playerLesson.getIframe().width, playerLesson.getIframe().height);
          playerLesson.destroy()
          player.playVideo();
          lessonIdNum++;
          if (lessonIdNum >= lessonsIdArr.length) lessonIdNum = 0;
          localStorage.setItem("lessonIdNum", lessonIdNum);
          console.log('lessonIdNum = ' + lessonIdNum);

        }
      }

      // 5. The API calls this function when the player's state changes.
      //    The function indicates that when playing a video (state=1),
      //    the player should play for six seconds and then stop.
      var done = false;
      function onPlayerStateChange(event) {
        if (event.data == YT.PlayerState.PLAYING && !done) {
          setTimeout(stopVideo, 6000);
          done = true;
        }
      }
      function stopVideo() {
        player.stopVideo();
      }

    var searchButton = document.getElementById("search");
    console.log("searchButton = " + searchButton);
    searchButton.addEventListener("click", function (e) {

        defineSearch();
    });
    

  /***** END BOILERPLATE CODE *****/

  
  function defineRequest() {
    // See full sample for buildApiRequest() code, which is not 
// specific to a particular API or API method.

buildApiRequest('GET',
                '/youtube/v3/search',
                {'maxResults': '25',
                 'part': 'snippet',
                 'q': 'surfing',
                 'type': ''});

  }
  
  
function defineSearch() {
    if (player) {player.destroy();}
    var searchForm = document.forms["search"];
    var keyBox = searchForm.elements["key"].value;
    buildApiRequest('GET',
                    '/youtube/v3/search',
                    {'maxResults': '25',
                     'part': 'snippet',
                     'q': keyBox,
                     'type': ''});
                     
    mixpanel.track(
    "Search",
    {"search": keyBox}
    );

  }

      
    mixpanel.track_links("#nav a", "click nav link", {
        "referrer": document.referrer
        });

    
    

