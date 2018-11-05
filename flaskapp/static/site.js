
var iteration = 1;

$(window).on('scroll', function(){
    var scrollTop = $(document).scrollTop();
    var windowHeight = $(window).height();
    var bodyHeight = $(document).height() - windowHeight;
    var scrollPercentage = (scrollTop / bodyHeight);
    if(scrollPercentage > 0.99) {
        setTimeout(function(){
            addPapers(iteration);
            iteration += 1;
        }, 1200);
    }
});

function addPapers(iteration) {
    $('#loader').innerHTML = "";
    var page = window.location.pathname;
    $.ajax({
        url: "/addpapers?iteration=" + iteration + "&page=" + page,
        type: "GET",
        success: function(papers) {
            $.each(papers, function(index, paper){
                $('#papers')
                    .append($("<li>")
                        .append($("<br><br>"))
                        .append($("<a>")
                            .attr('id','paper_title')
                            .attr('href', paper[1]['links'][1]['href'])
                            .attr('target','_blank')
                                .append($('<span>')
                                .append(paper[1]['title']))
                        )
                        .append($("<br><br>"))
                        .append($("<p>")
                            .attr('id','summary')
                                .append($('<span>')
                                .append(paper[1]['summary'])
                                )
                        )
                        .append($("<br>"))
                        .append($("<em>")
                            .append("Authors: ")
                        )
                        .append($("<em>")
                            .append(function(){
                                    var authorList = document.createElement('span');
                                    $.each(paper[1]['authors'], function(index, author){
                                        if (index == paper[1]['authors'].length - 1){
                                            authorList.append(author['name']);
                                        } else {
                                            authorList.append(author['name'] + ", ");
                                        }
                                    })
                                    return authorList;
                                }
                            )
                        )
                        .append($("<br>"))
                    )
            })
        }
    })
}