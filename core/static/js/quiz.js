document.addEventListener("DOMContentLoaded", function () {
    const quiz = document.getElementById("quiz");
    const resultDiv = document.getElementById("result");
    const resultText = document.getElementById("result-text");
    const shareTwitter = document.getElementById("share-twitter");
    const shareFacebook = document.getElementById("share-facebook");
    console.log("quiz.js loaded successfully!");
  
    document.getElementById("submit-quiz").addEventListener("click", function () {
      let scores = {
        "summer-lover": 0,
        "summer-hater": 0,
        "rain-hater": 0,
        "unaffected": 0,
      };
  
      // Collect answers and tally scores
      const questions = quiz.querySelectorAll(".question");
      questions.forEach((question) => {
        const selectedOption = question.querySelector("input[type='radio']:checked");
        if (selectedOption) {
          scores[selectedOption.value]++;
        }
      });
  
      // Determine the dominant personality type
      let resultType = Object.keys(scores).reduce((a, b) => (scores[a] > scores[b] ? a : b));
  
      // Assign result descriptions
      const descriptions = {
        "summer-lover": "You are a Summer Lover: Bright days energize you, and you thrive in warm, sunny weather!",
        "summer-hater": "You are a Summer Hater: You feel your best in cooler, more subdued weather.",
        "rain-hater": "You are a Rain Hater: Rainy days really put a damper on your mood.",
        "unaffected": "You are Unaffected: The weather doesn’t have much impact on your overall mood.",
      };
  
      // Display result
      resultText.textContent = descriptions[resultType];
      resultDiv.style.display = "block";
      quiz.style.display = "none";
  
      // Add share functionality for Twitter
      const siteUrl = "http://127.0.0.1:8000/en/blog/whats-your-weather-personality"; // Replace with your site URL
      const tweetText = encodeURIComponent(`I am a ${descriptions[resultType]}! Find your weather personality here: ${siteUrl}`);
      const tweetUrl = `https://twitter.com/intent/tweet?text=${tweetText}`;
      shareTwitter.setAttribute("href", tweetUrl);
  
      // Add share functionality for Facebook
      const facebookUrl = `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(siteUrl)}&quote=${encodeURIComponent(descriptions[resultType])}`;
      console.log("Facebook URL: ", facebookUrl); // Debugging line
      shareFacebook.setAttribute("href", facebookUrl);
    });
  });
  