# importing the libraries
from flask import Flask, request,render_template,redirect,url_for
import requests
from youtube_api import YouTubeDataAPI
from urllib.parse import urlparse
from transformers import pipeline

from youtube_transcript_api import YouTubeTranscriptApi
api_key="" # You need to get this from Google Developers
yt = YouTubeDataAPI(api_key)
summarizer = pipeline('summarization')


      
    
app = Flask(__name__)

@app.route("/" ,methods=["POST","GET"])
def index():
    theString=""

    transcriptDatalist=[]
    if request.method=="POST":
        linkRecieved=request.form["link"]
        url_data = urlparse(linkRecieved)
        vidID=url_data.query[2::]
        theTranscript=YouTubeTranscriptApi.get_transcript(vidID)
        
        
        summarized_text = []
        result = ""
        for i in theTranscript:
            result += ' ' + i['text']
        #print(result)
        print(len(result))
        num_iters = int(len(result)/1000)
        summarized_text = []
        for i in range(0, num_iters + 1):
          start = 0
          start = i * 1000
          end = (i + 1) * 1000
          
          out = summarizer(result[start:end])
          out = out[0]
          out = out['summary_text']
        
          summarized_text.append(out)
        print("Summarized text\n"+summarized_text[0])
        vidInfo=yt.get_video_metadata(vidID)
        for t in range(len(theTranscript)):

           theString += ' ' + theTranscript[t]["text"]
           transcriptDatalist.append(theTranscript[t]["text"].replace("\n", "."))
           
        return render_template('results.html', links=vidInfo["video_title"], thumbnail=vidInfo["video_thumbnail"],transcript=summarized_text)

    else:
            return render_template('home.html')


if __name__=="__main__":
    app.run(debug=True)
