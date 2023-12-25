const placeholderDOMElement = document.getElementsByName("q");

// The JS function is taken from a CodePen by Joe B. Lewis
// here: https://codepen.io/joelewis/pen/ePOrmV and modified
// for particular use case.
var suggestivePlaceholder = function (options) {
  this.options = options;
  this.element = options.element
  this.placeholderIdx = 0;
  this.charIdx = 0;
  this.setPlaceholder = function () {
    placeholder = options.placeholders[this.placeholderIdx];
    var placeholderChunk = placeholder.substring(0, this.charIdx + 1);
    placeholderDOMElement[0].placeholder = this.options.preText + placeholderChunk;
  };
  this.onTickReverse = function (afterReverse) {
    if (this.charIdx === 0) {
      afterReverse.bind(this)();
      clearInterval(this.intervalId);
      this.init();
    } else {
      this.setPlaceholder();
      this.charIdx--;
    }
  };
  this.goReverse = function () {
    clearInterval(this.intervalId);
    this.intervalId = setInterval(this.onTickReverse.bind(this, function () {
      this.charIdx = 0;
      this.placeholderIdx++;
      if (this.placeholderIdx === options.placeholders.length) {
        this.placeholderIdx = 0;
      }
    }), this.options.speed)
  };
  this.onTick = function () {
    var placeholder = options.placeholders[this.placeholderIdx];
    if (this.charIdx === placeholder.length) {
      setTimeout(this.goReverse.bind(this), this.options.stay);
    }
    this.setPlaceholder();
    this.charIdx++;
  }
  this.init = function () {
    this.intervalId = setInterval(this.onTick.bind(this), this.options.speed);
  }
  this.kill = function () {
    clearInterval(this.intervalId);
  }
}
var suggestivePlaceholderElement = new suggestivePlaceholder({
  // The placeholder array randomization/shuffling is taken from a
  // StackOverflow solution here: https://stackoverflow.com/a/46545530
  placeholders: [
    "Deep learning",
    "Machine learning",
    "Artificial Intelligence",
    "Artificial Neural Network",
    "ChatGPT",
    "Deep Neural Networks",
    "Convolutional Neural Networks",
    "Voice recognition",
    "Sound recognition",
    "Speech recognition",
    "Pattern recognition",
    "Image recognition",
    "Facial recognition",
    "Text mining",
    "Text analytics",
    "Large Language Model (LLM)",
    "BERT",
    "Robotics",
    "Hardware",
    "IoT",
    "Internet of Things",
    "Categorization",
    "Taxonomies",
    "Classification",
    "Big Data",
    "Prediction",
    "Data representation",
    "Data privacy",
    "Crowdsourcing",
    "Supervised learning from labeled data",].map(value => ({ value, sort: Math.random() })).sort((a, b) => a.sort - b.sort).map(({ value }) => value),
  preText: "Search for ",
  stay: 1000,
  speed: 100,
});

window.addEventListener("load", (event) => {
  suggestivePlaceholderElement.init();
})

// StackOverflow solution here: https://stackoverflow.com/a/22425498
window.onload = function () {
  var externalReference = document.getElementsByClassName("reference external");
  for (var idx = 0; idx < externalReference.length; idx++) {
    if (externalReference[idx].hostname != window.location.hostname) {
      externalReference[idx].setAttribute("target", "_blank");
    }
  }
}

window.onload = function () {
  const wordsPerMinute = 275;
  let result;
  let totalWordCount = 0;
  var section = document.querySelector("section");
  var paragraphs = section.querySelectorAll("p");

  paragraphs.forEach(p => {
    const words = p.textContent.trim().split(" ");
    totalWordCount += words.length;
  });

  if (totalWordCount > 0) {
    let value = Math.ceil(totalWordCount / wordsPerMinute);
    result = `${value} mins read`;
  }
  document.getElementById("readingTime").innerText = result;
}
