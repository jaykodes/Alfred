function speak(speech) {
    var msg = new SpeechSynthesisUtterance(speech);
    msg.rate = 0.8;
    msg.pitch = 1;
    msg.volume = 0.8;
    msg.voiceURI = "Alex";
    msg.lang = "en-GB";
    window.speechSynthesis.speak(msg);
}

function ajax_call(sentence) {

	url_base = 'YOUR-SERVER';
	url_extra = sentence.split(' ').join('_')
	url_actual = url_base.concat(url_extra);

	$.ajax({
		type: 'get', // This is the default though, you don't actually need to always mention it
		dataType: 'text',
		url: url_actual,
		success: function(data) {

			parts = sentence.split(' ');

			if (data == '"website"') {
				
				website_url="https://www.";
				site = "";
				
				for (var i = 0; i < parts.length; i += 1) {
					if (parts[i].indexOf('.com') > -1 || parts[i].indexOf('.ca') > -1 || parts[i].indexOf('.org') > -1 || parts[i].indexOf('.io') > -1) {
						site = parts[i];
						break;
					}
				}

				talk = "going to ".concat(site);
				speak(talk);
				window.open(website_url.concat(site));
			}
			else if (data == '"google false"') {

				searchUrl = "https://www.google.com/search?q=";
				search = "";
				google_point = parts.indexOf("google");
				search_point = parts.indexOf("search");
				slice_point = 0;

				if (google_point > -1 && search_point > -1) {
					slice_point = Math.min(google_point, search_point);
				}
				else {
					slice_point = Math.max(google_point, search_point);
				}

				search = parts.slice(slice_point + 1).join(' ');
				talk = "this is what i found on the web";
				speak(talk);
				window.open(searchUrl.concat(search));
			}
			else if (data == '"youtube"') {

				youtubeUrl = "https://www.youtube.com/results?q=";
				search = "";
				youtube_point = parts.indexOf("youtube");
				search = parts.slice(youtube_point + 1).join(' ');
				talk = "searching ".concat(search).concat(" on youtube");
				speak(talk);
				window.open(youtubeUrl.concat(search));
			}
			else if (data == '"play"') {

				youtubeUrl = "https://www.youtube.com/results?q=";
				search = "";
				play_point = parts.indexOf("play");
				search = parts.slice(play_point + 1).join(' ');
				talk = "playing ".concat(search).concat(" on youtube");
				speak(talk);
				window.open(youtubeUrl.concat(search));
			}
			else if (data == '"open"') {

				website_url="https://www.";
				site = "";
				open_point = parts.indexOf("open");
				site = parts[open_point + 1].concat(".com")
				talk = "going to ".concat(site);
				speak(talk);
				window.open(website_url.concat(site));
			}
			else if (data == '"google true"') {

				searchUrl = "https://www.google.com/search?q=";
				window.open(searchUrl.concat(sentence));
				talk = "this is what i found on the web";
				speak(talk);
			}
			else {
				talk = "i don't understand";
				speak(talk);
			}

		},
		failure: function(data) { 
			alert('Error with Request');
		}
	});
}

window.SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
			
const recognition = new webkitSpeechRecognition();
recognition.interimResults = true;
recognition.continous = true;

let p = document.createElement('p');
const words = document.querySelector('.words');
words.appendChild(p);

recognition.addEventListener('result', e => {
							
	const transcript = Array.from(e.results).map(result => result[0]).map(result => result.transcript).join('');
	p.textContent = transcript;

	if (e.results[0].isFinal) {

		if (transcript.split(' ')[0].toLowerCase() == "alfred") {
			ajax_call(transcript.toLowerCase());
		}
	}
});

recognition.addEventListener('end', recognition.start);
recognition.start();
