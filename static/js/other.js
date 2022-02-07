function truncateText(selector, maxLength) {
    var element = selector
        truncated = element.innerText;

    if (truncated.length > maxLength) {
        truncated = truncated.substr(0,maxLength) + '...';
    }
    return truncated;
}

function truncate(selector,maxLength){
  let array = document.querySelectorAll(selector)
    for (let i = 0; i < array.length; i++) {
      array[i].innerText = truncateText(array[i], 19)
    }

}
truncate('.top_news_titles_bold', 19)